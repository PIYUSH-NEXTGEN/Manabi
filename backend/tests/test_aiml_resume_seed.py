"""Guards the curated AI/ML resume pack and its long-form details."""

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import schemas
from app.db import Base
from app.models import Problem
from app.seed import runner
from app.seed.aiml_resume_details import DETAILS
from app.seed.seed_aiml_projects import PROBLEMS


def test_aiml_resume_pack_matches_schema():
    assert len(PROBLEMS) == 24
    assert len({p["source_id"] for p in PROBLEMS}) == 24
    assert set(DETAILS) == {p["source_id"] for p in PROBLEMS}

    for problem in PROBLEMS:
        assert problem["field"] == "aiml"
        assert problem["goal"] == "resume"
        schemas.ProblemCard.model_validate(problem)
        resume_kit = schemas.ResumeKit.model_validate(problem["resume_kit"])
        assert len(resume_kit.target_roles) == 3
        assert len(problem["build_guide"]) == 5
        assert DETAILS[problem["source_id"]]["description"].rstrip() in problem["summary"]
        for phase in problem["build_guide"]:
            schemas.BuildGuidePhase.model_validate(phase)
            assert len(phase["steps"]) == 4


def test_aiml_details_keep_responsible_use_last():
    for problem in PROBLEMS:
        summary = problem["summary"]
        marker = "\n\nResponsible use:"
        if marker in summary:
            description = DETAILS[problem["source_id"]]["description"].rstrip()
            assert summary.rfind(marker) > summary.rfind(description)


def test_seed_inserts_then_updates_without_duplicates(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    monkeypatch.setattr(runner, "get_session_factory", lambda: factory)

    runner.seed_problems(PROBLEMS)
    runner.seed_problems(PROBLEMS)
    runner.seed_problems(PROBLEMS, update=True)

    session = factory()
    try:
        count = session.scalar(select(func.count(Problem.id)))
        assert count == 24
        rows = session.scalars(select(Problem)).all()
        assert all(len(row.resume_kit["target_roles"]) == 3 for row in rows)
        assert all(len(row.build_guide) == 5 for row in rows)
        assert all(row.field == "aiml" and row.goal == "resume" for row in rows)
    finally:
        session.close()
