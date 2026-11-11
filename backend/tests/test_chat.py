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
from app.services.ratelimit import CHAT_DAILY_LIMITER


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
                field="aiml",
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
                field="web-dev",
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
    CHAT_DAILY_LIMITER.reset(db_session)
    return u


@pytest.fixture
def anon(db_session):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    CHAT_DAILY_LIMITER.reset(db_session)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def msg(role="user", content="Which problem should I build first?"):
    return {"role": role, "content": content}


def patch_reply(monkeypatch, reply):
    monkeypatch.setattr("app.routers.chat.llm_chat", lambda system, messages, **kwargs: reply, raising=False)


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


def test_catalog_search_understands_synonyms_and_plurals(db_session):
    from app.services.catalog_search import search_catalog

    # the flood brief never says "alerts monitoring system" verbatim, and the
    # classroom app never says "webapps", but both should still be found
    assert any(p.source_id == "SIH26001" for p, _ in search_catalog(db_session, "alert monitoring system"))
    assert any(p.source_id == "TCOE PS12" for p, _ in search_catalog(db_session, "webapps for attendance"))


def test_catalog_search_title_hit_outranks_summary_hit(db_session):
    from app.services.catalog_search import search_catalog

    # "attendance" appears in the classroom title AND summary; title hits score
    # higher so ordering stays stable when more rows join the board
    matches = search_catalog(db_session, "attendance app")
    assert matches and matches[0][0].source_id == "TCOE PS12"


def test_build_system_marks_empty_catalog_for_clarify(db_session):
    from app.routers.chat import build_system
    from app.schemas import ChatMessage

    system = build_system(db_session, [ChatMessage(role="user", content="quantum blockchain")], None)
    assert "no rows matched" in system
    assert "Ask ONE short question" in system


def test_build_system_injects_user_state_and_rejection_help(db_session, user):
    from app.models import Project
    from app.routers.chat import build_system
    from app.schemas import ChatMessage

    problem = db_session.query(Problem).first()
    db_session.add(
        Project(
            problem_id=problem.id,
            user_id=user.id,
            repo_owner="octocat",
            repo_name="triage",
            repo_url="https://github.com/octocat/triage",
            verification_status="rejected",
            relevance_reason="No README found",
        )
    )
    db_session.commit()

    system = build_system(db_session, [ChatMessage(role="user", content="hi")], None, user=user)

    assert "rejected=1" in system
    assert "No README found" in system
    assert "offer concrete next steps" in system


def test_build_system_skips_user_block_for_projectless_user(db_session, user):
    from app.routers.chat import build_system
    from app.schemas import ChatMessage

    system = build_system(db_session, [ChatMessage(role="user", content="hi")], None, user=user)
    assert "USER CONTEXT" not in system


# ---------------- system prompt ----------------

def test_build_system_cites_live_stats(db_session):
    from app.routers.chat import build_system
    from app.schemas import ChatMessage

    system = build_system(db_session, [ChatMessage(role="user", content="hello")], None)
    assert "2 published problems" in system
    assert "aiml=1" in system and "web-dev=1" in system
    assert "beginner=1" in system and "intermediate=1" in system


def test_build_system_empty_board_stats(db_session):
    from app.routers.chat import build_system
    from app.schemas import ChatMessage
    from sqlalchemy import delete

    db_session.execute(delete(Problem))
    db_session.commit()
    system = build_system(db_session, [ChatMessage(role="user", content="hello")], None)
    assert "problem board is empty right now" in system


# ---------------- endpoint ----------------

def test_chat_public_and_shape(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "MOCK-CHAT-REPLY: saw: hello")
    res = client.post("/api/chat", json={"messages": [msg(content="hello")], "page_context": None})
    assert res.status_code == 200
    data = res.json()
    assert set(data) == {"reply", "problems"}
    assert isinstance(data["problems"], list)


def test_chat_reference_kept_when_real(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "Start with [P1] this weekend.")
    data = client.post("/api/chat", json={"messages": [msg()]}).json()
    assert data["problems"] == [
        {"id": 1, "title": "Flood alert dashboard", "field": "aiml", "difficulty": "intermediate"}
    ]
    assert data["reply"].count("[P1]") == 1


def test_chat_invalid_reference_stripped(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "Try [P1] and [P4242].")
    data = client.post("/api/chat", json={"messages": [msg()]}).json()
    assert [p["id"] for p in data["problems"]] == [1]
    assert "[P4242]" not in data["reply"] and "[P1]" in data["reply"]


def test_chat_strips_inline_latex_but_keeps_money(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "Score with $F_2$ or $F_\\beta$; budget stays $5 and $10.")
    data = client.post("/api/chat", json={"messages": [msg()]}).json()
    reply = data["reply"]
    assert "F2" in reply and "Fβ" in reply
    assert "$F_2$" not in reply and "$F_\\beta$" not in reply
    assert "$5 and $10" in reply


def test_chat_catalog_in_system_prompt(client, db_session, user, monkeypatch):
    captured = {}

    def fake(system, messages, **kwargs):
        captured["system"] = system
        return "re"

    monkeypatch.setattr("app.routers.chat.llm_chat", fake, raising=False)
    client.post("/api/chat", json={"messages": [msg(content="flood rainfall villages")]})
    assert "[P1] Flood alert dashboard" in captured["system"]
    assert "CATALOG" in captured["system"]


def test_chat_system_prompt_requests_readable_markdown(client, db_session, user, monkeypatch):
    captured = {}

    def fake(system, messages, **kwargs):
        captured["system"] = system
        return "re"

    monkeypatch.setattr("app.routers.chat.llm_chat", fake, raising=False)
    client.post("/api/chat", json={"messages": [msg()]})
    assert "own line" in captured["system"]
    assert "No LaTeX" in captured["system"]


def test_chat_page_context_included(client, db_session, user, monkeypatch):
    captured = {}

    def fake(system, messages, **kwargs):
        captured["system"] = system
        return "re"

    monkeypatch.setattr("app.routers.chat.llm_chat", fake, raising=False)
    client.post(
        "/api/chat", json={"messages": [msg()], "page_context": {"problem_id": 2}}
    )
    assert "CURRENT PAGE CONTEXT" in captured["system"] and "[P2]" in captured["system"]


def test_chat_page_context_unknown_problem_ignored(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "re")
    res = client.post("/api/chat", json={"messages": [msg()], "page_context": {"problem_id": 9999}})
    assert res.status_code == 200


def test_chat_requires_login(client, db_session, anon):
    """Chat is login-only: anonymous callers get 401, never an LLM call."""
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 401


def test_chat_daily_limit_20(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "re")
    codes = []
    for _ in range(int(config.get_settings().CHAT_RATE_LIMIT_PER_DAY) + 1):
        res = client.post("/api/chat", json={"messages": [msg()]})
        codes.append(res.status_code)
    assert codes[-1] == 429 and 200 in codes
    assert "today" in client.post(
        "/api/chat", json={"messages": [msg()]}
    ).json()["detail"]


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


def test_chat_not_configured_503(client, db_session, user, monkeypatch):
    from app.services.llm import LLMConfigError as _LCE

    def boom(system, messages, **kwargs):
        raise _LCE("AI is not configured yet")

    monkeypatch.setattr("app.routers.chat.llm_chat", boom, raising=False)
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 503
    assert res.json()["detail"] == "AI is not configured yet"


def test_chat_provider_error_502(client, db_session, user, monkeypatch):
    from app.services.llm import LLMResponseError as _LRE

    def boom(system, messages, **kwargs):
        raise _LRE("x")

    monkeypatch.setattr("app.routers.chat.llm_chat", boom, raising=False)
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 502


def test_chat_unexpected_exception_maps_to_502(client, db_session, user, monkeypatch):
    """Any non-LLM crash must still answer JSON with 502. Never a bare 500."""
    def boom(system, messages, **kwargs):
        raise RuntimeError("unexpected provider crash")

    monkeypatch.setattr("app.routers.chat.llm_chat", boom, raising=False)
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 502
    assert res.json()["detail"]


def test_chat_empty_reply_gets_fallback_message(client, db_session, user, monkeypatch):
    patch_reply(monkeypatch, "")
    res = client.post("/api/chat", json={"messages": [msg()]})
    assert res.status_code == 200
    assert res.json()["reply"].strip()
