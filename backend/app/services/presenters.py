"""Row -> API-schema presenters shared by the routers.

Problem/project rows are surfaced by several routers (problems, projects,
profiles, recommendations, admin); keeping the single construction point
here stops the response shape from drifting between endpoints.
"""

from app import schemas
from app.models import Problem, Project


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


def project_out_safely(project: Project, include_private: bool = False) -> schemas.ProjectOut:
    """project_to_out with the cached progress JSON re-validated, so a
    hand-edited or stale progress blob cannot fail response validation."""
    out = project_to_out(project, include_private=include_private)
    if out.progress is not None:
        out.progress = schemas.Progress.model_validate(out.progress)
    return out
