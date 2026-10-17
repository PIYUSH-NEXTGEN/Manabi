from unittest import mock

import httpx
import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response as HTTPResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user
from app.main import app
from app.models import Problem, User
from app.services import extractor
from app.services.ratelimit import INGEST_LIMITER

PUBLIC_HTML = "<html><body><h1>District flood alert</h1><p>Build a flood risk model for riverside villages.</p></body></html>"


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
def user(db_session):
    u = User(github_id=1, username="octocat", name="O", avatar_url=None)
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    INGEST_LIMITER._hits.clear()
    return u


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def fake_dns(monkeypatch):
    """Never touch real DNS in tests: IP literals resolve to themselves, hostnames to a public address."""
    def fake_getaddrinfo(host, port, *args, **kwargs):
        import ipaddress as _ip

        try:
            ip = str(_ip.ip_address(host))
        except ValueError:
            ip = "93.184.216.34"
        return [(None, None, None, "", (ip, port))]
    monkeypatch.setattr(extractor.socket, "getaddrinfo", fake_getaddrinfo)


# ---------------- fetch / SSRF ----------------

def run_fetch(monkeypatch, url):
    """Call the async fetcher on a fresh event loop (no pytest-asyncio needed)."""
    import asyncio

    async def run():
        return await extractor.fetch_source_text(url)

    return asyncio.new_event_loop().run_until_complete(run())


def test_fetch_rejects_non_http(monkeypatch):
    for url in ["file:///etc/passwd", "ftp://x/y", "gopher://x"]:
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, url)
        assert "http" in str(exc.value)


def test_fetch_rejects_nonstandard_ports(monkeypatch, fake_dns):
    with pytest.raises(extractor.SourceFetchError) as exc:
        run_fetch(monkeypatch, "https://example.org:8080/x")
    assert "ports" in str(exc.value)


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "10.1.2.3", "169.254.1.1", "192.168.0.9"])
def test_fetch_rejects_private_addresses(monkeypatch, host):
    """No DNS mock on purpose for local addresses, but pin getaddrinfo for determinism."""
    monkeypatch.setattr(
        extractor.socket, "getaddrinfo", lambda h, p, *a, **k: [(None, None, None, "", (host if "." in host else "127.0.0.1", p))]
    )
    with pytest.raises(extractor.SourceFetchError) as exc:
        run_fetch(monkeypatch, f"https://{host}/x")
    assert "private" in str(exc.value)


def test_fetch_rejects_redirect_to_private(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/start").mock(
            return_value=HTTPResponse(302, headers={"location": "http://10.9.9.9/evil"})
        )
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, "https://example.org/start")
    assert "private" in str(exc.value)


def test_fetch_rejects_max_redirects(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(url__startswith="https://example.org/loop").mock(
            return_value=HTTPResponse(302, headers={"location": "https://example.org/loop-again"})
        )
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, "https://example.org/loop")


@respx.mock
def test_fetch_rejects_oversize_documents(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/big").mock(
            return_value=HTTPResponse(200, text="x" * (extractor.SOURCE_TEXT_CAP * 100))
        )
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, "https://example.org/big")
    assert "500 KB" in str(exc.value)


def test_fetch_rejects_pdf(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/doc.pdf").mock(
            return_value=HTTPResponse(200, content=b"%PDF-1.4", headers={"content-type": "application/pdf"})
        )
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, "https://example.org/doc.pdf")
    assert "paste the text" in str(exc.value)


def test_fetch_rejects_bad_status(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/gone").mock(return_value=HTTPResponse(404, text="nope"))
        with pytest.raises(extractor.SourceFetchError) as exc:
            run_fetch(monkeypatch, "https://example.org/gone")


def test_fetch_extracts_text_and_caps(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        html = PUBLIC_HTML + "<p>word</p>" * 20_000  # well under 500 KB, over 15k chars
        mock.get("https://example.org/ps").mock(
            return_value=HTTPResponse(200, text=html, headers={"content-type": "text/html"})
        )
        text = run_fetch(monkeypatch, "https://example.org/ps")
    assert len(text) <= extractor.SOURCE_TEXT_CAP
    assert "flood" in text


def test_follows_up_to_three_redirects(monkeypatch, fake_dns):
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/a").mock(
            return_value=HTTPResponse(302, headers={"location": "https://example.org/b"})
        )
        mock.get("https://example.org/b").mock(
            return_value=HTTPResponse(301, headers={"location": "https://example.org/c"})
        )
        mock.get("https://example.org/c").mock(
            return_value=HTTPResponse(200, text=PUBLIC_HTML, headers={"content-type": "text/html"})
        )
        text = run_fetch(monkeypatch, "https://example.org/a")
    assert "flood" in text


# ---------------- extract_draft (LLM) ----------------

def canned_llm(monkeypatch, payload: str):
    def fake(system, user, schema, model=None):
        return payload

    monkeypatch.setattr("app.services.llm._provider_raw_json", fake, raising=False)


def test_extract_draft_happy_path(monkeypatch):
    payload = """
    ```json
    {"is_problem": true, "title": "Flood alert", "summary": "Build a flood risk model.",
     "who_affected": "Riverside villages", "why_matters": "Deaths", "field": "ml",
     "domain": "disaster-management", "difficulty": "intermediate", "est_hours": 40,
     "tech_tags": ["PYTHON", "Pandas"], "datasets": [{"name": "CIC-IDS", "url": null}],
     "approaches": ["Classifier"], "source_note": null,
     "evidence": {"summary": "Build a flood risk model."}, "inferred_fields": ["difficulty"]}
    ```
    """
    canned_llm(monkeypatch, payload)
    draft, evidence, inferred = extractor.extract_draft("Some source text", None)
    assert draft.title == "Flood alert"
    assert draft.tech_tags == ["python", "pandas"]  # lowercased
    assert evidence["summary"] == "Build a flood risk model."
    assert inferred == ["difficulty"]


def test_extract_draft_no_problem(monkeypatch):
    canned_llm(monkeypatch, '{"is_problem": false, "title": "", "summary": ""}')
    with pytest.raises(extractor.NoClearProblem):
        extractor.extract_draft("junk", None)


# ---------------- /api/ingest ----------------

def test_ingest_requires_auth(client, db_session):
    res = client.post("/api/ingest", json={"text": "some problem text"})
    assert res.status_code == 401


def test_ingest_requires_exactly_one(client, user, db_session):
    only_url = client.post("/api/ingest", json={"url": "https://example.org/x", "text": "t"})
    assert only_url.status_code == 422
    both_missing = client.post("/api/ingest", json={})
    assert both_missing.status_code == 422


def test_ingest_full_url_flow(client, user, db_session, monkeypatch, fake_dns):
    INGEST_LIMITER._hits.clear()
    monkeypatch.setattr(
        "app.routers.ingest.INGEST_LIMITER.allowed", lambda key: True, raising=False
    )
    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://example.org/ps").mock(
            return_value=HTTPResponse(200, text=PUBLIC_HTML, headers={"content-type": "text/html"})
        )
        canned_llm(
            monkeypatch,
            '{"is_problem": true, "title": "Flood alert", "summary": "Build a flood risk model.",'
            '"who_affected": "Villages", "why_matters": "Deaths", "field": "ml", "domain": "disaster-management",'
            '"difficulty": "intermediate", "est_hours": 40, "tech_tags": ["ml"], "datasets": [],'
            '"approaches": ["x"], "source_note": null, "evidence": {"title": "District flood alert"},'
            '"inferred_fields": []}',
        )
        res = client.post("/api/ingest", json={"url": "https://example.org/ps"})
    assert res.status_code == 200
    data = res.json()
    assert data["draft"]["title"] == "Flood alert"
    assert data["draft"]["source_url"] == "https://example.org/ps"
    assert data["draft"]["source_name"] == "https://example.org/ps"
    assert data["source_url"] == "https://example.org/ps"
    assert data["evidence"] == {"title": "District flood alert"}
    assert data["draft"]["field"] == "ml"


def test_ingest_pasted_text_flow(client, user, db_session, monkeypatch):
    INGEST_LIMITER._hits.clear()
    canned_llm(
        monkeypatch,
        '{"is_problem": true, "title": "T", "summary": "S", "who_affected": "W", "why_matters": "Y",'
        '"field": "other", "domain": "other", "difficulty": "beginner", "est_hours": 10, "tech_tags": [],'
        '"datasets": [], "approaches": [], "source_note": null, "evidence": {}, "inferred_fields": []}',
    )
    res = client.post("/api/ingest", json={"text": "A clean problem description goes here."})
    assert res.status_code == 200
    data = res.json()
    assert data["draft"]["source_name"] == "Pasted text"
    assert data["source_url"] is None


def test_ingest_no_problem_422(client, user, db_session, monkeypatch):
    INGEST_LIMITER._hits.clear()
    monkeypatch.setattr("app.services.llm._provider_raw_json", lambda *a, **k: '{"is_problem": false}', raising=False)
    res = client.post("/api/ingest", json={"text": "buy my socks"})
    assert res.status_code == 422
    assert "Couldn't find a clear problem" in res.json()["detail"]


def test_ingest_rate_limited(client, user, db_session, monkeypatch):
    INGEST_LIMITER._hits.clear()
    monkeypatch.setattr("app.services.llm._provider_raw_json", lambda *a, **k: '{"is_problem": false}', raising=False)
    codes = []
    for _ in range(int(config.get_settings().AI_RATE_LIMIT_PER_HOUR) + 1):
        res = client.post("/api/ingest", json={"text": "some text"})
        codes.append(res.status_code)
    assert codes[-1] == 429
    assert 200 in codes or 422 in codes


def test_ingest_empty_text_422(client, user, db_session):
    res = client.post("/api/ingest", json={"text": "   "})
    assert res.status_code == 422


# ---------------- POST /api/problems ----------------

def draft_card_factory(**overrides):
    card = {
        "title": "Flood alert",
        "summary": "Build a flood risk model.",
        "who_affected": "Villages",
        "why_matters": "Deaths",
        "field": "ml",
        "domain": "disaster-management",
        "difficulty": "intermediate",
        "est_hours": 40,
        "tech_tags": ["ml"],
        "datasets": [],
        "approaches": [],
        "source_name": "Smart India Hackathon 2026",
        "source_id": "SIH26999",
        "source_url": "https://example.org/ps",
        "ai_fields": ["difficulty", "approaches"],
    }
    card.update(overrides)
    return card


def test_post_problem_requires_auth(client, db_session):
    res = client.post("/api/problems", json=draft_card_factory())
    assert res.status_code == 401


def test_post_problem_creates(db_session, client, user):
    from sqlalchemy import select

    res = client.post("/api/problems", json=draft_card_factory())
    assert res.status_code == 201, res.json()
    data = res.json()
    assert data["title"] == "Flood alert"
    assert data["ai_fields"] == ["difficulty", "approaches"]
    assert data["project_count"] == 0
    row = db_session.scalar(select(Problem).where(Problem.source_id == "SIH26999"))
    assert row is not None
    assert row.created_by == user.id
    assert row.original_text == "Build a flood risk model."


def test_post_problem_duplicate_409(db_session, client, user):
    problem_row = Problem(
        title="Existing", summary="s", who_affected="w", why_matters="y", field="ml",
        domain="other", difficulty="beginner", est_hours=10, tech_tags=[], datasets=[],
        approaches=[], source_name="Smart India Hackathon 2026", source_id="SIH26999",
        original_text="verbatim",
    )
    db_session.add(problem_row)
    db_session.commit()
    res = client.post("/api/problems", json=draft_card_factory())
    assert res.status_code == 409


def test_post_problem_invalid_enum_422(client, user, db_session):
    res = client.post("/api/problems", json=draft_card_factory(field="quantum-chess"))
    assert res.status_code == 422


def test_post_problem_tech_tags_lowercased(db_session, client, user):
    res = client.post("/api/problems", json=draft_card_factory(tech_tags=["Python", " FAST-API "]))
    assert res.status_code == 201
    assert res.json()["tech_tags"] == ["python", "fast-api"]


def test_ingest_offloads_llm_from_event_loop(client, user, db_session, monkeypatch):
    """The sync LLM SDK must stay off the loop: health answers DURING a slow ingest."""
    import threading
    import time

    from app.main import app as real_app
    from fastapi.testclient import TestClient
    from app.deps import get_current_user
    from app.services.extractor import NoClearProblem

    def slow_extract(text, source_url):
        time.sleep(2.0)
        raise NoClearProblem("Couldn't find a clear problem in this source")

    monkeypatch.setattr(extractor, "extract_draft", slow_extract)
    app.dependency_overrides[get_current_user] = lambda: user

    markers = {}

    def hit_health():
        with TestClient(real_app) as hc:
            hc.get("/api/health")
            markers["health_at"] = time.monotonic()

    t = threading.Thread(target=hit_health)
    t.start()
    started = time.monotonic()
    code = client.post("/api/ingest", json={"text": "some problem text"}).status_code
    ingest_at = time.monotonic()
    t.join(timeout=10)
    assert code == 422
    assert markers["health_at"] < ingest_at - 1.0, "event loop was blocked by the LLM call"
