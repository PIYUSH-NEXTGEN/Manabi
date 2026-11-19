from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.models import RateLimitHit
from app.services.ratelimit import RateLimiter, human_wait


def test_human_wait_speaks_in_minutes_under_an_hour():
    assert human_wait(2220) == "about 37 minutes"


def test_human_wait_says_one_minute():
    assert human_wait(60) == "about 1 minute"


def test_human_wait_switches_to_hours():
    assert human_wait(21600) == "about 6 hours"


def test_human_wait_switches_to_days():
    assert human_wait(86400) == "about 1 day"


def test_rate_limit_check_expires_stale_rows_for_other_keys():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    with Session(engine) as db:
        db.add_all(
            [
                RateLimitHit(
                    bucket="SUBMIT_RATE_LIMIT_PER_HOUR",
                    key="old-key",
                    created_at=now - timedelta(hours=2),
                ),
                RateLimitHit(
                    bucket="SUBMIT_RATE_LIMIT_PER_HOUR",
                    key="other-live-key",
                    created_at=now,
                ),
            ]
        )
        db.commit()

        limiter = RateLimiter("SUBMIT_RATE_LIMIT_PER_HOUR")
        assert limiter.check(db, "current-key") is None

        remaining = db.scalar(select(func.count()).select_from(RateLimitHit))
        # The expired row for a different key is gone; the live row and the
        # just-recorded hit remain.
        assert remaining == 2
    engine.dispose()
