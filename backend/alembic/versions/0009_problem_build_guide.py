"""Curated build guides: nullable `build_guide` JSON column on problems.

Upgrade adds a nullable `build_guide` JSON column to `problems`. Each entry
is a phase dict ({title, summary, steps}); rows without a guide keep NULL
and the UI falls back to a phase roadmap derived from `approaches`.

Everything is defensive: a column that already exists is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade removes the column; curated guides are lost (they live only in
seed data).

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0009_problem_build_guide
Revises: 0008_problem_learning_concepts
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_problem_build_guide"
down_revision: str | None = "0008_problem_learning_concepts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BUILD_GUIDE_COLUMN = sa.Column("build_guide", sa.JSON(), nullable=True)


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "build_guide" not in _existing_columns(bind, "problems"):
        # batch mode rebuilds the table on SQLite; plain column on Postgres.
        with op.batch_alter_table("problems") as batch:
            batch.add_column(BUILD_GUIDE_COLUMN)


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "build_guide" in _existing_columns(bind, "problems"):
        with op.batch_alter_table("problems") as batch:
            batch.drop_column("build_guide")
