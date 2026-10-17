from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.models import MLAttempt, MLQuestion, Problem, Project, User


def make_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return Session(engine)


def make_user(session: Session, github_id: int = 1, username: str = "octocat") -> User:
    user = User(github_id=github_id, username=username, name="Octo Cat", avatar_url="https://x/y.png")
    session.add(user)
    return user


def make_problem(session: Session, source_id: str = "SIH26017", title: str = "Flood alert app") -> Problem:
    problem = Problem(
        title=title,
        summary="A summary",
        who_affected="Coastal districts",
        why_matters="Flooding costs lives",
        field="ml",
        domain="disaster-management",
        difficulty="intermediate",
        est_hours=40,
        tech_tags=["python", "pandas"],
        datasets=[],
        approaches=["Build a classifier"],
        source_name="Smart India Hackathon 2026",
        source_id=source_id,
        source_url="https://example.org/ps",
        source_note=None,
        original_text="Verbatim original text.",
        ai_fields=["tech_tags", "approaches"],
    )
    session.add(problem)
    return problem


def test_create_all_and_user_roundtrip():
    session = make_session()
    user = make_user(session)
    session.commit()
    loaded = session.scalar(select(User).where(User.github_id == 1))
    assert loaded is not None
    assert loaded.username == "octocat"
    assert loaded.signals_json == {}
    assert loaded.github_token is None
    session.close()


def test_github_id_is_unique():
    session = make_session()
    session.add(User(github_id=1, username="a"))
    session.add(User(github_id=1, username="b"))
    try:
        session.commit()
        raised = False
    except Exception:
        session.rollback()
        raised = True
    assert raised
    session.close()


def test_problem_json_fields_and_defaults():
    session = make_session()
    problem = make_problem(session)
    session.commit()
    loaded = session.scalar(select(Problem))
    assert loaded.tech_tags == ["python", "pandas"]
    assert loaded.datasets == []
    assert loaded.ai_fields == ["tech_tags", "approaches"]
    assert loaded.created_by is None
    assert loaded.created_at is not None
    session.close()


def test_problem_unique_source_name_and_id():
    session = make_session()
    make_problem(session)
    make_problem(session)
    try:
        session.commit()
        raised = False
    except Exception:
        session.rollback()
        raised = True
    assert raised
    session.close()


def test_project_unique_per_problem_user_repo():
    session = make_session()
    user = make_user(session)
    problem = make_problem(session)
    session.commit()
    args = dict(
        repo_owner="octocat",
        repo_name="flood-app",
        repo_url="https://github.com/octocat/flood-app",
        open_for_contributors=True,
    )
    session.add(Project(problem_id=problem.id, user_id=user.id, **args))
    session.commit()
    session.add(Project(problem_id=problem.id, user_id=user.id, **args))
    try:
        session.commit()
        raised = False
    except Exception:
        session.rollback()
        raised = True
    assert raised
    session.close()


def test_project_relationships():
    session = make_session()
    user = make_user(session)
    problem = make_problem(session)
    session.commit()
    session.add(
        Project(problem_id=problem.id, user_id=user.id, repo_owner="o", repo_name="r", repo_url="https://github.com/o/r")
    )
    session.commit()
    loaded_problem = session.scalar(select(Problem))
    loaded_user = session.scalar(select(User))
    assert len(loaded_problem.projects) == 1
    assert loaded_user.projects[0].problem.title == "Flood alert app"
    assert loaded_user.projects[0].user.github_id == 1
    session.close()


def test_ml_question_and_attempt_roundtrip():
    session = make_session()
    user = make_user(session)
    rubric = [
        {"id": "r1", "point": "Identifies data leakage"},
        {"id": "r2", "point": "Proposes a fix"},
    ]
    question = MLQuestion(
        title="Why did the model collapse?",
        scenario="## Logs\nprecision dropped after launch",
        difficulty="intermediate",
        topic="data-leakage",
        rubric_json=rubric,
        explanation="Because of leakage.",
    )
    session.add(question)
    session.commit()
    session.add(
        MLAttempt(
            question_id=question.id,
            user_id=user.id,
            answer="The pipeline leaked future data.",
            feedback_json={"covered_count": 1, "total": 2},
        )
    )
    session.commit()
    loaded_q = session.scalar(select(MLQuestion))
    loaded_a = session.scalar(select(MLAttempt))
    assert loaded_q.rubric_json == rubric
    assert loaded_a.question.topic == "data-leakage"
    assert loaded_a.user.username == "octocat"
    assert loaded_a.feedback_json["covered_count"] == 1
    session.close()
