"""Hackathon pitch kit: nullable `team_plan` and `pitch_guide` JSON columns.

Upgrade adds two nullable JSON columns to `problems`:
- `team_plan`: {note, roles: [{role, covers}], milestones: [str]}
- `pitch_guide`: {one_liner, beats: [{heading, text}],
                  questions: [{question, answer}]}

Rows without them keep NULL; the UI only renders these sections when the
data exists, so non-hackathon rows are unaffected.

Everything is defensive: columns that already exist are skipped, so the
migration also succeeds on partially migrated databases.

Downgrade removes the columns; curated content is lost (it lives only in
seed data).

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0010_hackathon_pitch_kit
Revises: 0009_problem_build_guide
Create Date: 2026-11-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_hackathon_pitch_kit"
down_revision: str | None = "0009_problem_build_guide"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

COLUMNS = [
    sa.Column("team_plan", sa.JSON(), nullable=True),
    sa.Column("pitch_guide", sa.JSON(), nullable=True),
]


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    existing = _existing_columns(bind, "problems")
    missing = [column for column in COLUMNS if column.name not in existing]
    if not missing:
        return
    # batch mode rebuilds the table on SQLite; plain columns on Postgres.
    with op.batch_alter_table("problems") as batch:
        for column in missing:
            batch.add_column(column)


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    existing = _existing_columns(bind, "problems")
    present = [column for column in COLUMNS if column.name in existing]
    if not present:
        return
    with op.batch_alter_table("problems") as batch:
        for column in present:
            batch.drop_column(column.name)
