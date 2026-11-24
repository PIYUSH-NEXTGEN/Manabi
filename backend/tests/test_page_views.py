from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import PageView


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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


def _record(client: TestClient, path: str):
    return client.post("/api/views", json={"path": path})


def test_first_view_creates_one_row(client, db_session: Session):
    res = _record(client, "/problems")
    assert res.status_code == 204

    rows = db_session.scalars(select(PageView)).all()
    assert len(rows) == 1
    assert rows[0].path == "/problems"
    assert rows[0].day == datetime.now(UTC).date()
    assert rows[0].count == 1


def test_repeat_view_increments_the_same_row(client, db_session: Session):
    _record(client, "/")
    _record(client, "/")
    _record(client, "/")

    rows = db_session.scalars(select(PageView)).all()
    assert len(rows) == 1
    assert rows[0].count == 3


def test_paths_are_counted_separately(client, db_session: Session):
    _record(client, "/")
    _record(client, "/problems")
    _record(client, "/problems")

    counts = {
        row.path: row.count for row in db_session.scalars(select(PageView)).all()
    }
    assert counts == {"/": 1, "/problems": 2}


def test_path_must_start_with_a_slash(client):
    assert client.post("/api/views", json={"path": "problems"}).status_code == 422
    assert client.post("/api/views", json={"path": ""}).status_code == 422


def test_no_public_read_endpoint(client):
    assert client.get("/api/views").status_code == 405
