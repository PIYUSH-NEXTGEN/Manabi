"""Remove briefs for fields that are now marked coming soon in the UI.

The live catalog is web-dev and aiml. App-dev, cyber-security, devops-cloud,
and blockchain briefs are deleted together with their stars and submitted
projects (and those projects' stars and reports), so no orphaned rows remain.

The UI keeps those four names as disabled "coming soon" filter options; they
are deliberately absent from the API enum until packs are added again.

Historical migrations keep the earlier field catalogs as the record of that
period. Downgrade is a no-op because deleted briefs and submissions cannot be
reconstructed.

Revision ID: 0016_remove_upcoming_fields
Revises: 0015_remove_data_science_field
Create Date: 2026-11-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0016_remove_upcoming_fields"
down_revision: str | None = "0015_remove_data_science_field"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_REMOVED_FIELDS = "'app-dev', 'cyber-security', 'devops-cloud', 'blockchain'"
_REMOVED_PROBLEMS = f"SELECT id FROM problems WHERE field IN ({_REMOVED_FIELDS})"
_REMOVED_PROJECTS = f"SELECT id FROM projects WHERE problem_id IN ({_REMOVED_PROBLEMS})"


def _table_exists(bind, table: str) -> bool:
    return sa.inspect(bind).has_table(table)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, "problems"):
        return

    if _table_exists(bind, "project_stars"):
        bind.execute(
            sa.text(
                f"DELETE FROM project_stars WHERE project_id IN ({_REMOVED_PROJECTS})"
            )
        )
    if _table_exists(bind, "project_reports"):
        bind.execute(
            sa.text(
                f"DELETE FROM project_reports WHERE project_id IN ({_REMOVED_PROJECTS})"
            )
        )
    if _table_exists(bind, "projects"):
        bind.execute(
            sa.text(f"DELETE FROM projects WHERE problem_id IN ({_REMOVED_PROBLEMS})")
        )
    if _table_exists(bind, "problem_stars"):
        bind.execute(
            sa.text(
                f"DELETE FROM problem_stars WHERE problem_id IN ({_REMOVED_PROBLEMS})"
            )
        )
    bind.execute(
        sa.text(f"DELETE FROM problems WHERE field IN ({_REMOVED_FIELDS})")
    )

    if _table_exists(bind, "problem_drafts"):
        bind.execute(
            sa.text(f"DELETE FROM problem_drafts WHERE field IN ({_REMOVED_FIELDS})")
        )


def downgrade() -> None:
    # Removed briefs and projects are not recoverable.
    pass
