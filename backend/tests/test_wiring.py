import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.main import app
from app.models import MLAttempt, MLQuestion, Problem, Project, User


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
    question = MLQuestion(
        title="Q", scenario="s", difficulty="beginner", topic="class-imbalance",
        rubric_json=[], explanation="e",
    )
    db_session.add(question)
    db_session.commit()
    db_session.add_all(
        [MLAttempt(question_id=question.id, user_id=jane.id, answer="a", feedback_json={})
         for _ in range(2)]  # two attempts -> still one distinct question
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
    assert data["solved_ml_count"] == 1  # distinct questions, not attempt count


def test_profile_empty_counts(client, db_session):
    db_session.add(User(github_id=12, username="empty", name="E"))
    db_session.commit()
    data = client.get("/api/u/empty").json()
    assert data["projects"] == [] and data["solved_ml_count"] == 0


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

def test_spa_blocks_path_escape(client, fake_dist):
    from fastapi import HTTPException

    from app.main import _spa_response

    for evil in ["../secret.txt", "assets/../../etc/passwd", "..\\secret.txt", "//evil.com/share/x"]:
        with pytest.raises(HTTPException) as exc:
            _spa_response(fake_dist, evil, "text/html")
        assert exc.value.status_code == 404, evil
    assert _spa_response(fake_dist, "index.html", "text/html").status_code in (200, None)  # own file ok (starlette returns response)


def test_problem_create_rejects_oversize_fields(client, db_session, user):
    from tests.test_ingest import draft_card_factory

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
    from tests.test_ingest import draft_card_factory

    res = client.post(
        "/api/problems",
        json=draft_card_factory(title="x" * 300, summary="y" * 8000, est_hours=1)
    )
    assert res.status_code == 201, res.json()


def test_ingest_clamps_est_hours(client, db_session, user, monkeypatch):
    from app.services.ratelimit import INGEST_LIMITER
    from tests.test_ingest import canned_llm

    INGEST_LIMITER._hits.clear()
    canned_llm(
        monkeypatch,
        '{"is_problem": true, "title": "T", "summary": "S", "who_affected": "W", "why_matters": "Y",'
        '"field": "other", "domain": "other", "difficulty": "beginner", "est_hours": 999999, "tech_tags": [],'
        '"datasets": [], "approaches": [], "source_note": null, "evidence": {}, "inferred_fields": []}',
    )
    res = client.post("/api/ingest", json={"text": "A clean problem description goes here."})
    assert res.status_code == 200
    assert res.json()["draft"]["est_hours"] == 1000
