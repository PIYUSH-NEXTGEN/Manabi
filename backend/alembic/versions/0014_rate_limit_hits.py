"""DB-backed rate limiting: `rate_limit_hits` table.

Upgrade creates `rate_limit_hits`, one row per recorded rate-limit hit:

  id, bucket (which limiter), key (user id / IP), created_at

with an index on (bucket, key, created_at) for the sliding-window count.
The in-memory limiter is replaced by counting these rows, so limits
survive restarts and hold exactly under multi-worker deploys. Rows older
than a limiter's window are deleted opportunistically by check(), so the
table stays small without a background sweeper.

Everything is defensive: an already-existing table is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade drops the table and every recorded hit with it.

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0014_rate_limit_hits
Revises: 0013_problem_stars
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_rate_limit_hits"
down_revision: str | None = "0013_problem_stars"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "rate_limit_hits"):
        op.create_table(
            "rate_limit_hits",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("bucket", sa.String(length=64), nullable=False),
            sa.Column("key", sa.String(length=191), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
        )
        op.create_index(
            "ix_rate_limit_hits_bucket_key_created",
            "rate_limit_hits",
            ["bucket", "key", "created_at"],
        )


def downgrade() -> None:
    bind = op.get_bind()
    if _table_exists(bind, "rate_limit_hits"):
        op.drop_index(
            "ix_rate_limit_hits_bucket_key_created", table_name="rate_limit_hits"
        )
        op.drop_table("rate_limit_hits")
