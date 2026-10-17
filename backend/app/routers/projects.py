from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app import schemas
from app.deps import DB, CurrentUser, get_optional_user
from app.models import Problem, Project
from app.routers.problems import project_to_out
from app.services import github
from app.services.github import GitHubError

router = APIRouter(tags=["projects"])

CACHE_TTL = timedelta(minutes=10)


def _aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@router.post("/api/problems/{problem_id}/projects", response_model=schemas.ProjectOut)
async def submit_project(problem_id: int, body: schemas.ProjectCreate, user: CurrentUser, db: DB):
    problem = db.scalar(select(Problem).where(Problem.id == problem_id))
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    parsed = github.parse_repo_url(body.repo_url)
    if parsed is None:
        raise HTTPException(status_code=422, detail="Not a valid public GitHub repository URL")
    owner, name = parsed

    try:
        await github.get_repo(owner, name, user.github_token)
    except GitHubError as exc:
        if exc.status == 404:
            raise HTTPException(status_code=422, detail="Repository not found on GitHub or not public")
        raise HTTPException(status_code=502, detail=str(exc))

    duplicate = db.scalar(
        select(Project).where(
            Project.problem_id == problem_id,
            Project.user_id == user.id,
            Project.repo_owner == owner,
            Project.repo_name == name,
        )
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="You already linked this repository to this problem")

    project = Project(
        problem_id=problem_id,
        user_id=user.id,
        repo_owner=owner,
        repo_name=name,
        repo_url=body.repo_url.strip(),
        open_for_contributors=body.open_for_contributors,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project_to_out(project)


def _project_or_404(db, project_id: int) -> Project:
    project = db.scalar(
        select(Project).options(joinedload(Project.user), joinedload(Project.problem)).where(Project.id == project_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def project_out_safely(project: Project) -> schemas.ProjectOut:
    out = project_to_out(project)
    if out.progress is not None:
        out.progress = schemas.Progress.model_validate(out.progress)
    return out


@router.get("/api/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: DB):
    return project_out_safely(_project_or_404(db, project_id))


@router.get("/api/projects/{project_id}/progress", response_model=schemas.Progress)
async def get_project_progress(
    project_id: int,
    db: DB,
    request: Request,
    refresh: bool = Query(default=False),
):
    project = _project_or_404(db, project_id)
    now = datetime.now(timezone.utc)
    cached = project.progress_json
    cache_fresh = (
        cached is not None
        and project.progress_updated_at is not None
        and now - _aware(project.progress_updated_at) <= CACHE_TTL
    )
    if not refresh and cache_fresh:
        return schemas.Progress.model_validate(cached)

    user = get_optional_user(request, db)
    token = user.github_token if user else None
    progress = await github.get_progress(project.repo_owner, project.repo_name, token)
    if progress is None:
        if cached is not None:
            return schemas.Progress.model_validate(cached)
        raise HTTPException(status_code=502, detail="Could not fetch progress from GitHub")

    project.progress_json = progress
    project.progress_updated_at = datetime.now(timezone.utc)
    db.commit()
    return schemas.Progress.model_validate(progress)


@router.get("/api/me/projects", response_model=list[schemas.ProjectOut])
def my_projects(user: CurrentUser, db: DB):
    rows = db.scalars(
        select(Project).options(joinedload(Project.problem)).where(Project.user_id == user.id).order_by(Project.created_at.desc())
    ).all()
    return [project_out_safely(p) for p in rows]
