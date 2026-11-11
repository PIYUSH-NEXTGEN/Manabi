from datetime import datetime, timedelta, timezone

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response as HTTPResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import Problem, Project, User
from app.services.github import parse_repo_url

NOW = datetime.now(timezone.utc)
USER_ID = 42
SUMMARY = "Flood alert triage pipeline that ranks incoming reports, filters duplicates and alerts the field ministry in real time with python ml."


@pytest.fixture(autouse=True)
def env(monkeypatch):
    from app import config

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
    u = User(github_id=USER_ID, username="octocat", name="Octo", avatar_url="http://a/1.png", github_token=None)
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    return u


@pytest.fixture
def anon(db_session):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)


@pytest.fixture
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def problem(db_session):
    p = Problem(
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
    db_session.add(p)
    db_session.commit()
    return p


def commit(sha: str, date: datetime, message: str = "work") -> dict:
    return {"sha": sha, "commit": {"committer": {"date": date.strftime("%Y-%m-%dT%H:%M:%SZ")}, "message": message}}


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


@pytest.fixture
def github_repo_mock():
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/triage").mock(
            return_value=HTTPResponse(200, json=REPO_PAYLOAD)
        )
        mock.get("https://api.github.com/repos/octocat/triage/commits").mock(
            return_value=HTTPResponse(403, json={"message": "rate limit"})
        )
        mock.get("https://api.github.com/repos/octocat/triage/readme").mock(
            return_value=HTTPResponse(
                200,
                json={"content": __import__("base64").b64encode(
                    b"Flood alert triage pipeline that ranks incoming reports and alerts the field ministry."
                ).decode()},
            )
        )
        yield mock


def mock_progress_fetch(mock, commits: list[dict], readme_status=200, issues: list | None = None, issue_status=200):
    mock.get("https://api.github.com/repos/octocat/triage/commits").mock(
        return_value=HTTPResponse(200, json=commits)
    )
    mock.get("https://api.github.com/repos/octocat/triage/readme").mock(
        return_value=HTTPResponse(readme_status, json={"name": "README.md"})
    )
    mock.get("https://api.github.com/repos/octocat/triage/issues").mock(
        return_value=HTTPResponse(issue_status, json=issues if issues is not None else [])
    )


def make_project(db_session, user, problem, **overrides) -> Project:
    fields = dict(
        problem_id=problem.id,
        user_id=user.id,
        repo_owner="octocat",
        repo_name="triage",
        repo_url="https://github.com/octocat/triage",
        open_for_contributors=True,
    )
    fields.update(overrides)
    project = Project(**fields)
    db_session.add(project)
    db_session.commit()
    return project


# --- URL parsing ---

def test_parse_repo_url_variants():
    assert parse_repo_url("https://github.com/octocat/triage") == ("octocat", "triage")
    assert parse_repo_url("https://github.com/octocat/triage/") == ("octocat", "triage")
    assert parse_repo_url("https://github.com/octocat/triage.git") == ("octocat", "triage")
    assert parse_repo_url("https://www.github.com/octocat/triage") == ("octocat", "triage")
    assert parse_repo_url("http://github.com/octocat/triage/") == ("octocat", "triage")
    assert parse_repo_url("https://github.com/octocat/triage/extra") is None
    assert parse_repo_url("https://github.com/octocat") is None
    assert parse_repo_url("https://gitlab.com/octocat/triage") is None
    assert parse_repo_url("ftp://github.com/octocat/triage") is None
    assert parse_repo_url("") is None
    assert parse_repo_url("https://github.com/octocat/") is None


def test_parse_repo_url_rejects_garbage():
    assert parse_repo_url("not a url") is None
    assert parse_repo_url("https://github.com/octocat/.git") is None


def test_parse_repo_url_rejects_encoded_separators():
    """Percent-encodings that change when decoded must not smuggle path
    separators: e.g. /repos/a%2Fb/c on api.github.com actually resolves to
    /repos/a/b/c. A different repository than the URL the visitor saw."""
    assert parse_repo_url("https://github.com/a%2Fb/c") is None
    assert parse_repo_url("https://github.com/octocat/triage%2Fx") is None
    assert parse_repo_url("https://github.com/octocat/tra%252Fiage") is None  # double encoding
    assert parse_repo_url("https://github.com/octocat/tr%69age") is None
    assert parse_repo_url("https://github.com/../boss/c") is None


def test_parse_repo_url_still_accepts_plain_names():
    assert parse_repo_url("https://github.com/octocat/triage.web") == ("octocat", "triage.web")
    assert parse_repo_url("https://github.com/octocat/triage_2.0") == ("octocat", "triage_2.0")


def test_parse_repo_url_case_insensitive_host():
    assert parse_repo_url("https://GITHUB.com/octocat/triage") == ("octocat", "triage")


# --- submit project ---

def test_submit_project_requires_auth(db_session, client, problem, anon):
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage", "solution_summary": SUMMARY},
    )
    assert res.status_code == 401


def test_submit_project_happy_path(db_session, client, user, problem, github_repo_mock):
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage", "solution_summary": SUMMARY, "open_for_contributors": True},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["repo_owner"] == "octocat" and data["repo_name"] == "triage"
    assert data["problem_id"] == problem.id
    assert data["owner"] == {"username": "octocat", "avatar_url": "http://a/1.png"}
    assert data["open_for_contributors"] is True
    assert data["progress"] is None
    # mock LLM never verifies: fallback sends the row to needs_review
    assert data["verification_status"] == "needs_review"
    assert data["relevance_reason"] is not None
    assert data["review_note"] is None


def test_submit_project_invalid_url_422(client, user, problem, github_repo_mock):
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://gitlab.com/a/b", "solution_summary": SUMMARY},
    )
    assert res.status_code == 422
    assert res.json()["detail"]["code"] == "invalid_repo_url"


def test_submit_project_invalid_summary_422(client, user, problem, github_repo_mock):
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage", "solution_summary": "x" * 401},
    )
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"][-1] == "solution_summary"


def test_submit_project_summary_optional_and_demo_url(db_session, client, user, problem, github_repo_mock):
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage", "demo_url": "https://example.com/live"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["solution_summary"] is None
    assert data["demo_url"] == "https://example.com/live"


def test_submit_project_missing_or_private_repo_422(db_session, client, user, problem):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/ghost").mock(return_value=HTTPResponse(404, json={}))
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={"repo_url": "https://github.com/octocat/ghost", "solution_summary": SUMMARY},
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "repo_not_found"


def test_submit_project_duplicate_409(db_session, client, user, problem, github_repo_mock):
    res1 = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage", "solution_summary": SUMMARY, "open_for_contributors": True},
    )
    assert res1.status_code == 201
    res = client.post(
        f"/api/problems/{problem.id}/projects",
        json={"repo_url": "https://github.com/octocat/triage.git", "solution_summary": SUMMARY},
    )
    assert res.status_code == 409
    assert res.json()["detail"]["code"] == "already_submitted"


def test_submit_project_unknown_problem_404(db_session, client, user, github_repo_mock):
    res = client.post(
        "/api/problems/999/projects",
        json={"repo_url": "https://github.com/octocat/triage", "solution_summary": SUMMARY},
    )
    assert res.status_code == 404


def test_submit_project_github_down_503_github_unavailable(db_session, client, user, problem):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/down").mock(
            return_value=HTTPResponse(500, json={})
        )
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={"repo_url": "https://github.com/octocat/down", "solution_summary": SUMMARY},
        )
        assert res.status_code == 503
        assert res.json()["detail"]["code"] == "github_unavailable"


def test_submit_project_github_rate_limited_503(db_session, client, user, problem):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/limited").mock(
            return_value=HTTPResponse(403, json={"message": "API rate limit exceeded"})
        )
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={"repo_url": "https://github.com/octocat/limited", "solution_summary": SUMMARY},
        )
        assert res.status_code == 503
        assert res.json()["detail"]["code"] == "github_rate_limited"


def test_submit_project_fork_rejected_422(db_session, client, user, problem):
    payload = dict(REPO_PAYLOAD, fork=True)
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/forky").mock(
            return_value=HTTPResponse(200, json=payload)
        )
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={"repo_url": "https://github.com/octocat/forky", "solution_summary": SUMMARY},
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "fork_not_allowed"


def test_submit_project_archived_repo_rejected_422(db_session, client, user, problem):
    payload = dict(REPO_PAYLOAD, archived=True)
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/frozen").mock(
            return_value=HTTPResponse(200, json=payload)
        )
        res = client.post(
            f"/api/problems/{problem.id}/projects",
            json={"repo_url": "https://github.com/octocat/frozen", "solution_summary": SUMMARY},
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "repo_not_available"


# --- progress fetch + cache ---

def cached_progress(commits_ago_days: float):
    last = NOW - timedelta(days=commits_ago_days)
    return {
        "status": "active" if commits_ago_days <= 7 else "stale",
        "commit_count": 4,
        "last_commit_at": last.isoformat(),
        "has_readme": True,
        "recent_commits": [{"sha": "a", "message": "work", "date": last.isoformat()}],
        "open_issues": [],
    }


def test_progress_serves_fresh_cache_without_github(db_session, client, user, problem, anon):
    project = make_project(
        db_session, user, problem,
        progress_json=cached_progress(1),
        progress_updated_at=datetime.now(timezone.utc),
    )
    with respx.mock:
        res = client.get(f"/api/projects/{project.id}/progress")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "active"
    assert data["commit_count"] == 4


def test_progress_refreshes_when_cache_expired(db_session, client, user, problem, anon):
    project = make_project(
        db_session, user, problem,
        progress_json=cached_progress(1),
        progress_updated_at=NOW - timedelta(minutes=11),
    )
    with respx.mock(assert_all_called=False) as mock:
        mock_progress_fetch(mock, commits=[commit("s1", NOW)], issues=[])
        res = client.get(f"/api/projects/{project.id}/progress")
    assert res.status_code == 200
    data = res.json()
    assert data["commit_count"] == 1
    # contract 10.3: 0-1 commits => not_started, This takes precedence over recency
    assert data["status"] == "not_started"
    assert data["has_readme"] is True


def test_progress_refresh_param_forces_fetch(db_session, client, user, problem, anon):
    project = make_project(
        db_session, user, problem,
        progress_json=cached_progress(1),
        progress_updated_at=datetime.now(timezone.utc),
    )
    with respx.mock(assert_all_called=False) as mock:
        mock_progress_fetch(mock, commits=[commit("s1", NOW), commit("s2", NOW), commit("s3", NOW)], issues=[])
        res = client.get(f"/api/projects/{project.id}/progress", params={"refresh": "true"})
    assert res.status_code == 200
    assert res.json()["commit_count"] == 3


def test_progress_refresh_judges_ownership_by_submitter_not_viewer(
    db_session, client, user, problem
):
    project = make_project(
        db_session,
        user,
        problem,
        verification_status="verified",
        ownership_basis="owner",
        repo_github_id=999,
        progress_json=cached_progress(1),
        progress_updated_at=datetime.now(timezone.utc),
    )
    viewer = User(github_id=7, username="viewer", github_token=None)
    db_session.add(viewer)
    db_session.commit()
    # Someone else's project, viewed by a different logged-in account: the
    # refresh must not treat the viewer as the owner.
    app.dependency_overrides[get_optional_user] = lambda: viewer
    app.dependency_overrides[get_current_user] = lambda: viewer

    with respx.mock(assert_all_called=False) as mock:
        mock_progress_fetch(
            mock, commits=[commit("s1", NOW), commit("s2", NOW), commit("s3", NOW)], issues=[]
        )
        mock.get("https://api.github.com/repos/octocat/triage").mock(
            return_value=HTTPResponse(200, json=REPO_PAYLOAD)
        )
        res = client.get(f"/api/projects/{project.id}/progress", params={"refresh": "true"})

    assert res.status_code == 200
    db_session.refresh(project)
    assert project.verification_status == "verified"
    assert project.ownership_basis == "owner"


def test_progress_github_failure_returns_cached(db_session, client, user, problem, anon):
    project = make_project(
        db_session, user, problem,
        progress_json=cached_progress(1),
        progress_updated_at=NOW - timedelta(minutes=20),
    )
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/triage/commits").mock(
            return_value=HTTPResponse(403, json={"message": "rate limit"})
        )
        res = client.get(f"/api/projects/{project.id}/progress")
    assert res.status_code == 200
    data = res.json()
    assert data["commit_count"] == 4
    assert data["status"] == "active"


def test_progress_no_cache_github_failure_502(db_session, client, user, problem, anon):
    project = make_project(db_session, user, problem)
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/octocat/triage/commits").mock(
            return_value=HTTPResponse(403, json={"message": "rate limit"})
        )
        res = client.get(f"/api/projects/{project.id}/progress")
    assert res.status_code == 502


# --- status derivation (service level, no HTTP) ---

from app.services.github import get_progress, _status_for  # noqa: E402


def test_status_derivation():
    now = datetime.now(timezone.utc)
    assert _status_for(0, None) == "not_started"
    assert _status_for(1, now) == "not_started"
    assert _status_for(2, now) == "active"
    assert _status_for(5, now - timedelta(days=2)) == "active"
    assert _status_for(5, now - timedelta(days=8)) == "stale"


@pytest.mark.anyio
async def test_get_progress_builds_shape_and_filters_issues(db_session):
    commits = [
        commit("s1", NOW, "first commit"),
        commit("s2", NOW - timedelta(minutes=5), "second"),
        commit("s3", NOW - timedelta(days=9), "older"),
    ]
    issues = [
        {"number": 1, "title": "Fix bug", "html_url": "https://github.com/u/r/issues/1", "labels": []},
        {"number": 2, "title": "Improve startup", "html_url": "https://github.com/u/r/issues/2",
         "labels": [{"name": "good first issue"}]},
        {"number": 3, "title": "Docs", "html_url": "https://github.com/u/r/issues/3",
         "labels": [{"name": "help wanted"}]},
        {"number": 4, "title": "A pull request", "html_url": "https://github.com/u/r/pull/4",
         "labels": [], "pull_request": {"url": "x"}},
    ]
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://api.github.com/repos/u/r/commits").mock(return_value=HTTPResponse(200, json=commits))
        mock.get("https://api.github.com/repos/u/r/readme").mock(return_value=HTTPResponse(200, json={}))
        mock.get("https://api.github.com/repos/u/r/issues").mock(return_value=HTTPResponse(200, json=issues))
        progress = await get_progress("u", "r", token=None)
    assert progress is not None
    assert progress["status"] == "active"
    assert progress["commit_count"] == 3
    assert progress["has_readme"] is True
    assert len(progress["recent_commits"]) == 3
    assert progress["recent_commits"][0]["message"] == "first commit"
    issue_numbers = [i["number"] for i in progress["open_issues"]]
    assert issue_numbers == [2, 3, 1]  # good-first-issue/help-wanted first, PR excluded
    assert all(i["title"] != "A pull request" for i in progress["open_issues"])


def test_progress_recent_commits_max_five():
    commits = [commit(f"s{i}", NOW, f"m{i}") for i in range(9)]
    return_value = commits
    import asyncio

    async def run():
        with respx.mock(assert_all_called=False) as mock:
            mock.get("https://api.github.com/repos/u/r/commits").mock(
                return_value=HTTPResponse(200, json=return_value)
            )
            mock.get("https://api.github.com/repos/u/r/readme").mock(return_value=HTTPResponse(404, json={}))
            mock.get("https://api.github.com/repos/u/r/issues").mock(return_value=HTTPResponse(200, json=[]))
            return await get_progress("u", "r", None)

    progress = asyncio.get_event_loop_policy().new_event_loop().run_until_complete(run())
    assert progress["status"] == "active"
    assert progress["commit_count"] == 9
    assert len(progress["recent_commits"]) == 5
    assert progress["has_readme"] is False  # 404 README handled gracefully


# --- detail & me ---

def test_project_detail(db_session, client, user, problem, anon):
    project = make_project(
        db_session, user, problem,
        progress_json=cached_progress(1),
        verification_status="verified",
    )
    res = client.get(f"/api/projects/{project.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["repo_url"] == "https://github.com/octocat/triage"
    assert data["problem_title"] == "Flood alert app"
    assert data["owner"]["username"] == "octocat"
    assert data["progress"]["commit_count"] == 4
    assert "github_token" not in data
    assert "relevance_score" not in data


def test_project_detail_404(client, db_session):
    res = client.get("/api/projects/999")
    assert res.status_code == 404


def test_me_projects_lists_own_only(db_session, client, user, problem, github_repo_mock):
    from app.models import User as _User

    other = _User(github_id=7, username="other")
    db_session.add(other)
    db_session.commit()
    mine = make_project(db_session, user, problem)
    make_project(db_session, other, problem)
    res = client.get("/api/me/projects")
    assert res.status_code == 200
    ids = [p["id"] for p in res.json()]
    assert ids == [mine.id]


def test_me_projects_requires_auth(client, db_session, anon):
    res = client.get("/api/me/projects")
    assert res.status_code == 401
