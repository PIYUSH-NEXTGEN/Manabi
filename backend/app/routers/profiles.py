from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app import schemas
from app.deps import DB, public_user
from app.models import Problem, Project, STATUS_PUBLISHED, User
from app.routers.problems import project_to_out

router = APIRouter(tags=["profiles"])


@router.get("/api/u/{username}")
def public_profile(username: str, db: DB):
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    projects = db.scalars(
        select(Project)
        .join(Problem, Project.problem_id == Problem.id)
        .where(Project.user_id == user.id, Problem.status == STATUS_PUBLISHED)
        .order_by(Project.id.desc())
    ).all()
    return {
        "user": public_user(user),
        "projects": [project_to_out(project) for project in projects],
    }
