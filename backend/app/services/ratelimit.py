from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import RateLimitHit


class RateLimiter:
    """Sliding-window limiter backed by the rate_limit_hits table.

    Every hit is one row, keyed by (bucket, key). Counting happens against
    the DB, so limits survive restarts and hold exactly under multi-worker
    deploys (all workers count the same table).

    check() is the single entry point: it returns None when the request is
    allowed (and records one row), or the number of seconds until a slot
    opens when it is blocked (rejected requests are not recorded, so a
    blocked user never extends their own wait).
    """

    def __init__(self, limit_setting: str, window_seconds: int = 3600):
        self._limit_setting = limit_setting
        self._window = window_seconds

    @property
    def bucket(self) -> str:
        return self._limit_setting

    def _limit(self) -> int:
        value = getattr(get_settings(), self._limit_setting)
        return max(1, int(value))

    def check(self, db: Session, key: str) -> int | None:
        """None when allowed (hit recorded); seconds until retry when blocked."""
        # SQLite stores naive UTC datetimes, so everything here is naive UTC.
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        cutoff = now - timedelta(seconds=self._window)
        bucket_filter = RateLimitHit.bucket == self._limit_setting
        key_filter = RateLimitHit.key == key
        in_window = RateLimitHit.created_at >= cutoff

        # Opportunistic cleanup: expired rows for this key leave with it,
        # so the table never grows without bound.
        db.execute(
            delete(RateLimitHit).where(
                bucket_filter, key_filter, RateLimitHit.created_at < cutoff
            )
        )
        used = db.scalar(
            select(func.count(RateLimitHit.id)).where(
                bucket_filter, key_filter, in_window
            )
        ) or 0
        if used >= self._limit():
            oldest = db.scalar(
                select(func.min(RateLimitHit.created_at)).where(
                    bucket_filter, key_filter, in_window
                )
            )
            retry = self._window if oldest is None else int(
                (oldest + timedelta(seconds=self._window) - now).total_seconds()
            )
            db.commit()
            return max(1, retry)
        db.add(RateLimitHit(bucket=self._limit_setting, key=key, created_at=now))
        db.commit()
        return None

    def reset(self, db: Session) -> None:
        """Test helper: drop every recorded hit for this limiter's bucket."""
        db.execute(delete(RateLimitHit).where(RateLimitHit.bucket == self._limit_setting))
        db.commit()


CHAT_DAILY_LIMITER = RateLimiter("CHAT_RATE_LIMIT_PER_DAY", window_seconds=86400)


def rate_limited(retry_after: int, message: str) -> HTTPException:
    """The one 429 the API returns: a code clients can branch on plus a
    Retry-After header so the UI can show a live countdown."""
    return HTTPException(
        status_code=429,
        detail={"code": "rate_limited", "message": message},
        headers={"Retry-After": str(retry_after)},
    )


def human_wait(seconds: int) -> str:
    """A readable wait time for 429 messages: 'about 37 minutes', 'about 6 hours'."""
    minutes = max(1, round(seconds / 60))
    if minutes < 60:
        return f"about {minutes} minute{'s' if minutes != 1 else ''}"
    hours = round(minutes / 60)
    if hours < 24:
        return f"about {hours} hour{'s' if hours != 1 else ''}"
    days = round(hours / 24)
    return f"about {days} day{'s' if days != 1 else ''}"


# Sanity cap for admins, who are exempt from the per-user limits elsewhere.
# High enough that real admin work never feels it; low enough that a
# runaway or hijacked admin session stops before it drains the shared
# GitHub API quota unnoticed.
ADMIN_LIMITER = RateLimiter("ADMIN_RATE_LIMIT_PER_HOUR")
