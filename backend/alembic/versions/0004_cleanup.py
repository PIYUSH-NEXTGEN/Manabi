"""Cleanup migration: drop the unrelated advanced-project tables and the crawler leftovers.

Upgrade drops:
- the 40 tables created by 0003_advanced_projects (webhook, api-contract,
  tenant-security, incident, ingestion, analytics, accessibility, inventory,
  sync and workflow features), plus the crawler tables crawl_runs / crawl_items;
- the crawler-only problems columns: content_hash, source_status,
  first_seen_at, last_seen_at, last_crawled_at, extraction_confidence,
  review_notes, crawl_source_key (and the ix_problems_content_hash index).

Everything is defensive: the live schema is inspected first, and any table or
column that is already absent is skipped, so the migration also succeeds on a
partially migrated database (e.g. production that never applied 0002/0003).

Downgrade recreates the dropped tables (EMPTY) and columns. It does NOT
restore the dropped DATA — rows deleted by the upgrade are gone forever; the
only way back is the database backup taken before deploying this revision.

Do not edit 0001_baseline, 0002_crawler or 0003_advanced_projects to make this
migration work; they stay as the historical record.

Revision ID: 0004_cleanup
Revises: 0003_advanced_projects
Create Date: 2026-11-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_cleanup"
down_revision: str | None = "0003_advanced_projects"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Reverse dependency order: children first so foreign keys never dangle.
# The order matches the downgrade of 0003_advanced_projects, plus the two
# crawler tables (crawl_items holds an FK to problems; crawl_runs is standalone).
ADVANCED_TABLES = [
    "workflow_step_executions",
    "workflow_executions",
    "workflows",
    "sync_conflicts",
    "sync_records",
    "stock_reconciliations",
    "inventory_reservations",
    "inventory_items",
    "sales_channels",
    "accessibility_issues",
    "accessibility_scans",
    "monitored_websites",
    "retention_cohorts",
    "funnel_definitions",
    "data_retention_policies",
    "consent_records",
    "analytics_events",
    "processing_workers",
    "ingested_files",
    "ingestion_jobs",
    "incident_timeline_entries",
    "incident_assignments",
    "incident_events",
    "incidents",
    "role_permissions",
    "security_findings",
    "tenant_resources",
    "tenant_memberships",
    "tenants",
    "api_contract_checks",
    "api_monitoring_targets",
    "api_contract_comparisons",
    "api_specs",
    "webhook_deliveries",
    "webhook_events",
    "webhook_endpoints",
    "crawl_items",   # crawler bookkeeping (0002): FK -> problems.id
    "crawl_runs",    # crawler bookkeeping (0002): standalone
]

CRAWLER_COLUMNS = [
    "crawl_source_key",
    "review_notes",
    "extraction_confidence",
    "last_crawled_at",
    "last_seen_at",
    "first_seen_at",
    "source_status",
    "content_hash",   # carries ix_problems_content_hash; dropped via batch below
]


def _table_exists(conn, name: str) -> bool:
    return sa.inspect(conn).has_table(name)


def _existing_columns(conn, table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(conn).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()

    for table in ADVANCED_TABLES:
        if _table_exists(bind, table):
            op.drop_table(table)

    if not _table_exists(bind, "problems"):
        return
    problems_columns = _existing_columns(bind, "problems")
    if "content_hash" in problems_columns:
        # Drop the dependent index explicitly first (defensive: batch mode on
        # SQLite would also drop it during the table rebuild, but be explicit).
        index_names = {i["name"] for i in sa.inspect(bind).get_indexes("problems")}
        if "ix_problems_content_hash" in index_names:
            op.drop_index("ix_problems_content_hash", table_name="problems")

    for column in CRAWLER_COLUMNS:
        if column in problems_columns:
            with op.batch_alter_table("problems") as batch:
                batch.drop_column(column)


def downgrade() -> None:
    # Recreates the schema that 0003 created (advanced features) and the
    # crawler bookkeeping tables/columns from 0002 — but EMPTY.
    # No dropped data is restored; restore it from the pre-deploy backup.

    # ── Project 1: Webhook Reliability ──────────────────────────────────
    op.create_table(
        "webhook_endpoints",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("secret", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'active'")),
        sa.Column("retry_max_attempts", sa.Integer(), nullable=False, server_default=sa.text("5")),
        sa.Column("retry_initial_delay_ms", sa.Integer(), nullable=False, server_default=sa.text("1000")),
        sa.Column("retry_max_delay_ms", sa.Integer(), nullable=False, server_default=sa.text("300000")),
        sa.Column("timeout_ms", sa.Integer(), nullable=False, server_default=sa.text("30000")),
        sa.Column("event_types_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "name", name="uq_webhook_endpoint_user_name"),
    )
    op.create_table(
        "webhook_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("endpoint_id", sa.Integer(), sa.ForeignKey("webhook_endpoints.id"), nullable=False, index=True),
        sa.Column("event_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("headers_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("received_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("endpoint_id", "event_id", name="uq_webhook_event_endpoint_event"),
    )
    op.create_table(
        "webhook_deliveries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("endpoint_id", sa.Integer(), sa.ForeignKey("webhook_endpoints.id"), nullable=False, index=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("webhook_events.id"), nullable=True, index=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("http_status", sa.Integer(), nullable=True),
        sa.Column("response_body", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.Column("attempted_at", sa.DateTime(), nullable=True),
        sa.Column("next_retry_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── Project 2: API Contract Drift ───────────────────────────────────
    op.create_table(
        "api_specs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("spec_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default=sa.text("'upload'")),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'active'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "name", "version", name="uq_api_spec_user_name_version"),
    )
    op.create_table(
        "api_contract_comparisons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("spec_a_id", sa.Integer(), sa.ForeignKey("api_specs.id"), nullable=False, index=True),
        sa.Column("spec_b_id", sa.Integer(), sa.ForeignKey("api_specs.id"), nullable=False, index=True),
        sa.Column("breaking_changes_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("non_breaking_changes_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("comparison_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("affected_endpoints_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "api_monitoring_targets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.String(length=1000), nullable=False),
        sa.Column("spec_id", sa.Integer(), sa.ForeignKey("api_specs.id"), nullable=True),
        sa.Column("check_interval_seconds", sa.Integer(), nullable=False, server_default=sa.text("3600")),
        sa.Column("last_checked_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "api_contract_checks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("target_id", sa.Integer(), sa.ForeignKey("api_monitoring_targets.id"), nullable=False, index=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("breaking_changes_detected", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("results_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("checked_at", sa.DateTime(), nullable=False),
    )

    # ── Project 3: Multi-Tenant Security ────────────────────────────────
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column("plan", sa.String(length=50), nullable=False, server_default=sa.text("'free'")),
        sa.Column("settings_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "tenant_memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False, index=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default=sa.text("'member'")),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "tenant_id", name="uq_membership_user_tenant"),
    )
    op.create_table(
        "tenant_resources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False, index=True),
        sa.Column("resource_type", sa.String(length=100), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.Column("owner_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "security_findings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False, index=True),
        sa.Column("check_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("affected_resource", sa.String(length=500), nullable=True),
        sa.Column("remediation", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'open'")),
        sa.Column("detected_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "role_permissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role", sa.String(length=50), nullable=False, index=True),
        sa.Column("permission", sa.String(length=100), nullable=False, index=True),
        sa.Column("resource_type", sa.String(length=100), nullable=True),
        sa.UniqueConstraint("role", "permission", name="uq_role_permission"),
    )

    # ── Project 4: Incident Response ────────────────────────────────────
    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'open'")),
        sa.Column("reporter_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("assignee_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("postmortem_url", sa.String(length=1000), nullable=True),
        sa.Column("tags_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.create_table(
        "incident_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.Integer(), sa.ForeignKey("incidents.id"), nullable=False, index=True),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "incident_assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.Integer(), sa.ForeignKey("incidents.id"), nullable=False, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), nullable=False),
        sa.Column("unassigned_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "incident_timeline_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.Integer(), sa.ForeignKey("incidents.id"), nullable=False, index=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("entry_type", sa.String(length=50), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )

    # ── Project 5: File Ingestion ───────────────────────────────────────
    op.create_table(
        "ingestion_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("total_files", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("processed_files", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("failed_files", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("skipped_duplicates", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("config_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("result_summary_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "ingested_files",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("ingestion_jobs.id"), nullable=False, index=True),
        sa.Column("original_filename", sa.String(length=500), nullable=False),
        sa.Column("stored_path", sa.String(length=1000), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=True, index=True),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("mime_type", sa.String(length=200), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("validation_errors_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("is_duplicate", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("duplicate_of_file_id", sa.Integer(), sa.ForeignKey("ingested_files.id"), nullable=True),
        sa.Column("processing_result_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "processing_workers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("worker_name", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'idle'")),
        sa.Column("last_heartbeat_at", sa.DateTime(), nullable=True),
        sa.Column("current_job_id", sa.Integer(), sa.ForeignKey("ingestion_jobs.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── Project 6: Privacy Analytics ────────────────────────────────────
    op.create_table(
        "analytics_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("session_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("anonymous_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("event_name", sa.String(length=200), nullable=False, index=True),
        sa.Column("event_properties_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("user_properties_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("timestamp", sa.DateTime(), nullable=False, index=True),
        sa.Column("consumed_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "consent_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("anonymous_id", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("consent_status", sa.String(length=20), nullable=False, server_default=sa.text("'unknown'")),
        sa.Column("consent_version", sa.String(length=50), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "data_retention_policies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("event_retention_days", sa.Integer(), nullable=False, server_default=sa.text("90")),
        sa.Column("raw_data_retention_days", sa.Integer(), nullable=False, server_default=sa.text("30")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "funnel_definitions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("steps_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "retention_cohorts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("cohort_date", sa.Date(), nullable=False, index=True),
        sa.Column("cohort_size", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("retention_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("computed_at", sa.DateTime(), nullable=False),
    )

    # ── Project 7: Accessibility Monitoring ─────────────────────────────
    op.create_table(
        "monitored_websites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("scan_interval_minutes", sa.Integer(), nullable=False, server_default=sa.text("1440")),
        sa.Column("wcag_level", sa.String(length=10), nullable=False, server_default=sa.text("'AA'")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("last_scan_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "accessibility_scans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("website_id", sa.Integer(), sa.ForeignKey("monitored_websites.id"), nullable=False, index=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("pages_scanned", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("issues_found", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("wcag_level", sa.String(length=10), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("summary_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "accessibility_issues",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scan_id", sa.Integer(), sa.ForeignKey("accessibility_scans.id"), nullable=False, index=True),
        sa.Column("page_url", sa.String(length=1000), nullable=False),
        sa.Column("component_selector", sa.String(length=500), nullable=True),
        sa.Column("rule_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("rule_name", sa.String(length=500), nullable=False),
        sa.Column("wcag_level", sa.String(length=10), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("remediation", sa.Text(), nullable=True),
        sa.Column("element_html", sa.Text(), nullable=True),
        sa.Column("detected_at", sa.DateTime(), nullable=False),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    )

    # ── Project 8: Inventory Reservation ────────────────────────────────
    op.create_table(
        "sales_channels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("channel_type", sa.String(length=100), nullable=False),
        sa.Column("config_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("channel_id", sa.Integer(), sa.ForeignKey("sales_channels.id"), nullable=False, index=True),
        sa.Column("sku", sa.String(length=255), nullable=False, index=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("total_quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("reserved_quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("available_quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("reorder_threshold", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "inventory_reservations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), sa.ForeignKey("inventory_items.id"), nullable=False, index=True),
        sa.Column("channel_id", sa.Integer(), sa.ForeignKey("sales_channels.id"), nullable=False, index=True),
        sa.Column("external_order_id", sa.String(length=500), nullable=True, index=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'active'")),
        sa.Column("reserved_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("consumed_at", sa.DateTime(), nullable=True),
        sa.Column("released_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "stock_reconciliations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), sa.ForeignKey("inventory_items.id"), nullable=False, index=True),
        sa.Column("expected_quantity", sa.Integer(), nullable=False),
        sa.Column("actual_quantity", sa.Integer(), nullable=False),
        sa.Column("discrepancy", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("reconciled_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("reconciled_at", sa.DateTime(), nullable=False),
    )

    # ── Project 9: Offline Sync ─────────────────────────────────────────
    op.create_table(
        "sync_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("device_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("collection", sa.String(length=200), nullable=False, index=True),
        sa.Column("record_id", sa.String(length=255), nullable=False),
        sa.Column("version_vector_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("data_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("operation", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("conflict_with_record_id", sa.String(length=255), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("synced_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "device_id", "collection", "record_id", name="uq_sync_record_device_collection_record"
        ),
    )
    op.create_table(
        "sync_conflicts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("collection", sa.String(length=200), nullable=False, index=True),
        sa.Column("record_id", sa.String(length=255), nullable=False),
        sa.Column("local_version_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("remote_version_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("local_vector_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("remote_vector_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("resolution_strategy", sa.String(length=100), nullable=True),
        sa.Column("resolved_data_json", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'open'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )

    # ── Project 10: Visual Workflow ─────────────────────────────────────
    op.create_table(
        "workflows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("definition_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'draft'")),
        sa.Column("trigger_type", sa.String(length=50), nullable=True),
        sa.Column("trigger_config_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "workflow_executions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workflow_id", sa.Integer(), sa.ForeignKey("workflows.id"), nullable=False, index=True),
        sa.Column("trigger_payload_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("context_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("error_message", sa.Text(), nullable=True),
    )
    op.create_table(
        "workflow_step_executions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("execution_id", sa.Integer(), sa.ForeignKey("workflow_executions.id"), nullable=False, index=True),
        sa.Column("step_id", sa.String(length=255), nullable=False),
        sa.Column("step_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("input_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("output_json", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("max_retries", sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("depends_on_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )

    # ── Crawler bookkeeping (from 0002) ────────────────────────────────
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

    # ── Crawler columns on problems (from 0002) ────────────────────────
    with op.batch_alter_table("problems") as batch:
        batch.add_column(sa.Column("content_hash", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("source_status", sa.String(length=20), nullable=False, server_default=sa.text("'unknown'")))
        batch.add_column(sa.Column("first_seen_at", sa.DateTime(), nullable=True))
        batch.add_column(sa.Column("last_seen_at", sa.DateTime(), nullable=True))
        batch.add_column(sa.Column("last_crawled_at", sa.DateTime(), nullable=True))
        batch.add_column(sa.Column("extraction_confidence", sa.Float(), nullable=True))
        batch.add_column(sa.Column("review_notes", sa.Text(), nullable=True))
        batch.add_column(sa.Column("crawl_source_key", sa.String(length=64), nullable=True))
    op.create_index("ix_problems_content_hash", "problems", ["content_hash"])
