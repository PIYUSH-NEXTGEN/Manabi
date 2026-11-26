"""Readable presence times: `visitors_ist` view.

`visitors.first_seen` / `last_seen` stay stored in UTC, because the online
window compares them against `datetime.now(UTC)` and the all-time/online counts
would silently break if the stored values moved to a local clock. This revision
only adds a read-only view that converts them for people reading the table:

  visitor_id, device_key, first_seen_ist, last_seen_ist, user_id

IST is UTC+05:30 with no daylight saving, so the conversion is a fixed offset
(an interval on Postgres, `datetime(..., '+330 minutes')` on SQLite).

Downgrade drops the view; the table and its UTC values are untouched.

Revision ID: 0023_visitors_ist
Revises: 0022_presence_device_key
Create Date: 2026-11-26
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0023_visitors_ist"
down_revision: str | None = "0022_presence_device_key"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

VIEW = "visitors_ist"


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "visitors"):
        return
    if bind.dialect.name == "postgresql":
        first_seen = "(first_seen AT TIME ZONE 'UTC') AT TIME ZONE 'Asia/Kolkata'"
        last_seen = "(last_seen AT TIME ZONE 'UTC') AT TIME ZONE 'Asia/Kolkata'"
        create = f"CREATE OR REPLACE VIEW {VIEW} AS"
    else:
        first_seen = "datetime(first_seen, '+330 minutes')"
        last_seen = "datetime(last_seen, '+330 minutes')"
        # SQLite has no CREATE OR REPLACE VIEW, so recreate it instead.
        op.execute(f"DROP VIEW IF EXISTS {VIEW}")
        create = f"CREATE VIEW {VIEW} AS"
    op.execute(
        f"""
        {create}
        SELECT visitor_id,
               device_key,
               {first_seen} AS first_seen_ist,
               {last_seen} AS last_seen_ist,
               user_id
        FROM visitors
        """
    )


def downgrade() -> None:
    op.execute(f"DROP VIEW IF EXISTS {VIEW}")
