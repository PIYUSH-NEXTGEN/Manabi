"""Crawler pipeline: problem review status/origin columns + crawl bookkeeping tables.

Adds §6.2 columns to problems and the §6.3 crawl_runs / crawl_items tables.
Existing problems become status='published' (nothing disappears) and stay
origin='manual'. Works on SQLite and Postgres.

Revision ID: 0002_crawler
Revises: 0001_baseline
Create Date: 2026-11-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_crawler"
down_revision: str | None = "0001_baseline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "problems", sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'published'"))
    )
    op.add_column(
        "problems", sa.Column("origin", sa.String(length=20), nullable=False, server_default=sa.text("'manual'"))
    )
    op.add_column("problems", sa.Column("content_hash", sa.String(length=64), nullable=True))
    op.create_index("ix_problems_content_hash", "problems", ["content_hash"])
    op.add_column("problems", sa.Column("source_year", sa.Integer(), nullable=True))
    op.add_column("problems", sa.Column("edition", sa.String(length=100), nullable=True))
    op.add_column("problems", sa.Column("organisation", sa.String(length=255), nullable=True))
    op.add_column("problems", sa.Column("deadline", sa.Date(), nullable=True))
    op.add_column(
        "problems", sa.Column("source_status", sa.String(length=20), nullable=False, server_default=sa.text("'unknown'"))
    )
    op.add_column("problems", sa.Column("first_seen_at", sa.DateTime(), nullable=True))
    op.add_column("problems", sa.Column("last_seen_at", sa.DateTime(), nullable=True))
    op.add_column("problems", sa.Column("last_crawled_at", sa.DateTime(), nullable=True))
    op.add_column("problems", sa.Column("extraction_confidence", sa.Float(), nullable=True))
    op.add_column("problems", sa.Column("review_notes", sa.Text(), nullable=True))
    op.add_column("problems", sa.Column("crawl_source_key", sa.String(length=64), nullable=True))

    op.create_table(
        "crawl_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_key", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'running'")),
        sa.Column("counts", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("llm_calls", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("triggered_by", sa.String(length=10), nullable=False, server_default=sa.text("'manual'")),
    )

    op.create_table(
        "crawl_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_key", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("problem_id", sa.Integer(), sa.ForeignKey("problems.id"), nullable=True),
        sa.Column("last_status", sa.String(length=20), nullable=True),
        sa.Column("etag", sa.String(length=255), nullable=True),
        sa.Column("last_modified", sa.String(length=100), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("url", name="uq_crawl_items_url"),
    )


def downgrade() -> None:
    op.drop_table("crawl_items")
    op.drop_table("crawl_runs")
    op.drop_index("ix_problems_content_hash", "problems")
    op.drop_column("problems", "crawl_source_key")
    op.drop_column("problems", "review_notes")
    op.drop_column("problems", "extraction_confidence")
    op.drop_column("problems", "last_crawled_at")
    op.drop_column("problems", "last_seen_at")
    op.drop_column("problems", "first_seen_at")
    op.drop_column("problems", "source_status")
    op.drop_column("problems", "deadline")
    op.drop_column("problems", "organisation")
    op.drop_column("problems", "edition")
    op.drop_column("problems", "source_year")
    op.drop_column("problems", "content_hash")
    op.drop_column("problems", "origin")
    op.drop_column("problems", "status")
