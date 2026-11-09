import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user
from app.main import app
from app.models import Problem, Project, ProjectReport, User


@pytest.fixture(autouse=True)
def env(monkeypatch):
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
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def seeded(db_session):
    """A verified project owned by 'owner', so other users can report it."""
    owner = User(github_id=11, username="owner", name="Owner", avatar_url=None)
    reporter = User(github_id=22, username="reporter", name="Reporter", avatar_url=None)
    db_session.add_all([owner, reporter])
    db_session.commit()
    problem = Problem(
        title="Flood model", summary="s", who_affected="w", why_matters="y", field="ml",
        domain="other", difficulty="beginner", est_hours=10, tech_tags=[], datasets=[],
        approaches=[], source_name="S", source_id="S1", original_text="verbatim",
    )
    db_session.add(problem)
    db_session.commit()
    project = Project(
        problem_id=problem.id, user_id=owner.id, repo_owner="owner", repo_name="flood",
        repo_url="https://github.com/owner/flood", open_for_contributors=True,
        verification_status="verified",
    )
    db_session.add(project)
    db_session.commit()
    return {"owner": owner, "reporter": reporter, "project": project, "problem": problem}


@pytest.fixture
def reporter(seeded):
    u = seeded["reporter"]
    app.dependency_overrides[get_current_user] = lambda: u
    return u


def test_report_roundtrip_persists_and_counts(client, seeded, reporter, db_session):
    res = client.post(
        f"/api/projects/{seeded['project'].id}/report",
        json={"reason": "This repo does not solve the stated problem."},
    )
    assert res.status_code == 201, res.json()
    assert res.json() == {"ok": True, "report_count": 1}

    saved = db_session.query(ProjectReport).one()
    assert saved.project_id == seeded["project"].id
    assert saved.reporter_user_id == reporter.id


def test_report_reason_is_trimmed(client, seeded, reporter, db_session):
    # Pydantic caps the raw payload at 300 chars; surrounding whitespace must
    # still be trimmed by the endpoint before storing.
    res = client.post(
        f"/api/projects/{seeded['project'].id}/report",
        json={"reason": "   " + "x" * 290 + "   "},
    )
    assert res.status_code == 201, res.json()
    assert len(db_session.query(ProjectReport).one().reason) == 290


def test_report_requires_reason(client, seeded, reporter):
    res = client.post(f"/api/projects/{seeded['project'].id}/report", json={"reason": ""})
    assert res.status_code == 422


def test_report_own_project_rejected(client, seeded, db_session):
    from app.deps import get_current_user

    app.dependency_overrides[get_current_user] = lambda: seeded["owner"]
    res = client.post(
        f"/api/projects/{seeded['project'].id}/report",
        json={"reason": "Reporting my own project for science."},
    )
    assert res.status_code == 422
    assert res.json()["detail"]["code"] == "cannot_report_own_project"


def test_report_unknown_project_404(client, reporter):
    res = client.post("/api/projects/9999/report", json={"reason": "Not a real project id."})
    assert res.status_code == 404


def test_report_missing_reason_fails_validation(client, seeded, reporter):
    res = client.post(f"/api/projects/{seeded['project'].id}/report", json={})
    assert res.status_code == 422


def test_report_duplicate_returns_409(client, seeded, reporter):
    res = client.post(
        f"/api/projects/{seeded['project'].id}/report", json={"reason": "First valid report."}
    )
    assert res.status_code == 201, res.json()
    res = client.post(
        f"/api/projects/{seeded['project'].id}/report", json={"reason": "Second report."}
    )
    assert res.status_code == 409
    assert res.json()["detail"]["code"] == "already_reported"


def test_report_rate_limited_after_quota(client, seeded, reporter):
    from app.routers.projects import REPORT_LIMITER

    # The limiter (per-user) is checked before the duplicate-report guard, so a
    # capped quota on one user surfaces 429 for the same-user repeat.
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("REPORT_RATE_LIMIT_PER_HOUR", "1")
    config.get_settings.cache_clear()
    REPORT_LIMITER._hits.clear()
    try:
        first = client.post(f"/api/projects/{seeded['project'].id}/report", json={"reason": "one"})
        assert first.status_code == 201, first.json()
        second = client.post(f"/api/projects/{seeded['project'].id}/report", json={"reason": "two"})
        assert second.status_code == 429
        assert second.json()["detail"]["code"] == "rate_limited"
    finally:
        monkeypatch.undo()
        config.get_settings.cache_clear()
        REPORT_LIMITER._hits.clear()


def test_report_threshold_flips_problem_to_needs_review(client, seeded, db_session):
    from app.deps import get_current_user

    reporters = [
        User(github_id=31 + i, username=f"watcher{i}", name=f"W{i}", avatar_url=None)
        for i in range(3)
    ]
    db_session.add_all(reporters)
    db_session.commit()

    statuses = []
    for watcher in reporters:
        app.dependency_overrides[get_current_user] = lambda w=watcher: w
        res = client.post(
            f"/api/projects/{seeded['project'].id}/report", json={"reason": f"issue by {watcher.username}"}
        )
        statuses.append(res.status_code)
    app.dependency_overrides.pop(get_current_user, None)
    assert statuses == [201, 201, 201]

    project = db_session.query(Project).filter_by(id=seeded["project"].id).one()
    assert project.verification_status == "needs_review"
    assert db_session.query(ProjectReport).count() == 3
