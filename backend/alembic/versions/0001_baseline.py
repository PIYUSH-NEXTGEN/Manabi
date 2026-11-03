"""Baseline schema — state of MANABI before the crawler (§6.1).

Represents the schema that `Base.metadata.create_all()` had been producing
until the crawler phase: users, problems, projects (the ML practice tables
were removed by an earlier refactor; existing Postgres deployments keep any
orphaned tables until a later migration drops them).
SQLite and Postgres compatible (JSON works natively on both via sa.JSON).

Revision ID: 0001_baseline
Revises:
Create Date: 2026-11-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("github_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("github_token", sa.String(length=255), nullable=True),
        sa.Column("signals_json", sa.JSON(), nullable=False),
        sa.Column("signals_updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_github_id", "users", ["github_id"], unique=True)
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "problems",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("who_affected", sa.Text(), nullable=False),
        sa.Column("why_matters", sa.Text(), nullable=False),
        sa.Column("field", sa.String(length=50), nullable=False),
        sa.Column("domain", sa.String(length=50), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("est_hours", sa.Integer(), nullable=False),
        sa.Column("tech_tags", sa.JSON(), nullable=False),
        sa.Column("datasets", sa.JSON(), nullable=False),
        sa.Column("approaches", sa.JSON(), nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("source_id", sa.String(length=100), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("source_note", sa.Text(), nullable=True),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("ai_fields", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("source_name", "source_id", name="uq_problem_source"),
    )
    op.create_index("ix_problems_field", "problems", ["field"])
    op.create_index("ix_problems_domain", "problems", ["domain"])
    op.create_index("ix_problems_difficulty", "problems", ["difficulty"])

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("problem_id", sa.Integer(), sa.ForeignKey("problems.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("repo_owner", sa.String(length=255), nullable=False),
        sa.Column("repo_name", sa.String(length=255), nullable=False),
        sa.Column("repo_url", sa.String(length=1000), nullable=False),
        sa.Column("open_for_contributors", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("progress_json", sa.JSON(), nullable=True),
        sa.Column("progress_updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "problem_id", "user_id", "repo_owner", "repo_name", name="uq_project_repo"
        ),
    )


def downgrade() -> None:
    op.drop_table("projects")
    op.drop_index("ix_problems_difficulty", "problems")
    op.drop_index("ix_problems_domain", "problems")
    op.drop_index("ix_problems_field", "problems")
    op.drop_table("problems")
    op.drop_index("ix_users_username", "users")
    op.drop_index("ix_users_github_id", "users")
    op.drop_table("users")
