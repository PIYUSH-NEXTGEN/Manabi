"""Guards the curated Web Dev hackathon pack from webdev_projects.md."""

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import schemas
from app.db import Base
from app.models import Problem
from app.seed import runner
from app.seed.seed_webdev_hackathon_projects import PROBLEMS


def test_webdev_hackathon_pack_matches_schema():
    assert len(PROBLEMS) == 22
    assert len({p["source_id"] for p in PROBLEMS}) == 22
    assert len({p["summary"] for p in PROBLEMS}) == 22

    for problem in PROBLEMS:
        assert problem["field"] == "web-dev"
        assert problem["goal"] == "hackathon"
        assert "resume_kit" not in problem
        assert problem["summary"].count("\n\n") == 1
        assert len(problem["summary"]) <= 600
        schemas.ProblemCard.model_validate(problem)

        team_plan = schemas.TeamPlan.model_validate(problem["team_plan"])
        assert len(team_plan.roles) == 3
        assert len(team_plan.milestones) == 4

        pitch_guide = schemas.PitchGuide.model_validate(problem["pitch_guide"])
        assert len(pitch_guide.beats) == 5
        assert len(pitch_guide.judge_questions) == 4

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
        assert count == 22
        rows = session.scalars(select(Problem)).all()
        assert all(row.team_plan is not None for row in rows)
        assert all(row.pitch_guide is not None for row in rows)
        assert all(len(row.build_guide) == 5 for row in rows)
        assert all(row.goal == "hackathon" for row in rows)
    finally:
        session.close()
