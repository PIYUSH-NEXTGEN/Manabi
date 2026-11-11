from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app import schemas
from app.deps import DB, CurrentUser, public_user
from app.models import Problem, Project, STATUS_PUBLISHED, User
from app.services.presenters import project_to_out
from app.services import github
from app.services.visibility import filter_visible

router = APIRouter(tags=["profiles"])


@router.get("/api/u/{username}")
def public_profile(username: str, db: DB):
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    rows = db.scalars(
        select(Project)
        .join(Problem, Project.problem_id == Problem.id)
        .where(Project.user_id == user.id, Problem.status == STATUS_PUBLISHED)
        .order_by(Project.id.desc())
    ).all()
    # Public profile: verified rows only. For everyone (the owner has their
    # own dashboard for non-verified states).
    projects = filter_visible(rows, None)
    return {
        "user": public_user(user),
        "projects": [project_to_out(project) for project in projects],
    }


@router.get("/api/me/github-heatmap", response_model=schemas.HeatmapOut)
async def github_heatmap(user: CurrentUser):
    """Daily public push activity for the logged-in user (last 13 weeks).

    Degrades to `{days: [], total: 0, window_days: N}` when GitHub is
    unreachable. The UI shows an honest empty grid, never fake data.
    """
    days = await github.fetch_contribution_histogram(user.username, user.github_token)
    if days is None:
        return schemas.HeatmapOut(days=[], total=0, window_days=github.HEATMAP_DAYS)
    return schemas.HeatmapOut(
        days=[schemas.HeatmapDay(**day) for day in days],
        total=sum(day["count"] for day in days),
        window_days=github.HEATMAP_DAYS,
    )
