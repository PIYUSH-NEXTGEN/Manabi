"""Admin submissions queue: auth, filters, approve/reject, evidence fields."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user
from app.main import app
from app.models import Project, Problem, User


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
def user(db_session):
    u = User(github_id=42, username="octocat", name="Octo", avatar_url="http://a/1.png")
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    return u


@pytest.fixture
def other(db_session):
    u = User(github_id=7, username="helper")
    db_session.add(u)
    db_session.commit()
    return u


@pytest.fixture
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


def make_problem(db_session, **overrides) -> Problem:
    fields = dict(
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
        source_id="SIH26001",
        original_text="verbatim",
    )
    fields.update(overrides)
    problem = Problem(**fields)
    db_session.add(problem)
    db_session.commit()
    return problem


def make_project(db_session, user, problem, **overrides) -> Project:
    fields = dict(
        problem_id=problem.id,
        user_id=user.id,
        repo_owner="octocat",
        repo_name="triage",
        repo_url="https://github.com/octocat/triage",
    )
    fields.update(overrides)
    project = Project(**fields)
    db_session.add(project)
    db_session.commit()
    return project


def test_admin_queue_requires_auth(db_session, client):
    app.dependency_overrides.pop(get_current_user, None)
    res = client.get("/api/admin/submissions")
    assert res.status_code == 401


def test_admin_queue_forbidden_for_non_admin(db_session, client, user, monkeypatch):
    monkeypatch.setenv("ADMIN_GITHUB_USERNAMES", "somebody-else")
    config.get_settings.cache_clear()
    try:
        res = client.get("/api/admin/submissions")
        assert res.status_code == 403
    finally:
        config.get_settings.cache_clear()


def test_admin_queue_lists_evidence(db_session, client, user, other):
    problem = make_problem(db_session)
    make_project(
        db_session, other, problem, verification_status="needs_review",
        relevance_score=0.42, relevance_reason="keywords", ownership_basis="contributor",
    )
    res = client.get("/api/admin/submissions")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    item = data["items"][0]
    assert item["relevance_score"] == 0.42
    assert item["ownership_basis"] == "contributor"
    assert item["submitter"] == "helper"
    assert item["problem_title"] == "Flood alert app"
    assert item["report_count"] == 0


def test_admin_filter_by_status(db_session, client, user, other):
    problem = make_problem(db_session)
    make_project(db_session, other, problem, verification_status="needs_review")
    make_project(db_session, other, problem, repo_name="t2", repo_url="https://github.com/octocat/t2",
                 verification_status="rejected")
    res = client.get("/api/admin/submissions", params={"status": "rejected"})
    data = res.json()
    assert data["total"] == 1
    assert data["items"][0]["verification_status"] == "rejected"


def test_admin_approve_verifies(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem, verification_status="needs_review")
    res = client.post(f"/api/admin/submissions/{project.id}/approve", params={"note": "checked manually"})
    assert res.status_code == 200
    assert res.json()["verification_status"] == "verified"
    row = db_session.get(Project, project.id)
    assert row.verification_status == "verified"
    assert row.review_note == "checked manually"


def test_admin_reject_rejects(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem, verification_status="needs_review")
    res = client.post(f"/api/admin/submissions/{project.id}/reject")
    assert res.status_code == 200
    assert db_session.get(Project, project.id).verification_status == "rejected"


def test_admin_unknown_submission_404(db_session, client, user):
    res = client.post("/api/admin/submissions/999/approve")
    assert res.status_code == 404
