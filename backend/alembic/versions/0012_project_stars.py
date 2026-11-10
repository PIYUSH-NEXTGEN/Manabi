"""Starred projects: `project_stars` join table.

Upgrade creates `project_stars`, one row per (project, user) pair:

  id, project_id (FK projects.id, CASCADE), user_id (FK users.id),
  created_at

with a unique constraint so a user can star a project at most once. Rows
are deleted with their project (ondelete=CASCADE); un-starring removes the
row. Nothing else changes, so old data is untouched.

Everything is defensive: an already-existing table is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade drops the table and the stars with it.

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0012_project_stars
Revises: 0011_problem_resume_kit
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_project_stars"
down_revision: str | None = "0011_problem_resume_kit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "project_stars"):
        op.create_table(
            "project_stars",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "project_id",
                sa.Integer(),
                sa.ForeignKey("projects.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column(
                "user_id",
                sa.Integer(),
                sa.ForeignKey("users.id"),
                nullable=False,
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.UniqueConstraint("project_id", "user_id", name="uq_project_star_project_user"),
        )
        op.create_index("ix_project_stars_project_id", "project_stars", ["project_id"])
        op.create_index("ix_project_stars_user_id", "project_stars", ["user_id"])


def downgrade() -> None:
    bind = op.get_bind()
    if _table_exists(bind, "project_stars"):
        op.drop_index("ix_project_stars_user_id", table_name="project_stars")
        op.drop_index("ix_project_stars_project_id", table_name="project_stars")
        op.drop_table("project_stars")
