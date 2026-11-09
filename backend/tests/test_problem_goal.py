"""Problem track labels ('Browse by goal' board): admin curation endpoint and
public exposure of the `goal` field on problem list/detail payloads."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user
from app.main import app
from app.models import Problem, User


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("ADMIN_GITHUB_USERNAMES", "octocat")
    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = factory()
    app.dependency_overrides[get_db] = lambda: session
    yield session
    app.dependency_overrides.clear()
    session.close()
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def admin(db_session):
    u = User(github_id=42, username="octocat", name="Octo", avatar_url="http://a/1.png")
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    return u


@pytest.fixture
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


def make_problem(db_session, source_id="SIH26001") -> Problem:
    problem = Problem(
        title="Flood alert app",
        summary="Predict floods",
        who_affected="Ministry X",
        why_matters="Saves people",
        field="ml",
        domain="disaster-management",
        difficulty="intermediate",
        est_hours=30,
        tech_tags=["python"],
        datasets=[],
        approaches=[],
        source_name="Smart India Hackathon 2026",
        source_id=source_id,
        original_text="verbatim",
    )
    db_session.add(problem)
    db_session.commit()
    return problem


# ---------------- admin endpoint ----------------

def test_set_goal_requires_auth(db_session, client):
    problem = make_problem(db_session)
    res = client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": "resume"})
    assert res.status_code in (401, 403)


def test_set_goal_forbidden_for_non_admin(db_session, client, monkeypatch):
    db_session.add(User(github_id=7, username="helper"))
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: db_session.query(User).filter_by(username="helper").first()
    problem = make_problem(db_session)
    res = client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": "resume"})
    assert res.status_code == 403


def test_set_goal_happy_path(db_session, client, admin):
    problem = make_problem(db_session)
    res = client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": "hackathon"})
    assert res.status_code == 200
    assert res.json() == {"ok": True, "problem_id": problem.id, "goal": "hackathon"}
    db_session.expire_all()
    assert problem.goal == "hackathon"


def test_clear_goal_with_null(db_session, client, admin):
    problem = make_problem(db_session)
    db_session.refresh(problem)
    problem.goal = "learning"
    db_session.commit()
    res = client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": None})
    assert res.status_code == 200
    db_session.expire_all()
    assert problem.goal is None


def test_set_goal_invalid_value_422(db_session, client, admin):
    problem = make_problem(db_session)
    res = client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": "internship"})
    assert res.status_code == 422
    db_session.expire_all()
    assert problem.goal is None


def test_set_goal_unknown_problem_404(db_session, client, admin):
    res = client.post("/api/admin/problems/9999/goal", json={"goal": "resume"})
    assert res.status_code == 404


# ---------------- public exposure ----------------

def test_list_and_detail_expose_goal(db_session, client, admin):
    problem = make_problem(db_session)
    client.post(f"/api/admin/problems/{problem.id}/goal", json={"goal": "resume"})

    items = client.get("/api/problems").json()["items"]
    assert [it["goal"] for it in items if it["id"] == problem.id] == ["resume"]

    detail = client.get(f"/api/problems/{problem.id}").json()
    assert detail["goal"] == "resume"


def test_unlabelled_goal_is_null_in_api(db_session, client):
    problem = make_problem(db_session)
    items = client.get("/api/problems").json()["items"]
    assert next(it for it in items if it["id"] == problem.id)["goal"] is None
    assert client.get(f"/api/problems/{problem.id}").json()["goal"] is None
