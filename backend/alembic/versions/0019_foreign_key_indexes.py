"""Add covering indexes for foreign keys Postgres does not index for us.

Postgres creates an index for primary keys and unique constraints, never for a
plain foreign key column. Without one, every lookup that filters on the column
is a sequential scan, and every DELETE on the parent table scans the child to
verify nothing still references the row it is removing.

The Supabase performance advisor reports these three as INFO:

  projects.user_id             "projects submitted by this user"
  project_reports.reporter_user_id   reports filed by a user
  problems.created_by          admin-authored problems

All three are additive: no table rewrite, no long lock (the tables are small
today), and no change to any constraint. The model columns carry index=True so
a create_all environment (local SQLite) produces the same schema.

Revision ID: 0019_foreign_key_indexes
Revises: 0018_public_schema_lockdown
Create Date: 2026-11-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0019_foreign_key_indexes"
down_revision: str | None = "0018_public_schema_lockdown"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

INDEXES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("ix_projects_user_id", "projects", ("user_id",)),
    ("ix_project_reports_reporter_user_id", "project_reports", ("reporter_user_id",)),
    ("ix_problems_created_by", "problems", ("created_by",)),
)


def _existing(bind, table: str) -> set[str]:
    return {index["name"] for index in sa.inspect(bind).get_indexes(table)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for name, table, columns in INDEXES:
        if not inspector.has_table(table):
            continue
        if name in _existing(bind, table):
            continue
        op.create_index(name, table, list(columns))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for name, table, _columns in INDEXES:
        if not inspector.has_table(table):
            continue
        if name in _existing(bind, table):
            op.drop_index(name, table_name=table)
