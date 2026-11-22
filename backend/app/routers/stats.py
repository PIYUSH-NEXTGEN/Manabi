from fastapi import APIRouter, Response
from sqlalchemy import func, select

from app import schemas
from app.deps import DB
from app.models import Problem, Project, STATUS_PUBLISHED, VERIFICATION_VERIFIED
from app.services.public_cache import (
    AGGREGATE_CACHE_CONTROL,
    AGGREGATE_TTL_SECONDS,
    PUBLIC_CACHE,
    STATS_KEY_PREFIX,
)

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats", response_model=schemas.StatsOut)
def stats(db: DB, response: Response):
    # Public counters are identical for every viewer and change slowly, so a
    # short-lived entry removes the whole database round trip from repeat
    # traffic instead of re-counting on every page view.
    cache_key = (STATS_KEY_PREFIX,)
    cached = PUBLIC_CACHE.get(cache_key)
    if cached is not None:
        response.headers["Cache-Control"] = AGGREGATE_CACHE_CONTROL
        return cached

    published = Problem.status == STATUS_PUBLISHED
    # Four subselects in one statement: one database round trip instead of four,
    # which matters because each one crosses a network hop on the free tier.
    row = db.execute(
        select(
            select(func.count(Problem.id))
            .where(published)
            .scalar_subquery(),
            select(func.count(func.distinct(Problem.source_name)))
            .where(published)
            .scalar_subquery(),
            select(func.count(func.distinct(Problem.field)))
            .where(published)
            .scalar_subquery(),
            # Public counters show verified submissions only (§7.4)
            select(func.count(Project.id))
            .where(Project.verification_status == VERIFICATION_VERIFIED)
            .scalar_subquery(),
        )
    ).one()
    problems, sources, fields, projects = (int(value or 0) for value in row)

    payload = schemas.StatsOut(
        problems=problems, sources=sources, fields=fields, projects=projects
    )
    PUBLIC_CACHE.set(cache_key, payload, AGGREGATE_TTL_SECONDS)
    response.headers["Cache-Control"] = AGGREGATE_CACHE_CONTROL
    return payload
