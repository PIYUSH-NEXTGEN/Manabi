from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import DEFAULT_SESSION_SECRET, app, guard_deploy_secrets


def settings(base_url: str, secret: str) -> SimpleNamespace:
    return SimpleNamespace(BASE_URL=base_url, SESSION_SECRET=secret)


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


def test_security_headers_and_api_no_store():
    with TestClient(app) as client:
        res = client.get("/api/this-route-does-not-exist")
    assert res.status_code == 404
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert res.headers["Content-Security-Policy"] == "frame-ancestors 'none'"
    assert res.headers["Cache-Control"] == "no-store"
