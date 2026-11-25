"""Device-level presence: `visitors.device_key`.

Upgrade adds one nullable column to the existing table instead of creating a
new one:

  device_key (nullable, unique when set)

Rows written before this revision keep `device_key = NULL` and still count as
one visitor each, so the all-time total does not move. New heartbeats are
keyed by a salted hash of the request (IP, OS family, language, and coarse
device hints) and adopt an existing browser-id row when the browser still
sends its old id, so a returning visitor is not counted twice.

Downgrade drops the column; rows created under device keys stay and continue
to count like any other visitor id.

Revision ID: 0022_presence_device_key
Revises: 0021_page_views
Create Date: 2026-11-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0022_presence_device_key"
down_revision: str | None = "0021_page_views"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def _column_exists(conn, table: str, column: str) -> bool:
    return column in {
        item["name"] for item in sa.inspect(conn).get_columns(table)
    }


def _index_exists(conn, table: str, name: str) -> bool:
    return name in {
        index["name"] for index in sa.inspect(conn).get_indexes(table)
    }


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "visitors"):
        return
    if not _column_exists(bind, "visitors", "device_key"):
        op.add_column(
            "visitors", sa.Column("device_key", sa.String(length=64), nullable=True)
        )
    # NULLs are ignored by a unique index on both SQLite and Postgres, so the
    # legacy rows can stay NULL without tripping the constraint.
    if not _index_exists(bind, "visitors", "ix_visitors_device_key"):
        op.create_index(
            "ix_visitors_device_key", "visitors", ["device_key"], unique=True
        )


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "visitors"):
        return
    if _index_exists(bind, "visitors", "ix_visitors_device_key"):
        op.drop_index("ix_visitors_device_key", table_name="visitors")
    if _column_exists(bind, "visitors", "device_key"):
        op.drop_column("visitors", "device_key")
