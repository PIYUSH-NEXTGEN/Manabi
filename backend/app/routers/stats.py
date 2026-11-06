from fastapi import APIRouter
from sqlalchemy import func, select

from app import schemas
from app.deps import DB
from app.models import Problem, Project, STATUS_PUBLISHED, VERIFICATION_VERIFIED

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats", response_model=schemas.StatsOut)
def stats(db: DB):
    problems = db.scalar(select(func.count(Problem.id)).where(Problem.status == STATUS_PUBLISHED)) or 0
    sources = db.scalar(
        select(func.count(func.distinct(Problem.source_name))).where(Problem.status == STATUS_PUBLISHED)
    ) or 0
    fields = db.scalar(
        select(func.count(func.distinct(Problem.field))).where(Problem.status == STATUS_PUBLISHED)
    ) or 0
    # Public counters show verified submissions only (§7.4)
    projects = db.scalar(
        select(func.count(Project.id)).where(Project.verification_status == VERIFICATION_VERIFIED)
    ) or 0
    return schemas.StatsOut(problems=problems, sources=sources, fields=fields, projects=projects)
