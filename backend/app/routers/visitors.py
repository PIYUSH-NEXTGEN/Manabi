"""Anonymous live-presence counters.

The browser mints a random id once and stores it in localStorage, then sends a
small heartbeat while the tab is visible. This module stores no IP, cookie or
account data: a row means "this browser has been seen", last_seen decides
whether it is online right now, and the row count is the all-time unique
visitors. Nothing here is exposed per visitor, only two aggregate numbers.
"""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Request
from sqlalchemy import func, select

from app import schemas
from app.config import get_settings
from app.deps import DB, OptionalUser
from app.models import Visitor
from app.services.ratelimit import RateLimiter, rate_limited

router = APIRouter(prefix="/api", tags=["presence"])

VISITOR_LIMITER = RateLimiter("PRESENCE_RATE_LIMIT_PER_HOUR")
IP_LIMITER = RateLimiter("PRESENCE_IP_RATE_LIMIT_PER_HOUR")


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _utcnow() -> datetime:
    """Naive UTC matches the DateTime columns on SQLite and Postgres."""
    return datetime.now(UTC).replace(tzinfo=None)


def _upsert_visitor(
    db, visitor_id: str, now: datetime, user_id: int | None
) -> None:
    values = {
        "visitor_id": visitor_id,
        "first_seen": now,
        "last_seen": now,
        "user_id": user_id,
    }
    updates: dict[str, object] = {"last_seen": now}
    if user_id is not None:
        # A visitor who later logs in keeps their anonymous first_seen but is
        # linked to the account for aggregate reporting.
        updates["user_id"] = user_id

    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    elif dialect == "sqlite":
        from sqlalchemy.dialects.sqlite import insert
    else:
        # Unknown dialect: keep a portable read-then-write fallback.
        existing = db.get(Visitor, visitor_id)
        if existing is None:
            db.add(Visitor(**values))
        else:
            existing.last_seen = now
            if user_id is not None:
                existing.user_id = user_id
        return

    stmt = insert(Visitor).values(**values)
    db.execute(
        stmt.on_conflict_do_update(
            index_elements=[Visitor.visitor_id], set_=updates
        )
    )


@router.post("/visitors/heartbeat", response_model=schemas.PresenceOut)
def heartbeat(
    body: schemas.HeartbeatIn, request: Request, db: DB, user: OptionalUser
) -> schemas.PresenceOut:
    retry = VISITOR_LIMITER.check(
        db, f"presence-visitor:{body.visitor_id}"
    )
    if retry is None:
        retry = IP_LIMITER.check(db, f"presence-ip:{_client_ip(request)}")
    if retry is not None:
        raise rate_limited(
            retry, "Too many presence updates. Try again shortly."
        )

    now = _utcnow()
    _upsert_visitor(db, body.visitor_id, now, user.id if user else None)
    db.commit()

    window = max(1, int(get_settings().PRESENCE_ONLINE_WINDOW_SECONDS))
    cutoff = now - timedelta(seconds=window)
    online = db.scalar(
        select(func.count())
        .select_from(Visitor)
        .where(Visitor.last_seen >= cutoff)
    ) or 0
    total = db.scalar(select(func.count()).select_from(Visitor)) or 0
    return schemas.PresenceOut(online=online, total=total)
