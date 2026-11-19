"""Database-level integrity constraints for critical lifecycle values.

These values were previously enforced only by the API schemas and a handful of
service functions. Seed/import scripts, admin operations and any future worker
also write these tables, so the database is the last line of defence:

  problems.status             published / pending_review / rejected / removed
  problems.goal               NULL / resume / hackathon / learning
  problems.est_hours          1..1000 (matches the request schema)
  projects.verification_status verified / needs_review / rejected
  projects.ownership_basis    NULL / owner / push_access / contributor

Compatibility is checked before any constraint is added. If existing rows
contain a value outside a list, the migration raises a clear error and changes
nothing; it never silently rewrites or deletes data. Take a backup first (see
DEPLOY.md).

Downgrade drops only the constraints added here.

Revision ID: 0017_integrity_constraints
Revises: 0016_remove_upcoming_fields
Create Date: 2026-11-20
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0017_integrity_constraints"
down_revision: str | None = "0016_remove_upcoming_fields"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

CHECKS: tuple[tuple[str, str, str], ...] = (
    (
        "problems",
        "ck_problems_status",
        "status IN ('published', 'pending_review', 'rejected', 'removed')",
    ),
    (
        "problems",
        "ck_problems_goal",
        "goal IS NULL OR goal IN ('resume', 'hackathon', 'learning')",
    ),
    (
        "problems",
        "ck_problems_est_hours",
        "est_hours >= 1 AND est_hours <= 1000",
    ),
    (
        "projects",
        "ck_projects_verification_status",
        "verification_status IN ('verified', 'needs_review', 'rejected')",
    ),
    (
        "projects",
        "ck_projects_ownership_basis",
        "ownership_basis IS NULL OR ownership_basis IN ('owner', 'push_access', 'contributor')",
    ),
)


def _table_exists(bind, table: str) -> bool:
    return sa.inspect(bind).has_table(table)


def _check_names(bind, table: str) -> set[str]:
    return {
        check["name"]
        for check in sa.inspect(bind).get_check_constraints(table)
        if check.get("name")
    }


def _preflight(bind) -> None:
    """Refuse to add constraints over incompatible rows, without changing them."""
    invalid: list[str] = []
    for table, name, expression in CHECKS:
        if not _table_exists(bind, table):
            continue
        count = bind.scalar(
            sa.text(f"SELECT COUNT(*) FROM {table} WHERE NOT ({expression})")
        )
        if count:
            invalid.append(f"{table}.{name}: {count} row(s) violate `{expression}`")
    if invalid:
        raise RuntimeError(
            "Cannot add integrity constraints; existing rows are incompatible. "
            "Inspect and correct them (or restore a backup) before retrying:\n"
            + "\n".join(invalid)
        )


def upgrade() -> None:
    bind = op.get_bind()
    _preflight(bind)

    for table in ("problems", "projects"):
        if not _table_exists(bind, table):
            continue
        existing = _check_names(bind, table)
        with op.batch_alter_table(table) as batch:
            for check_table, name, expression in CHECKS:
                if check_table == table and name not in existing:
                    batch.create_check_constraint(name, expression)


def downgrade() -> None:
    bind = op.get_bind()
    for table in ("projects", "problems"):
        if not _table_exists(bind, table):
            continue
        existing = _check_names(bind, table)
        with op.batch_alter_table(table) as batch:
            for check_table, name, _expression in CHECKS:
                if check_table == table and name in existing:
                    batch.drop_constraint(name, type_="check")
