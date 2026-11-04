from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

Difficulty = Literal["beginner", "intermediate", "advanced"]
FieldEnum = Literal[
    "ml", "computer-vision", "nlp-llm", "cybersecurity", "web-fullstack", "mobile",
    "data-engineering", "geospatial", "optimization", "iot-embedded",
    "distributed-systems", "blockchain", "devops-cloud", "data-science", "developer-tools", "other",
]
DomainEnum = Literal[
    "healthcare", "education", "agriculture", "fintech", "climate", "governance",
    "transport", "disaster-management", "industry", "social-impact", "developer-tools", "cybersecurity", "computer-vision", "iot-embedded", "distributed-systems", "ml", "devops-cloud", "nlp-llm", "cloud", "blockchain", "web3", "databases", "systems", "other",
]


MAX_TITLE = 300
MAX_SUMMARY = 8000
MAX_SHORT = 2000
MAX_TAG = 40
MAX_DATASET_URL = 500

_problem_tag_item = Annotated[str, Field(min_length=1, max_length=MAX_TAG)]


class ProblemCard(BaseModel):
    title: str = Field(min_length=1, max_length=MAX_TITLE)
    summary: str = Field(min_length=1, max_length=MAX_SUMMARY)
    who_affected: str = Field(min_length=1, max_length=MAX_SHORT)
    why_matters: str = Field(min_length=1, max_length=MAX_SHORT)
    field: FieldEnum
    domain: DomainEnum
    difficulty: Difficulty
    est_hours: int = Field(ge=1, le=1000)
    tech_tags: list[_problem_tag_item] = Field(max_length=25)
    datasets: list[dict] = Field(max_length=15)
    approaches: list[Annotated[str, Field(min_length=1, max_length=800)]] = Field(max_length=8)
    source_name: str = Field(min_length=1, max_length=MAX_TITLE)
    source_id: str | None = Field(default=None, max_length=100)
    source_url: str | None = Field(default=None, max_length=MAX_DATASET_URL)
    source_note: str | None = Field(default=None, max_length=MAX_TITLE)


class ProblemOut(ProblemCard):
    id: int
    project_count: int
    ai_fields: list[str]
    origin: str = "manual"
    source_year: int | None = None
    edition: str | None = None
    organisation: str | None = None
    source_status: str = "unknown"
    deadline: date | None = None


class ProjectCreate(BaseModel):
    repo_url: str
    open_for_contributors: bool = False


class Progress(BaseModel):
    status: Literal["not_started", "active", "stale"]
    commit_count: int
    last_commit_at: str | None
    has_readme: bool
    recent_commits: list[dict]
    open_issues: list[dict]


class ProjectOut(BaseModel):
    id: int
    problem_id: int
    problem_title: str
    repo_url: str
    repo_owner: str
    repo_name: str
    open_for_contributors: bool
    owner: dict
    progress: Progress | None
    progress_updated_at: datetime | None


class ProblemDetail(ProblemOut):
    original_text: str
    projects: list[ProjectOut]
    display_policy: Literal["summary_only", "summary_plus_excerpt"] = "summary_plus_excerpt"


class AdminProblemOut(ProblemOut):
    status: str
    origin: str
    source_year: int | None
    edition: str | None
    organisation: str | None
    deadline: date | None
    source_status: str
    extraction_confidence: float | None
    review_notes: str | None
    crawl_source_key: str | None
    first_seen_at: datetime | None
    last_seen_at: datetime | None
    created_at: datetime


class AdminReviewOut(BaseModel):
    items: list[AdminProblemOut]
    total: int


class ProblemPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=MAX_TITLE)
    summary: str | None = Field(default=None, min_length=1, max_length=MAX_SUMMARY)
    who_affected: str | None = Field(default=None, min_length=1, max_length=MAX_SHORT)
    why_matters: str | None = Field(default=None, min_length=1, max_length=MAX_SHORT)
    field: FieldEnum | None = None
    domain: DomainEnum | None = None
    difficulty: Difficulty | None = None
    est_hours: int | None = Field(default=None, ge=1, le=1000)
    tech_tags: list[_problem_tag_item] | None = Field(default=None, max_length=25)
    approaches: list[Annotated[str, Field(min_length=1, max_length=800)]] | None = Field(default=None, max_length=8)
    review_notes: str | None = Field(default=None, max_length=4000)


class AdminActionOut(BaseModel):
    ok: bool
    problem_id: int
    status: str


class CrawlRunOut(BaseModel):
    id: int
    source_key: str
    started_at: datetime
    finished_at: datetime | None
    status: str
    counts: dict[str, int]
    llm_calls: int
    error_summary: str | None
    triggered_by: str


class TakedownOut(BaseModel):
    ok: bool
    source_key: str
    unpublished: int


class DatasetIn(BaseModel):
    name: str
    url: str | None = None


class ProblemIn(ProblemCard):
    """POST /api/problems body: ProblemCard per contract, plus optional ai_fields (see docs/REQUESTS.md)."""

    ai_fields: list[str] = []


class RecommendationItem(BaseModel):
    problem: ProblemOut
    score: int
    reasons: list[str]


class RecommendationsOut(BaseModel):
    items: list[RecommendationItem]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=1000)


class ChatPageContext(BaseModel):
    problem_id: int | None = Field(default=None, ge=1)


class ChatIn(BaseModel):
    messages: list[ChatMessage] = Field(max_length=12, min_length=1)
    page_context: ChatPageContext | None = None


class ChatProblemItem(BaseModel):
    id: int
    title: str
    field: FieldEnum
    difficulty: Difficulty


class ChatOut(BaseModel):
    reply: str
    problems: list[ChatProblemItem]


class Facet(BaseModel):
    value: str
    count: int
    last_updated: datetime | None = None


class FacetsOut(BaseModel):
    fields: list[Facet]
    domains: list[Facet]
    difficulties: list[Facet]
    tech_tags: list[Facet]
    sources: list[Facet]


class StatsOut(BaseModel):
    problems: int
    sources: int
    fields: int
    projects: int


class ProblemsListOut(BaseModel):
    items: list[ProblemOut]
    total: int


# ============================================================================
# Project 1: Webhook Reliability & Event Delivery Infrastructure
# ============================================================================

class WebhookEndpointBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    url: str = Field(min_length=1, max_length=1000)
    secret: str | None = Field(default=None, max_length=500)
    retry_max_attempts: int = Field(default=5, ge=1, le=50)
    retry_initial_delay_ms: int = Field(default=1000, ge=100)
    retry_max_delay_ms: int = Field(default=300000, ge=1000)
    timeout_ms: int = Field(default=30000, ge=1000, le=300000)
    event_types: list[str] = Field(default=list, max_length=50)


class WebhookEndpointCreate(WebhookEndpointBase):
    pass


class WebhookEndpointUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    url: str | None = Field(default=None, min_length=1, max_length=1000)
    secret: str | None = Field(default=None, max_length=500)
    status: str | None = None
    retry_max_attempts: int | None = Field(default=None, ge=1, le=50)
    retry_initial_delay_ms: int | None = Field(default=None, ge=100)
    retry_max_delay_ms: int | None = Field(default=None, ge=1000)
    timeout_ms: int | None = Field(default=None, ge=1000, le=300000)
    event_types: list[str] | None = Field(default=None, max_length=50)


class WebhookEndpointOut(WebhookEndpointBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime


class WebhookEventBase(BaseModel):
    event_id: str = Field(min_length=1, max_length=255)
    event_type: str = Field(min_length=1, max_length=100)
    payload: dict = Field(default=dict)
    headers: dict = Field(default=dict)


class WebhookEventCreate(WebhookEventBase):
    endpoint_id: int


class WebhookEventOut(WebhookEventBase):
    id: int
    endpoint_id: int
    received_at: datetime


class WebhookDeliveryBase(BaseModel):
    endpoint_id: int
    event_id: int | None = None
    attempt_number: int = Field(default=1, ge=1)
    status: str
    http_status: int | None = None
    response_body: str | None = None
    error_message: str | None = None


class WebhookDeliveryOut(WebhookDeliveryBase):
    id: int
    scheduled_at: datetime
    attempted_at: datetime | None
    next_retry_at: datetime | None
    created_at: datetime


class WebhookDeliveryCreate(BaseModel):
    endpoint_id: int
    event_id: int | None = None
    status: str = "queued"
    scheduled_at: datetime | None = None


# ============================================================================
# Project 2: API Contract Drift & Breaking Change Detection Platform
# ============================================================================

class ApiSpecBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=100)
    spec: dict = Field(default=dict)
    source_type: str = Field(default="upload", max_length=50)
    source_url: str | None = Field(default=None, max_length=1000)


class ApiSpecCreate(ApiSpecBase):
    pass


class ApiSpecUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str | None = Field(default=None, min_length=1, max_length=100)
    spec: dict | None = None
    source_type: str | None = Field(default=None, max_length=50)
    source_url: str | None = Field(default=None, max_length=1000)
    status: str | None = None


class ApiSpecOut(ApiSpecBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime


class ApiContractComparisonBase(BaseModel):
    spec_b_id: int
    comparison: dict = Field(default=dict)
    affected_endpoints: list[str] = Field(default=list, max_length=100)


class ApiContractComparisonCreate(ApiContractComparisonBase):
    spec_a_id: int


class ApiContractComparisonOut(ApiContractComparisonBase):
    id: int
    spec_a_id: int
    breaking_changes_count: int
    non_breaking_changes_count: int
    created_at: datetime


class ApiMonitoringTargetBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_url: str = Field(min_length=1, max_length=1000)
    spec_id: int | None = None
    check_interval_seconds: int = Field(default=3600, ge=60)
    is_active: bool = True


class ApiMonitoringTargetCreate(ApiMonitoringTargetBase):
    pass


class ApiMonitoringTargetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    base_url: str | None = Field(default=None, min_length=1, max_length=1000)
    spec_id: int | None = None
    check_interval_seconds: int | None = Field(default=None, ge=60)
    is_active: bool | None = None


class ApiMonitoringTargetOut(ApiMonitoringTargetBase):
    id: int
    user_id: int
    last_checked_at: datetime | None
    created_at: datetime


class ApiContractCheckBase(BaseModel):
    status: str
    breaking_changes_detected: int = Field(default=0, ge=0)
    results: dict = Field(default=dict)


class ApiContractCheckCreate(ApiContractCheckBase):
    target_id: int


class ApiContractCheckOut(ApiContractCheckBase):
    id: int
    target_id: int
    checked_at: datetime


# ============================================================================
# Project 3: Multi-Tenant Security & Authorization Audit Platform
# ============================================================================

class TenantBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=100)
    plan: str = Field(default="free", max_length=50)
    settings: dict = Field(default=dict)


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    plan: str | None = Field(default=None, max_length=50)
    settings: dict | None = None


class TenantOut(TenantBase):
    id: int
    created_at: datetime


class TenantMembershipBase(BaseModel):
    user_id: int
    tenant_id: int
    role: str = Field(default="member", max_length=50)


class TenantMembershipCreate(TenantMembershipBase):
    pass


class TenantMembershipOut(TenantMembershipBase):
    id: int
    joined_at: datetime


class TenantResourceBase(BaseModel):
    tenant_id: int
    resource_type: str = Field(min_length=1, max_length=100)
    resource_id: str = Field(min_length=1, max_length=255)
    owner_user_id: int | None = None
    metadata: dict = Field(default=dict)


class TenantResourceCreate(TenantResourceBase):
    pass


class TenantResourceOut(TenantResourceBase):
    id: int
    created_at: datetime


class SecurityFindingBase(BaseModel):
    tenant_id: int
    check_type: str = Field(min_length=1, max_length=100)
    severity: str
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1)
    affected_resource: str | None = Field(default=None, max_length=500)
    remediation: str | None = None
    status: str = Field(default="open", max_length=20)


class SecurityFindingCreate(SecurityFindingBase):
    pass


class SecurityFindingUpdate(BaseModel):
    severity: str | None = None
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, min_length=1)
    affected_resource: str | None = Field(default=None, max_length=500)
    remediation: str | None = None
    status: str | None = Field(default=None, max_length=20)


class SecurityFindingOut(SecurityFindingBase):
    id: int
    detected_at: datetime
    resolved_at: datetime | None


class RolePermissionBase(BaseModel):
    role: str = Field(min_length=1, max_length=50)
    permission: str = Field(min_length=1, max_length=100)
    resource_type: str | None = Field(default=None, max_length=100)


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionOut(RolePermissionBase):
    id: int


# ============================================================================
# Project 4: Real-Time Incident Response & Investigation Platform
# ============================================================================

class IncidentBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1)
    severity: str
    assignee_user_id: int | None = None
    tags: list[str] = Field(default=list, max_length=20)


class IncidentCreate(IncidentBase):
    reporter_user_id: int | None = None


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, min_length=1)
    severity: str | None = None
    status: str | None = None
    assignee_user_id: int | None = None
    tags: list[str] | None = Field(default=None, max_length=20)
    postmortem_url: str | None = Field(default=None, max_length=1000)


class IncidentOut(IncidentBase):
    id: int
    reporter_user_id: int | None
    assignee_user_id: int | None
    status: str
    started_at: datetime
    resolved_at: datetime | None
    closed_at: datetime | None
    postmortem_url: str | None
    created_at: datetime


class IncidentEventBase(BaseModel):
    incident_id: int
    source: str = Field(min_length=1, max_length=100)
    source_id: str | None = Field(default=None, max_length=255)
    event_type: str = Field(min_length=1, max_length=100)
    payload: dict = Field(default=dict)
    occurred_at: datetime


class IncidentEventCreate(IncidentEventBase):
    pass


class IncidentEventOut(IncidentEventBase):
    id: int
    created_at: datetime


class IncidentAssignmentBase(BaseModel):
    incident_id: int
    user_id: int
    role: str = Field(min_length=1, max_length=100)


class IncidentAssignmentCreate(IncidentAssignmentBase):
    pass


class IncidentAssignmentOut(IncidentAssignmentBase):
    id: int
    assigned_at: datetime
    unassigned_at: datetime | None


class IncidentTimelineEntryBase(BaseModel):
    incident_id: int
    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
    entry_type: str = Field(min_length=1, max_length=50)
    occurred_at: datetime
    created_by_user_id: int | None = None
    metadata: dict = Field(default=dict)


class IncidentTimelineEntryCreate(IncidentTimelineEntryBase):
    pass


class IncidentTimelineEntryOut(IncidentTimelineEntryBase):
    id: int
    created_at: datetime


# ============================================================================
# Project 5: Intelligent Large-Scale File Ingestion & Processing Platform
# ============================================================================

class IngestionJobBase(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    config: dict = Field(default=dict)


class IngestionJobCreate(IngestionJobBase):
    pass


class IngestionJobUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=500)
    config: dict | None = None


class IngestionJobOut(IngestionJobBase):
    id: int
    user_id: int
    status: str
    total_files: int
    processed_files: int
    failed_files: int
    skipped_duplicates: int
    result_summary: dict | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None


class IngestedFileBase(BaseModel):
    job_id: int
    original_filename: str = Field(min_length=1, max_length=500)
    stored_path: str = Field(min_length=1, max_length=1000)
    content_hash: str | None = Field(default=None, max_length=64)
    file_size: int = Field(ge=0)
    mime_type: str | None = Field(default=None, max_length=200)
    is_duplicate: bool = False
    duplicate_of_file_id: int | None = None


class IngestedFileCreate(IngestedFileBase):
    pass


class IngestedFileOut(IngestedFileBase):
    id: int
    status: str
    validation_errors: list[str]
    processing_result: dict | None
    created_at: datetime


class ProcessingWorkerBase(BaseModel):
    worker_name: str = Field(min_length=1, max_length=255)
    status: str = Field(default="idle", max_length=20)


class ProcessingWorkerCreate(ProcessingWorkerBase):
    pass


class ProcessingWorkerOut(ProcessingWorkerBase):
    id: int
    last_heartbeat_at: datetime | None
    current_job_id: int | None
    created_at: datetime


# ============================================================================
# Project 6: Privacy-First Product Analytics Infrastructure
# ============================================================================

class AnalyticsEventBase(BaseModel):
    project_id: str = Field(min_length=1, max_length=255)
    session_id: str = Field(min_length=1, max_length=255)
    anonymous_id: str = Field(min_length=1, max_length=255)
    event_name: str = Field(min_length=1, max_length=200)
    event_properties: dict = Field(default=dict)
    user_properties: dict = Field(default=dict)
    timestamp: datetime


class AnalyticsEventCreate(AnalyticsEventBase):
    pass


class AnalyticsEventOut(AnalyticsEventBase):
    id: int
    consumed_at: datetime | None


class ConsentRecordBase(BaseModel):
    anonymous_id: str = Field(min_length=1, max_length=255)
    consent_status: str = Field(default="unknown", max_length=20)
    consent_version: str | None = Field(default=None, max_length=50)


class ConsentRecordCreate(ConsentRecordBase):
    pass


class ConsentRecordUpdate(BaseModel):
    consent_status: str | None = Field(default=None, max_length=20)
    consent_version: str | None = Field(default=None, max_length=50)


class ConsentRecordOut(ConsentRecordBase):
    id: int
    updated_at: datetime


class DataRetentionPolicyBase(BaseModel):
    project_id: str = Field(min_length=1, max_length=255)
    event_retention_days: int = Field(default=90, ge=1)
    raw_data_retention_days: int = Field(default=30, ge=1)
    is_active: bool = True


class DataRetentionPolicyCreate(DataRetentionPolicyBase):
    pass


class DataRetentionPolicyUpdate(BaseModel):
    event_retention_days: int | None = Field(default=None, ge=1)
    raw_data_retention_days: int | None = Field(default=None, ge=1)
    is_active: bool | None = None


class DataRetentionPolicyOut(DataRetentionPolicyBase):
    id: int
    created_at: datetime


class FunnelDefinitionBase(BaseModel):
    project_id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    steps: list[dict] = Field(default=list, max_length=50)


class FunnelDefinitionCreate(FunnelDefinitionBase):
    pass


class FunnelDefinitionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    steps: list[dict] | None = Field(default=None, max_length=50)


class FunnelDefinitionOut(FunnelDefinitionBase):
    id: int
    created_at: datetime


class RetentionCohortBase(BaseModel):
    project_id: str = Field(min_length=1, max_length=255)
    cohort_date: date
    cohort_size: int = Field(default=0, ge=0)
    retention: dict = Field(default=dict)


class RetentionCohortCreate(RetentionCohortBase):
    pass


class RetentionCohortOut(RetentionCohortBase):
    id: int
    computed_at: datetime


# ============================================================================
# Project 7: Continuous Website Accessibility Monitoring Platform
# ============================================================================

class MonitoredWebsiteBase(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    url: str = Field(min_length=1, max_length=1000)
    scan_interval_minutes: int = Field(default=1440, ge=5)
    wcag_level: str = Field(default="AA", max_length=10)
    is_active: bool = True


class MonitoredWebsiteCreate(MonitoredWebsiteBase):
    pass


class MonitoredWebsiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=500)
    url: str | None = Field(default=None, min_length=1, max_length=1000)
    scan_interval_minutes: int | None = Field(default=None, ge=5)
    wcag_level: str | None = Field(default=None, max_length=10)
    is_active: bool | None = None


class MonitoredWebsiteOut(MonitoredWebsiteBase):
    id: int
    user_id: int
    last_scan_at: datetime | None
    created_at: datetime


class AccessibilityScanBase(BaseModel):
    website_id: int
    wcag_level: str = Field(min_length=1, max_length=10)


class AccessibilityScanCreate(AccessibilityScanBase):
    pass


class AccessibilityScanOut(AccessibilityScanBase):
    id: int
    status: str
    pages_scanned: int
    issues_found: int
    score: float | None
    summary: dict
    started_at: datetime
    completed_at: datetime | None


class AccessibilityIssueBase(BaseModel):
    scan_id: int
    page_url: str = Field(min_length=1, max_length=1000)
    component_selector: str | None = Field(default=None, max_length=500)
    rule_id: str = Field(min_length=1, max_length=100)
    rule_name: str = Field(min_length=1, max_length=500)
    wcag_level: str = Field(min_length=1, max_length=10)
    severity: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1)
    remediation: str | None = None
    element_html: str | None = None


class AccessibilityIssueCreate(AccessibilityIssueBase):
    pass


class AccessibilityIssueOut(AccessibilityIssueBase):
    id: int
    detected_at: datetime
    is_resolved: bool


# ============================================================================
# Project 8: Cross-Platform Inventory Reservation & Consistency Engine
# ============================================================================

class SalesChannelBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    channel_type: str = Field(min_length=1, max_length=100)
    config: dict = Field(default=dict)
    is_active: bool = True


class SalesChannelCreate(SalesChannelBase):
    pass


class SalesChannelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    channel_type: str | None = Field(default=None, min_length=1, max_length=100)
    config: dict | None = None
    is_active: bool | None = None


class SalesChannelOut(SalesChannelBase):
    id: int
    created_at: datetime


class InventoryItemBase(BaseModel):
    channel_id: int
    sku: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=500)
    total_quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    available_quantity: int = Field(default=0, ge=0)
    reorder_threshold: int = Field(default=0, ge=0)
    metadata: dict = Field(default=dict)


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    sku: str | None = Field(default=None, min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=500)
    total_quantity: int | None = Field(default=None, ge=0)
    reserved_quantity: int | None = Field(default=None, ge=0)
    available_quantity: int | None = Field(default=None, ge=0)
    reorder_threshold: int | None = Field(default=None, ge=0)
    metadata: dict | None = None


class InventoryItemOut(InventoryItemBase):
    id: int
    updated_at: datetime


class InventoryReservationBase(BaseModel):
    item_id: int
    channel_id: int
    external_order_id: str | None = Field(default=None, max_length=500)
    quantity: int = Field(ge=1)
    expires_at: datetime | None = None


class InventoryReservationCreate(InventoryReservationBase):
    pass


class InventoryReservationUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=20)
    external_order_id: str | None = Field(default=None, max_length=500)


class InventoryReservationOut(InventoryReservationBase):
    id: int
    status: str
    reserved_at: datetime
    consumed_at: datetime | None
    released_at: datetime | None


class StockReconciliationBase(BaseModel):
    item_id: int
    expected_quantity: int = Field(ge=0)
    actual_quantity: int = Field(ge=0)
    reason: str | None = Field(default=None, max_length=500)


class StockReconciliationCreate(StockReconciliationBase):
    reconciled_by_user_id: int | None = None


class StockReconciliationOut(StockReconciliationBase):
    id: int
    discrepancy: int
    reconciled_by_user_id: int | None
    reconciled_at: datetime


# ============================================================================
# Project 9: Offline-First Data Synchronization & Conflict Resolution Platform
# ============================================================================

class SyncRecordBase(BaseModel):
    device_id: str = Field(min_length=1, max_length=255)
    collection: str = Field(min_length=1, max_length=200)
    record_id: str = Field(min_length=1, max_length=255)
    version_vector: dict = Field(default=dict)
    data: dict = Field(default=dict)
    operation: str = Field(min_length=1, max_length=20)


class SyncRecordCreate(SyncRecordBase):
    pass


class SyncRecordUpdate(BaseModel):
    version_vector: dict | None = None
    data: dict | None = None
    operation: str | None = Field(default=None, min_length=1, max_length=20)
    status: str | None = Field(default=None, max_length=20)
    conflict_with_record_id: str | None = Field(default=None, max_length=255)


class SyncRecordOut(SyncRecordBase):
    id: int
    status: str
    synced_at: datetime | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime


class SyncConflictBase(BaseModel):
    collection: str = Field(min_length=1, max_length=200)
    record_id: str = Field(min_length=1, max_length=255)
    local_version: dict = Field(default=dict)
    remote_version: dict = Field(default=dict)
    local_vector: dict = Field(default=dict)
    remote_vector: dict = Field(default=dict)
    resolution_strategy: str | None = Field(default=None, max_length=100)
    resolved_data: dict | None = None


class SyncConflictCreate(SyncConflictBase):
    pass


class SyncConflictUpdate(BaseModel):
    resolution_strategy: str | None = Field(default=None, max_length=100)
    resolved_data: dict | None = None
    status: str | None = Field(default=None, max_length=20)


class SyncConflictOut(SyncConflictBase):
    id: int
    status: str
    created_at: datetime
    resolved_at: datetime | None


# ============================================================================
# Project 10: Visual Workflow Execution & Automation Engine
# ============================================================================

class WorkflowBase(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    description: str | None = None
    definition: dict = Field(default=dict)
    trigger_type: str | None = Field(default=None, max_length=50)
    trigger_config: dict = Field(default=dict)


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    definition: dict | None = None
    status: str | None = Field(default=None, max_length=20)
    trigger_type: str | None = Field(default=None, max_length=50)
    trigger_config: dict | None = None


class WorkflowOut(WorkflowBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime


class WorkflowExecutionBase(BaseModel):
    workflow_id: int
    trigger_payload: dict = Field(default=dict)
    context: dict = Field(default=dict)


class WorkflowExecutionCreate(WorkflowExecutionBase):
    pass


class WorkflowExecutionOut(WorkflowExecutionBase):
    id: int
    status: str
    started_at: datetime
    completed_at: datetime | None
    error_message: str | None


class WorkflowStepExecutionBase(BaseModel):
    execution_id: int
    step_id: str = Field(min_length=1, max_length=255)
    step_type: str = Field(min_length=1, max_length=100)
    input: dict = Field(default=dict)
    max_retries: int = Field(default=3, ge=0)
    depends_on: list[str] = Field(default=list, max_length=20)


class WorkflowStepExecutionCreate(WorkflowStepExecutionBase):
    pass


class WorkflowStepExecutionOut(WorkflowStepExecutionBase):
    id: int
    status: str
    output: dict | None
    error_message: str | None
    attempt_number: int
    started_at: datetime | None
    completed_at: datetime | None


