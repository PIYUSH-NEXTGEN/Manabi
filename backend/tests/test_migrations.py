"""Migration tests (§11): alembic upgrade path on SQLite, no network, no LLM.

- upgrade head from empty DB == what create_all produces (sanity, no drift errors)
- upgrade from the baseline with pre-existing rows keeps them visible as
  status='published' (§6.2: nothing disappears)
- 0004_cleanup drops the removed ops tables/columns and keeps every existing
  row of users / problems / projects intact
- downgrade -1 works and recreates the dropped schema (empty)
"""

import pytest
from sqlalchemy import create_engine, inspect, text

from alembic import command
from app.migrations import alembic_config, upgrade_to_head
from app.models import Base

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

REMOVED_TABLES = {
    "webhook_endpoints", "webhook_events", "webhook_deliveries",
    "api_specs", "api_contract_comparisons", "api_monitoring_targets",
    "api_contract_checks", "tenants", "tenant_memberships", "tenant_resources",
    "security_findings", "role_permissions", "incidents", "incident_events",
    "incident_assignments", "incident_timeline_entries", "ingestion_jobs",
    "ingested_files", "processing_workers", "analytics_events",
    "consent_records", "data_retention_policies", "funnel_definitions",
    "retention_cohorts", "monitored_websites", "accessibility_scans",
    "accessibility_issues", "sales_channels", "inventory_items",
    "inventory_reservations", "stock_reconciliations", "sync_records",
    "sync_conflicts", "workflows", "workflow_executions",
    "workflow_step_executions", "crawl_runs", "crawl_items",
}

REMOVED_PROBLEM_COLUMNS = {
    "content_hash", "source_status", "first_seen_at", "last_seen_at",
    "last_crawled_at", "extraction_confidence", "review_notes",
    "crawl_source_key",
}

PROJECT_0005_COLUMNS = {
    "verification_status", "ownership_basis", "solution_summary",
    "relevance_score", "relevance_reason", "relevance_checked_at",
    "review_note", "repo_github_id", "repo_created_at", "completed_at",
    "demo_url", "reflection",
}


def _seed_project_row(cfg, sqlite_url) -> None:
    """Create the schema up to 0004 plus one pre-0005 project row."""
    command.upgrade(cfg, "0004_cleanup")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        conn.execute(text("""INSERT INTO users (github_id, username, name, signals_json, created_at)
                           VALUES (7, 'u', NULL, '{}', '2026-01-01 00:00:00'),
                                  (8, 'v', NULL, '{}', '2026-01-01 00:00:00')"""))
        conn.execute(text(BASELINE_PROBLEM_SQL))
        conn.execute(text("""INSERT INTO projects (problem_id, user_id, repo_owner, repo_name, repo_url, created_at)
                           SELECT pr.id, u.id, 'own', 'repo', 'https://github.com/own/repo', '2026-01-01 00:00:00'
                           FROM problems pr, users u LIMIT 1"""))
    engine.dispose()


@pytest.fixture
def sqlite_url(tmp_path):
    return f"sqlite:///{tmp_path/'mig.db'}"


def _seed_baseline_rows(cfg, sqlite_url):
    """Create the 0001 baseline + one row per kept table (pre-0003 layout)."""
    command.upgrade(cfg, "0001_baseline")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        conn.execute(text(BASELINE_PROBLEM_SQL))
        conn.execute(text("INSERT INTO users (github_id, username, name, signals_json, created_at) "
                          "VALUES (7, 'u', NULL, '{}', '2026-01-01 00:00:00')"))
        conn.execute(text("INSERT INTO problems (title, summary, who_affected, why_matters, field, domain, difficulty, est_hours, tech_tags, datasets, approaches, source_name, original_text, ai_fields, created_by, created_at) "
                          "SELECT 'Seed p', 'd', 'w', 'y', 'ml', 'other', 'beginner', 2, '[]', '[]', '[]', 'SeedSrc', 'v', '[]', u.id, '2026-01-01 00:00:00' FROM users u LIMIT 1"))  # noqa: E501
        conn.execute(text("INSERT INTO projects (problem_id, user_id, repo_owner, repo_name, repo_url, created_at) "
                          "SELECT pr.id, u.id, 'own', 'repo', 'https://github.com/own/repo', '2026-01-01 00:00:00' "
                          "FROM problems pr, users u LIMIT 1"))  # noqa: E501
    engine.dispose()


def test_upgrade_head_from_empty(sqlite_url):
    upgrade_to_head(sqlite_url)
    engine = create_engine(sqlite_url)
    names = set(inspect(engine).get_table_names())
    engine.dispose()
    assert {"users", "problems", "projects"} <= names
    assert not (REMOVED_TABLES & names)  # ops + crawler tables gone (0004)
    assert not {"ml_questions", "ml_attempts"} <= names  # ML tables removed by an earlier refactor


def test_upgrade_is_idempotent(sqlite_url):
    upgrade_to_head(sqlite_url)
    upgrade_to_head(sqlite_url)  # second run must not create duplicates


def test_upgrade_to_head_keeps_problem_rows_visible(sqlite_url):
    cfg = alembic_config(sqlite_url)
    _seed_baseline_rows(cfg, sqlite_url)
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        status, origin = conn.execute(
            text("SELECT status, origin FROM problems ORDER BY id LIMIT 1")
        ).one()
        columns = {c["name"] for c in inspect(engine).get_columns("problems")}
    engine.dispose()
    assert status == "published"  # existing rows never disappear (§6.2)
    assert origin == "manual"
    assert not REMOVED_PROBLEM_COLUMNS & columns  # crawler columns dropped (0004)
    # 0002-only columns that the app still uses must survive the cleanup
    assert {"status", "origin", "source_year", "edition", "organisation", "deadline"} <= columns


def test_0004_upgrade_preserves_existing_row_values(sqlite_url):
    cfg = alembic_config(sqlite_url)
    _seed_baseline_rows(cfg, sqlite_url)
    command.upgrade(cfg, "0002_crawler")  # crawler columns exist from here on
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        # dirty the crawler columns: 0004 must drop them without touching row data
        conn.execute(text("UPDATE problems SET content_hash = 'abc', review_notes = 'note', "
                          "crawl_source_key = 'sih', extraction_confidence = 0.5"))
    with engine.begin() as conn:
        conn_facts = conn.execute(text(
            "SELECT (SELECT COUNT(*) FROM users), (SELECT COUNT(*) FROM problems), "
            "(SELECT COUNT(*) FROM projects)"
        )).one()
        user_before, problem_before, project_before = conn_facts
        problem_rows_before = conn.execute(text(
            "SELECT title, summary, field, status, origin FROM problems ORDER BY id"
        )).all()
        project_rows_before = conn.execute(text(
            "SELECT problem_id, user_id, repo_owner, repo_name, repo_url FROM projects ORDER BY id"
        )).all()
    engine.dispose()

    command.upgrade(cfg, "head")

    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        user_after, problem_after, project_after = conn.execute(text(
            "SELECT (SELECT COUNT(*) FROM users), (SELECT COUNT(*) FROM problems), "
            "(SELECT COUNT(*) FROM projects)"
        )).one()
        problem_rows_after = conn.execute(text(
            "SELECT title, summary, field, status, origin FROM problems ORDER BY id"
        )).all()
        project_rows_after = conn.execute(text(
            "SELECT problem_id, user_id, repo_owner, repo_name, repo_url FROM projects ORDER BY id"
        )).all()
        user_row_after = conn.execute(text(
            "SELECT github_id, username FROM users"
        )).one()
    engine.dispose()
    assert (user_before, problem_before, project_before) == (1, 2, 1)  # sanity: we seeded something
    assert (user_after, problem_after, project_after) == (1, 2, 1)  # no rows deleted (§8)
    assert problem_rows_before == problem_rows_after
    assert project_rows_after == [
        (1, 1, "own", "repo", "https://github.com/own/repo"),
    ]
    assert user_row_after == (7, "u")


def test_downgrade_last_step_recreates_schema_empty(sqlite_url):
    cfg = alembic_config(sqlite_url)
    _seed_baseline_rows(cfg, sqlite_url)
    command.upgrade(cfg, "head")
    # head used to be 0004; since 0005 the 0004-downgrade tail is reached via a
    # relative step, which grows by one with every appended migration
    # (0006: -3 == 0006 -> 0005 -> 0004 -> 0003).
    # (0005/0006 own downgrades are covered by the dedicated tests below.)
    command.downgrade(cfg, "-3")  # -> 0003
    engine = create_engine(sqlite_url)
    names = set(inspect(engine).get_table_names())
    cols = {c["name"] for c in inspect(engine).get_columns("problems")}
    with engine.begin() as conn:
        counts = conn.execute(text(
            "SELECT (SELECT COUNT(*) FROM crawl_runs), (SELECT COUNT(*) FROM webhook_endpoints)"
        )).one()
    engine.dispose()
    assert REMOVED_TABLES <= names  # recreated (empty)
    assert REMOVED_PROBLEM_COLUMNS <= cols
    assert counts == (0, 0)
    # and forward again: upgrade must re-drop everything idempotently
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    names = set(inspect(engine).get_table_names())
    engine.dispose()
    assert not (REMOVED_TABLES & names)


def test_models_match_migrated_schema(sqlite_url):
    """No drift: after upgrade head, the migrated DB matches Base.metadata."""
    upgrade_to_head(sqlite_url)
    engine = create_engine(sqlite_url)
    inspector = inspect(engine)
    db_tables = {t for t in inspector.get_table_names() if t != "alembic_version"}
    model_tables = set(Base.metadata.tables)

    # Local-only leftovers that exist neither in models nor migrations are fine,
    # but the migrated schema must contain every model table.
    assert model_tables <= db_tables, f"missing tables: {model_tables - db_tables}"

    for table in sorted(model_tables):
        db_cols = {c["name"] for c in inspector.get_columns(table)}
        model_cols = {c.name for c in Base.metadata.tables[table].columns}
        assert model_cols <= db_cols, f"{table}: missing columns {model_cols - db_cols}"
        if table == "problems":
            assert not REMOVED_PROBLEM_COLUMNS & db_cols

    # tighten: migrated schema must not contain tables the app forgot about
    assert db_tables == model_tables, f"extra tables: {db_tables - model_tables}"
    engine.dispose()


# ---------------- 0005_project_verification ----------------


def _seed_pre0006_rows(cfg, sqlite_url) -> None:
    """Create the schema up to 0005 plus one problem row to survive 0006."""
    command.upgrade(cfg, "0005_project_verification")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        conn.execute(text(BASELINE_PROBLEM_SQL))
    engine.dispose()


def test_0006_upgrade_adds_nullable_goal(sqlite_url):
    cfg = alembic_config(sqlite_url)
    _seed_pre0006_rows(cfg, sqlite_url)
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        title, goal = conn.execute(text("SELECT title, goal FROM problems ORDER BY id LIMIT 1")).one()
        nullable = next(
            c["nullable"] for c in inspect(engine).get_columns("problems") if c["name"] == "goal"
        )
        # one row per problem means the column was added without dropping data
        problem_count = conn.execute(text("SELECT COUNT(*) FROM problems")).one()[0]
    engine.dispose()
    assert problem_count == 1  # rows survive the (batch) column add
    assert title == "Old problem" and goal is None  # unlabelled by default
    assert nullable  # NULL means "never appears under a track filter"


def test_0006_upgrade_from_empty_then_downgrade(sqlite_url):
    cfg = alembic_config(sqlite_url)
    command.upgrade(cfg, "0005_project_verification")
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "-1")  # back to 0005: the goal column is gone again
    engine = create_engine(sqlite_url)
    cols = {c["name"] for c in inspect(engine).get_columns("problems")}
    engine.dispose()
    assert "goal" not in cols
    # forward again works
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    cols = {c["name"] for c in inspect(engine).get_columns("problems")}
    engine.dispose()
    assert "goal" in cols


# ---------------- 0005_project_verification ----------------


def test_0005_upgrade_keeps_rows_and_backfills_needs_review(sqlite_url):
    """Pre-0005 rows survive with verification_status='needs_review'."""
    cfg = alembic_config(sqlite_url)
    _seed_project_row(cfg, sqlite_url)
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    with engine.begin() as conn:
        rows = conn.execute(text(
            "SELECT repo_owner, verification_status, ownership_basis, solution_summary FROM projects"
        )).all()
        counts = conn.execute(text(
            "SELECT (SELECT COUNT(*) FROM projects), (SELECT COUNT(*) FROM project_reports)"
        )).one()
        cols = {c["name"] for c in inspect(engine).get_columns("projects")}
        has_partial_index = any(
            i["name"] == "uq_project_repo_github_id_user_id" for i in inspect(engine).get_indexes("projects")
        )
    engine.dispose()
    assert len(PROJECT_0005_COLUMNS & cols) == len(PROJECT_0005_COLUMNS)
    assert rows == [("own", "needs_review", None, "")]
    assert counts == (1, 0)  # no rows lost, empty reports table
    assert has_partial_index


def test_0005_upgrade_from_empty_then_downgrade(sqlite_url):
    cfg = alembic_config(sqlite_url)
    command.upgrade(cfg, "0004_cleanup")
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "0004_cleanup")  # explicit: 0006 and 0005 objects gone again
    engine = create_engine(sqlite_url)
    problem_cols = {c["name"] for c in inspect(engine).get_columns("problems")}
    project_cols = {c["name"] for c in inspect(engine).get_columns("projects")}
    names = set(inspect(engine).get_table_names())
    engine.dispose()
    assert not ("project_reports" in names)
    assert not (PROJECT_0005_COLUMNS & project_cols)
    assert not ("goal" in problem_cols)  # 0006 must not survive an earlier downgrade
    # forward again works
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)
    problem_cols = {c["name"] for c in inspect(engine).get_columns("problems")}
    project_cols = {c["name"] for c in inspect(engine).get_columns("projects")}
    names = set(inspect(engine).get_table_names())
    engine.dispose()
    assert "project_reports" in names
    assert len(PROJECT_0005_COLUMNS & project_cols) == len(PROJECT_0005_COLUMNS)
    assert "goal" in problem_cols


def test_0005_reports_table_unique_and_cascade(sqlite_url):
    cfg = alembic_config(sqlite_url)
    _seed_project_row(cfg, sqlite_url)
    command.upgrade(cfg, "head")
    engine = create_engine(sqlite_url)

    def project_report_values(reason: str) -> str:
        return f"SELECT p.id, u.id, '{reason}', '2026-01-01 00:00:00' FROM projects p CROSS JOIN users u"

    with engine.begin() as conn:
        # one report per (project, reporter): a second identical pair is rejected
        conn.execute(text(
            "INSERT INTO project_reports (project_id, reporter_user_id, reason, created_at) "
            + project_report_values("first")
        ))
        with pytest.raises(Exception):
            conn.execute(text(
                "INSERT INTO project_reports (project_id, reporter_user_id, reason, created_at) "
                + project_report_values("duplicate")
            ))
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")  # must run outside a transaction
        before = conn.execute(text("SELECT COUNT(*) FROM project_reports")).one()[0]
        conn.execute(text("DELETE FROM projects WHERE id = (SELECT id FROM projects LIMIT 1)"))
        after = conn.execute(text("SELECT COUNT(*) FROM project_reports")).one()[0]
    engine.dispose()
    assert before == 2  # one report per user of the single project
    assert after == 0
    engine.dispose()
    assert after == 0
