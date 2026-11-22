"""Guards the curated Web Dev learning pack from webdev_projects.md."""

from collections import Counter

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import schemas
from app.db import Base
from app.models import Problem
from app.seed import runner
from app.seed.seed_webdev_learning_projects import PROBLEMS


def test_webdev_learning_pack_matches_schema():
    assert len(PROBLEMS) == 36
    assert len({p["source_id"] for p in PROBLEMS}) == 36
    assert len({p["title"] for p in PROBLEMS}) == 36
    assert len({p["summary"] for p in PROBLEMS}) == 36
    assert Counter(p["difficulty"] for p in PROBLEMS) == {
        "beginner": 10,
        "intermediate": 19,
        "advanced": 7,
    }

    for problem in PROBLEMS:
        assert problem["field"] == "web-dev"
        assert problem["goal"] == "learning"
        assert "resume_kit" not in problem
        assert "team_plan" not in problem
        assert "pitch_guide" not in problem
        assert len(problem["learning_concepts"]) >= 4
        schemas.ProblemCard.model_validate(problem)

        assert len(problem["build_guide"]) == 5
        for phase in problem["build_guide"]:
            schemas.BuildGuidePhase.model_validate(phase)
            assert len(phase["steps"]) == 4


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
        assert count == 36
        rows = session.scalars(select(Problem)).all()
        assert all(row.goal == "learning" for row in rows)
        assert all(len(row.learning_concepts) >= 4 for row in rows)
        assert all(row.resume_kit is None for row in rows)
        assert all(row.team_plan is None for row in rows)
        assert all(row.pitch_guide is None for row in rows)
        assert all(len(row.build_guide) == 5 for row in rows)
    finally:
        session.close()
