from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Visitor
from app.routers.visitors import _utcnow

WINDOWS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15"

HINTS = {"screen": "1920x1080", "cores": 8, "timezone": "Asia/Kolkata"}


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


def _heartbeat(
    client: TestClient,
    visitor_id: str,
    *,
    user_agent: str = WINDOWS,
    language: str = "en-US",
    hints: dict | None = HINTS,
):
    return client.post(
        "/api/visitors/heartbeat",
        json={"visitor_id": visitor_id, **(hints if hints is not None else {})},
        headers={"user-agent": user_agent, "accept-language": language},
    )


def test_first_heartbeat_counts_one_online_and_one_total(client, db_session: Session):
    res = _heartbeat(client, "visitor-aaaaaaaa")
    assert res.status_code == 200
    assert res.json() == {"online": 1, "total": 1}

    row = db_session.scalars(
        select(Visitor).where(Visitor.device_key.is_not(None))
    ).first()
    assert row is not None
    assert row.first_seen == row.last_seen
    assert row.device_key is not None
    # The browser id is not the identity any more; the device key is.
    assert row.visitor_id == row.device_key


def test_clearing_storage_does_not_create_a_new_visitor(client):
    """The point of the device key: a new browser id from the same device."""
    assert _heartbeat(client, "visitor-aaaaaaaa").json() == {
        "online": 1,
        "total": 1,
    }
    assert _heartbeat(client, "visitor-bbbbbbbb").json() == {
        "online": 1,
        "total": 1,
    }


def test_repeat_heartbeat_updates_last_seen_without_new_row(client, db_session: Session):
    _heartbeat(client, "visitor-cccccccc")
    row = db_session.scalars(
        select(Visitor).where(Visitor.device_key.is_not(None))
    ).first()
    assert row is not None
    original_first_seen = row.first_seen

    assert _heartbeat(client, "visitor-cccccccc").json() == {
        "online": 1,
        "total": 1,
    }

    db_session.expire_all()
    refreshed = db_session.scalars(
        select(Visitor).where(Visitor.device_key.is_not(None))
    ).first()
    assert refreshed is not None
    assert refreshed.first_seen == original_first_seen
    assert refreshed.last_seen >= original_first_seen


def test_different_devices_are_counted_separately(client):
    assert _heartbeat(client, "visitor-dddddddd").json() == {
        "online": 1,
        "total": 1,
    }
    other = _heartbeat(
        client,
        "visitor-eeeeeeee",
        user_agent=MAC,
        hints={"screen": "2560x1440", "cores": 10, "timezone": "Europe/Paris"},
    )
    assert other.json() == {"online": 2, "total": 2}


def test_legacy_row_is_adopted_instead_of_duplicated(client, db_session: Session):
    legacy = Visitor(
        visitor_id="visitor-legacy01",
        first_seen=_utcnow() - timedelta(days=3),
        last_seen=_utcnow() - timedelta(days=3),
    )
    db_session.add(legacy)
    db_session.commit()

    assert _heartbeat(client, "visitor-legacy01").json() == {
        "online": 1,
        "total": 1,
    }

    db_session.expire_all()
    row = db_session.get(Visitor, "visitor-legacy01")
    assert row is not None
    assert row.device_key is not None
    # Adopting keeps the original row (and its first_seen) instead of adding.
    assert row.first_seen <= _utcnow() - timedelta(days=2)

    # Later heartbeats with no browser id at all still land on that row.
    assert _heartbeat(client, "visitor-ffffffff").json() == {
        "online": 1,
        "total": 1,
    }


def test_stale_visitor_stays_in_total_but_not_online(client, db_session: Session):
    stale = Visitor(
        visitor_id="visitor-gggggggg",
        first_seen=_utcnow() - timedelta(hours=2),
        last_seen=_utcnow() - timedelta(hours=2),
    )
    db_session.add(stale)
    db_session.commit()

    res = _heartbeat(client, "visitor-hhhhhhhh")
    assert res.status_code == 200
    assert res.json() == {"online": 1, "total": 2}


def test_invalid_visitor_id_is_rejected(client):
    assert _heartbeat(client, "short").status_code == 422
    assert _heartbeat(client, "bad id with spaces").status_code == 422


def test_invalid_device_hints_are_rejected(client):
    bad_screen = _heartbeat(
        client, "visitor-iiiiiiii", hints={"screen": "wide", "cores": 8}
    )
    assert bad_screen.status_code == 422
    too_many_cores = _heartbeat(
        client, "visitor-jjjjjjjj", hints={"screen": "1920x1080", "cores": 9999}
    )
    assert too_many_cores.status_code == 422
