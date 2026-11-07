from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app import schemas
from app.config import get_settings
from app.deps import CurrentUser, DB, OptionalUser
from app.models import (
    STATUS_PUBLISHED,
    Problem,
    Project,
    ProjectReport,
    User,
    VERIFICATION_NEEDS_REVIEW,
    VERIFICATION_REJECTED,
    VERIFICATION_VERIFIED,
    utcnow,
)
from app.routers.problems import project_to_out
from app.services import github, verification, visibility
from app.services.ratelimit import RateLimiter
from app.services.verification import SubmissionError

router = APIRouter(tags=["projects"])

CACHE_TTL = timedelta(minutes=10)

REPORT_LIMITER = RateLimiter("CHAT_RATE_LIMIT_USER_PER_HOUR")  # per-user, hourly


def _aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _error(err: SubmissionError) -> HTTPException:
    return HTTPException(status_code=err.status, detail={"code": err.code, "message": err.message})


def _project_or_404(db, project_id: int) -> Project:
    project = db.scalar(
        select(Project).options(joinedload(Project.user), joinedload(Project.problem)).where(Project.id == project_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def project_out_safely(project: Project, include_private: bool = False) -> schemas.ProjectOut:
    out = project_to_out(project, include_private=include_private)
    if out.progress is not None:
        out.progress = schemas.Progress.model_validate(out.progress)
    return out


# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------


@router.post("/api/problems/{problem_id}/projects", response_model=schemas.ProjectOut, status_code=201)
async def submit_project(problem_id: int, body: schemas.ProjectCreate, user: CurrentUser, db: DB):
    problem = db.scalar(
        select(Problem).where(Problem.id == problem_id, Problem.status == STATUS_PUBLISHED)
    )
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    try:
        project = await verification.create_submission(
            db,
            user,
            problem,
            repo_url=body.repo_url,
            solution_summary=body.solution_summary,
            open_for_contributors=body.open_for_contributors,
            demo_url=body.demo_url,
        )
    except SubmissionError as err:
        raise _error(err)
    return project_out_safely(project, include_private=True)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


@router.get("/api/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: DB, user: OptionalUser):
    project = _project_or_404(db, project_id)
    if not visibility.can_view_project(project, user):
        # Never reveal the existence of a non-verified project to others.
        raise HTTPException(status_code=404, detail="Project not found")
    include_private = user is not None and (user.id == project.user_id or visibility.is_admin(user))
    return project_out_safely(project, include_private=include_private)


@router.get("/api/projects/{project_id}/progress", response_model=schemas.Progress)
async def get_project_progress(
    project_id: int,
    db: DB,
    refresh: bool = Query(default=False),
    user: OptionalUser = None,
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

    token = user.github_token if user else None
    progress = await github.get_progress(project.repo_owner, project.repo_name, token)
    if progress is None:
        if cached is not None:
            return schemas.Progress.model_validate(cached)
        raise HTTPException(status_code=502, detail="Could not fetch progress from GitHub")

    project.progress_json = progress
    project.progress_updated_at = datetime.now(timezone.utc)

    # §6.7: re-verification opportunities on the refresh path. Only happens
    # for logged-in viewers (permission checks need a token) and never breaks
    # the progress call itself.
    if (refresh or not cache_fresh) and user is not None:
        try:
            await verification.refresh_project_state(db, project, user)
            if project.verification_status == VERIFICATION_NEEDS_REVIEW:
                problem = project.problem or db.get(Problem, project.problem_id)
                if problem is not None:
                    await verification.auto_reverify(db, project, problem, user)
        except Exception:  # noqa: BLE001 - verification must never break progress
            db.rollback()
    else:
        db.commit()
    return schemas.Progress.model_validate(progress)


# ---------------------------------------------------------------------------
# Owner list
# ---------------------------------------------------------------------------


@router.get("/api/me/projects", response_model=list[schemas.ProjectOut])
def my_projects(user: CurrentUser, db: DB):
    rows = db.scalars(
        select(Project).options(joinedload(Project.problem)).where(Project.user_id == user.id).order_by(Project.created_at.desc())
    ).all()
    # The owner sees every status of their own rows, with the private fields.
    return [project_out_safely(p, include_private=True) for p in rows]


# ---------------------------------------------------------------------------
# Remove / edit / complete (§7)
# ---------------------------------------------------------------------------


@router.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: int, user: CurrentUser, db: DB):
    project = _project_or_404(db, project_id)
    if user.id != project.user_id and not visibility.is_admin(user):
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


@router.patch("/api/projects/{project_id}", response_model=schemas.ProjectOut)
async def edit_project(project_id: int, body: schemas.ProjectPatch, user: CurrentUser, db: DB):
    project = _project_or_404(db, project_id)
    if user.id != project.user_id and not visibility.is_admin(user):
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        new_summary = None
        if body.solution_summary is not None:
            new_summary = verification.validate_solution_summary(body.solution_summary)
        if body.demo_url is not None:
            project.demo_url = verification.validate_demo_url(body.demo_url)
        if body.open_for_contributors is not None:
            project.open_for_contributors = body.open_for_contributors
        if new_summary is not None:
            project.solution_summary = new_summary

        db.commit()
        db.refresh(project)

        if new_summary is not None:
            # summary edits re-run the relevance check (rate limited by the
            # auto-reverify interval); all SubmissionErrors map to clean
            # {"code", "message"} responses — the PATCH itself still succeeded.
            await verification.reverify_after_summary_edit(db, project, project.problem, user, new_summary)
    except SubmissionError as err:
        db.rollback()
        raise _error(err)
    except Exception:  # noqa: BLE001 - verification must never break the PATCH
        db.rollback()
    db.refresh(project)
    return project_out_safely(project, include_private=True)


async def _completion_checklist(project: Project, user: User) -> tuple[list[schemas.CompletionChecklistItem], dict | None]:
    settings = get_settings()
    progress = await github.get_progress(project.repo_owner, project.repo_name, user.github_token)
    if progress is None:
        return [], None
    verify_ok = project.verification_status == VERIFICATION_VERIFIED
    readme_ok = bool(progress.get("has_readme"))
    commits = int(progress.get("commit_count") or 0)
    commits_ok = commits >= settings.COMPLETE_MIN_COMMITS
    checklist = [
        schemas.CompletionChecklistItem(item="Verified submission", ok=verify_ok),
        schemas.CompletionChecklistItem(item="README", ok=readme_ok),
        schemas.CompletionChecklistItem(
            item=f"At least {settings.COMPLETE_MIN_COMMITS} commits", ok=commits_ok
        ),
    ]
    return checklist, progress


@router.post("/api/projects/{project_id}/complete", response_model=schemas.ProjectOut)
async def complete_project(project_id: int, body: schemas.CompleteIn, user: CurrentUser, db: DB):
    project = _project_or_404(db, project_id)
    if user.id != project.user_id:
        raise HTTPException(status_code=404, detail="Project not found")

    demo_url = verification.validate_demo_url(body.demo_url)
    reflection = verification.clean_text(body.reflection) or None
    if reflection and len(reflection) > 800:
        raise HTTPException(
            status_code=422,
            detail={"code": "invalid_reflection", "message": "Reflection must be at most 800 characters."},
        )

    checklist, progress = await _completion_checklist(project, user)
    if progress is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "github_unavailable", "message": "GitHub is not reachable right now — try again shortly."},
        )
    if not all(item.ok for item in checklist):
        raise HTTPException(
            status_code=422,
            detail={
                "code": "not_ready_to_complete",
                "message": "Not ready to mark this project as completed yet.",
                "checklist": [item.model_dump() for item in checklist],
            },
        )
    if demo_url:
        project.demo_url = demo_url
    if reflection:
        project.reflection = reflection
    project.completed_at = utcnow()
    db.commit()
    db.refresh(project)
    return project_out_safely(project, include_private=True)


@router.post("/api/projects/{project_id}/reopen", response_model=schemas.ProjectOut)
def reopen_project(project_id: int, user: CurrentUser, db: DB):
    project = _project_or_404(db, project_id)
    if user.id != project.user_id:
        raise HTTPException(status_code=404, detail="Project not found")
    project.completed_at = None
    db.commit()
    db.refresh(project)
    return project_out_safely(project, include_private=True)


# ---------------------------------------------------------------------------
# Reports (§8) — logged-in users, once per project, not the owner
# ---------------------------------------------------------------------------


@router.post("/api/projects/{project_id}/report", status_code=201)
def report_project(project_id: int, body: schemas.ReportIn, user: CurrentUser, db: DB):
    project = _project_or_404(db, project_id)
    if not visibility.can_view_project(project, user):
        raise HTTPException(status_code=404, detail="Project not found")
    if user.id == project.user_id:
        raise HTTPException(
            status_code=422,
            detail={"code": "cannot_report_own_project", "message": "You cannot report your own submission."},
        )
    if not REPORT_LIMITER.allowed(f"report:{user.id}"):
        raise HTTPException(
            status_code=429, detail={"code": "rate_limited", "message": "Too many reports this hour — try again later."}
        )
    reason = verification.clean_text(body.reason)[:300]
    existing = db.scalar(
        select(ProjectReport).where(
            ProjectReport.project_id == project.id, ProjectReport.reporter_user_id == user.id
        )
    )
    if existing is not None:
        raise HTTPException(
            status_code=409, detail={"code": "already_reported", "message": "You already reported this project."}
        )
    report = ProjectReport(project_id=project.id, reporter_user_id=user.id, reason=reason)
    db.add(report)
    db.commit()
    count = db.scalar(select(func.count(ProjectReport.id)).where(ProjectReport.project_id == project.id)) or 0
    settings = get_settings()
    if count >= settings.REPORTS_BEFORE_REVIEW and project.verification_status != VERIFICATION_REJECTED:
        project.verification_status = VERIFICATION_NEEDS_REVIEW
        project.relevance_reason = "Reported by users"
        db.commit()
    return {"ok": True, "report_count": int(count)}
