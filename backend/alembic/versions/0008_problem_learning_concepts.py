"""Learning-track extras: `learning_concepts` JSON list on problems.

Upgrade adds a non-null `learning_concepts` JSON column (default '[]') to
`problems`, so learning-track briefs can list the concepts a builder picks
up while finishing the brief. Other tracks keep it empty; the UI section
only renders when the list is non-empty.

Everything is defensive: a column that already exists is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade removes the column; curated concept lists are lost (they live
only in seed data).

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0008_problem_learning_concepts
Revises: 0007_field_catalog
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_problem_learning_concepts"
down_revision: str | None = "0007_field_catalog"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LEARNING_CONCEPTS_COLUMN = sa.Column(
    "learning_concepts", sa.JSON(), nullable=False, server_default="[]"
)


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "learning_concepts" not in _existing_columns(bind, "problems"):
        # batch mode rebuilds the table on SQLite; plain column on Postgres.
        with op.batch_alter_table("problems") as batch:
            batch.add_column(LEARNING_CONCEPTS_COLUMN)


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "learning_concepts" in _existing_columns(bind, "problems"):
        with op.batch_alter_table("problems") as batch:
            batch.drop_column("learning_concepts")
