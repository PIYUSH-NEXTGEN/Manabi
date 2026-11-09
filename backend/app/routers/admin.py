"""Admin submissions queue (§8): list needs_review/rejected/verified rows with
their evidence, approve or reject them. Problem-review endpoints were removed
deliberately — this queue is for project submissions only."""

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app import schemas
from app.deps import AdminUser, DB
from app.models import Problem, Project, ProjectReport, VERIFICATION_NEEDS_REVIEW, VERIFICATION_REJECTED, VERIFICATION_VERIFIED
from app.services import verification

router = APIRouter(prefix="/api/admin/submissions", tags=["admin"])

# Manual track curation (§ board "Browse by goal"). Separate router so the
# submissions-only contract above stays untouched.
problems_router = APIRouter(prefix="/api/admin/problems", tags=["admin"])


@problems_router.post("/{problem_id}/goal", response_model=schemas.AdminGoalOut)
def set_problem_goal(problem_id: int, body: schemas.AdminGoalSetIn, user: AdminUser, db: DB):
    """Label (or unlabel) a problem as resume / hackathon / learning material.

    Only admins can curate; null clears the label. Invalid values are rejected
    by the schema as 422.
    """
    problem = db.scalar(select(Problem).where(Problem.id == problem_id))
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    problem.goal = body.goal
    db.commit()
    return schemas.AdminGoalOut(ok=True, problem_id=problem.id, goal=problem.goal)


def _submission_reports(db, project_ids: list[int]) -> dict[int, tuple[int, str | None]]:
    """Bulk (report_count, latest_note) for the page's projects.

    Earlier revisions ran two scalar queries per row here (classic N+1 — 102
    queries for a 50-row page). Two grouped statements replace them; the
    latest-note tie-break (id desc) is deterministic, which the per-row
    `created_at desc, limit 1` version was not on ties.
    """
    if not project_ids:
        return {}
    counts = dict(db.execute(
        select(ProjectReport.project_id, func.count(ProjectReport.id))
        .where(ProjectReport.project_id.in_(project_ids))
        .group_by(ProjectReport.project_id)
    ).all())
    ranked = select(
        ProjectReport.project_id,
        ProjectReport.reason,
        func.row_number()
        .over(
            partition_by=ProjectReport.project_id,
            order_by=(ProjectReport.created_at.desc(), ProjectReport.id.desc()),
        )
        .label("rn"),
    ).where(ProjectReport.project_id.in_(project_ids)).subquery()
    latest: dict[int, str | None] = {}
    for project_id, reason in db.execute(
        select(ranked.c.project_id, ranked.c.reason).where(ranked.c.rn == 1)
    ).all():
        latest[project_id] = reason
    return {
        pid: (int(counts.get(pid, 0)), latest.get(pid))
        for pid in project_ids
    }


def _submission_to_out(
    db,
    project: Project,
    reports: tuple[int, str | None],
) -> schemas.AdminSubmissionOut:
    problem = project.problem
    user = project.user
    report_count, latest_note = reports
    return schemas.AdminSubmissionOut(
        id=project.id,
        problem_id=project.problem_id,
        problem_title=problem.title if problem else "",
        repo_url=project.repo_url,
        repo_owner=project.repo_owner,
        repo_name=project.repo_name,
        submitter=user.username if user else "",
        submitter_avatar_url=user.avatar_url if user else None,
        verification_status=project.verification_status,
        ownership_basis=project.ownership_basis,
        relevance_score=project.relevance_score,
        relevance_reason=project.relevance_reason or latest_note,
        solution_summary=project.solution_summary or None,
        review_note=project.review_note,
        demo_url=project.demo_url,
        reflection=project.reflection,
        open_for_contributors=project.open_for_contributors,
        report_count=int(report_count),
        created_at=project.created_at,
        completed_at=project.completed_at,
    )


@router.get("", response_model=schemas.AdminSubmissionsOut)
def list_submissions(
    user: AdminUser,
    db: DB,
    status: str = VERIFICATION_NEEDS_REVIEW,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    if status not in (VERIFICATION_VERIFIED, VERIFICATION_NEEDS_REVIEW, VERIFICATION_REJECTED):
        raise HTTPException(status_code=422, detail="Unknown status filter")
    query = select(Project).options(
        joinedload(Project.problem), joinedload(Project.user)
    ).where(Project.verification_status == status)
    total = db.scalar(select(func.count(Project.id)).where(Project.verification_status == status)) or 0
    rows = db.scalars(query.order_by(Project.created_at.desc()).limit(limit).offset(offset)).all()
    reports = _submission_reports(db, [p.id for p in rows])
    return schemas.AdminSubmissionsOut(
        items=[_submission_to_out(db, p, reports[p.id]) for p in rows], total=int(total)
    )


@router.post("/{project_id}/approve", response_model=schemas.AdminSubmissionActionOut)
def approve_submission(project_id: int, user: AdminUser, db: DB, note: str | None = None):
    project = db.scalar(select(Project).options(joinedload(Project.problem)).where(Project.id == project_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project.verification_status = VERIFICATION_VERIFIED
    if note:
        project.review_note = verification.clean_text(note)[:2000]
    db.commit()
    return schemas.AdminSubmissionActionOut(ok=True, project_id=project.id, verification_status=project.verification_status)


@router.post("/{project_id}/reject", response_model=schemas.AdminSubmissionActionOut)
def reject_submission(project_id: int, user: AdminUser, db: DB, note: str | None = None):
    project = db.scalar(select(Project).where(Project.id == project_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project.verification_status = VERIFICATION_REJECTED
    if note:
        project.review_note = verification.clean_text(note)[:2000]
    db.commit()
    return schemas.AdminSubmissionActionOut(ok=True, project_id=project.id, verification_status=project.verification_status)
