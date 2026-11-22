"""Phase 14: structured logging, request correlation, and failure intake."""

import json
import logging
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config, main
from app.db import Base, get_db
from app.logging_config import (
    ContextFilter,
    JsonFormatter,
    TextFormatter,
    configure_logging,
    redact,
    request_id_var,
)
from app.main import app
from app.routers.client_errors import CLIENT_ERROR_LIMITER


def _record(message: str, *args, level: int = logging.INFO) -> logging.LogRecord:
    return logging.LogRecord("app.test", level, __file__, 1, message, args, None)


def _events(caplog, name: str) -> list[logging.LogRecord]:
    return [r for r in caplog.records if getattr(r, "event", None) == name]


@pytest.fixture(autouse=True)
def env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
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


# ---------------- redaction ----------------

def test_redact_masks_bearer_and_credential_values():
    bearer = redact("Authorization: Bearer abcdefghijklmnop")
    assert "abcdefghijklmnop" not in bearer
    assert "***" in bearer

    password = redact("password=hunter2")
    assert "hunter2" not in password
    assert "password=***" in password


def test_redact_masks_provider_tokens_and_database_urls():
    assert "ghp_" not in redact("token ghp_" + "a" * 30)
    assert "AIza" not in redact("key AIza" + "b" * 30)
    masked = redact("postgresql://manabi:s3cret@db.internal/manabi")
    assert "s3cret" not in masked
    assert "manabi:***@db.internal" in masked


def test_redact_keeps_ordinary_text():
    assert redact("Request completed status=200 path=/api/problems") == (
        "Request completed status=200 path=/api/problems"
    )


# ---------------- formatters ----------------

def test_json_formatter_emits_one_line_with_context_fields():
    token = request_id_var.set("req-json-1")
    try:
        record = _record("Unhandled error token=%s", "ghp_" + "c" * 30, level=logging.ERROR)
        record.event = "unhandled_exception"
        record.status = 500
        record.error_type = "RuntimeError"
        record.client_stack = "fetch token=ghp_" + "c" * 30
        ContextFilter("production", "v1").filter(record)
        line = JsonFormatter().format(record)
    finally:
        request_id_var.reset(token)

    assert "\n" not in line
    payload = json.loads(line)
    assert payload["level"] == "ERROR"
    assert payload["service"] == "manabi-api"
    assert payload["environment"] == "production"
    assert payload["version"] == "v1"
    assert payload["request_id"] == "req-json-1"
    assert payload["event"] == "unhandled_exception"
    assert payload["status"] == 500
    assert payload["error_type"] == "RuntimeError"
    assert "ghp_" not in payload["message"]
    assert "ghp_" not in payload["client_stack"]


def test_json_formatter_redacts_exception_text():
    secret = "ghp_" + "d" * 30
    try:
        raise RuntimeError(f"password=hunter2 {secret}")
    except RuntimeError:
        import sys

        record = _record("boom", level=logging.ERROR)
        record.exc_info = sys.exc_info()
        ContextFilter("production", "v1").filter(record)
        payload = json.loads(JsonFormatter().format(record))

    assert payload["error_type"] == "RuntimeError"
    assert payload["exception"]
    assert "hunter2" not in payload["exception"]
    assert secret not in payload["exception"]


def test_text_formatter_includes_request_id_and_redacts():
    token = request_id_var.set("req-text-1")
    try:
        record = _record("password=hunter2")
        ContextFilter("development", "dev").filter(record)
        line = TextFormatter().format(record)
    finally:
        request_id_var.reset(token)

    assert "[request_id=req-text-1]" in line
    assert "hunter2" not in line
    assert "password=***" in line


def test_configure_logging_routes_uvicorn_through_the_app_handler():
    uvicorn_logger = logging.getLogger("uvicorn.error")
    uvicorn_logger.addHandler(logging.NullHandler())
    uvicorn_logger.propagate = False
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.addHandler(logging.NullHandler())
    access_logger.propagate = True

    configure_logging(
        SimpleNamespace(
            APP_ENV="test", LOG_LEVEL="INFO", LOG_FORMAT="text", APP_VERSION="v1"
        )
    )

    assert uvicorn_logger.handlers == []
    assert uvicorn_logger.propagate is True
    assert access_logger.handlers == []
    assert access_logger.propagate is False


# ---------------- request correlation and access logs ----------------

def test_response_carries_request_id_and_security_headers(client):
    response = client.get("/api/problems", headers={"X-Request-ID": "trace-1"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "trace-1"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Content-Security-Policy"] == "frame-ancestors 'none'"
    # The anonymous public board is deliberately shareable: it carries no
    # per-viewer data and the edge cache serves it.
    assert response.headers["Cache-Control"].startswith("public")


def test_private_api_stays_no_store(client):
    for path in ("/api/auth/me", "/api/me/projects"):
        response = client.get(path)
        assert response.headers["Cache-Control"] == "no-store", path


def test_invalid_request_id_is_minted(client):
    response = client.get("/api/problems", headers={"X-Request-ID": 'bad id\n"x"'})

    request_id = response.headers["X-Request-ID"]
    assert len(request_id) == 32
    assert all(char in "0123456789abcdef" for char in request_id)


def test_non_health_request_is_access_logged(client, caplog):
    caplog.set_level(logging.INFO)
    caplog.clear()

    client.get("/api/problems", headers={"X-Request-ID": "logged-1"})

    completed = [
        r
        for r in _events(caplog, "request_completed")
        if getattr(r, "path", None) == "/api/problems"
    ]
    assert completed
    assert completed[-1].status == 200
    assert completed[-1].request_id == "logged-1"
    assert completed[-1].duration_ms >= 0


def test_healthy_health_probes_are_not_access_logged(client, caplog):
    caplog.set_level(logging.INFO)
    caplog.clear()

    client.get("/api/health")
    client.get("/api/health/live")
    client.get("/api/health/ready")

    health = [
        r
        for r in caplog.records
        if getattr(r, "event", None) in {"request_completed", "request_failed", "slow_request"}
        and str(getattr(r, "path", "")).startswith("/api/health")
    ]
    assert health == []


def test_failed_health_probe_is_access_logged(monkeypatch, caplog):
    original = main.get_engine

    def down():
        from sqlalchemy.exc import OperationalError

        raise OperationalError("SELECT 1", {}, ConnectionError("down"))

    caplog.set_level(logging.ERROR)
    caplog.clear()
    with TestClient(main.app) as test_client:
        monkeypatch.setattr(main, "get_engine", down)
        try:
            response = test_client.get("/api/health")
        finally:
            monkeypatch.setattr(main, "get_engine", original)

    assert response.status_code == 503
    failed = _events(caplog, "request_failed")
    assert failed
    assert failed[-1].status == 503
    assert failed[-1].path == "/api/health"


def test_slow_request_emits_warning(monkeypatch, caplog):
    request = SimpleNamespace(
        method="GET",
        url=SimpleNamespace(path="/api/problems"),
        scope={"route": SimpleNamespace(path="/api/problems")},
        headers={},
    )
    monkeypatch.setattr(main, "get_settings", lambda: SimpleNamespace(SLOW_REQUEST_MS=1))
    caplog.set_level(logging.WARNING)
    caplog.clear()

    main._log_access(request, 200, 50)

    slow = _events(caplog, "slow_request")
    assert slow
    assert slow[-1].status == 200
    assert slow[-1].duration_ms == 50


# ---------------- browser error intake ----------------

def test_client_error_report_is_accepted_and_logged(client, db_session, caplog):
    CLIENT_ERROR_LIMITER.reset(db_session)
    caplog.set_level(logging.ERROR)
    caplog.clear()

    response = client.post(
        "/api/client-errors",
        headers={"X-Request-ID": "browser-1"},
        json={
            "event": "react_error_boundary",
            "message": "Cannot read properties of undefined",
            "error_name": "TypeError",
            "route": "/problems/17",
            "app_version": "v1",
            "backend_request_id": "backend-9",
        },
    )

    assert response.status_code == 204
    reports = _events(caplog, "client_error")
    assert reports
    report = reports[-1]
    assert report.request_id == "browser-1"
    assert report.client_event == "react_error_boundary"
    assert report.client_route == "/problems/17"
    assert report.client_app_version == "v1"
    assert report.backend_request_id == "backend-9"


def test_client_error_report_rate_limited_per_ip(client, db_session, monkeypatch):
    monkeypatch.setenv("CLIENT_ERROR_RATE_LIMIT_PER_HOUR", "2")
    config.get_settings.cache_clear()
    CLIENT_ERROR_LIMITER.reset(db_session)
    body = {"event": "error", "message": "boom"}

    try:
        assert client.post("/api/client-errors", json=body).status_code == 204
        assert client.post("/api/client-errors", json=body).status_code == 204
        blocked = client.post("/api/client-errors", json=body)
    finally:
        config.get_settings.cache_clear()
        CLIENT_ERROR_LIMITER.reset(db_session)

    assert blocked.status_code == 429
    assert int(blocked.headers["Retry-After"]) > 0


def test_client_error_rejects_oversized_report(client, db_session):
    response = client.post(
        "/api/client-errors",
        json={"event": "error", "message": "x" * 1001},
    )

    assert response.status_code == 422
