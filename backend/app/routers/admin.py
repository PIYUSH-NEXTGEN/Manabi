"""Admin-only review queue, moderation, crawl runs, and takedown (§9.2)."""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from sqlalchemy import func, select

from app import schemas
from app.crawler import config as crawler_config
from app.crawler.run import run_source
from app.db import session_scope
from app.deps import AdminUser, DB
from app.models import (
    CrawlRun,
    Problem,
    STATUS_PENDING_REVIEW,
    STATUS_PUBLISHED,
    STATUS_REJECTED,
    STATUS_REMOVED,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _admin_problem(problem: Problem) -> schemas.AdminProblemOut:
    return schemas.AdminProblemOut(
        id=problem.id,
        title=problem.title,
        summary=problem.summary,
        who_affected=problem.who_affected,
        why_matters=problem.why_matters,
        field=problem.field,
        domain=problem.domain,
        difficulty=problem.difficulty,
        est_hours=problem.est_hours,
        tech_tags=problem.tech_tags,
        datasets=problem.datasets,
        approaches=problem.approaches,
        source_name=problem.source_name,
        source_id=problem.source_id,
        source_url=problem.source_url,
        source_note=problem.source_note,
        ai_fields=problem.ai_fields,
        project_count=len(problem.projects),
        status=problem.status,
        origin=problem.origin,
        source_year=problem.source_year,
        edition=problem.edition,
        organisation=problem.organisation,
        deadline=problem.deadline,
        source_status=problem.source_status,
        extraction_confidence=problem.extraction_confidence,
        review_notes=problem.review_notes,
        crawl_source_key=problem.crawl_source_key,
        first_seen_at=problem.first_seen_at,
        last_seen_at=problem.last_seen_at,
        created_at=problem.created_at,
    )


def _get_problem(db, problem_id: int) -> Problem:
    problem = db.get(Problem, problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.get("/review", response_model=schemas.AdminReviewOut)
def review_queue(
    db: DB,
    _admin: AdminUser,
    status: str = Query(default=STATUS_PENDING_REVIEW),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    query = select(Problem).where(Problem.status == status)
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.scalars(query.order_by(Problem.created_at.desc()).limit(limit).offset(offset)).all()
    return schemas.AdminReviewOut(items=[_admin_problem(row) for row in rows], total=total)


def _moderate(db, problem_id: int, status: str, admin: str) -> schemas.AdminActionOut:
    problem = _get_problem(db, problem_id)
    problem.status = status
    problem.review_notes = f"approved by admin {admin}" if status == STATUS_PUBLISHED else f"set to {status} by admin {admin}"
    db.commit()
    return schemas.AdminActionOut(ok=True, problem_id=problem.id, status=problem.status)


@router.post("/problems/{problem_id}/approve", response_model=schemas.AdminActionOut)
def approve(problem_id: int, db: DB, admin: AdminUser):
    return _moderate(db, problem_id, STATUS_PUBLISHED, admin.username)


@router.post("/problems/{problem_id}/reject", response_model=schemas.AdminActionOut)
def reject(problem_id: int, db: DB, admin: AdminUser):
    return _moderate(db, problem_id, STATUS_REJECTED, admin.username)


@router.post("/problems/{problem_id}/unpublish", response_model=schemas.AdminActionOut)
def unpublish(problem_id: int, db: DB, admin: AdminUser):
    return _moderate(db, problem_id, STATUS_REMOVED, admin.username)


@router.patch("/problems/{problem_id}", response_model=schemas.AdminActionOut)
def edit_problem(problem_id: int, body: schemas.ProblemPatch, db: DB, admin: AdminUser):
    problem = _get_problem(db, problem_id)
    changes = body.model_dump(exclude_unset=True, exclude_none=True)
    for field_name, value in changes.items():
        if field_name == "tech_tags":
            value = [tag.strip().lower() for tag in value]
        setattr(problem, field_name, value)
    problem.review_notes = f"human edit by {admin.username}"
    db.commit()
    return schemas.AdminActionOut(ok=True, problem_id=problem.id, status=problem.status)


@router.get("/crawl-runs", response_model=list[schemas.CrawlRunOut])
def crawl_runs(db: DB, _admin: AdminUser, limit: int = Query(default=20, ge=1, le=100)):
    rows = db.scalars(select(CrawlRun).order_by(CrawlRun.started_at.desc()).limit(limit)).all()
    return [
        schemas.CrawlRunOut(
            id=row.id,
            source_key=row.source_key,
            started_at=row.started_at,
            finished_at=row.finished_at,
            status=row.status,
            counts=row.counts,
            llm_calls=row.llm_calls,
            error_summary=row.error_summary,
            triggered_by=row.triggered_by,
        )
        for row in rows
    ]


@router.get("/crawl-runs/{run_id}", response_model=schemas.CrawlRunOut)
def crawl_run(run_id: int, db: DB, _admin: AdminUser):
    row = db.get(CrawlRun, run_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Crawl run not found")
    return schemas.CrawlRunOut(
        id=row.id,
        source_key=row.source_key,
        started_at=row.started_at,
        finished_at=row.finished_at,
        status=row.status,
        counts=row.counts,
        llm_calls=row.llm_calls,
        error_summary=row.error_summary,
        triggered_by=row.triggered_by,
    )


@router.post("/sources/{source_key}/unpublish-all", response_model=schemas.TakedownOut)
def unpublish_source(source_key: str, db: DB, admin: AdminUser):
    problems = db.scalars(select(Problem).where(Problem.crawl_source_key == source_key)).all()
    for problem in problems:
        problem.status = STATUS_REMOVED
        problem.review_notes = f"source takedown by admin {admin.username}"
    db.commit()
    return schemas.TakedownOut(ok=True, source_key=source_key, unpublished=len(problems))


@router.post("/crawl/{source_key}", status_code=202)
def trigger_crawl(source_key: str, background: BackgroundTasks, _admin: AdminUser):
    if not crawler_config.enabled():
        raise HTTPException(status_code=409, detail="CRAWLER_ENABLED is false")
    if not crawler_config.user_agent():
        raise HTTPException(status_code=409, detail="CRAWLER_CONTACT is not configured")

    def _job() -> None:
        with session_scope() as db:
            import asyncio

            asyncio.run(run_source(source_key, db=db, triggered_by="manual"))

    background.add_task(_job)
    return {"status": "accepted", "source_key": source_key}


@router.get("/problems/{problem_id}", response_model=schemas.AdminProblemOut)
def admin_problem(problem_id: int, db: DB, _admin: AdminUser):
    return _admin_problem(_get_problem(db, problem_id))
