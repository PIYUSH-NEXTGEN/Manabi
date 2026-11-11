"""Starred problem briefs: `problem_stars` join table.

Upgrade creates `problem_stars`, one row per (problem, user) pair:

  id, problem_id (FK problems.id, CASCADE), user_id (FK users.id),
  created_at

with a unique constraint so a user can star a problem at most once. Rows
are deleted with their problem (ondelete=CASCADE); un-starring removes the
row. Nothing else changes, so old data is untouched.

Everything is defensive: an already-existing table is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade drops the table and the stars with it.

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0013_problem_stars
Revises: 0012_project_stars
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013_problem_stars"
down_revision: str | None = "0012_project_stars"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problem_stars"):
        op.create_table(
            "problem_stars",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "problem_id",
                sa.Integer(),
                sa.ForeignKey("problems.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column(
                "user_id",
                sa.Integer(),
                sa.ForeignKey("users.id"),
                nullable=False,
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.UniqueConstraint("problem_id", "user_id", name="uq_problem_star_problem_user"),
        )
        op.create_index("ix_problem_stars_problem_id", "problem_stars", ["problem_id"])
        op.create_index("ix_problem_stars_user_id", "problem_stars", ["user_id"])


def downgrade() -> None:
    bind = op.get_bind()
    if _table_exists(bind, "problem_stars"):
        op.drop_index("ix_problem_stars_user_id", table_name="problem_stars")
        op.drop_index("ix_problem_stars_problem_id", table_name="problem_stars")
        op.drop_table("problem_stars")
