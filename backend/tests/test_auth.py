from urllib.parse import parse_qs, urlparse

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response as HTTPResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config
from app.db import Base, get_db
from app.main import app
from app.models import User

GH_USER_ID = 987654
GH_USER = {
    "id": GH_USER_ID,
    "login": "octocat",
    "name": "Octo Cat",
    "avatar_url": "https://avatars.githubusercontent.com/octocat",
}


@pytest.fixture(autouse=True)
def github_env(monkeypatch):
    get_settings = config.get_settings
    monkeypatch.setenv("GITHUB_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-key")
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
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_github():
    with respx.mock(assert_all_called=False) as mock:
        mock.post("https://github.com/login/oauth/access_token").mock(
            return_value=HTTPResponse(200, json={"access_token": "gh-token-1", "token_type": "bearer"})
        )
        mock.get("https://api.github.com/user").mock(
            return_value=HTTPResponse(200, json=GH_USER, headers={"content-type": "application/json"})
        )
        yield mock


def test_me_requires_login(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not logged in"}


def test_logout_without_session_ok(client):
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    assert res.json() == {"ok": True}


def test_login_redirects_to_github_with_read_user_scope(client, mock_github):
    res = client.get("/api/auth/github/login", follow_redirects=False)
    assert res.status_code == 302
    location = res.headers["location"]
    assert location.startswith("https://github.com/login/oauth/authorize")
    parsed = parse_qs(urlparse(location).query)
    assert parsed["scope"] == ["read:user"]
    assert "state" in parsed
    assert "client_id" in parsed


def test_full_oauth_flow_upserts_token_and_session(client, db_session, mock_github):
    login_res = client.get("/api/auth/github/login", follow_redirects=False)
    state = parse_qs(urlparse(login_res.headers["location"]).query)["state"][0]

    res = client.get("/api/auth/github/callback", params={"code": "abc", "state": state}, follow_redirects=False)
    assert res.status_code == 302
    assert res.headers["location"] == "/"

    user = db_session.query(User).filter(User.github_id == GH_USER_ID).one()
    assert user.username == "octocat"
    assert user.name == "Octo Cat"
    assert user.github_token == "gh-token-1"

    me_res = client.get("/api/auth/me")
    assert me_res.status_code == 200
    assert me_res.json() == {"id": user.id, "username": "octocat", "name": "Octo Cat", "avatar_url": GH_USER["avatar_url"]}


def test_callback_reuses_existing_user_and_updates_token(client, db_session, mock_github):
    existing = User(github_id=GH_USER_ID, username="old-name", name="Old", avatar_url=None, github_token="stale")
    db_session.add(existing)
    db_session.commit()

    login_res = client.get("/api/auth/github/login", follow_redirects=False)
    state = parse_qs(urlparse(login_res.headers["location"]).query)["state"][0]
    res = client.get("/api/auth/github/callback", params={"code": "abc", "state": state}, follow_redirects=False)
    assert res.status_code == 302

    db_session.expire_all()
    users = db_session.query(User).filter(User.github_id == GH_USER_ID).all()
    assert len(users) == 1
    assert users[0].username == "octocat"
    assert users[0].github_token == "gh-token-1"
    me = client.get("/api/auth/me").json()
    assert me["username"] == "octocat"


def test_token_stored_server_side_and_never_exposed(client, db_session, mock_github):
    login_res = client.get("/api/auth/github/login", follow_redirects=False)
    state = parse_qs(urlparse(login_res.headers["location"]).query)["state"][0]
    client.get("/api/auth/github/callback", params={"code": "abc", "state": state}, follow_redirects=False)
    me = client.get("/api/auth/me")
    assert "github_token" not in me.json()


def test_logout_clears_session(client, db_session, mock_github):
    login_res = client.get("/api/auth/github/login", follow_redirects=False)
    state = parse_qs(urlparse(login_res.headers["location"]).query)["state"][0]
    client.get("/api/auth/github/callback", params={"code": "abc", "state": state}, follow_redirects=False)
    assert client.get("/api/auth/me").status_code == 200

    res = client.post("/api/auth/logout")
    assert res.json() == {"ok": True}
    assert client.get("/api/auth/me").status_code == 401


def test_callback_with_bad_state_rejected(client, db_session, mock_github):
    client.get("/api/auth/github/login", follow_redirects=False)
    res = client.get("/api/auth/github/callback", params={"code": "abc", "state": "wrong"}, follow_redirects=False)
    assert res.status_code == 403
    assert "CSRF" in res.json()["detail"] or "state" in res.json()["detail"].lower()
    assert client.get("/api/auth/me").status_code == 401


def test_routes_documented_in_openapi():
    paths = app.openapi()["paths"]
    assert "/api/auth/github/login" in paths
    assert "/api/auth/github/callback" in paths
    assert "/api/auth/me" in paths
    assert "/api/auth/logout" in paths
