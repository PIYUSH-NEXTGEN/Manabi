"""Aggregate page-view counters.

Every recorded view increments one row per (UTC day, path). Rows carry no IP,
cookie, visitor id or account data, and no endpoint reads this table: the
numbers are kept in the database (and so in Supabase) for the owner to query,
never rendered in the app.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Request, Response, status
from sqlalchemy import select

from app import schemas
from app.models import PageView
from app.deps import DB
from app.services.ratelimit import RateLimiter, rate_limited

router = APIRouter(prefix="/api", tags=["views"])

VIEW_IP_LIMITER = RateLimiter("VIEWS_IP_RATE_LIMIT_PER_HOUR")


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _utcnow() -> datetime:
    """Naive UTC matches the DateTime columns on SQLite and Postgres."""
    return datetime.now(UTC).replace(tzinfo=None)


def _increment(db, day, path: str) -> None:
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    elif dialect == "sqlite":
        from sqlalchemy.dialects.sqlite import insert
    else:
        # Unknown dialect: keep a portable read-then-write fallback.
        row = db.scalar(
            select(PageView).where(PageView.day == day, PageView.path == path)
        )
        if row is None:
            db.add(PageView(day=day, path=path, count=1))
        else:
            row.count += 1
        return

    stmt = insert(PageView).values(day=day, path=path, count=1)
    db.execute(
        stmt.on_conflict_do_update(
            index_elements=[PageView.day, PageView.path],
            set_={"count": PageView.count + 1},
        )
    )


@router.post("/views", status_code=status.HTTP_204_NO_CONTENT)
def record_view(
    body: schemas.PageViewIn, request: Request, db: DB
) -> Response:
    retry = VIEW_IP_LIMITER.check(db, f"views-ip:{_client_ip(request)}")
    if retry is not None:
        raise rate_limited(retry, "Too many page views. Try again shortly.")

    _increment(db, _utcnow().date(), body.path)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
