import re
from io import BytesIO
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import Text, case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, joinedload

from app import schemas
from app.deps import DB, CurrentUser, OptionalUser
from app.models import Problem, Project, STATUS_PUBLISHED, VERIFICATION_VERIFIED
from app.services.ratelimit import RateLimiter
from app.services.visibility import can_view_project, is_admin

router = APIRouter(prefix="/api/problems", tags=["problems"])

SortParam = Literal["newest", "popular"]
DistinctParam = Literal["field", "domain"]

PROBLEM_CREATE_LIMITER = RateLimiter("PROBLEM_CREATE_PER_HOUR")


def problem_to_out(problem: Problem, project_count: int, completed_count: int = 0) -> schemas.ProblemOut:
    return schemas.ProblemOut(
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
        project_count=project_count,
        completed_count=completed_count,
        origin=problem.origin,
        source_year=problem.source_year,
        edition=problem.edition,
        organisation=problem.organisation,
        deadline=problem.deadline,
        goal=problem.goal,
    )


def project_to_out(project: Project, include_private: bool = False) -> schemas.ProjectOut:
    """Public shape for a project row.

    include_private adds the owner/admin-only fields (relevance reason,
    ownership basis, review note). relevance_score is never part of this
    schema — it is not exposed publicly beyond the admin queue.
    """
    out = schemas.ProjectOut(
        id=project.id,
        problem_id=project.problem_id,
        problem_title=project.problem.title,
        repo_url=project.repo_url,
        repo_owner=project.repo_owner,
        repo_name=project.repo_name,
        open_for_contributors=project.open_for_contributors,
        owner={"username": project.user.username, "avatar_url": project.user.avatar_url},
        progress=project.progress_json,
        progress_updated_at=project.progress_updated_at,
        verification_status=project.verification_status,
        solution_summary=project.solution_summary or None,
        completed_at=project.completed_at,
        demo_url=project.demo_url,
        reflection=project.reflection,
    )
    if include_private:
        out.relevance_reason = project.relevance_reason
        out.ownership_basis = project.ownership_basis
        out.review_note = project.review_note
    return out


def verified_problem_counts(db) -> dict[int, tuple[int, int]]:
    """Verified-only (building, completed) counts per problem id."""
    completed = func.sum(
        case((Project.completed_at.is_not(None), 1), else_=0)
    ).label("completed")
    rows = db.execute(
        select(Project.problem_id, func.count(Project.id), completed)
        .where(Project.verification_status == VERIFICATION_VERIFIED)
        .group_by(Project.problem_id)
    ).all()
    return {pid: (int(building), int(completed)) for pid, building, completed in rows}


def _counts_by_column(db, column) -> list[tuple[str, int]]:
    query = select(column, func.count(Problem.id)).where(Problem.status == STATUS_PUBLISHED).group_by(column)
    rows = db.execute(query).all()
    return [(str(value), int(count)) for value, count in rows if value is not None]


@router.get("", response_model=schemas.ProblemsListOut)
def list_problems(
    db: DB,
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
    query = select(Problem).where(Problem.status == STATUS_PUBLISHED)

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

    project_counts = (
        select(Project.problem_id, func.count(Project.id).label("n"))
        .where(Project.verification_status == VERIFICATION_VERIFIED)
        .group_by(Project.problem_id)
        .subquery()
    )
    query = query.outerjoin(project_counts, Problem.id == project_counts.c.problem_id)
    popularity = func.coalesce(project_counts.c.n, 0)
    if sort == "popular":
        ordering = [popularity.desc(), Problem.created_at.desc(), Problem.id.desc()]
    else:
        ordering = [Problem.created_at.desc(), Problem.id.desc()]
    query = query.order_by(*ordering)

    if distinct:
        # One brief per field/domain, keeping each group's best-ranked row, so a
        # short list (e.g. the hero showcase) spans topics instead of one field.
        ranked = query.add_columns(
            popularity.label("popularity"),
            func.row_number()
            .over(partition_by=Problem.field if distinct == "field" else Problem.domain, order_by=ordering)
            .label("rank"),
        ).subquery()
        problem = aliased(Problem, ranked)
        total = db.scalar(select(func.count(func.distinct(ranked.c[distinct])))) or 0
        rows = db.scalars(
            select(problem)
            .where(ranked.c.rank == 1)
            .order_by(ranked.c.popularity.desc(), ranked.c.created_at.desc(), ranked.c.id.desc())
            .limit(limit)
            .offset(offset)
        ).all()
    else:
        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        rows = db.scalars(query.limit(limit).offset(offset)).all()
    counts = verified_problem_counts(db)
    items = [problem_to_out(p, counts.get(p.id, (0, 0))[0], counts.get(p.id, (0, 0))[1]) for p in rows]
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


_FORMULA_PREFIX = re.compile(r"^[=+\-@\t\r]")


def _safe_cell(value):
    """Neutralise spreadsheet formulae that could execute when opened.

    A string cell starting with = + - @ or a tab/CR is treated as a formula
    by Excel/LibreOffice when a user opens the exported file. Prefixing with
    an apostrophe keeps the text literal. User-controlled problem text can
    reach these cells, so every string cell passes through here.
    """
    if isinstance(value, str) and _FORMULA_PREFIX.match(value):
        return "'" + value
    return value


@router.get("/{problem_id}/export.xlsx")
def export_problem(problem_id: int, db: DB):
    """One-problem XLSX built from MANABI's structured summary (never verbatim text)."""
    from openpyxl import Workbook

    problem = db.scalar(
        select(Problem).where(Problem.id == problem_id, Problem.status == STATUS_PUBLISHED)
    )
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Problem"
    rows = [
        ("Field", "Value"),
        ("Statement ID", problem.source_id or str(problem.id)),
        ("Title", problem.title),
        ("Organisation", problem.organisation or ""),
        ("Year", problem.source_year or ""),
        ("Source", problem.source_name),
        ("Official source link", problem.source_url or ""),
        ("Field / domain", f"{problem.field} / {problem.domain}"),
        ("Difficulty", problem.difficulty),
        ("Estimated hours", problem.est_hours),
        ("Summary (generated by MANABI)", problem.summary),
        ("Who is affected", problem.who_affected),
        ("Why it matters", problem.why_matters),
        ("Tech tags", ", ".join(problem.tech_tags)),
        ("Approaches", "\n".join(problem.approaches)),
        (
            "Notice",
            "Summary generated by MANABI from the original problem statement; "
            f"the original is owned by {problem.organisation or problem.source_name}.",
        ),
    ]
    for row in rows:
        sheet.append([_safe_cell(cell) for cell in row])
    sheet.column_dimensions["A"].width = 34
    sheet.column_dimensions["B"].width = 100

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    identifier = re.sub(r"[^A-Za-z0-9_-]+", "-", problem.source_id or str(problem.id))
    filename = f"MANABI-{identifier}-statement.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
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
    base = problem_to_out(problem, project_count, completed_count)
    detail = base.model_dump()
    detail["original_text"] = problem.original_text
    detail["display_policy"] = "summary_plus_excerpt"
    detail["projects"] = [
        project_to_out(p, include_private=(user is not None and (user.id == p.user_id or is_admin(user)))).model_dump(mode="json")
        for p in visible
    ]
    return schemas.ProblemDetail(**detail)


@router.post("", response_model=schemas.ProblemOut, status_code=201)
def create_problem(body: schemas.ProblemIn, user: CurrentUser, db: DB):
    # Publishing content on the public board is an abuse-prone, unbounded
    # action: rate-limit ordinary users (admins curate and are exempt).
    if not is_admin(user) and not PROBLEM_CREATE_LIMITER.allowed(f"problem-create:{user.id}"):
        raise HTTPException(
            status_code=429,
            detail={"code": "rate_limited", "message": "Too many problems created this hour — try again later."},
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
        datasets=[d.model_dump() for d in body.datasets],
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
