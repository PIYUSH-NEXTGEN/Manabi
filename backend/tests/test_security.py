from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from pydantic import ValidationError

from app.config import Settings, get_settings
from app.main import DEFAULT_SESSION_SECRET, app, create_app, guard_deploy_secrets


def settings(
    base_url: str,
    secret: str,
    app_env: str = "development",
    database_url: str = "postgresql://user:pass@db.example/manabi",
) -> SimpleNamespace:
    return SimpleNamespace(
        APP_ENV=app_env,
        BASE_URL=base_url,
        SESSION_SECRET=secret,
        DATABASE_URL=database_url,
    )


@pytest.mark.parametrize(
    "secret",
    [DEFAULT_SESSION_SECRET, "", "   ", "short-but-not-the-placeholder"],
)
def test_deploy_guard_rejects_weak_session_secrets(secret):
    with pytest.raises(RuntimeError, match="SESSION_SECRET"):
        guard_deploy_secrets(settings("https://manabi.example.com", secret))


def test_deploy_guard_accepts_a_long_random_secret():
    guard_deploy_secrets(settings("https://manabi.example.com", "a" * 43))


def test_deploy_guard_keeps_local_defaults_convenient():
    guard_deploy_secrets(settings("http://localhost:5173", DEFAULT_SESSION_SECRET))
    guard_deploy_secrets(settings("http://127.0.0.1:8000", ""))


def test_production_rejects_http_and_localhost_origins():
    for base_url in (
        "http://manabi.example.com",
        "https://localhost:8443",
        "https://127.0.0.1:8443",
    ):
        with pytest.raises(RuntimeError, match="BASE_URL"):
            guard_deploy_secrets(
                settings(base_url, "a" * 43, app_env="production")
            )


def test_production_rejects_sqlite_database():
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        guard_deploy_secrets(
            settings(
                "https://manabi.example.com",
                "a" * 43,
                app_env="production",
                database_url="sqlite:///./app.db",
            )
        )


def test_production_accepts_public_https_and_postgres():
    guard_deploy_secrets(
        settings(
            "https://manabi.example.com",
            "a" * 43,
            app_env="production",
            database_url="postgres://user:pass@db.example/manabi",
        )
    )


@pytest.mark.parametrize(
    "base_url",
    [
        "manabi.example.com",
        "ftp://manabi.example.com",
        "https://manabi.example.com/path",
        "https://manabi.example.com/?query=1",
    ],
)
def test_base_url_must_be_a_plain_http_origin(base_url):
    with pytest.raises(ValidationError, match="BASE_URL"):
        Settings(BASE_URL=base_url, _env_file=None)


def test_security_headers_and_api_no_store():
    with TestClient(app) as client:
        res = client.get("/api/this-route-does-not-exist")
    assert res.status_code == 404
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert res.headers["Content-Security-Policy"] == "frame-ancestors 'none'"
    assert res.headers["Cache-Control"] == "no-store"
    assert "Strict-Transport-Security" not in res.headers


def test_https_production_sets_hsts_and_secure_session_cookie(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("BASE_URL", "https://manabi.example.com")
    monkeypatch.setenv("SESSION_SECRET", "a" * 43)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@db.example/manabi")
    get_settings.cache_clear()
    try:
        secure_app = create_app()
        response = TestClient(secure_app).get("/api/this-route-does-not-exist")
        session_middleware = next(
            middleware
            for middleware in secure_app.user_middleware
            if middleware.cls.__name__ == "SessionMiddleware"
        )
    finally:
        get_settings.cache_clear()

    assert response.headers["Strict-Transport-Security"] == "max-age=31536000"
    assert session_middleware.kwargs["https_only"] is True
