"""Endpoint visibility (§7.4): problems list/detail counts, /api/stats,
public profile. Alongside is_admin behaviour."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import Problem, Project, User
from app.services.visibility import can_view_project, is_admin

USER_ID = 42


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
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
    app.dependency_overrides.pop(get_optional_user, None)


@pytest.fixture
def user(db_session):
    u = User(github_id=USER_ID, username="octocat", name="Octo", avatar_url="http://a/1.png")
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    return u


@pytest.fixture
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def anon():
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)


def make_problem(db_session, **overrides) -> Problem:
    fields = dict(
        title="Flood alert app",
        summary="Predict floods",
        who_affected="Ministry X",
        why_matters="Saves people",
        field="aiml",
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
        verification_status="verified",
    )
    fields.update(overrides)
    project = Project(**fields)
    db_session.add(project)
    db_session.commit()
    return project


# --- is_admin / can_view ---


def test_is_admin_from_env(monkeypatch):
    monkeypatch.setenv("ADMIN_GITHUB_USERNAMES", "octocat")
    config.get_settings.cache_clear()
    try:
        admin = User(github_id=1, username="OctoCat")
        other = User(github_id=2, username="someone")
        assert is_admin(admin) is True
        assert is_admin(other) is False
        assert is_admin(None) is False
    finally:
        config.get_settings.cache_clear()


def test_can_view_project_rules():
    other = User(github_id=2, username="other")
    verified = Project(problem_id=1, user_id=other.id, repo_owner="a", repo_name="b",
                       verification_status="verified")
    needs = Project(problem_id=1, user_id=other.id, repo_owner="a", repo_name="b",
                    verification_status="needs_review")
    rejected = Project(problem_id=1, user_id=other.id, repo_owner="a", repo_name="b",
                       verification_status="rejected")
    assert can_view_project(verified, None) is True
    assert can_view_project(needs, None) is False
    assert can_view_project(rejected, None) is False
    # owner sees their own rows in any status
    mine = Project(problem_id=1, user_id=1, repo_owner="a", repo_name="c",
                   verification_status="needs_review")
    assert can_view_project(mine, other) is False
    assert can_view_project(mine, User(github_id=3, username="x", id=1)) is True


# --- problem list & detail counts ---


def test_board_counts_verified_only(db_session, client, user, anon):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    problem = make_problem(db_session)
    make_project(db_session, user, problem, verification_status="verified", completed_at=datetime.now(timezone.utc))
    make_project(db_session, user, problem, repo_name="t2", repo_url="https://github.com/octocat/t2",
                 verification_status="needs_review")
    res = client.get("/api/problems")
    data = res.json()
    item = data["items"][0]
    assert item["project_count"] == 1
    assert item["completed_count"] == 1


def test_board_sort_uses_verified_counts(db_session, client, user, anon):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    ranked = make_problem(db_session, title="Ranked problem")
    hidden = make_problem(db_session, title="Hidden problem", source_id="SIH26002")
    # rows in db that must NOT influence popularity
    make_project(db_session, user, hidden, verification_status="needs_review")
    make_project(db_session, user, ranked, verification_status="verified")
    res = client.get("/api/problems", params={"sort": "popular"})
    data = res.json()
    titles = [i["title"] for i in data["items"]]
    assert titles[0] == "Ranked problem"


def test_problem_detail_filters_non_visible(db_session, client, user, anon):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    problem = make_problem(db_session)
    make_project(db_session, user, problem, verification_status="verified", completed_at=datetime.now(timezone.utc))
    make_project(db_session, user, problem, repo_name="t2", repo_url="https://github.com/octocat/t2",
                 verification_status="needs_review")
    res = client.get(f"/api/problems/{problem.id}")
    data = res.json()
    assert len(data["projects"]) == 1
    assert data["project_count"] == 1
    assert data["completed_count"] == 1
    assert data["projects"][0]["verification_status"] == "verified"


def test_problem_detail_owner_sees_all_statuses(db_session, client, user):
    problem = make_problem(db_session)
    make_project(db_session, user, problem, verification_status="verified")
    make_project(db_session, user, problem, repo_name="t3", repo_url="https://github.com/octocat/t3",
                 verification_status="needs_review", relevance_reason="needs admin review")
    res = client.get(f"/api/problems/{problem.id}")
    assert res.status_code == 200
    data = res.json()
    assert len(data["projects"]) == 2
    statuses = {p["verification_status"] for p in data["projects"]}
    assert statuses == {"verified", "needs_review"}
    needs = next(p for p in data["projects"] if p["verification_status"] == "needs_review")
    assert needs["relevance_reason"] == "needs admin review"


# --- stats + profile ---


def test_stats_counts_verified_only(db_session, client, user, anon):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    problem = make_problem(db_session)
    make_project(db_session, user, problem, verification_status="verified")
    make_project(db_session, user, problem, repo_name="t2", repo_url="https://github.com/octocat/t2",
                 verification_status="rejected")
    res = client.get("/api/stats")
    assert res.status_code == 200
    assert res.json()["projects"] == 1


def test_public_profile_verified_only(db_session, client, user, anon):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    problem = make_problem(db_session)
    make_project(db_session, user, problem, verification_status="verified")
    make_project(db_session, user, problem, repo_name="t4", repo_url="https://github.com/octocat/t4",
                 verification_status="rejected")
    res = client.get("/api/u/octocat")
    assert res.status_code == 200
    data = res.json()
    assert len(data["projects"]) == 1
    assert data["projects"][0]["verification_status"] == "verified"
