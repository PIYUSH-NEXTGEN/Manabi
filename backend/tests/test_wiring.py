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
        title="Flood model", summary="s", who_affected="w", why_matters="y", field="aiml",
        domain="other", difficulty="beginner", est_hours=10, tech_tags=[], datasets=[],
        approaches=[], source_name="S", source_id="S1", original_text="verbatim",
    )
    db_session.add(problem)
    db_session.commit()
    db_session.add(
        Project(
            problem_id=problem.id, user_id=jane.id, repo_owner="jane", repo_name="flood",
            repo_url="https://github.com/jane/flood", open_for_contributors=True,
            verification_status="verified",
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
        "field": "web-dev",
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


def test_problem_create_requires_login(client, db_session):
    """No auth override installed -> the create endpoint must demand a user."""
    res = client.post("/api/problems", json=draft_card_factory())
    assert res.status_code == 401


def test_problem_create_rejects_duplicate_source_id(client, db_session, user):
    res = client.post(
        "/api/problems",
        json=draft_card_factory(source_name="SIH 2026", source_id="PS-42"),
    )
    assert res.status_code == 201, res.json()
    res = client.post(
        "/api/problems",
        json=draft_card_factory(source_name="SIH 2026", source_id="PS-42"),
    )
    assert res.status_code == 409
    assert res.json()["detail"] == "A problem with this source ID already exists"


def test_problem_create_stores_datasets(client, db_session, user):
    """datasets is a free-form list[dict]; posted entries must be stored and
    echoed back verbatim (regression: create used to call .model_dump() on
    plain dicts and crash with a 500)."""
    card = draft_card_factory(source_id="DATASET-1")
    card["datasets"] = [
        {"name": "Landslide inventory", "url": None},
        {"name": "Sentinel-2 tiles", "url": "https://example.com/tiles"},
    ]
    res = client.post("/api/problems", json=card)
    assert res.status_code == 201, res.json()
    assert res.json()["datasets"] == card["datasets"]


def test_problem_create_rate_limited_for_regular_users(client, db_session, user, monkeypatch):
    from app.routers.problems import PROBLEM_CREATE_LIMITER

    monkeypatch.setenv("PROBLEM_CREATE_PER_HOUR", "2")
    config.get_settings.cache_clear()
    PROBLEM_CREATE_LIMITER.reset(db_session)
    try:
        assert client.post("/api/problems", json=draft_card_factory()).status_code == 201
        assert client.post("/api/problems", json=draft_card_factory()).status_code == 201
        res = client.post("/api/problems", json=draft_card_factory())
        assert res.status_code == 429
        assert res.json()["detail"]["code"] == "rate_limited"
    finally:
        config.get_settings.cache_clear()
        PROBLEM_CREATE_LIMITER.reset(db_session)


def test_problem_create_admins_are_exempt(client, db_session, user, monkeypatch):
    from app.routers.problems import ADMIN_LIMITER

    monkeypatch.setenv("PROBLEM_CREATE_PER_HOUR", "1")
    monkeypatch.setenv("ADMIN_GITHUB_USERNAMES", "fixer")
    config.get_settings.cache_clear()
    ADMIN_LIMITER.reset(db_session)
    try:
        for index in range(3):
            res = client.post(
                "/api/problems",
                json=draft_card_factory(source_id=f"ADM{index}"),
            )
            assert res.status_code == 201, res.json()
    finally:
        config.get_settings.cache_clear()
        ADMIN_LIMITER.reset(db_session)


def test_problem_create_admins_still_have_sanity_cap(client, db_session, user, monkeypatch):
    """Admins bypass the user quota but not the shared 100/h sanity cap."""
    from app.routers.problems import ADMIN_LIMITER

    monkeypatch.setenv("ADMIN_GITHUB_USERNAMES", "fixer")
    monkeypatch.setenv("ADMIN_RATE_LIMIT_PER_HOUR", "2")
    config.get_settings.cache_clear()
    ADMIN_LIMITER.reset(db_session)
    try:
        for index in range(2):
            assert client.post(
                "/api/problems", json=draft_card_factory(source_id=f"ADMCAP{index}")
            ).status_code == 201
        res = client.post("/api/problems", json=draft_card_factory(source_id="ADMCAP-X"))
        assert res.status_code == 429
        assert res.json()["detail"]["code"] == "rate_limited"
        assert int(res.headers["Retry-After"]) > 0
    finally:
        config.get_settings.cache_clear()
        ADMIN_LIMITER.reset(db_session)

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


# ---------------- regression: removed advanced/ops feature surface ----------------

REMOVED_API_PREFIXES = (
    "/api/webhooks",
    "/api/api-contracts",
    "/api/tenant-security",
    "/api/incidents",
    "/api/ingestion",
    "/api/analytics",
    "/api/accessibility",
    "/api/inventory",
    "/api/sync",
    "/api/workflows",
)

REMOVED_TABLE_NAMES = {
    "webhook_endpoints", "webhook_events", "webhook_deliveries",
    "api_specs", "api_contract_comparisons", "api_monitoring_targets", "api_contract_checks",
    "tenants", "tenant_memberships", "tenant_resources", "security_findings", "role_permissions",
    "incidents", "incident_events", "incident_assignments", "incident_timeline_entries",
    "ingestion_jobs", "ingested_files", "processing_workers",
    "analytics_events", "consent_records", "data_retention_policies", "funnel_definitions", "retention_cohorts",
    "monitored_websites", "accessibility_scans", "accessibility_issues",
    "sales_channels", "inventory_items", "inventory_reservations", "stock_reconciliations",
    "sync_records", "sync_conflicts",
    "workflows", "workflow_executions", "workflow_step_executions",
}

CORE_API_ROUTES = (
    "/api/health",
    "/api/problems",
    "/api/problems/facets",
    "/api/problems/{problem_id}",
    "/api/problems/{problem_id}/projects",
    "/api/stats",
    "/api/chat",
    "/api/recommendations",
    "/api/me/projects",
    "/api/auth/github/login",
    "/api/auth/github/callback",
    "/api/auth/me",
    "/api/auth/logout",
    "/api/u/{username}",
    "/api/projects/{project_id}",
    "/api/projects/{project_id}/progress",
)


def _registered_api_paths() -> set[str]:
    return set(app.openapi()["paths"])


def test_removed_feature_api_prefixes_are_gone():
    # FastAPI 0.143 wraps include_router with nested routers, so read the
    # resolved OpenAPI path map rather than app.routes.
    registered = _registered_api_paths()
    for prefix in REMOVED_API_PREFIXES:
        matches = [p for p in registered if p == prefix or p.startswith(prefix + "/")]
        assert not matches, f"removed feature route still registered: {matches}"


def test_core_api_routes_are_registered():
    registered = _registered_api_paths()
    missing = [path for path in CORE_API_ROUTES if path not in registered]
    assert missing == [], f"core MANABI routes missing: {missing}"


def test_removed_feature_tables_are_not_models():
    tables = set(Base.metadata.tables)
    leftover = REMOVED_TABLE_NAMES & tables
    assert leftover == set(), f"removed feature models still registered: {sorted(leftover)}"
    for kept in ("users", "problems", "projects"):
        assert kept in tables


