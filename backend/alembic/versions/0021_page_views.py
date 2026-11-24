"""Aggregate page views: `page_views` table.

Upgrade creates `page_views`, one row per route path per UTC day:

  id (primary key), day, path, count

A unique constraint on (day, path) lets the API increment `count` with an
upsert; `day` is indexed for "views per day" queries. Rows carry no visitor
identifier, IP, or account data. Nothing reads this table through the API: it
exists so total view counts stay in the database (and therefore Supabase).

Revision ID: 0021_page_views
Revises: 0020_visitors
Create Date: 2026-11-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0021_page_views"
down_revision: str | None = "0020_visitors"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def _index_exists(conn, table: str, name: str) -> bool:
    return name in {
        index["name"] for index in sa.inspect(conn).get_indexes(table)
    }


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "page_views"):
        op.create_table(
            "page_views",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("day", sa.Date(), nullable=False),
            sa.Column("path", sa.String(length=255), nullable=False),
            sa.Column("count", sa.Integer(), nullable=False, server_default=sa.text("0")),
            sa.UniqueConstraint("day", "path", name="uq_page_views_day_path"),
        )
    if _table_exists(bind, "page_views") and not _index_exists(
        bind, "page_views", "ix_page_views_day"
    ):
        op.create_index("ix_page_views_day", "page_views", ["day"])

    # The lockdown migration revoked default privileges, but enabling RLS here
    # keeps a table created later consistent with the rest of the schema.
    if bind.dialect.name == "postgresql":
        bind.execute(sa.text('ALTER TABLE public."page_views" ENABLE ROW LEVEL SECURITY'))


def downgrade() -> None:
    bind = op.get_bind()
    if _table_exists(bind, "page_views"):
        if _index_exists(bind, "page_views", "ix_page_views_day"):
            op.drop_index("ix_page_views_day", table_name="page_views")
        op.drop_table("page_views")
