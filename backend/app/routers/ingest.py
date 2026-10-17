import asyncio

from fastapi import APIRouter, HTTPException

from app import schemas
from app.deps import CurrentUser, DB
from app.services import extractor
from app.services.extractor import NoClearProblem, SourceFetchError
from app.services.llm import LLMConfigError, LLMResponseError
from app.services.ratelimit import INGEST_LIMITER

router = APIRouter(tags=["ingest"])

MAX_EST_HOURS = 1000


def _map_llm_errors(exc: Exception) -> HTTPException:
    if isinstance(exc, LLMConfigError):
        return HTTPException(status_code=503, detail="AI is not configured yet")
    if isinstance(exc, LLMResponseError):
        return HTTPException(status_code=502, detail="The AI could not process this source")
    return HTTPException(status_code=502, detail=str(exc))


@router.post("/api/ingest", response_model=schemas.IngestOut)
async def ingest(body: schemas.IngestRequest, user: CurrentUser, db: DB):
    has_url, has_text = body.url is not None, body.text is not None
    if has_url == has_text:
        raise HTTPException(status_code=422, detail="Provide exactly one of url or text")
    if not INGEST_LIMITER.allowed(f"user:{user.id}"):
        raise HTTPException(status_code=429, detail="Too many AI jobs this hour — try again later")

    try:
        if body.url:
            source_url = body.url.strip()
            text = await extractor.fetch_source_text(source_url)
        else:
            source_url = None
            text = body.text.strip()
            if not text:
                raise HTTPException(status_code=422, detail="The pasted text is empty")
        # generate_json is a blocking sync SDK call — never run it on the event loop
        draft, evidence, inferred_fields = await asyncio.to_thread(
            extractor.extract_draft, text, source_url
        )
    except (SourceFetchError, NoClearProblem) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except (LLMConfigError, LLMResponseError) as exc:
        raise _map_llm_errors(exc)

    return schemas.IngestOut(
        draft=schemas.ProblemCard(
            title=draft.title.strip(),
            summary=draft.summary.strip(),
            who_affected=draft.who_affected,
            why_matters=draft.why_matters,
            field=draft.field,
            domain=draft.domain,
            difficulty=draft.difficulty,
            est_hours=max(1, min(draft.est_hours, MAX_EST_HOURS)),
            tech_tags=draft.tech_tags,
            datasets=draft.datasets,
            approaches=draft.approaches,
            source_name=source_url or "Pasted text",
            source_id=None,
            source_url=source_url,
            source_note=draft.source_note,
        ),
        evidence=evidence,
        source_url=source_url,
    )
