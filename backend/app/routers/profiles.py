from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app import schemas
from app.deps import DB, public_user
from app.models import MLAttempt, Project, User
from app.routers.problems import project_to_out

router = APIRouter(tags=["profiles"])


@router.get("/api/u/{username}")
def public_profile(username: str, db: DB):
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    projects = db.scalars(select(Project).where(Project.user_id == user.id).order_by(Project.id.desc())).all()
    solved_ml_count = db.scalar(
        select(func.count(func.distinct(MLAttempt.question_id))).where(MLAttempt.user_id == user.id)
    )
    return {
        "user": public_user(user),
        "projects": [project_to_out(project) for project in projects],
        "solved_ml_count": solved_ml_count or 0,
    }
