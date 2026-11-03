import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.main import app
from app.models import Problem, Project, User


@pytest.fixture(autouse=True)
def env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


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
def user(db_session):
    from app.deps import get_current_user

    u = User(github_id=77, username="fixer", name="F", avatar_url=None)
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    return u


# ---------------- stretch: GET /api/u/{username} ----------------

@pytest.fixture
def seeded(db_session):
    jane = User(github_id=11, username="jane", name="Jane", avatar_url="http://a/img.png", github_token="secret-token")
    db_session.add(jane)
    db_session.commit()
    problem = Problem(
        title="Flood model", summary="s", who_affected="w", why_matters="y", field="ml",
        domain="other", difficulty="beginner", est_hours=10, tech_tags=[], datasets=[],
        approaches=[], source_name="S", source_id="S1", original_text="verbatim",
    )
    db_session.add(problem)
    db_session.commit()
    db_session.add(
        Project(
            problem_id=problem.id, user_id=jane.id, repo_owner="jane", repo_name="flood",
            repo_url="https://github.com/jane/flood", open_for_contributors=True,
        )
    )
    db_session.commit()
    return jane


def test_profile_404(client, db_session):
    assert client.get("/api/u/nobody").status_code == 404


def test_profile_shape(client, db_session, seeded):
    res = client.get("/api/u/jane")
    assert res.status_code == 200
    data = res.json()
    assert data["user"] == {"id": seeded.id, "username": "jane", "name": "Jane", "avatar_url": "http://a/img.png"}
    assert "secret-token" not in str(data)  # github_token never leaks
    assert "github_token" not in data["user"]
    assert len(data["projects"]) == 1
    assert data["projects"][0]["repo_url"] == "https://github.com/jane/flood"


def test_profile_empty_counts(client, db_session):
    db_session.add(User(github_id=12, username="empty", name="E"))
    db_session.commit()
    data = client.get("/api/u/empty").json()
    assert data["projects"] == []


# ---------------- static / SPA (B11) ----------------

@pytest.fixture
def fake_dist(tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>MANABI-SPA</html>")
    (dist / "favicon.svg").write_text("<svg/>")
    (dist / "assets" / "app.js").write_text("console.log(1)")
    monkeypatch.setattr("app.main.frontend_dist", lambda: dist)
    return dist


def test_spa_serves_index_for_unknown_paths(client, fake_dist):
    res = client.get("/problems/17", headers={"accept": "text/html"})
    assert res.status_code == 200
    assert "MANABI-SPA" in res.text
    res = client.get("/", headers={"accept": "text/html"})
    assert res.status_code == 200 and "MANABI-SPA" in res.text


def test_spa_serves_existing_files(client, fake_dist):
    res = client.get("/favicon.svg")
    assert res.status_code == 200 and "<svg/>" in res.text
    res = client.get("/assets/app.js")
    assert res.status_code == 200 and "console.log" in res.text


def test_api_404_stays_json_not_spa(client, fake_dist):
    res = client.get("/api/nonexistent-route")
    assert res.status_code == 404
    assert res.json()["detail"] == "Not found"


# ---------------- security/perf fixes ----------------

def draft_card_factory(**overrides):
    card = {
        "title": "Valid title",
        "summary": "A summary that is long enough.",
        "who_affected": "Someone affected",
        "why_matters": "It matters somehow",
        "field": "other",
        "domain": "other",
        "difficulty": "beginner",
        "est_hours": 10,
        "tech_tags": [],
        "datasets": [],
        "approaches": [],
        "source_name": "Test source",
        "source_id": None,
        "source_url": None,
        "source_note": None,
    }
    card.update(overrides)
    return card


def test_problem_create_rejects_oversize_fields(client, db_session, user):
    res = client.post("/api/problems", json=draft_card_factory(title="x" * 301))
    assert res.status_code == 422
    res = client.post("/api/problems", json=draft_card_factory(summary="x" * 8001))
    assert res.status_code == 422
    res = client.post("/api/problems", json=draft_card_factory(est_hours=0))
    assert res.status_code == 422
    res = client.post("/api/problems", json=draft_card_factory(est_hours=1001))
    assert res.status_code == 422
    res = client.post("/api/problems", json=draft_card_factory(tech_tags=["x" * 41]))
    assert res.status_code == 422


def test_problem_create_accepts_boundary_sizes(client, db_session, user):
    res = client.post(
        "/api/problems",
        json=draft_card_factory(title="x" * 300, summary="y" * 8000, est_hours=1)
    )
    assert res.status_code == 201, res.json()

@pytest.fixture
def _escape_probe_dist(tmp_path, monkeypatch):
    """A clean, isolated dist tree for the path-escape probes.

    Use a dedicated sub-folder of tmp_path rather than relying on the
    generic 'dist' fixture so this test cannot be affected by another
    test's tmp_path teardown or by a shared mutable distribution tree.
    """
    dist = tmp_path / "spa_escape_probe" / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>MANABI-SPA</html>")
    (dist / "favicon.svg").write_text("<svg/>")
    (dist / "assets" / "app.js").write_text("console.log(1)")
    monkeypatch.setattr("app.main.frontend_dist", lambda: dist)
    return dist


def test_spa_blocks_path_escape(_escape_probe_dist):
    import os

    from fastapi import HTTPException

    from app.main import _spa_response

    # Genuine traversal escapes on every platform -> must 404.
    for evil in ["../secret.txt", "assets/../../etc/passwd", "//evil.com/share/x"]:
        with pytest.raises(HTTPException) as exc:
            _spa_response(_escape_probe_dist, evil, "text/html")
        assert exc.value.status_code == 404, evil

    # Backslash traversal: on Windows "\" is a path separator, so this escapes
    # dist and must 404. On POSIX a backslash is an ordinary filename byte, so
    # the candidate resolves to a literal "..\\secret.txt" file *inside* dist
    # (not an escape) and the SPA correctly falls back to index.html instead
    # of a 404.
    evil_bs = "..\\secret.txt"
    if os.name == "nt":
        with pytest.raises(HTTPException) as exc:
            _spa_response(_escape_probe_dist, evil_bs, "text/html")
        assert exc.value.status_code == 404, evil_bs
    else:
        resp = _spa_response(_escape_probe_dist, evil_bs, "text/html")
        assert resp.status_code in (200, None)  # literal filename inside dist -> index fallback

    assert _spa_response(_escape_probe_dist, "index.html", "text/html").status_code in (200, None)  # own file ok (starlette returns response)

