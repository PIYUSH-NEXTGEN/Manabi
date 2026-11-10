import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import Problem, Project, ProjectStar, User


def login_as(user):
    """Override both user dependencies (detail GET uses the optional one)."""
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_optional_user] = lambda: user


def logout():
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)


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
    """A verified project owned by 'owner' that other users can star."""
    owner = User(github_id=11, username="owner", name="Owner", avatar_url=None)
    starer = User(github_id=22, username="starer", name="Starer", avatar_url=None)
    db_session.add_all([owner, starer])
    db_session.commit()
    problem = Problem(
        title="Flood model", summary="s", who_affected="w", why_matters="y", field="aiml",
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
    return {"owner": owner, "starer": starer, "project": project, "problem": problem}


@pytest.fixture
def starer(seeded):
    u = seeded["starer"]
    login_as(u)
    return u


def test_star_roundtrip_count_and_flag(client, seeded, starer, db_session):
    project_id = seeded["project"].id

    # The detail response carries the count and the viewer flag.
    detail = client.get(f"/api/projects/{project_id}").json()
    assert detail["star_count"] == 0
    assert detail["starred_by_me"] is False

    response = client.post(f"/api/projects/{project_id}/star")
    assert response.status_code == 201
    assert response.json() == {"ok": True, "star_count": 1}

    # The star endpoints commit in one request; the shared test session
    # identity-maps the project, so expire stale relationship state.
    db_session.expire_all()
    detail = client.get(f"/api/projects/{project_id}").json()
    assert detail["star_count"] == 1
    assert detail["starred_by_me"] is True

    # Un-starring removes the row; count drops and the flag clears.
    assert client.delete(f"/api/projects/{project_id}/star").status_code == 204
    db_session.expire_all()
    detail = client.get(f"/api/projects/{project_id}").json()
    assert detail["star_count"] == 0
    assert detail["starred_by_me"] is False


def test_star_is_one_per_user(client, seeded, starer, db_session):
    project_id = seeded["project"].id
    assert client.post(f"/api/projects/{project_id}/star").status_code == 201
    second = client.post(f"/api/projects/{project_id}/star")
    assert second.status_code == 409
    assert second.json()["detail"]["code"] == "already_starred"

    rows = db_session.query(ProjectStar).all()
    assert len(rows) == 1


def test_unstar_is_idempotent(client, seeded, starer):
    project_id = seeded["project"].id
    # Un-starring something that was never starred still succeeds quietly.
    assert client.delete(f"/api/projects/{project_id}/star").status_code == 204


def test_starring_requires_login(client, seeded):
    project_id = seeded["project"].id
    response = client.post(f"/api/projects/{project_id}/star")
    assert response.status_code == 401


def test_star_flag_is_per_viewer(client, seeded, starer, db_session):
    project_id = seeded["project"].id
    client.post(f"/api/projects/{project_id}/star")

    # A different anonymous viewer sees the count but no personal flag.
    logout()
    detail = client.get(f"/api/projects/{project_id}").json()
    assert detail["star_count"] == 1
    assert detail["starred_by_me"] is False

    # The project owner also sees the count without their own star.
    owner = seeded["owner"]
    login_as(owner)
    detail = client.get(f"/api/projects/{project_id}").json()
    assert detail["star_count"] == 1
    assert detail["starred_by_me"] is False


def test_stars_survive_project_read_via_problem_detail(client, seeded, starer, db_session):
    client.post(f"/api/projects/{seeded['project'].id}/star")
    db_session.expire_all()
    detail = client.get(f"/api/problems/{seeded['problem'].id}").json()
    rows = [p for p in detail["projects"] if p["id"] == seeded["project"].id]
    assert rows and rows[0]["star_count"] == 1
    assert rows[0]["starred_by_me"] is True
