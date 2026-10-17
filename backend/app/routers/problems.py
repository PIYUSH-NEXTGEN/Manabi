from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Text, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app import schemas
from app.deps import DB, CurrentUser
from app.models import Problem, Project

router = APIRouter(prefix="/api/problems", tags=["problems"])

SortParam = Literal["newest", "popular"]


def problem_to_out(problem: Problem, project_count: int) -> schemas.ProblemOut:
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
    )


def project_to_out(project: Project) -> schemas.ProjectOut:
    return schemas.ProjectOut(
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
    )


def _counts_by_column(db, column) -> list[tuple[str, int]]:
    rows = db.execute(select(column, func.count(Problem.id)).group_by(column)).all()
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
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = select(Problem)

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

    if sort == "popular":
        project_counts = (
            select(Project.problem_id, func.count(Project.id).label("n")).group_by(Project.problem_id).subquery()
        )
        query = query.outerjoin(project_counts, Problem.id == project_counts.c.problem_id).order_by(
            func.coalesce(project_counts.c.n, 0).desc(), Problem.created_at.desc(), Problem.id.desc()
        )
    else:
        query = query.order_by(Problem.created_at.desc(), Problem.id.desc())

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.scalars(query.limit(limit).offset(offset)).all()
    counts = dict(db.execute(select(Project.problem_id, func.count(Project.id)).group_by(Project.problem_id)).all())
    items = [problem_to_out(p, counts.get(p.id, 0)) for p in rows]
    return schemas.ProblemsListOut(items=items, total=total)


@router.get("/facets", response_model=schemas.FacetsOut)
def facets(db: DB):
    tech_rows = db.scalars(select(Problem.tech_tags)).all()
    tech_counter: dict[str, int] = {}
    for tags in tech_rows:
        for tag in tags:
            tech_counter[tag.lower()] = tech_counter.get(tag.lower(), 0) + 1
    source_rows = db.execute(
        select(Problem.source_name, func.count(Problem.id)).group_by(Problem.source_name)
    ).all()
    return schemas.FacetsOut(
        fields=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.field)],
        domains=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.domain)],
        difficulties=[schemas.Facet(value=v, count=c) for v, c in _counts_by_column(db, Problem.difficulty)],
        tech_tags=[
            schemas.Facet(value=v, count=c)
            for v, c in sorted(tech_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        sources=[schemas.Facet(value=name, count=count) for name, count in source_rows],
    )


@router.get("/{problem_id}", response_model=schemas.ProblemDetail)
def get_problem(problem_id: int, db: DB):
    problem = db.scalar(
        select(Problem)
        .options(joinedload(Problem.projects).joinedload(Project.user))
        .where(Problem.id == problem_id)
    )
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    base = problem_to_out(problem, len(problem.projects))
    detail = base.model_dump()
    detail["original_text"] = problem.original_text
    detail["projects"] = [project_to_out(p).model_dump() for p in problem.projects]
    return schemas.ProblemDetail(**detail)


@router.post("", response_model=schemas.ProblemOut, status_code=201)
def create_problem(body: schemas.ProblemIn, user: CurrentUser, db: DB):
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
    return problem_to_out(problem, 0)
