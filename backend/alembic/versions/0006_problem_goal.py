"""Problem track labels: optional manual `goal` column on problems.

Upgrade adds a nullable `goal` (resume | hackathon | learning | NULL) to
`problems`, so admins can curate the board's "Browse by track" filters. NULL
means unlabelled: the row simply never appears under a track filter.

Everything is defensive: a column that already exists is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade removes the column; curated labels are lost (they live only here).

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0006_problem_goal
Revises: 0005_project_verification
Create Date: 2026-11-09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_problem_goal"
down_revision: str | None = "0005_project_verification"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

GOAL_COLUMN = sa.Column("goal", sa.String(length=20), nullable=True)


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "goal" not in _existing_columns(bind, "problems"):
        # batch mode rebuilds the table on SQLite; plain column on Postgres.
        with op.batch_alter_table("problems") as batch:
            batch.add_column(GOAL_COLUMN)


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "goal" in _existing_columns(bind, "problems"):
        with op.batch_alter_table("problems") as batch:
            batch.drop_column("goal")
