"""Anonymous live-presence counters.

Identity is derived on the server from a salted hash of the request: client IP,
OS family, primary language and three coarse device hints the browser sends
(screen size, CPU cores, timezone). Nothing in that hash is stored raw, no
cookie is set, and clearing browser storage cannot create a new visitor —
which is the whole point, since a localStorage id did exactly that.

A row means "this device has been seen", `last_seen` decides whether it is
online right now, and the row count is the all-time total. Rows written before
device keys existed have `device_key = NULL` and count one each, so the total
never resets when the identity scheme changes. A browser that still sends its
old localStorage id has that row adopted rather than duplicated.

Nothing here is exposed per visitor, only two aggregate numbers.
"""

import hashlib
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Request
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app import schemas
from app.config import get_settings
from app.deps import DB, OptionalUser
from app.models import Visitor
from app.services.ratelimit import RateLimiter, rate_limited

router = APIRouter(prefix="/api", tags=["presence"])

VISITOR_LIMITER = RateLimiter("PRESENCE_RATE_LIMIT_PER_HOUR")
IP_LIMITER = RateLimiter("PRESENCE_IP_RATE_LIMIT_PER_HOUR")

# Version-free OS families: a browser update must not invent a new visitor.
_OS_HINTS = (
    ("android", "android"),
    ("iphone", "ios"),
    ("ipad", "ios"),
    ("ipod", "ios"),
    ("windows", "windows"),
    ("cros", "chromeos"),
    ("macintosh", "macos"),
    ("mac os x", "macos"),
    ("linux", "linux"),
)


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _utcnow() -> datetime:
    """Naive UTC matches the DateTime columns on SQLite and Postgres."""
    return datetime.now(UTC).replace(tzinfo=None)


def _os_family(user_agent: str) -> str:
    lowered = user_agent.lower()
    for hint, family in _OS_HINTS:
        if hint in lowered:
            return family
    return "other"


def _device_key(request: Request, body: schemas.HeartbeatIn) -> str:
    """Stable per-device key: salted hash, truncated to fit the column.

    The salt is what stops the hash from being reversible by enumerating the
    IPv4 space, so it must never reach the browser.
    """
    settings = get_settings()
    salt = settings.PRESENCE_HASH_SALT or settings.SESSION_SECRET
    language = request.headers.get("accept-language", "").split(",")[0]
    parts = (
        salt,
        _client_ip(request),
        _os_family(request.headers.get("user-agent", "")),
        language.strip().lower(),
        body.screen or "",
        str(body.cores if body.cores is not None else ""),
        (body.timezone or "").lower(),
    )
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:40]


def _find_device(db, device_key: str) -> Visitor | None:
    return db.scalar(select(Visitor).where(Visitor.device_key == device_key))


def _touch_visitor(
    db, device_key: str, legacy_id: str, now: datetime, user_id: int | None
) -> None:
    """Record one heartbeat, adopting a pre-existing browser-id row if any.

    Adoption keeps `first_seen` and the row's original primary key, so a
    visitor who was already counted is never added twice.
    """
    row = _find_device(db, device_key)
    if row is None:
        legacy = db.get(Visitor, legacy_id)
        if legacy is not None and legacy.device_key is None:
            legacy.device_key = device_key
            row = legacy
    if row is None:
        db.add(
            Visitor(
                visitor_id=device_key,
                device_key=device_key,
                first_seen=now,
                last_seen=now,
                user_id=user_id,
            )
        )
        return
    row.last_seen = now
    if user_id is not None:
        # A visitor who later logs in keeps their anonymous first_seen but is
        # linked to the account for aggregate reporting.
        row.user_id = user_id


def _totals(db, now: datetime) -> schemas.PresenceOut:
    window = max(1, int(get_settings().PRESENCE_ONLINE_WINDOW_SECONDS))
    cutoff = now - timedelta(seconds=window)
    online = db.scalar(
        select(func.count())
        .select_from(Visitor)
        .where(Visitor.last_seen >= cutoff)
    ) or 0
    total = db.scalar(select(func.count()).select_from(Visitor)) or 0
    return schemas.PresenceOut(online=online, total=total)


@router.post("/visitors/heartbeat", response_model=schemas.PresenceOut)
def heartbeat(
    body: schemas.HeartbeatIn, request: Request, db: DB, user: OptionalUser
) -> schemas.PresenceOut:
    device_key = _device_key(request, body)
    retry = VISITOR_LIMITER.check(db, f"presence-visitor:{device_key}")
    if retry is None:
        retry = IP_LIMITER.check(db, f"presence-ip:{_client_ip(request)}")
    if retry is not None:
        raise rate_limited(
            retry, "Too many presence updates. Try again shortly."
        )

    now = _utcnow()
    user_id = user.id if user else None
    try:
        _touch_visitor(db, device_key, body.visitor_id, now, user_id)
        db.commit()
    except IntegrityError:
        # Two heartbeats for a new device raced; the other one inserted the
        # row, so this one only refreshes it.
        db.rollback()
        row = _find_device(db, device_key)
        if row is not None:
            row.last_seen = now
            if user_id is not None:
                row.user_id = user_id
            db.commit()

    return _totals(db, now)
