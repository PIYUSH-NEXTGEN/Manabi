import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import Problem, User
from app.services.ratelimit import CHAT_ANON_LIMITER, CHAT_USER_LIMITER


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
                title="Flood alert dashboard",
                summary="Predict flood risk along rivers and alert villages 48 hours ahead using rainfall data.",
                who_affected="Villages",
                why_matters="Deaths",
                field="ml",
                domain="disaster-management",
                difficulty="intermediate",
                est_hours=40,
                tech_tags=["python", "pandas"],
                datasets=[],
                approaches=[],
                source_name="Smart India Hackathon 2026",
                source_id="SIH26001",
                original_text="verbatim",
            ),
            Problem(
                title="Classroom starter app",
                summary="Simple attendance web app for schools with offline sync.",
                who_affected="Teachers",
                why_matters="Time",
                field="web-fullstack",
                domain="education",
                difficulty="beginner",
                est_hours=20,
                tech_tags=["react"],
                datasets=[],
                approaches=[],
                source_name="TCOE",
                source_id="TCOE PS12",
                original_text="verbatim",
            ),
        ]
    )
    session.commit()
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def user(db_session):
    u = User(github_id=1, username="octocat", name="O", avatar_url=None)
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    CHAT_USER_LIMITER._hits.clear()
    CHAT_ANON_LIMITER._hits.clear()
    return u


@pytest.fixture
def anon(db_session):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    CHAT_USER_LIMITER._hits.clear()
    CHAT_ANON_LIMITER._hits.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def msg(role="user", content="Which problem should I build first?"):
    return {"role": role, "content": content}


def patch_reply(monkeypatch, reply):
    monkeypatch.setattr("app.routers.chat.llm_chat", lambda system, messages: reply, raising=False)


# ---------------- catalog search ----------------

def test_catalog_search_matches_keywords(db_session):
    from app.services.catalog_search import search_catalog

    matches = search_catalog(db_session, "flood rainfall villages")
    assert matches and matches[0][0].source_id == "SIH26001" and matches[0][1] > 0
    assert all("Classroom" not in p.title for p, _ in matches)


def test_catalog_search_matches_source_id(db_session):
    from app.services.catalog_search import search_catalog

    matches = search_catalog(db_session, "TCOE PS12")
    assert matches and matches[0][0].source_id == "TCOE PS12"


def test_catalog_search_no_match_empty(db_session):
    from app.services.catalog_search import search_catalog

    assert search_catalog(db_session, "blockchain voting quantum") == []


# ---------------- endpoint ----------------

def test_chat_public_and_shape(client, db_session, anon, monkeypatch):
    patch_reply(monkeypatch, "MOCK-CHAT-REPLY: saw: hello")
    res = client.post("/api/chat", json={"messages": [msg(content="hello")], "page_context": None})
    assert res.status_code == 200
    data = res.json()
    assert set(data) == {"reply", "problems"}
    assert isinstance(data["problems"], list)


def test_chat_reference_kept_when_real(client, db_session, anon, monkeypatch):
    patch_reply(monkeypatch, "Start with [P1] this weekend.")
    data = client.post("/api/chat", json={"messages": [msg()]}).json()
    assert data["problems"] == [
        {"id": 1, "title": "Flood alert dashboard", "field": "ml", "difficulty": "intermediate"}
    ]
    assert data["reply"].count("[P1]") == 1


def test_chat_invalid_reference_stripped(client, db_session, anon, monkeypatch):
    patch_reply(monkeypatch, "Try [P1] and [P4242].")
    data = client.post("/api/chat", json={"messages": [msg()]}).json()
    assert [p["id"] for p in data["problems"]] == [1]
    assert "[P4242]" not in data["reply"] and "[P1]" in data["reply"]


def test_chat_catalog_in_system_prompt(client, db_session, anon, monkeypatch):
    captured = {}

    def fake(system, messages):
        captured["system"] = system
        return "re"

    monkeypatch.setattr("app.routers.chat.llm_chat", fake, raising=False)
    client.post("/api/chat", json={"messages": [msg(content="flood rainfall villages")]})
    assert "[P1] Flood alert dashboard" in captured["system"]
    assert "CATALOG" in captured["system"]


def test_chat_page_context_included(client, db_session, anon, monkeypatch):
    captured = {}

    def fake(system, messages):
        captured["system"] = system
        return "re"

    monkeypatch.setattr("app.routers.chat.llm_chat", fake, raising=False)
    client.post(
        "/api/chat", json={"messages": [msg()], "page_context": {"problem_id": 2}}
    )
    assert "CURRENT PAGE CONTEXT" in captured["system"] and "[P2]" in captured["system"]


def test_chat_page_context_unknown_problem_ignored(client, db_session, anon, monkeypatch):
    patch_reply(monkeypatch, "re")
    res = client.post("/api/chat", json={"messages": [msg()], "page_context": {"problem_id": 9999}})
    assert res.status_code == 200


def test_chat_rate_limited_anon(client, db_session, anon, monkeypatch):
    patch_reply(monkeypatch, "re")
    codes = []
    for _ in range(int(config.get_settings().CHAT_RATE_LIMIT_ANON_PER_HOUR) + 1):
        res = client.post("/api/chat", json={"messages": [msg()]})
        codes.append(res.status_code)
    assert codes[-1] == 429 and 200 in codes


def test_chat_rate_limited_user(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "re")
    codes = []
    for _ in range(int(config.get_settings().CHAT_RATE_LIMIT_USER_PER_HOUR) + 1):
        res = client.post("/api/chat", json={"messages": [msg()]})
        codes.append(res.status_code)
    assert codes[-1] == 429 and 200 in codes


def test_chat_too_many_messages_422(client, db_session, user):
    res = client.post("/api/chat", json={"messages": [msg() for _ in range(13)]})
    assert res.status_code == 422


def test_chat_message_too_long_422(client, db_session, user):
    res = client.post("/api/chat", json={"messages": [msg(content="x" * 1001)]})
    assert res.status_code == 422


def test_chat_bad_role_422(client, db_session, user):
    res = client.post("/api/chat", json={"messages": [{"role": "system", "content": "hi"}]})
    assert res.status_code == 422


def test_chat_empty_messages_422(client, db_session, user):
    res = client.post("/api/chat", json={"messages": []})
    assert res.status_code == 422


def test_chat_not_configured_503(client, db_session, anon, monkeypatch):
    from app.services.llm import LLMConfigError as _LCE

    def boom(system, messages):
        raise _LCE("AI is not configured yet")

    monkeypatch.setattr("app.routers.chat.llm_chat", boom, raising=False)
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 503
    assert res.json()["detail"] == "AI is not configured yet"


def test_chat_provider_error_502(client, db_session, anon, monkeypatch):
    from app.services.llm import LLMResponseError as _LRE

    def boom(system, messages):
        raise _LRE("x")

    monkeypatch.setattr("app.routers.chat.llm_chat", boom, raising=False)
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 502
