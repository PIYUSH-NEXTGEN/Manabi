from datetime import datetime, timedelta, timezone

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response as HTTPResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.deps import get_current_user, get_optional_user
from app.main import app
from app.models import User


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()


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
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def user(db_session):
    u = User(github_id=42, username="octocat", name="Octo", avatar_url="http://a/1.png",
             github_token="tok")
    db_session.add(u)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_optional_user] = lambda: u
    return u


def _iso(day_offset: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=day_offset)).isoformat()


@respx.mock
def test_heatmap_counts_push_events_per_day(client, user):
    respx.get("https://api.github.com/users/octocat/events/public").mock(
        return_value=HTTPResponse(200, json=[
            {"type": "PushEvent", "created_at": _iso(3)},
            {"type": "PushEvent", "created_at": _iso(3)},
            {"type": "IssuesEvent", "created_at": _iso(3)},
            {"type": "PushEvent", "created_at": _iso(200)},  # outside the window
        ])
    )
    res = client.get("/api/me/github-heatmap")
    assert res.status_code == 200
    body = res.json()
    assert body["window_days"] == 91
    assert body["total"] == 2
    recent_day = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
    entry = next(d for d in body["days"] if d["date"] == recent_day)
    assert entry["count"] == 2


@respx.mock
def test_heatmap_degrades_with_empty_grid_when_github_down(client, user):
    respx.get("https://api.github.com/users/octocat/events/public").mock(
        return_value=HTTPResponse(502, json={})
    )
    res = client.get("/api/me/github-heatmap")
    assert res.status_code == 200
    assert res.json() == {"days": [], "total": 0, "window_days": 91}


def test_heatmap_requires_login(client):
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_optional_user, None)
    res = client.get("/api/me/github-heatmap")
    assert res.status_code == 401
