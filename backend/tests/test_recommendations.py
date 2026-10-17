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
from app.services import recommender


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
    session.add_all(
        [
            Problem(
                title="Pandas flood model",
                summary="Predict flood risk with rainfall data.",
                who_affected="Villages", why_matters="Deaths",
                field="ml", domain="disaster-management", difficulty="intermediate",
                est_hours=40, tech_tags=["python", "pandas"], datasets=[], approaches=[],
                source_name="S", source_id="S1", original_text="verbatim",
            ),
            Problem(
                title="Rust vuln scanner",
                summary="Static analysis for vulnerable crates.",
                who_affected="Maintainers", why_matters="Supply chain",
                field="cybersecurity", domain="developer-tools", difficulty="advanced",
                est_hours=80, tech_tags=["rust"], datasets=[], approaches=[],
                source_name="S", source_id="S2", original_text="verbatim",
            ),
            Problem(
                title="Simple quiz app",
                summary="Attendance and quiz web app for schools.",
                who_affected="Teachers", why_matters="Time",
                field="web-fullstack", domain="education", difficulty="beginner",
                est_hours=16, tech_tags=["javascript"], datasets=[], approaches=[],
                source_name="S", source_id="S3", original_text="verbatim",
            ),
        ]
    )
    session.commit()
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def user(db_session):
    u = User(
        github_id=1, username="octocat", name="O", avatar_url=None, github_token=None,
        signals_json={"languages": {"Python": 12}, "topics": ["ml", "pandas"]},
        signals_updated_at=None,
    )
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    return u


@pytest.fixture
def anon(db_session):
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def ids(items):
    return [i["problem"]["id"] for i in items]


# ---------------- scoring ----------------

def test_tag_matches_dominate(db_session, user):
    recs = recommender.recommendations_for_user(db_session, user)
    top = recs[0]
    assert top[0].source_id == "S1"  # python+pandas, ml topic, intermediate
    assert any("pandas" in r for r in top[2])
    assert any("You write Python" in r for r in top[2])


def test_field_topic_match_reason(db_session, user):
    recs = recommender.recommendations_for_user(db_session, user)
    flood = next(r for r in recs if r[0].source_id == "S1")
    assert any("You explore ml" in r for r in flood[2])
    # field match + 2 tags + intermediate bonus = 3*2 + 2 + 1 = 9
    assert flood[1] == 9


def test_no_matching_problem_excluded(db_session, user):
    recs = recommender.recommendations_for_user(db_session, user)
    rust = next((r for r in recs if r[0].source_id == "S2"), None)
    assert rust is None  # rust, no difficulty bonus for advanced... but S3 gets beginner bonus; S2 has zero reason match


def test_beginner_bonus_with_topic_field_match(db_session, user):
    user.signals_json = {"languages": {}, "topics": ["education"]}
    db_session.commit()
    recs = recommender.recommendations_for_user(db_session, user)
    quiz = [(p, s, r) for p, s, r in recs if p.source_id == "S3"]
    assert quiz, "field match + beginner bonus should appear"
    assert quiz[0][1] == recommender.FIELD_DOMAIN_BONUS + recommender.DIFFICULTY_BONUS
    assert any("You explore education" in r for r in quiz[0][2])


def test_problem_with_no_overlap_is_excluded(db_session, user):
    recs = recommender.recommendations_for_user(db_session, user)
    assert all(p.source_id != "S3" for p, _s, _r in recs)


def test_no_signals_fallback(db_session):
    u = User(github_id=2, username="noob", signals_json=None, signals_updated_at=None)
    db_session.add(u)
    db_session.commit()
    recs = recommender.recommendations_for_user(db_session, u)
    assert len(recs) == 3
    assert all(r[1] == 0 and r[2] == ["Newest on MANABI"] for r in recs)
    assert [r[0].id for r in recs] == [3, 2, 1]  # newest first


def test_limit_eight(db_session):
    for i in range(12):
        db_session.add(
            Problem(
                title=f"P{i}", summary="s", who_affected="w", why_matters="y",
                field="ml", domain="other", difficulty="beginner", est_hours=10,
                tech_tags=["python"], datasets=[], approaches=[],
                source_name="S", source_id=f"SX{i}", original_text="verbatim",
            )
        )
    db_session.commit()
    u = User(github_id=3, username="many", signals_json={"languages": {"python": 1}}, signals_updated_at=None)
    db_session.add(u)
    db_session.commit()
    assert len(recommender.recommendations_for_user(db_session, u)) == 8


# ---------------- endpoint ----------------

def test_recommendations_requires_auth(client, db_session, anon):
    assert client.get("/api/recommendations").status_code == 401


def test_recommendations_shape(client, db_session, user, monkeypatch):
    async def fresh(token):
        return {"languages": {"Python": 12}, "topics": ["ml", "pandas"]}

    monkeypatch.setattr("app.routers.recommendations.github.get_user_signals", fresh)
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    data = res.json()
    assert set(data) == {"items"}
    first = data["items"][0]
    assert set(first) == {"problem", "score", "reasons"}
    assert first["problem"]["tech_tags"] == ["python", "pandas"]
    assert isinstance(first["score"], int) and isinstance(first["reasons"], list)


def test_recommendations_refreshes_signals(client, db_session, user, monkeypatch):
    async def fresh(token):
        return {"languages": {"Rust": 5}, "topics": ["cybersecurity"]}

    monkeypatch.setattr("app.routers.recommendations.github.get_user_signals", fresh)
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    top = res.json()["items"][0]
    assert "rust" in top["problem"]["tech_tags"]
    db_session.refresh(user)
    assert user.signals_json["languages"] == {"Rust": 5}
    assert user.signals_updated_at is not None


def test_recommendations_keeps_cached_when_fresh(client, db_session, user, monkeypatch):
    from app.models import utcnow

    called = []

    async def boom(token):
        called.append(True)
        raise AssertionError("must not refresh within TTL")

    user.signals_json = {"languages": {"python": 1}, "topics": []}
    user.signals_updated_at = utcnow()
    db_session.commit()
    monkeypatch.setattr("app.routers.recommendations.github.get_user_signals", boom)
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    assert not called


def test_recommendations_survives_github_failure(client, db_session, user, monkeypatch):
    async def fail(token):
        return None

    user.signals_json = None  # nothing cached, refresh fails -> newest fallback, no crash
    db_session.commit()
    monkeypatch.setattr("app.routers.recommendations.github.get_user_signals", fail)
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    data = res.json()
    assert data["items"][0]["reasons"] == ["Newest on MANABI"]


def test_failed_refresh_keeps_stale_signals(client, db_session, user, monkeypatch):
    async def fail(token):
        return None

    monkeypatch.setattr("app.routers.recommendations.github.get_user_signals", fail)
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    top = res.json()["items"][0]
    assert "pandas" in top["problem"]["tech_tags"]  # old signals still usable
