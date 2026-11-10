"""Normalise problem fields to the seven-tier catalog.

MANABI's field taxonomy collapses to exactly seven values: web-dev, app-dev,
aiml, data-science, cyber-security, devops-cloud, blockchain. Existing rows
written under the old 16-value taxonomy are remapped to the closest tier:

  web-fullstack, developer-tools, other   -> web-dev
  mobile, iot-embedded                    -> app-dev
  ml, computer-vision, nlp-llm, optimization -> aiml
  data-engineering, geospatial            -> data-science
  cybersecurity                           -> cyber-security
  distributed-systems                     -> devops-cloud

Any value not listed already matches the new catalog and is left untouched.
Rows whose field is still outside the seven-value catalog afterwards (free
strings written directly into the DB, e.g. "biology" or "education") are
removed entirely: they do not belong to any part of the field taxonomy.
Applied to both `problems` and `problem_drafts`.

Downgrade is a no-op: the original distinctions are not recoverable.

Revision ID: 0007_field_catalog
Revises: 0006_problem_goal
Create Date: 2026-11-10
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0007_field_catalog"
down_revision: str | None = "0006_problem_goal"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REMAP = {
    "web-fullstack": "web-dev",
    "developer-tools": "web-dev",
    "other": "web-dev",
    "mobile": "app-dev",
    "iot-embedded": "app-dev",
    "ml": "aiml",
    "computer-vision": "aiml",
    "nlp-llm": "aiml",
    "optimization": "aiml",
    "data-engineering": "data-science",
    "geospatial": "data-science",
    "cybersecurity": "cyber-security",
    "distributed-systems": "devops-cloud",
}

_TABLES = ("problems", "problem_drafts")

# Anything still outside the catalog after the remap (free strings written
# straight into the DB, e.g. "biology") does not belong and is deleted.
FIELD_VALUES = (
    "web-dev", "app-dev", "aiml", "data-science", "cyber-security", "devops-cloud", "blockchain",
)
_FIELD_VALUES_SQL = ", ".join(f"'{value}'" for value in FIELD_VALUES)

_TABLES = ("problems", "problem_drafts")

FIELD_VALUES = (
    "web-dev", "app-dev", "aiml", "data-science", "cyber-security", "devops-cloud", "blockchain",
)


def _table_exists(bind, name: str) -> bool:
    return sa.inspect(bind).has_table(name)


def upgrade() -> None:
    bind = op.get_bind()
    for table in _TABLES:
        if not _table_exists(bind, table):
            continue
        bind.execute(
            sa.text(
                f"UPDATE {table} SET field = :new_field WHERE field = :old_field"
            ).bindparams(),
            [
                {"old_field": old, "new_field": new}
                for old, new in REMAP.items()
            ],
        )
        bind.execute(sa.text(f"DELETE FROM {table} WHERE field NOT IN ({_FIELD_VALUES_SQL})"))


def downgrade() -> None:
    # Old distinctions are not recoverable after the collapse.
    pass
