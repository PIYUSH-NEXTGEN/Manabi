"""Project management surface (§7): owner-only DELETE / PATCH / complete /
reopen and their guards."""

from datetime import datetime, timedelta, timezone

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response as HTTPResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import Problem, Project, User

NOW = datetime.now(timezone.utc)


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


@pytest.fixture
def user(db_session):
    u = User(github_id=42, username="octocat", name="Octo", avatar_url="http://a/1.png",
             github_token="tok")
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    return u


@pytest.fixture
def other(db_session):
    u = User(github_id=7, username="other")
    db_session.add(u)
    db_session.commit()
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
        verification_status="verified",
        solution_summary="Flood alert triage pipeline that ranks incoming reports and alerts the ministry.",
    )
    fields.update(overrides)
    project = Project(**fields)
    db_session.add(project)
    db_session.commit()
    return project


def mock_repo_progress(commits=1, readme_status=200):
    commits_list = [
        {"sha": f"s{i}", "commit": {"committer": {"date": "2026-11-01T00:00:00Z"}, "message": "work"}}
        for i in range(commits)
    ]
    ctx = respx.mock(assert_all_called=False)
    ctx.get("https://api.github.com/repos/octocat/triage/commits").mock(
        return_value=HTTPResponse(200, json=commits_list)
    )
    ctx.get("https://api.github.com/repos/octocat/triage/readme").mock(
        return_value=HTTPResponse(readme_status, json={})
    )
    ctx.get("https://api.github.com/repos/octocat/triage/issues").mock(
        return_value=HTTPResponse(200, json=[])
    )
    return ctx


REPO_PAYLOAD = {
    "id": 999,
    "name": "triage",
    "full_name": "octocat/triage",
    "owner": {"login": "octocat", "id": 42, "type": "User"},
    "private": False,
    "fork": False,
    "archived": False,
    "disabled": False,
    "size": 120,
    "description": "flood triage tool",
    "topics": [],
    "language": "Python",
    "created_at": "2026-10-01T00:00:00Z",
}


def mock_repo_for_reverify():
    ctx = respx.mock(assert_all_called=False)
    ctx.get("https://api.github.com/repos/octocat/triage").mock(
        return_value=HTTPResponse(200, json=REPO_PAYLOAD)
    )
    ctx.get("https://api.github.com/repos/octocat/triage/readme").mock(
        return_value=HTTPResponse(404, json={})
    )
    ctx.get("https://api.github.com/repos/octocat/triage/commits").mock(
        return_value=HTTPResponse(200, json=[
            {"sha": "s", "commit": {"committer": {"date": "2026-11-01T00:00:00Z"}, "message": "work"}}
        ])
    )
    return ctx


# --- DELETE ---


def test_delete_own_project_204(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    res = client.delete(f"/api/projects/{project.id}")
    assert res.status_code == 204
    assert db_session.get(Project, project.id) is None


def test_delete_other_project_404(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem)
    res = client.delete(f"/api/projects/{project.id}")
    assert res.status_code == 404
    assert db_session.get(Project, project.id) is not None


# --- PATCH ---


def test_patch_summary_and_demo(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    new_summary = "Flood alert triage pipeline, now with faster deduplication and alert cadence tuning."
    with mock_repo_for_reverify():
        res = client.patch(
            f"/api/projects/{project.id}",
            json={"solution_summary": new_summary, "demo_url": "https://example.com/demo", "open_for_contributors": False},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["solution_summary"] == new_summary
    assert data["demo_url"] == "https://example.com/demo"
    assert data["open_for_contributors"] is False


def test_patch_rejects_bad_demo_url(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    res = client.patch(f"/api/projects/{project.id}", json={"demo_url": "javascript:alert(1)"})
    assert res.status_code == 422
    assert res.json()["detail"]["code"] == "invalid_demo_url"


def test_patch_summary_triggers_reverify(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    # the LLM stays on mock: the fallback is decided by tokens, so this PATCH
    # lands needs_review even though the row was verified before
    with mock_repo_for_reverify():
        res = client.patch(
            f"/api/projects/{project.id}",
            json={"solution_summary": "Flood alert triage pipeline, now with faster dedup and cadence tuning for alerts."},
        )
    assert res.status_code == 200
    assert res.json()["verification_status"] in ("needs_review", "verified")


def test_patch_other_project_404(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem)
    res = client.patch(
        f"/api/projects/{project.id}",
        json={"solution_summary": "Flood alert triage pipeline, now with faster deduplication cadence."},
    )
    assert res.status_code == 404


# --- complete / reopen ---


def test_complete_requires_checklist(db_session, client, user):
    problem = make_problem(db_session)
    # needs_review => checklist item 1 fails even with README + commits
    project = make_project(db_session, user, problem, verification_status="needs_review")
    with mock_repo_progress(commits=6):
        res = client.post(
            f"/api/projects/{project.id}/complete",
            json={"demo_url": "https://example.com/demo", "reflection": "Learned rate limiting."},
        )
        assert res.status_code == 422
        data = res.json()
        assert data["detail"]["code"] == "not_ready_to_complete"
        items = {item["item"]: item["ok"] for item in data["detail"]["checklist"]}
        assert items["Verified submission"] is False
        assert items["README"] is True
        assert items["At least 5 commits"] is True


def test_complete_success_sets_completed_at(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    with mock_repo_progress(commits=8):
        res = client.post(
            f"/api/projects/{project.id}/complete",
            json={"demo_url": "https://example.com/demo", "reflection": "Learned a lot."},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["completed_at"] is not None
    assert db_session.get(Project, project.id).completed_at is not None


def test_complete_github_down_503(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/triage/commits").mock(
            return_value=HTTPResponse(403, json={})
        )
        res = client.post(f"/api/projects/{project.id}/complete", json={"demo_url": "https://example.com/d"})
    assert res.status_code == 503
    assert res.json()["detail"]["code"] == "github_unavailable"


def test_complete_other_project_404(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem)
    res = client.post(f"/api/projects/{project.id}/complete", json={"demo_url": "https://example.com/d"})
    assert res.status_code == 404


def test_reopen_clears_completed_at(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem, completed_at=datetime.now(timezone.utc))
    res = client.post(f"/api/projects/{project.id}/reopen")
    assert res.status_code == 200
    assert res.json()["completed_at"] is None
    assert db_session.get(Project, project.id).completed_at is None


def test_reopen_other_project_404(db_session, client, user, other):
    problem = make_problem(db_session)
    project = make_project(db_session, other, problem, completed_at=datetime.now(timezone.utc))
    res = client.post(f"/api/projects/{project.id}/reopen")
    assert res.status_code == 404


# --- cross-user / admin detail visibility ---


def test_detail_owner_sees_private_fields(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem, verification_status="needs_review",
                           relevance_reason="pre", ownership_basis="owner")
    res = client.get(f"/api/projects/{project.id}")
    data = res.json()
    assert data["relevance_reason"] == "pre"
    assert data["ownership_basis"] == "owner"


def test_detail_public_sees_verified_and_no_private(db_session, client, user, other, anon):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem)  # owner != viewer; verified
    res = client.get(f"/api/projects/{project.id}")
    data = res.json()
    assert res.status_code == 200
    assert data["relevance_reason"] is None
    assert data["ownership_basis"] is None


def test_detail_hides_unverified_from_others(db_session, client, user, other, anon):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem, verification_status="needs_review")
    res = client.get(f"/api/projects/{project.id}")
    assert res.status_code == 404


def test_detail_owner_sees_unverified_own(db_session, client, user):
    problem = make_problem(db_session)
    project = make_project(db_session, user, problem, verification_status="needs_review")
    res = client.get(f"/api/projects/{project.id}")
    assert res.status_code == 200
    assert res.json()["verification_status"] == "needs_review"
