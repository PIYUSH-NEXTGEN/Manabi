"""Migration tests (§11): alembic upgrade path on SQLite, no network, no LLM.

- upgrade head from empty DB == what create_all produces (sanity, no drift errors)
- upgrade from the baseline with pre-existing rows keeps them visible as
  status='published' (§6.2: nothing disappears)
"""

import pytest
from sqlalchemy import create_engine, inspect, text

from app.migrations import alembic_config, upgrade_to_head
from alembic import command

BASELINE_PROBLEM_SQL = """
INSERT INTO problems (
    title, summary, who_affected, why_matters, field, domain, difficulty,
    est_hours, tech_tags, datasets, approaches, source_name, original_text,
    ai_fields, created_at
) VALUES (
    'Old problem', 's', 'w', 'y', 'ml', 'other', 'beginner', 5,
    '[]', '[]', '[]', 'Seed source', 'verbatim', '[]', '2026-01-01 00:00:00'
)
"""


@pytest.fixture
def sqlite_url(tmp_path):
    return f"sqlite:///{tmp_path/'mig.db'}"


def test_upgrade_head_from_empty(sqlite_url):
    upgrade_to_head(sqlite_url)
    engine = create_engine(sqlite_url)
    names = set(inspect(engine).get_table_names())
    engine.dispose()
    assert {"users", "problems", "projects", "crawl_runs", "crawl_items"} <= names
    assert not {"ml_questions", "ml_attempts"} <= names  # ML tables removed by an earlier refactor


def test_upgrade_is_idempotent(sqlite_url):
    upgrade_to_head(sqlite_url)
    upgrade_to_head(sqlite_url)  # second run must not create duplicates


def test_upgrade_from_baseline_keeps_rows_published(sqlite_url):
    cfg = alembic_config(sqlite_url)
    command.upgrade(cfg, "0001_baseline")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        conn.execute(text(BASELINE_PROBLEM_SQL))
        conn.execute(text("INSERT INTO users (github_id, username, name, signals_json, created_at) "
                          "VALUES (7, 'u', NULL, '{}', '2026-01-01 00:00:00')"))
    command.upgrade(cfg, "head")
    with engine.begin() as conn:
        status, origin, source_status = conn.execute(
            text("SELECT status, origin, source_status FROM problems")
        ).one()
        columns = {c["name"] for c in inspect(engine).get_columns("problems")}
    engine.dispose()
    assert status == "published"  # existing rows never disappear (§6.2)
    assert origin == "manual"
    assert source_status == "unknown"
    assert {"content_hash", "source_year", "first_seen_at", "crawl_source_key"} <= columns
