from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Visitor
from app.routers.visitors import _utcnow


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


def _heartbeat(client: TestClient, visitor_id: str):
    return client.post("/api/visitors/heartbeat", json={"visitor_id": visitor_id})


def test_first_heartbeat_counts_one_online_and_one_total(client, db_session: Session):
    res = _heartbeat(client, "visitor-aaaaaaaa")
    assert res.status_code == 200
    assert res.json() == {"online": 1, "total": 1}

    row = db_session.get(Visitor, "visitor-aaaaaaaa")
    assert row is not None
    assert row.first_seen == row.last_seen


def test_repeat_heartbeat_updates_last_seen_without_new_row(client, db_session: Session):
    _heartbeat(client, "visitor-bbbbbbbb")
    first = db_session.get(Visitor, "visitor-bbbbbbbb")
    assert first is not None
    original_first_seen = first.first_seen

    res = _heartbeat(client, "visitor-bbbbbbbb")
    assert res.status_code == 200
    assert res.json() == {"online": 1, "total": 1}

    db_session.expire_all()
    row = db_session.get(Visitor, "visitor-bbbbbbbb")
    assert row is not None
    assert row.first_seen == original_first_seen
    assert row.last_seen >= original_first_seen


def test_multiple_visitors_are_counted_separately(client):
    assert _heartbeat(client, "visitor-cccccccc").json() == {"online": 1, "total": 1}
    assert _heartbeat(client, "visitor-dddddddd").json() == {"online": 2, "total": 2}


def test_stale_visitor_stays_in_total_but_not_online(client, db_session: Session):
    stale = Visitor(
        visitor_id="visitor-eeeeeeee",
        first_seen=_utcnow() - timedelta(hours=2),
        last_seen=_utcnow() - timedelta(hours=2),
    )
    db_session.add(stale)
    db_session.commit()

    res = _heartbeat(client, "visitor-ffffffff")
    assert res.status_code == 200
    assert res.json() == {"online": 1, "total": 2}


def test_invalid_visitor_id_is_rejected(client):
    assert _heartbeat(client, "short").status_code == 422
    assert _heartbeat(client, "bad id with spaces").status_code == 422
