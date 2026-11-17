"""Remove the data-science field and every project brief filed under it.

The field catalog is now six values: web-dev, app-dev, aiml, cyber-security,
devops-cloud, blockchain. This migration deletes data-science problem briefs
together with their stars and submitted projects (and those projects' stars
and reports), so the destructive step does not leave orphaned rows.

Historical migrations keep the seven-value catalog as the record of that
period. Downgrade is a no-op because deleted briefs and submissions cannot be
reconstructed.

Revision ID: 0015_remove_data_science_field
Revises: 0014_rate_limit_hits
Create Date: 2026-11-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0015_remove_data_science_field"
down_revision: str | None = "0014_rate_limit_hits"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DATA_SCIENCE_PROBLEMS = "SELECT id FROM problems WHERE field = 'data-science'"
_DATA_SCIENCE_PROJECTS = (
    f"SELECT id FROM projects WHERE problem_id IN ({_DATA_SCIENCE_PROBLEMS})"
)


def _table_exists(bind, table: str) -> bool:
    return sa.inspect(bind).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if _table_exists(bind, "project_stars"):
        bind.execute(
            sa.text(
                f"DELETE FROM project_stars WHERE project_id IN ({_DATA_SCIENCE_PROJECTS})"
            )
        )
    if _table_exists(bind, "project_reports"):
        bind.execute(
            sa.text(
                f"DELETE FROM project_reports WHERE project_id IN ({_DATA_SCIENCE_PROJECTS})"
            )
        )
    if _table_exists(bind, "projects"):
        bind.execute(
            sa.text(f"DELETE FROM projects WHERE problem_id IN ({_DATA_SCIENCE_PROBLEMS})")
        )
    if _table_exists(bind, "problem_stars"):
        bind.execute(
            sa.text(
                f"DELETE FROM problem_stars WHERE problem_id IN ({_DATA_SCIENCE_PROBLEMS})"
            )
        )
    bind.execute(sa.text("DELETE FROM problems WHERE field = 'data-science'"))

    if _table_exists(bind, "problem_drafts"):
        bind.execute(
            sa.text("DELETE FROM problem_drafts WHERE field = 'data-science'")
        )


def downgrade() -> None:
    # Removed briefs and projects are not recoverable.
    pass
