"""Failure-path tests for the API error boundary and shutdown cleanup."""

import asyncio
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app import main
from app.main import database_unavailable_handler, unhandled_exception_handler
from app.services import github


def _request(path: str = "/api/test", request_id: str | None = None):
    headers = {"X-Request-ID": request_id} if request_id else {}
    return SimpleNamespace(
        headers=headers,
        state=SimpleNamespace(),
        method="GET",
        url=SimpleNamespace(path=path),
    )


def _body(response) -> dict:
    return json.loads(response.body)


def test_unhandled_exception_handler_returns_safe_json():
    response = asyncio.run(
        unhandled_exception_handler(
            _request(request_id="req-123"),
            RuntimeError("secret internal detail"),
        )
    )

    assert response.status_code == 500
    assert response.headers["x-request-id"] == "req-123"
    body = _body(response)
    assert body["detail"]["code"] == "internal_error"
    assert "secret internal detail" not in body["detail"]["message"]
    assert "Traceback" not in body["detail"]["message"]


def test_database_unavailable_handler_returns_503():
    response = asyncio.run(
        database_unavailable_handler(
            _request(request_id="db-1"),
            OperationalError("SELECT 1", {}, ConnectionError("down")),
        )
    )

    assert response.status_code == 503
    body = _body(response)
    assert body["detail"]["code"] == "database_unavailable"
    assert "SELECT" not in body["detail"]["message"]


def test_request_id_is_minted_when_header_is_invalid():
    response = asyncio.run(
        unhandled_exception_handler(
            _request(request_id='bad id with spaces\n"'),
            RuntimeError("boom"),
        )
    )

    request_id = response.headers["x-request-id"]
    assert len(request_id) == 32
    assert all(char in "0123456789abcdef" for char in request_id)


def test_database_outage_maps_to_503_through_the_app(monkeypatch):
    original = main.get_engine

    def down():
        raise OperationalError("SELECT 1", {}, ConnectionError("database down"))

    with TestClient(main.app) as client:
        monkeypatch.setattr(main, "get_engine", down)
        try:
            live = client.get("/api/health/live")
            response = client.get("/api/health")
        finally:
            monkeypatch.setattr(main, "get_engine", original)

    assert live.status_code == 200
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "database_unavailable"
    assert response.headers["x-request-id"]


def test_unexpected_route_failure_maps_to_safe_json(monkeypatch):
    original = main.get_engine

    def boom():
        raise RuntimeError("unexpected secret")

    with TestClient(main.app, raise_server_exceptions=False) as client:
        monkeypatch.setattr(main, "get_engine", boom)
        try:
            response = client.get("/api/health")
        finally:
            monkeypatch.setattr(main, "get_engine", original)

    assert response.status_code == 500
    assert response.json()["detail"]["code"] == "internal_error"
    assert "unexpected secret" not in response.text


@pytest.mark.anyio
async def test_close_client_releases_shared_http_client(monkeypatch):
    class FakeClient:
        closed = False

        async def aclose(self):
            self.closed = True

    fake = FakeClient()
    monkeypatch.setattr(github, "_shared_client", fake)

    await github.close_client()

    assert fake.closed is True
    assert github._shared_client is None
