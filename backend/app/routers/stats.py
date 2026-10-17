from fastapi import APIRouter
from sqlalchemy import func, select

from app import schemas
from app.deps import DB
from app.models import MLQuestion, Problem, Project

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats", response_model=schemas.StatsOut)
def stats(db: DB):
    problems = db.scalar(select(func.count(Problem.id))) or 0
    sources = db.scalar(select(func.count(func.distinct(Problem.source_name)))) or 0
    fields = db.scalar(select(func.count(func.distinct(Problem.field)))) or 0
    projects = db.scalar(select(func.count(Project.id))) or 0
    ml_questions = db.scalar(select(func.count(MLQuestion.id))) or 0
    return schemas.StatsOut(
        problems=problems, sources=sources, fields=fields, projects=projects, ml_questions=ml_questions
    )
