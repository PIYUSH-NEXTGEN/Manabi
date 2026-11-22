"""Anonymous live presence: `visitors` table.

Upgrade creates `visitors`, one row per anonymous browser id:

  visitor_id (primary key), first_seen, last_seen, user_id (nullable)

`last_seen` is indexed because the online counter filters on a moving window;
the row count is the all-time unique visitors. `user_id` links a visitor to an
account when they log in, and is set to NULL if that account is removed.

Downgrade drops the table and every recorded visitor with it.

Revision ID: 0020_visitors
Revises: 0019_foreign_key_indexes
Create Date: 2026-11-22
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0020_visitors"
down_revision: str | None = "0019_foreign_key_indexes"
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
    if not _table_exists(bind, "visitors"):
        op.create_table(
            "visitors",
            sa.Column("visitor_id", sa.String(length=64), primary_key=True),
            sa.Column("first_seen", sa.DateTime(), nullable=False),
            sa.Column("last_seen", sa.DateTime(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
                name="fk_visitors_user_id_users",
                ondelete="SET NULL",
            ),
        )
    if _table_exists(bind, "visitors") and not _index_exists(
        bind, "visitors", "ix_visitors_last_seen"
    ):
        op.create_index("ix_visitors_last_seen", "visitors", ["last_seen"])


def downgrade() -> None:
    bind = op.get_bind()
    if _table_exists(bind, "visitors"):
        if _index_exists(bind, "visitors", "ix_visitors_last_seen"):
            op.drop_index("ix_visitors_last_seen", table_name="visitors")
        op.drop_table("visitors")
