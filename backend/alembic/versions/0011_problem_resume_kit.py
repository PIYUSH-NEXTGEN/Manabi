"""Resume-track extras: nullable `resume_kit` JSON column on problems.

Upgrade adds a nullable `resume_kit` JSON column to `problems`:
{
  scope_levels: [{level, text, checks}],
  target_roles: [{role, how_it_helps}],
  resume_bullets: [{bullet, example}],
  interview_points: [{question, answer}],
  differentiators: [str],
}

Rows without it keep NULL; the UI only renders the sections when the data
exists, so non-resume rows are unaffected.

Everything is defensive: a column that already exists is skipped, so the
migration also succeeds on partially migrated databases.

Downgrade removes the column; curated content is lost (it lives only in
seed data).

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0011_problem_resume_kit
Revises: 0010_hackathon_pitch_kit
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_problem_resume_kit"
down_revision: str | None = "0010_hackathon_pitch_kit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

RESUME_KIT_COLUMN = sa.Column("resume_kit", sa.JSON(), nullable=True)


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "resume_kit" not in _existing_columns(bind, "problems"):
        # batch mode rebuilds the table on SQLite; plain column on Postgres.
        with op.batch_alter_table("problems") as batch:
            batch.add_column(RESUME_KIT_COLUMN)


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if "resume_kit" in _existing_columns(bind, "problems"):
        with op.batch_alter_table("problems") as batch:
            batch.drop_column("resume_kit")
