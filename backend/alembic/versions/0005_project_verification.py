"""Project submission verification: statuses, ownership basis, relevance,
reports and the completed tick (§5).

Upgrade adds to `projects`: verification_status (existing rows backfilled to
'needs_review' so nothing unverified is silently trusted), ownership_basis,
solution_summary, relevance_score/reason/checked_at, review_note,
repo_github_id (+ partial-unique (repo_github_id, user_id) index),
repo_created_at, completed_at, demo_url, reflection; and creates the
`project_reports` table (unique per project+reporter, CASCADE delete with the
project).

Everything is defensive: columns/indexes/tables that already exist are skipped,
so the migration also succeeds on partially migrated databases.

Downgrade removes exactly what upgrade added. Row data in the added columns is
lost on downgrade; the only way back is the pre-deploy backup.

Do not edit earlier migrations to make this work; they stay as the
historical record.

Revision ID: 0005_project_verification
Revises: 0004_cleanup
Create Date: 2026-11-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_project_verification"
down_revision: str | None = "0004_cleanup"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECT_COLUMNS = [
    sa.Column("verification_status", sa.String(length=20), nullable=False, server_default=sa.text("'needs_review'")),
    sa.Column("ownership_basis", sa.String(length=20), nullable=True),
    sa.Column("solution_summary", sa.Text(), nullable=False, server_default=sa.text("''")),
    sa.Column("relevance_score", sa.Float(), nullable=True),
    sa.Column("relevance_reason", sa.String(length=300), nullable=True),
    sa.Column("relevance_checked_at", sa.DateTime(), nullable=True),
    sa.Column("review_note", sa.Text(), nullable=True),
    sa.Column("repo_github_id", sa.Integer(), nullable=True),
    sa.Column("repo_created_at", sa.DateTime(), nullable=True),
    sa.Column("completed_at", sa.DateTime(), nullable=True),
    sa.Column("demo_url", sa.String(length=500), nullable=True),
    sa.Column("reflection", sa.Text(), nullable=True),
]

PARTIAL_INDEX_WHERE = "repo_github_id IS NOT NULL"


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def _table_exists(conn, table: str) -> bool:
    return sa.inspect(conn).has_table(table)


def _index_names(conn, table: str) -> set[str]:
    return {i["name"] for i in sa.inspect(conn).get_indexes(table)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(bind, "projects"):
        return

    columns = {c["name"] for c in inspector.get_columns("projects")}
    missing = [col for col in PROJECT_COLUMNS if col.name not in columns]
    if missing:
        # batch mode rebuilds the table on SQLite; plain columns on Postgres.
        with op.batch_alter_table("projects") as batch:
            for col in missing:
                batch.add_column(col)

    indexes = _index_names(bind, "projects")
    if "ix_projects_verification_status" not in indexes:
        op.create_index("ix_projects_verification_status", "projects", ["verification_status"])
    if "uq_project_repo_github_id_user_id" not in indexes:
        op.create_index(
            "uq_project_repo_github_id_user_id",
            "projects",
            ["repo_github_id", "user_id"],
            unique=True,
            sqlite_where=sa.text(PARTIAL_INDEX_WHERE),
            postgresql_where=sa.text(PARTIAL_INDEX_WHERE),
        )

    if not _table_exists(bind, "project_reports"):
        op.create_table(
            "project_reports",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("reporter_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("reason", sa.String(length=300), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.UniqueConstraint("project_id", "reporter_user_id", name="uq_project_report_project_reporter"),
        )


def downgrade() -> None:
    bind = op.get_bind()

    if _table_exists(bind, "project_reports"):
        op.drop_table("project_reports")

    if not _table_exists(bind, "projects"):
        return

    indexes = _index_names(bind, "projects")
    for name in ("uq_project_repo_github_id_user_id", "ix_projects_verification_status"):
        if name in indexes:
            op.drop_index(name, table_name="projects")

    existing = _existing_columns(bind, "projects")
    droppable = [
        col.name
        for col in PROJECT_COLUMNS
        if col.name in existing and col.name != "verification_status"
    ]
    # verification_status last, so a half-applied state still keeps rows visible.
    droppable.append("verification_status")
    if droppable:
        with op.batch_alter_table("projects") as batch:
            for name in droppable:
                batch.drop_column(name)
