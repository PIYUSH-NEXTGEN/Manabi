from datetime import date, datetime, timezone

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Review-lifecycle values for Problem.status (§6.2). Public read paths only
# ever surface PUBLISHED rows; everything else lives in the review queue.
STATUS_PUBLISHED = "published"
STATUS_PENDING_REVIEW = "pending_review"
STATUS_REJECTED = "rejected"
STATUS_REMOVED = "removed"

ORIGIN_MANUAL = "manual"
ORIGIN_CRAWLER = "crawler"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    github_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    signals_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    signals_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="user")


class Problem(Base):
    __tablename__ = "problems"
    __table_args__ = (UniqueConstraint("source_name", "source_id", name="uq_problem_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    who_affected: Mapped[str] = mapped_column(Text, nullable=False)
    why_matters: Mapped[str] = mapped_column(Text, nullable=False)
    field: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    est_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    tech_tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    datasets: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    approaches: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    ai_fields: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    # Crawler/review pipeline (§6.2). Existing rows default to published so the
    # migration never makes already-visible content disappear.
    status: Mapped[str] = mapped_column(String(20), default=STATUS_PUBLISHED, nullable=False)
    origin: Mapped[str] = mapped_column(String(20), default=ORIGIN_MANUAL, nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    source_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    edition: Mapped[str | None] = mapped_column(String(100), nullable=True)
    organisation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    source_status: Mapped[str] = mapped_column(String(20), default="unknown", nullable=False)
    first_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_crawled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    extraction_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    crawl_source_key: Mapped[str | None] = mapped_column(String(64), nullable=True)

    creator: Mapped[User | None] = relationship()
    projects: Mapped[list["Project"]] = relationship(back_populates="problem")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("problem_id", "user_id", "repo_owner", "repo_name", name="uq_project_repo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    repo_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(255), nullable=False)
    repo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    open_for_contributors: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    progress_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    progress_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    problem: Mapped[Problem] = relationship(back_populates="projects")
    user: Mapped[User] = relationship(back_populates="projects")


class CrawlRun(Base):
    __tablename__ = "crawl_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_key: Mapped[str] = mapped_column(String(64), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="running", nullable=False)
    counts: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    llm_calls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    triggered_by: Mapped[str] = mapped_column(String(10), default="manual", nullable=False)


class CrawlItem(Base):
    __tablename__ = "crawl_items"
    __table_args__ = (UniqueConstraint("url", name="uq_crawl_items_url"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_key: Mapped[str] = mapped_column(String(64), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    problem_id: Mapped[int | None] = mapped_column(ForeignKey("problems.id"), nullable=True)
    last_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    etag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_modified: Mapped[str | None] = mapped_column(String(100), nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


# ============================================================================
# Project 1: Webhook Reliability & Event Delivery Infrastructure
# ============================================================================

WEBHOOK_STATUS_ACTIVE = "active"
WEBHOOK_STATUS_DISABLED = "disabled"


class WebhookEndpoint(Base):
    __tablename__ = "webhook_endpoints"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_webhook_endpoint_user_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    secret: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=WEBHOOK_STATUS_ACTIVE, nullable=False)
    retry_max_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    retry_initial_delay_ms: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    retry_max_delay_ms: Mapped[int] = mapped_column(Integer, default=300000, nullable=False)
    timeout_ms: Mapped[int] = mapped_column(Integer, default=30000, nullable=False)
    event_types_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped[User | None] = relationship()
    deliveries: Mapped[list["WebhookDelivery"]] = relationship(back_populates="endpoint")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    __table_args__ = (UniqueConstraint("endpoint_id", "event_id", name="uq_webhook_event_endpoint_event"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endpoint_id: Mapped[int] = mapped_column(ForeignKey("webhook_endpoints.id"), nullable=False, index=True)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    headers_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    endpoint: Mapped[WebhookEndpoint | None] = relationship()
    deliveries: Mapped[list["WebhookDelivery"]] = relationship(back_populates="event")


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endpoint_id: Mapped[int] = mapped_column(ForeignKey("webhook_endpoints.id"), nullable=False, index=True)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("webhook_events.id"), nullable=True, index=True)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # queued, sent, delivered, failed, dead_letter
    http_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    attempted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_retry_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    endpoint: Mapped[WebhookEndpoint | None] = relationship(back_populates="deliveries")
    event: Mapped[WebhookEvent | None] = relationship(back_populates="deliveries")


# ============================================================================
# Project 2: API Contract Drift & Breaking Change Detection Platform
# ============================================================================

API_SPEC_STATUS_ACTIVE = "active"
API_SPEC_STATUS_ARCHIVED = "archived"


class ApiSpec(Base):
    __tablename__ = "api_specs"
    __table_args__ = (UniqueConstraint("user_id", "name", "version", name="uq_api_spec_user_name_version"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    spec_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), default="upload", nullable=False)  # upload, url, git
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=API_SPEC_STATUS_ACTIVE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped[User | None] = relationship()


class ApiContractComparison(Base):
    __tablename__ = "api_contract_comparisons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spec_a_id: Mapped[int] = mapped_column(ForeignKey("api_specs.id"), nullable=False, index=True)
    spec_b_id: Mapped[int] = mapped_column(ForeignKey("api_specs.id"), nullable=False, index=True)
    breaking_changes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    non_breaking_changes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comparison_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    affected_endpoints_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    spec_a: Mapped[ApiSpec | None] = relationship(foreign_keys=[spec_a_id])


class ApiMonitoringTarget(Base):
    __tablename__ = "api_monitoring_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    spec_id: Mapped[int | None] = mapped_column(ForeignKey("api_specs.id"), nullable=True)
    check_interval_seconds: Mapped[int] = mapped_column(Integer, default=3600, nullable=False)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    checks: Mapped[list["ApiContractCheck"]] = relationship(back_populates="target")


class ApiContractCheck(Base):
    __tablename__ = "api_contract_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("api_monitoring_targets.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pass, fail, error
    breaking_changes_detected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    results_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    target: Mapped[ApiMonitoringTarget | None] = relationship(back_populates="checks")


# ============================================================================
# Project 3: Multi-Tenant Security & Authorization Audit Platform
# ============================================================================

ROLE_ADMIN = "admin"
ROLE_MEMBER = "member"
ROLE_VIEWER = "viewer"

FINDING_SEVERITY_LOW = "low"
FINDING_SEVERITY_MEDIUM = "medium"
FINDING_SEVERITY_HIGH = "high"
FINDING_SEVERITY_CRITICAL = "critical"


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = (UniqueConstraint("name", name="uq_tenant_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    plan: Mapped[str] = mapped_column(String(50), default="free", nullable=False)
    settings_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    memberships: Mapped[list["TenantMembership"]] = relationship(back_populates="tenant")
    resources: Mapped[list["TenantResource"]] = relationship(back_populates="tenant")
    audit_findings: Mapped[list["SecurityFinding"]] = relationship(back_populates="tenant")


class TenantMembership(Base):
    __tablename__ = "tenant_memberships"
    __table_args__ = (UniqueConstraint("user_id", "tenant_id", name="uq_membership_user_tenant"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), default=ROLE_MEMBER, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    tenant: Mapped[Tenant | None] = relationship(back_populates="memberships")
    user: Mapped[User | None] = relationship()


class TenantResource(Base):
    __tablename__ = "tenant_resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    tenant: Mapped[Tenant | None] = relationship(back_populates="resources")


class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    check_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    affected_resource: Mapped[str | None] = mapped_column(String(500), nullable=True)
    remediation: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)  # open, resolved, dismissed
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    tenant: Mapped[Tenant | None] = relationship(back_populates="audit_findings")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role", "permission", name="uq_role_permission"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    permission: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)


# ============================================================================
# Project 4: Real-Time Incident Response & Investigation Platform
# ============================================================================

INCIDENT_STATUS_OPEN = "open"
INCIDENT_STATUS_INVESTIGATING = "investigating"
INCIDENT_STATUS_MITIGATED = "mitigated"
INCIDENT_STATUS_RESOLVED = "resolved"
INCIDENT_STATUS_CLOSED = "closed"

INCIDENT_SEVERITY_LOW = "low"
INCIDENT_SEVERITY_MEDIUM = "medium"
INCIDENT_SEVERITY_HIGH = "high"
INCIDENT_SEVERITY_CRITICAL = "critical"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=INCIDENT_STATUS_OPEN, nullable=False)
    reporter_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    assignee_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    postmortem_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    tags_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    events: Mapped[list["IncidentEvent"]] = relationship(back_populates="incident", cascade="all, delete-orphan")
    assignments: Mapped[list["IncidentAssignment"]] = relationship(back_populates="incident")
    timeline_entries: Mapped[list["IncidentTimelineEntry"]] = relationship(back_populates="incident")


class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # alert, chat, manual, monitoring
    source_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    incident: Mapped[Incident | None] = relationship(back_populates="events")


class IncidentAssignment(Base):
    __tablename__ = "incident_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)  # incident_commander, responder, stakeholder
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    unassigned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    incident: Mapped[Incident | None] = relationship(back_populates="assignments")


class IncidentTimelineEntry(Base):
    __tablename__ = "incident_timeline_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_type: Mapped[str] = mapped_column(String(50), nullable=False)  # status_change, comment, action, alert
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    incident: Mapped[Incident | None] = relationship(back_populates="timeline_entries")


# ============================================================================
# Project 5: Intelligent Large-Scale File Ingestion & Processing Platform
# ============================================================================

INGESTION_JOB_STATUS_PENDING = "pending"
INGESTION_JOB_STATUS_VALIDATING = "validating"
INGESTION_JOB_STATUS_PROCESSING = "processing"
INGESTION_JOB_STATUS_COMPLETED = "completed"
INGESTION_JOB_STATUS_FAILED = "failed"
INGESTION_JOB_STATUS_CANCELLED = "cancelled"


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=INGESTION_JOB_STATUS_PENDING, nullable=False)
    total_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processed_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    skipped_duplicates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    config_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    result_summary_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    files: Mapped[list["IngestedFile"]] = relationship(back_populates="job", cascade="all, delete-orphan")


class IngestedFile(Base):
    __tablename__ = "ingested_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("ingestion_jobs.id"), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    validation_errors_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    duplicate_of_file_id: Mapped[int | None] = mapped_column(ForeignKey("ingested_files.id"), nullable=True)
    processing_result_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    job: Mapped[IngestionJob | None] = relationship(back_populates="files")


class ProcessingWorker(Base):
    __tablename__ = "processing_workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    worker_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="idle", nullable=False)  # idle, busy, offline
    last_heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    current_job_id: Mapped[int | None] = mapped_column(ForeignKey("ingestion_jobs.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


# ============================================================================
# Project 6: Privacy-First Product Analytics Infrastructure
# ============================================================================

CONSENT_GRANTED = "granted"
CONSENT_DENIED = "denied"
CONSENT_UNKNOWN = "unknown"


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    anonymous_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    event_properties_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    user_properties_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False, index=True)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anonymous_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    consent_status: Mapped[str] = mapped_column(String(20), default=CONSENT_UNKNOWN, nullable=False)
    consent_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class DataRetentionPolicy(Base):
    __tablename__ = "data_retention_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_retention_days: Mapped[int] = mapped_column(Integer, default=90, nullable=False)
    raw_data_retention_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


class FunnelDefinition(Base):
    __tablename__ = "funnel_definitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    steps_json: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


class RetentionCohort(Base):
    __tablename__ = "retention_cohorts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cohort_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    cohort_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    retention_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


# ============================================================================
# Project 7: Continuous Website Accessibility Monitoring Platform
# ============================================================================

SCAN_STATUS_PENDING = "pending"
SCAN_STATUS_RUNNING = "running"
SCAN_STATUS_COMPLETED = "completed"
SCAN_STATUS_FAILED = "failed"

WCAG_LEVEL_A = "A"
WCAG_LEVEL_AA = "AA"
WCAG_LEVEL_AAA = "AAA"


class MonitoredWebsite(Base):
    __tablename__ = "monitored_websites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    scan_interval_minutes: Mapped[int] = mapped_column(Integer, default=1440, nullable=False)  # daily
    wcag_level: Mapped[str] = mapped_column(String(10), default=WCAG_LEVEL_AA, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_scan_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    scans: Mapped[list["AccessibilityScan"]] = relationship(back_populates="website")


class AccessibilityScan(Base):
    __tablename__ = "accessibility_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    website_id: Mapped[int] = mapped_column(ForeignKey("monitored_websites.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default=SCAN_STATUS_PENDING, nullable=False)
    pages_scanned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    issues_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wcag_level: Mapped[str] = mapped_column(String(10), nullable=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    summary_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    website: Mapped[MonitoredWebsite | None] = relationship(back_populates="scans")
    issues: Mapped[list["AccessibilityIssue"]] = relationship(back_populates="scan", cascade="all, delete-orphan")


class AccessibilityIssue(Base):
    __tablename__ = "accessibility_issues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("accessibility_scans.id"), nullable=False, index=True)
    page_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    component_selector: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rule_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(500), nullable=False)
    wcag_level: Mapped[str] = mapped_column(String(10), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    remediation: Mapped[str | None] = mapped_column(Text, nullable=True)
    element_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    scan: Mapped[AccessibilityScan | None] = relationship(back_populates="issues")


# ============================================================================
# Project 8: Cross-Platform Inventory Reservation & Consistency Engine
# ============================================================================

RESERVATION_STATUS_ACTIVE = "active"
RESERVATION_STATUS_CONSUMED = "consumed"
RESERVATION_STATUS_RELEASED = "released"
RESERVATION_STATUS_EXPIRED = "expired"


class SalesChannel(Base):
    __tablename__ = "sales_channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(100), nullable=False)  # web, marketplace, pos, api
    config_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="channel")
    reservations: Mapped[list["InventoryReservation"]] = relationship(back_populates="channel")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("sales_channels.id"), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    total_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_threshold: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    channel: Mapped[SalesChannel | None] = relationship(back_populates="inventory_items")
    reservations: Mapped[list["InventoryReservation"]] = relationship(back_populates="item")


class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False, index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("sales_channels.id"), nullable=False, index=True)
    external_order_id: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=RESERVATION_STATUS_ACTIVE, nullable=False)
    reserved_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    item: Mapped[InventoryItem | None] = relationship(back_populates="reservations")
    channel: Mapped[SalesChannel | None] = relationship(back_populates="reservations")


class StockReconciliation(Base):
    __tablename__ = "stock_reconciliations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False, index=True)
    expected_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    discrepancy: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    reconciled_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reconciled_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


# ============================================================================
# Project 9: Offline-First Data Synchronization & Conflict Resolution Platform
# ============================================================================

SYNC_RECORD_STATUS_PENDING = "pending"
SYNC_RECORD_STATUS_SYNCED = "synced"
SYNC_RECORD_STATUS_CONFLICT = "conflict"
SYNC_RECORD_STATUS_RESOLVED = "resolved"
SYNC_RECORD_STATUS_FAILED = "failed"


class SyncRecord(Base):
    __tablename__ = "sync_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    collection: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    record_id: Mapped[str] = mapped_column(String(255), nullable=False)
    version_vector_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    data_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    operation: Mapped[str] = mapped_column(String(20), nullable=False)  # create, update, delete
    status: Mapped[str] = mapped_column(String(20), default=SYNC_RECORD_STATUS_PENDING, nullable=False)
    conflict_with_record_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("device_id", "collection", "record_id", name="uq_sync_record_device_collection_record"),
    )


class SyncConflict(Base):
    __tablename__ = "sync_conflicts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    collection: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    record_id: Mapped[str] = mapped_column(String(255), nullable=False)
    local_version_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    remote_version_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    local_vector_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    remote_vector_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    resolution_strategy: Mapped[str | None] = mapped_column(String(100), nullable=True)  # last_write_wins, merge, manual
    resolved_data_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)  # open, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# ============================================================================
# Project 10: Visual Workflow Execution & Automation Engine
# ============================================================================

WORKFLOW_STATUS_DRAFT = "draft"
WORKFLOW_STATUS_ACTIVE = "active"
WORKFLOW_STATUS_ARCHIVED = "archived"

EXECUTION_STATUS_PENDING = "pending"
EXECUTION_STATUS_RUNNING = "running"
EXECUTION_STATUS_COMPLETED = "completed"
EXECUTION_STATUS_FAILED = "failed"
EXECUTION_STATUS_CANCELLED = "cancelled"

STEP_STATUS_PENDING = "pending"
STEP_STATUS_RUNNING = "running"
STEP_STATUS_COMPLETED = "completed"
STEP_STATUS_FAILED = "failed"
STEP_STATUS_SKIPPED = "skipped"
STEP_STATUS_RETRYING = "retrying"


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    definition_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)  # nodes + edges
    status: Mapped[str] = mapped_column(String(20), default=WORKFLOW_STATUS_DRAFT, nullable=False)
    trigger_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # event, schedule, manual, webhook
    trigger_config_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    executions: Mapped[list["WorkflowExecution"]] = relationship(back_populates="workflow", cascade="all, delete-orphan")


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), nullable=False, index=True)
    trigger_payload_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=EXECUTION_STATUS_PENDING, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    context_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    workflow: Mapped[Workflow | None] = relationship(back_populates="executions")
    steps: Mapped[list["WorkflowStepExecution"]] = relationship(back_populates="execution", cascade="all, delete-orphan")


class WorkflowStepExecution(Base):
    __tablename__ = "workflow_step_executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("workflow_executions.id"), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    step_type: Mapped[str] = mapped_column(String(100), nullable=False)  # http, condition, delay, transform, approval
    status: Mapped[str] = mapped_column(String(20), default=STEP_STATUS_PENDING, nullable=False)
    input_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    depends_on_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    execution: Mapped[WorkflowExecution | None] = relationship(back_populates="steps")
