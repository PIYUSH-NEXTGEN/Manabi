from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Text, case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, joinedload

from app import schemas
from app.deps import DB, CurrentUser, OptionalUser
from app.models import (
    STATUS_PUBLISHED,
    Problem,
    ProblemStar,
    Project,
    VERIFICATION_VERIFIED,
)
from app.services.presenters import problem_to_out, project_to_out
from app.services.ratelimit import ADMIN_LIMITER, RateLimiter
from app.services.visibility import can_view_project, is_admin

router = APIRouter(prefix="/api/problems", tags=["problems"])

SortParam = Literal["newest", "popular"]
DistinctParam = Literal["field", "domain"]

PROBLEM_CREATE_LIMITER = RateLimiter("PROBLEM_CREATE_PER_HOUR")
PROBLEM_STAR_LIMITER = RateLimiter("STAR_RATE_LIMIT_PER_HOUR")


def _completed_count():
    """Verified-completed share of a problem's verified submissions."""
    return func.sum(
        case((Project.completed_at.is_not(None), 1), else_=0)
    ).label("completed")


def apply_problem_filters(query, q, field, domain, difficulty, tech, source):
    """Shared WHERE filters for the board list and any aggregate over it."""
    if q:
        needle = f"%{q.lower()}%"
        tech_text = func.lower(func.cast(Problem.tech_tags, Text))
        query = query.where(
            func.lower(Problem.title).like(needle)
            | func.lower(Problem.summary).like(needle)
            | func.lower(Problem.source_id).like(needle)
            | tech_text.like(needle)
        )
    if field:
        query = query.where(Problem.field == field)
    if domain:
        query = query.where(Problem.domain == domain)
    if difficulty:
        query = query.where(Problem.difficulty == difficulty)
    for tag in tech:
        tag_text = func.lower(func.cast(Problem.tech_tags, Text))
        query = query.where(tag_text.like(f'%"{tag.lower()}"%'))
    if source:
        source_needle = f"%{source.lower()}%"
        query = query.where(
            func.lower(Problem.source_name).like(source_needle)
            | func.lower(Problem.source_id).like(source_needle)
        )
    return query


def _counts_by_column(db, column) -> list[tuple[str, int]]:
    query = select(column, func.count(Problem.id)).where(Problem.status == STATUS_PUBLISHED).group_by(column)
    rows = db.execute(query).all()
    return [(str(value), int(count)) for value, count in rows if value is not None]


def _star_counts_by_problem(db, problem_ids: list[int]) -> dict[int, int]:
    """One grouped query for the card list, instead of a lazy load per row."""
    if not problem_ids:
        return {}
    rows = db.execute(
        select(ProblemStar.problem_id, func.count(ProblemStar.id))
        .where(ProblemStar.problem_id.in_(problem_ids))
        .group_by(ProblemStar.problem_id)
    ).all()
    return {int(problem_id): int(count) for problem_id, count in rows}


def _viewer_starred_ids(db, viewer, problem_ids: list[int]) -> set[int]:
    if viewer is None or not problem_ids:
        return set()
    return set(
        db.scalars(
            select(ProblemStar.problem_id).where(
                ProblemStar.user_id == viewer.id,
                ProblemStar.problem_id.in_(problem_ids),
            )
        ).all()
    )


@router.get("", response_model=schemas.ProblemsListOut)
def list_problems(
    db: DB,
    user: OptionalUser,
    q: str | None = None,
    field: schemas.FieldEnum | None = None,
    domain: schemas.DomainEnum | None = None,
    difficulty: schemas.Difficulty | None = None,
    tech: list[str] = Query(default=[]),
    source: str | None = None,
    sort: SortParam = "newest",
    distinct: DistinctParam | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = apply_problem_filters(
        select(Problem).where(Problem.status == STATUS_PUBLISHED), q, field, domain, difficulty, tech, source
    )

    # One aggregate over the same popularity subquery serves ordering AND the
    # card counts on the page; a separate full-table counts query per request
    # was removed (quantified in docs/PERF_2026-11-09.md, FIN-2).
    counts_sub = (
        select(
            Project.problem_id,
            func.count(Project.id).label("n"),
            _completed_count(),
        )
        .where(Project.verification_status == VERIFICATION_VERIFIED)
        .group_by(Project.problem_id)
        .subquery()
    )
    popularity = func.coalesce(counts_sub.c.n, 0).label("n")
    query = query.add_columns(popularity, counts_sub.c["completed"]).outerjoin(counts_sub, Problem.id == counts_sub.c.problem_id)
    if sort == "popular":
        ordering = [popularity.desc(), Problem.created_at.desc(), Problem.id.desc()]
    else:
        ordering = [Problem.created_at.desc(), Problem.id.desc()]
    query = query.order_by(*ordering)

    if distinct:
        # One brief per field/domain, keeping each group's best-ranked row, so a
        # short list (e.g. the hero showcase) spans topics instead of one field.
        ranked = query.add_columns(
            func.row_number()
            .over(partition_by=Problem.field if distinct == "field" else Problem.domain, order_by=ordering)
            .label("rank"),
        ).subquery()
        problem = aliased(Problem, ranked)
        # Distinct count of group values comes from the plain filtered set:
        # it does not need the window/join machinery of the ranked subquery,
        # and the old form re-ran it per request (docs/PERF_2026-11-09.md, FIN-3).
        base_col = Problem.field if distinct == "field" else Problem.domain
        distinct_base = select(base_col).where(Problem.status == STATUS_PUBLISHED)
        distinct_base = apply_problem_filters(distinct_base, q, field, domain, difficulty, tech, source)
        total = db.scalar(select(func.count()).select_from(distinct_base.distinct().subquery())) or 0
        rows = db.execute(
            select(
                problem,
                ranked.c["n"],
                ranked.c["completed"],
            )
            .where(ranked.c["rank"] == 1)
            .order_by(ranked.c["n"].desc(), ranked.c.created_at.desc(), ranked.c.id.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        ids = [p.id for p, _, _ in rows]
        star_counts = _star_counts_by_problem(db, ids)
        starred = _viewer_starred_ids(db, user, ids)
        items = [
            problem_to_out(
                p,
                int(n or 0),
                int(c or 0),
                star_count=star_counts.get(p.id, 0),
                starred_by_me=p.id in starred,
            )
            for p, n, c in rows
        ]
        return schemas.ProblemsListOut(items=items, total=total)

    total = (
        db.scalar(
            select(func.count()).select_from(query.order_by(None).subquery())
        )
        or 0
    )  # popularity/completed columns are carried but ignored by count(*)
    rows = db.execute(query.limit(limit).offset(offset)).all()
    ids = [p.id for p, _, _ in rows]
    star_counts = _star_counts_by_problem(db, ids)
    starred = _viewer_starred_ids(db, user, ids)
    items = [
        problem_to_out(
            p,
            int(n or 0),
            int(c or 0),
            star_count=star_counts.get(p.id, 0),
            starred_by_me=p.id in starred,
        )
        for p, n, c in rows
    ]
    return schemas.ProblemsListOut(items=items, total=total)


@router.get("/facets", response_model=schemas.FacetsOut, response_model_exclude_none=True)
def facets(db: DB):
    tech_rows = db.scalars(
        select(Problem.tech_tags).where(Problem.status == STATUS_PUBLISHED)
    ).all()
    tech_counter: dict[str, int] = {}
    for tags in tech_rows:
        for tag in tags:
            tech_counter[tag.lower()] = tech_counter.get(tag.lower(), 0) + 1
    source_rows = db.execute(
        select(
            Problem.source_name,
            func.count(Problem.id),
            func.max(Problem.created_at),
        )
        .where(Problem.status == STATUS_PUBLISHED)
        .group_by(Problem.source_name)
    ).all()
    return schemas.FacetsOut(
        fields=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.field)],
        domains=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.domain)],
        difficulties=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.difficulty)],
        tech_tags=[
            schemas.Facet(value=v, count=c)
            for v, c in sorted(tech_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        sources=[
            schemas.Facet(value=name, count=count, last_updated=updated)
            for name, count, updated in source_rows
        ],
    )


@router.get("/{problem_id}", response_model=schemas.ProblemDetail)
def get_problem(problem_id: int, db: DB, user: OptionalUser):
    problem = db.scalar(
        select(Problem)
        .options(joinedload(Problem.projects).joinedload(Project.user))
        .where(Problem.id == problem_id, Problem.status == STATUS_PUBLISHED)
    )
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    # Anonymous visitors and other users see verified submissions only; the
    # owner (and admins) additionally see their own rows in every status.
    visible = [p for p in problem.projects if can_view_project(p, user)]
    project_count = len(visible)
    completed_count = sum(1 for p in visible if p.completed_at is not None and p.verification_status == VERIFICATION_VERIFIED)
    base = problem_to_out(problem, project_count, completed_count, viewer=user)
    detail = base.model_dump()
    detail["original_text"] = problem.original_text
    detail["display_policy"] = "summary_plus_excerpt"
    detail["projects"] = [
        project_to_out(
            p,
            include_private=(user is not None and (user.id == p.user_id or is_admin(user))),
            viewer=user,
        ).model_dump(mode="json")
        for p in visible
    ]
    return schemas.ProblemDetail(**detail)


@router.post("", response_model=schemas.ProblemOut, status_code=201)
def create_problem(body: schemas.ProblemIn, user: CurrentUser, db: DB):
    # Publishing content on the public board is an abuse-prone, unbounded
    # action: rate-limit ordinary users; admins bypass that but still pass a
    # shared sanity cap so a runaway or hijacked admin session gets stopped.
    if is_admin(user):
        retry = ADMIN_LIMITER.check(db, f"admin:{user.id}")
    else:
        retry = PROBLEM_CREATE_LIMITER.check(db, f"problem-create:{user.id}")
    if retry is not None:
        raise HTTPException(
            status_code=429,
            detail={"code": "rate_limited", "message": "Too many problems created this hour. Try again later."},
            headers={"Retry-After": str(retry)},
        )
    if body.source_id:
        existing = db.scalar(
            select(Problem).where(Problem.source_name == body.source_name, Problem.source_id == body.source_id)
        )
        if existing is not None:
            raise HTTPException(status_code=409, detail="A problem with this source ID already exists")
    problem = Problem(
        title=body.title.strip(),
        summary=body.summary.strip(),
        who_affected=body.who_affected,
        why_matters=body.why_matters,
        field=body.field,
        domain=body.domain,
        difficulty=body.difficulty,
        est_hours=max(1, body.est_hours),
        tech_tags=[t.strip().lower() for t in body.tech_tags],
        # datasets arrive as validated JSON dicts (list[dict]) and are stored
        # verbatim; they also flow back out unchanged in ProblemOut.
        datasets=list(body.datasets),
        approaches=body.approaches,
        source_name=body.source_name,
        source_id=body.source_id,
        source_url=body.source_url,
        source_note=body.source_note,
        original_text=body.summary.strip(),
        ai_fields=body.ai_fields,
        created_by=user.id,
    )
    db.add(problem)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A problem with this source ID already exists")
    db.refresh(problem)
    return problem_to_out(problem, 0, 0)


# ---------------------------------------------------------------------------
# Stars. Logged-in users, one per user per problem, visible to everyone
# ---------------------------------------------------------------------------


def _problem_star_count(db, problem_id: int) -> int:
    return int(
        db.scalar(
            select(func.count(ProblemStar.id)).where(ProblemStar.problem_id == problem_id)
        )
        or 0
    )


@router.post("/{problem_id}/star", status_code=201)
def star_problem(problem_id: int, user: CurrentUser, db: DB):
    problem = db.scalar(
        select(Problem).where(Problem.id == problem_id, Problem.status == STATUS_PUBLISHED)
    )
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    if (retry := PROBLEM_STAR_LIMITER.check(db, f"star:{user.id}")) is not None:
        raise HTTPException(
            status_code=429,
            detail={"code": "rate_limited", "message": "Too many star actions this hour. Try again later."},
            headers={"Retry-After": str(retry)},
        )
    existing = db.scalar(
        select(ProblemStar).where(
            ProblemStar.problem_id == problem.id, ProblemStar.user_id == user.id
        )
    )
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail={"code": "already_starred", "message": "You already starred this problem."},
        )
    db.add(ProblemStar(problem_id=problem.id, user_id=user.id))
    db.commit()
    return {"ok": True, "star_count": _problem_star_count(db, problem.id)}


@router.delete("/{problem_id}/star", status_code=204)
def unstar_problem(problem_id: int, user: CurrentUser, db: DB):
    if (retry := PROBLEM_STAR_LIMITER.check(db, f"star:{user.id}")) is not None:
        raise HTTPException(
            status_code=429,
            detail={"code": "rate_limited", "message": "Too many star actions this hour. Try again later."},
            headers={"Retry-After": str(retry)},
        )
    star = db.scalar(
        select(ProblemStar).where(
            ProblemStar.problem_id == problem_id, ProblemStar.user_id == user.id
        )
    )
    if star is not None:
        db.delete(star)
        db.commit()
