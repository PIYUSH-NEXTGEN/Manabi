// Advanced project API clients — 10 project domains
import { apiFetch } from './client';

/* ============================================================================
   Project 1: Webhook Reliability & Event Delivery
   ========================================================================== */

export interface WebhookEndpoint {
  id: number;
  user_id: number;
  name: string;
  url: string;
  secret: string | null;
  status: string;
  retry_max_attempts: number;
  retry_initial_delay_ms: number;
  retry_max_delay_ms: number;
  timeout_ms: number;
  event_types: string[];
  created_at: string;
  updated_at: string;
}

export interface WebhookEndpointCreate {
  name: string;
  url: string;
  secret?: string;
  retry_max_attempts?: number;
  retry_initial_delay_ms?: number;
  retry_max_delay_ms?: number;
  timeout_ms?: number;
  event_types?: string[];
}

export interface WebhookEndpointUpdate {
  name?: string;
  url?: string;
  secret?: string;
  status?: string;
  retry_max_attempts?: number;
  retry_initial_delay_ms?: number;
  retry_max_delay_ms?: number;
  timeout_ms?: number;
  event_types?: string[];
}

export interface WebhookEvent {
  id: number;
  endpoint_id: number;
  event_id: string;
  event_type: string;
  payload: Record<string, unknown>;
  headers: Record<string, unknown>;
  received_at: string;
}

export interface WebhookEventCreate {
  endpoint_id: number;
  event_id: string;
  event_type: string;
  payload?: Record<string, unknown>;
  headers?: Record<string, unknown>;
}

export interface WebhookDelivery {
  id: number;
  endpoint_id: number;
  event_id: number | null;
  attempt_number: number;
  status: string;
  http_status: number | null;
  response_body: string | null;
  error_message: string | null;
  scheduled_at: string;
  attempted_at: string | null;
  next_retry_at: string | null;
  created_at: string;
}

export interface WebhookDeliveryCreate {
  endpoint_id: number;
  event_id?: number;
  status?: string;
  scheduled_at?: string;
}

export interface DeliveryStats {
  total_endpoints: number;
  active_endpoints: number;
  total_deliveries: number;
  failed_deliveries: number;
  dead_letter_deliveries: number;
  success_rate: number;
}

export function listWebhookEndpoints(): Promise<WebhookEndpoint[]> {
  return apiFetch<WebhookEndpoint[]>('/api/webhooks/endpoints');
}

export function createWebhookEndpoint(body: WebhookEndpointCreate): Promise<WebhookEndpoint> {
  return apiFetch<WebhookEndpoint>('/api/webhooks/endpoints', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getWebhookEndpoint(id: number): Promise<WebhookEndpoint> {
  return apiFetch<WebhookEndpoint>(`/api/webhooks/endpoints/${id}`);
}

export function updateWebhookEndpoint(id: number, body: WebhookEndpointUpdate): Promise<WebhookEndpoint> {
  return apiFetch<WebhookEndpoint>(`/api/webhooks/endpoints/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteWebhookEndpoint(id: number): Promise<void> {
  return apiFetch<void>(`/api/webhooks/endpoints/${id}`, { method: 'DELETE' });
}

export function ingestWebhookEvent(endpointId: number, body: WebhookEventCreate): Promise<WebhookEvent> {
  return apiFetch<WebhookEvent>(`/api/webhooks/endpoints/${endpointId}/events`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listWebhookEvents(
  endpointId: number,
  limit = 50,
): Promise<WebhookEvent[]> {
  return apiFetch<WebhookEvent[]>(
    `/api/webhooks/endpoints/${endpointId}/events?limit=${limit}`,
  );
}

export function createWebhookDelivery(body: WebhookDeliveryCreate): Promise<WebhookDelivery> {
  return apiFetch<WebhookDelivery>('/api/webhooks/deliveries', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listWebhookDeliveries({
  endpointId,
  status,
  limit = 50,
}: {
  endpointId?: number;
  status?: string;
  limit?: number;
}): Promise<WebhookDelivery[]> {
  const params = new URLSearchParams();
  if (endpointId != null) params.set('endpoint_id', String(endpointId));
  if (status) params.set('status', status);
  if (limit != null) params.set('limit', String(limit));
  return apiFetch<WebhookDelivery[]>(
    `/api/webhooks/deliveries${params.toString() ? `?${params}` : ''}`,
  );
}

export function getWebhookDelivery(id: number): Promise<WebhookDelivery> {
  return apiFetch<WebhookDelivery>(`/api/webhooks/deliveries/${id}`);
}

export function updateWebhookDelivery(
  id: number,
  body: Partial<WebhookDelivery>,
): Promise<WebhookDelivery> {
  return apiFetch<WebhookDelivery>(`/api/webhooks/deliveries/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function retryWebhookDelivery(id: number): Promise<WebhookDelivery> {
  return apiFetch<WebhookDelivery>(`/api/webhooks/deliveries/${id}/retry`, {
    method: 'POST',
  });
}

export function getDeliveryStats(): Promise<DeliveryStats> {
  return apiFetch<DeliveryStats>('/api/webhooks/stats/summary');
}

/* ============================================================================
   Project 2: API Contract Drift & Breaking Change Detection
   ========================================================================== */

export interface ApiSpec {
  id: number;
  user_id: number;
  name: string;
  version: string;
  spec: Record<string, unknown>;
  source_type: string;
  source_url: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ApiSpecCreate {
  name: string;
  version: string;
  spec: Record<string, unknown>;
  source_type?: string;
  source_url?: string;
}

export interface ApiSpecUpdate {
  name?: string;
  version?: string;
  spec?: Record<string, unknown>;
  source_type?: string;
  source_url?: string;
  status?: string;
}

export interface ApiContractComparison {
  id: number;
  spec_a_id: number;
  spec_b_id: number;
  breaking_changes_count: number;
  non_breaking_changes_count: number;
  comparison: Record<string, unknown>;
  affected_endpoints: string[];
  created_at: string;
}

export interface ApiContractComparisonCreate {
  spec_a_id: number;
  spec_b_id: number;
  comparison: Record<string, unknown>;
  affected_endpoints: string[];
}

export interface ApiMonitoringTarget {
  id: number;
  user_id: number;
  name: string;
  base_url: string;
  spec_id: number | null;
  check_interval_seconds: number;
  last_checked_at: string | null;
  is_active: boolean;
  created_at: string;
}

export interface ApiMonitoringTargetCreate {
  name: string;
  base_url: string;
  spec_id?: number;
  check_interval_seconds?: number;
  is_active?: boolean;
}

export interface ApiMonitoringTargetUpdate {
  name?: string;
  base_url?: string;
  spec_id?: number;
  check_interval_seconds?: number;
  is_active?: boolean;
}

export interface ApiContractCheck {
  id: number;
  target_id: number;
  status: string;
  breaking_changes_detected: number;
  results: Record<string, unknown>;
  checked_at: string;
}

export interface ApiContractCheckCreate {
  target_id: number;
  status: string;
  breaking_changes_detected?: number;
  results?: Record<string, unknown>;
}

export function listApiSpecs(): Promise<ApiSpec[]> {
  return apiFetch<ApiSpec[]>('/api/api-contracts/specs');
}

export function createApiSpec(body: ApiSpecCreate): Promise<ApiSpec> {
  return apiFetch<ApiSpec>('/api/api-contracts/specs', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getApiSpec(id: number): Promise<ApiSpec> {
  return apiFetch<ApiSpec>(`/api/api-contracts/specs/${id}`);
}

export function updateApiSpec(id: number, body: ApiSpecUpdate): Promise<ApiSpec> {
  return apiFetch<ApiSpec>(`/api/api-contracts/specs/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteApiSpec(id: number): Promise<void> {
  return apiFetch<void>(`/api/api-contracts/specs/${id}`, { method: 'DELETE' });
}

export function createApiComparison(
  body: ApiContractComparisonCreate,
): Promise<ApiContractComparison> {
  return apiFetch<ApiContractComparison>('/api/api-contracts/comparisons', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listApiComparisons(limit = 50): Promise<ApiContractComparison[]> {
  return apiFetch<ApiContractComparison[]>(
    `/api/api-contracts/comparisons?limit=${limit}`,
  );
}

export function getApiComparison(id: number): Promise<ApiContractComparison> {
  return apiFetch<ApiContractComparison>(`/api/api-contracts/comparisons/${id}`);
}

export function listMonitoringTargets(): Promise<ApiMonitoringTarget[]> {
  return apiFetch<ApiMonitoringTarget[]>('/api/api-contracts/monitoring-targets');
}

export function createMonitoringTarget(
  body: ApiMonitoringTargetCreate,
): Promise<ApiMonitoringTarget> {
  return apiFetch<ApiMonitoringTarget>('/api/api-contracts/monitoring-targets', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function updateMonitoringTarget(
  id: number,
  body: ApiMonitoringTargetUpdate,
): Promise<ApiMonitoringTarget> {
  return apiFetch<ApiMonitoringTarget>(`/api/api-contracts/monitoring-targets/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteMonitoringTarget(id: number): Promise<void> {
  return apiFetch<void>(`/api/api-contracts/monitoring-targets/${id}`, {
    method: 'DELETE',
  });
}

export function runContractCheck(targetId: number): Promise<ApiContractCheck> {
  return apiFetch<ApiContractCheck>(
    `/api/api-contracts/monitoring-targets/${targetId}/check`,
    { method: 'POST' },
  );
}

export function listContractChecks(
  targetId: number,
  limit = 50,
): Promise<ApiContractCheck[]> {
  return apiFetch<ApiContractCheck[]>(
    `/api/api-contracts/monitoring-targets/${targetId}/checks?limit=${limit}`,
  );
}

/* ============================================================================
   Project 3: Multi-Tenant Security & Authorization Audit
   ========================================================================== */

export interface Tenant {
  id: number;
  name: string;
  slug: string;
  plan: string;
  settings: Record<string, unknown>;
  created_at: string;
}

export interface TenantCreate {
  name: string;
  slug: string;
  plan?: string;
  settings?: Record<string, unknown>;
}

export interface TenantUpdate {
  name?: string;
  slug?: string;
  plan?: string;
  settings?: Record<string, unknown>;
}

export interface TenantMembership {
  id: number;
  user_id: number;
  tenant_id: number;
  role: string;
  joined_at: string;
}

export interface TenantMembershipCreate {
  user_id: number;
  tenant_id: number;
  role?: string;
}

export interface TenantResource {
  id: number;
  tenant_id: number;
  resource_type: string;
  resource_id: string;
  owner_user_id: number | null;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface TenantResourceCreate {
  tenant_id: number;
  resource_type: string;
  resource_id: string;
  owner_user_id?: number;
  metadata?: Record<string, unknown>;
}

export interface SecurityFinding {
  id: number;
  tenant_id: number;
  check_type: string;
  severity: string;
  title: string;
  description: string;
  affected_resource: string | null;
  remediation: string | null;
  status: string;
  detected_at: string;
  resolved_at: string | null;
}

export interface SecurityFindingCreate {
  tenant_id: number;
  check_type: string;
  severity: string;
  title: string;
  description: string;
  affected_resource?: string;
  remediation?: string;
  status?: string;
}

export interface SecurityFindingUpdate {
  severity?: string;
  title?: string;
  description?: string;
  affected_resource?: string;
  remediation?: string;
  status?: string;
}

export interface RolePermission {
  id: number;
  role: string;
  permission: string;
  resource_type: string | null;
}

export interface RolePermissionCreate {
  role: string;
  permission: string;
  resource_type?: string;
}

export interface AuditSummary {
  total_tenants: number;
  open_findings: number;
  critical_findings: number;
  high_findings: number;
}

export function listTenants(): Promise<Tenant[]> {
  return apiFetch<Tenant[]>('/api/tenant-security/tenants');
}

export function createTenant(body: TenantCreate): Promise<Tenant> {
  return apiFetch<Tenant>('/api/tenant-security/tenants', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getTenant(id: number): Promise<Tenant> {
  return apiFetch<Tenant>(`/api/tenant-security/tenants/${id}`);
}

export function updateTenant(id: number, body: TenantUpdate): Promise<Tenant> {
  return apiFetch<Tenant>(`/api/tenant-security/tenants/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteTenant(id: number): Promise<void> {
  return apiFetch<void>(`/api/tenant-security/tenants/${id}`, { method: 'DELETE' });
}

export function listMemberships(tenantId: number): Promise<TenantMembership[]> {
  return apiFetch<TenantMembership[]>(
    `/api/tenant-security/tenants/${tenantId}/memberships`,
  );
}

export function createMembership(
  tenantId: number,
  body: TenantMembershipCreate,
): Promise<TenantMembership> {
  return apiFetch<TenantMembership>(
    `/api/tenant-security/tenants/${tenantId}/memberships`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function updateMembership(
  tenantId: number,
  membershipId: number,
  body: { role?: string },
): Promise<TenantMembership> {
  return apiFetch<TenantMembership>(
    `/api/tenant-security/tenants/${tenantId}/memberships/${membershipId}`,
    { method: 'PATCH', body: JSON.stringify(body) },
  );
}

export function deleteMembership(tenantId: number, membershipId: number): Promise<void> {
  return apiFetch<void>(
    `/api/tenant-security/tenants/${tenantId}/memberships/${membershipId}`,
    { method: 'DELETE' },
  );
}

export function listResources(tenantId: number): Promise<TenantResource[]> {
  return apiFetch<TenantResource[]>(
    `/api/tenant-security/tenants/${tenantId}/resources`,
  );
}

export function createResource(
  tenantId: number,
  body: TenantResourceCreate,
): Promise<TenantResource> {
  return apiFetch<TenantResource>(
    `/api/tenant-security/tenants/${tenantId}/resources`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function listFindings(
  tenantId: number,
  { severity, status }: { severity?: string; status?: string } = {},
): Promise<SecurityFinding[]> {
  const params = new URLSearchParams();
  if (severity) params.set('severity', severity);
  if (status) params.set('status', status);
  return apiFetch<SecurityFinding[]>(
    `/api/tenant-security/tenants/${tenantId}/findings${params.toString() ? `?${params}` : ''}`,
  );
}

export function createFinding(
  body: SecurityFindingCreate,
): Promise<SecurityFinding> {
  return apiFetch<SecurityFinding>('/api/tenant-security/findings', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function updateFinding(
  id: number,
  body: SecurityFindingUpdate,
): Promise<SecurityFinding> {
  return apiFetch<SecurityFinding>(`/api/tenant-security/findings/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function listRolePermissions(): Promise<RolePermission[]> {
  return apiFetch<RolePermission[]>('/api/tenant-security/roles/permissions');
}

export function createRolePermission(
  body: RolePermissionCreate,
): Promise<RolePermission> {
  return apiFetch<RolePermission>('/api/tenant-security/roles/permissions', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function deleteRolePermission(id: number): Promise<void> {
  return apiFetch<void>(`/api/tenant-security/roles/permissions/${id}`, {
    method: 'DELETE',
  });
}

export function getAuditSummary(): Promise<AuditSummary> {
  return apiFetch<AuditSummary>('/api/tenant-security/audit/summary');
}

/* ============================================================================
   Project 4: Real-Time Incident Response & Investigation
   ========================================================================== */

export interface Incident {
  id: number;
  title: string;
  description: string;
  severity: string;
  status: string;
  reporter_user_id: number | null;
  assignee_user_id: number | null;
  started_at: string;
  resolved_at: string | null;
  closed_at: string | null;
  postmortem_url: string | null;
  tags: string[];
}

export interface IncidentCreate {
  title: string;
  description: string;
  severity: string;
  assignee_user_id?: number;
  tags?: string[];
  reporter_user_id?: number;
}

export interface IncidentUpdate {
  title?: string;
  description?: string;
  severity?: string;
  status?: string;
  assignee_user_id?: number;
  tags?: string[];
  postmortem_url?: string;
}

export interface IncidentEvent {
  id: number;
  incident_id: number;
  source: string;
  source_id: string | null;
  event_type: string;
  payload: Record<string, unknown>;
  occurred_at: string;
  created_at: string;
}

export interface IncidentEventCreate {
  incident_id: number;
  source: string;
  source_id?: string;
  event_type: string;
  payload?: Record<string, unknown>;
  occurred_at: string;
}

export interface IncidentAssignment {
  id: number;
  incident_id: number;
  user_id: number;
  role: string;
  assigned_at: string;
  unassigned_at: string | null;
}

export interface IncidentAssignmentCreate {
  incident_id: number;
  user_id: number;
  role: string;
}

export interface IncidentTimelineEntry {
  id: number;
  incident_id: number;
  title: string;
  description: string | null;
  entry_type: string;
  occurred_at: string;
  created_by_user_id: number | null;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface IncidentTimelineEntryCreate {
  incident_id: number;
  title: string;
  description?: string;
  entry_type: string;
  occurred_at: string;
  created_by_user_id?: number;
  metadata?: Record<string, unknown>;
}

export interface IncidentStats {
  total_incidents: number;
  open: number;
  investigating: number;
  resolved: number;
  critical: number;
}

export function listIncidents({
  status,
  severity,
}: { status?: string; severity?: string } = {}): Promise<Incident[]> {
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  if (severity) params.set('severity', severity);
  return apiFetch<Incident[]>(
    `/api/incidents${params.toString() ? `?${params}` : ''}`,
  );
}

export function createIncident(body: IncidentCreate): Promise<Incident> {
  return apiFetch<Incident>('/api/incidents', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getIncident(id: number): Promise<Incident> {
  return apiFetch<Incident>(`/api/incidents/${id}`);
}

export function updateIncident(id: number, body: IncidentUpdate): Promise<Incident> {
  return apiFetch<Incident>(`/api/incidents/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteIncident(id: number): Promise<void> {
  return apiFetch<void>(`/api/incidents/${id}`, { method: 'DELETE' });
}

export function createIncidentEvent(
  body: IncidentEventCreate,
): Promise<IncidentEvent> {
  return apiFetch<IncidentEvent>(`/api/incidents/${body.incident_id}/events`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listIncidentEvents(incidentId: number): Promise<IncidentEvent[]> {
  return apiFetch<IncidentEvent[]>(`/api/incidents/${incidentId}/events`);
}

export function createIncidentAssignment(
  body: IncidentAssignmentCreate,
): Promise<IncidentAssignment> {
  return apiFetch<IncidentAssignment>(
    `/api/incidents/${body.incident_id}/assignments`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function listIncidentAssignments(incidentId: number): Promise<IncidentAssignment[]> {
  return apiFetch<IncidentAssignment[]>(`/api/incidents/${incidentId}/assignments`);
}

export function createIncidentTimelineEntry(
  body: IncidentTimelineEntryCreate,
): Promise<IncidentTimelineEntry> {
  return apiFetch<IncidentTimelineEntry>(
    `/api/incidents/${body.incident_id}/timeline`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function listIncidentTimeline(incidentId: number): Promise<IncidentTimelineEntry[]> {
  return apiFetch<IncidentTimelineEntry[]>(`/api/incidents/${incidentId}/timeline`);
}

export function getIncidentStats(): Promise<IncidentStats> {
  return apiFetch<IncidentStats>('/api/incidents/stats/summary');
}

/* ============================================================================
   Project 5: Intelligent Large-Scale File Ingestion
   ========================================================================== */

export interface IngestionJob {
  id: number;
  user_id: number;
  name: string;
  status: string;
  total_files: number;
  processed_files: number;
  failed_files: number;
  skipped_duplicates: number;
  config: Record<string, unknown>;
  result_summary: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface IngestionJobCreate {
  name: string;
  config?: Record<string, unknown>;
}

export interface IngestionJobUpdate {
  name?: string;
  config?: Record<string, unknown>;
}

export interface IngestedFile {
  id: number;
  job_id: number;
  original_filename: string;
  stored_path: string;
  content_hash: string | null;
  file_size: number;
  mime_type: string | null;
  status: string;
  validation_errors: string[];
  is_duplicate: boolean;
  duplicate_of_file_id: number | null;
  processing_result: Record<string, unknown> | null;
  created_at: string;
}

export interface IngestedFileCreate {
  job_id: number;
  original_filename: string;
  stored_path: string;
  content_hash?: string;
  file_size: number;
  mime_type?: string;
  is_duplicate?: boolean;
  duplicate_of_file_id?: number;
}

export interface ProcessingWorker {
  id: number;
  worker_name: string;
  status: string;
  last_heartbeat_at: string | null;
  current_job_id: number | null;
  created_at: string;
}

export interface ProcessingWorkerCreate {
  worker_name: string;
  status?: string;
}

export interface IngestionStats {
  total_jobs: number;
  pending_jobs: number;
  total_files: number;
  duplicate_files: number;
}

export function listIngestionJobs({ status }: { status?: string } = {}): Promise<IngestionJob[]> {
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  return apiFetch<IngestionJob[]>(
    `/api/ingestion/jobs${params.toString() ? `?${params}` : ''}`,
  );
}

export function createIngestionJob(body: IngestionJobCreate): Promise<IngestionJob> {
  return apiFetch<IngestionJob>('/api/ingestion/jobs', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getIngestionJob(id: number): Promise<IngestionJob> {
  return apiFetch<IngestionJob>(`/api/ingestion/jobs/${id}`);
}

export function updateIngestionJob(id: number, body: IngestionJobUpdate): Promise<IngestionJob> {
  return apiFetch<IngestionJob>(`/api/ingestion/jobs/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteIngestionJob(id: number): Promise<void> {
  return apiFetch<void>(`/api/ingestion/jobs/${id}`, { method: 'DELETE' });
}

export function addIngestedFile(body: IngestedFileCreate): Promise<IngestedFile> {
  return apiFetch<IngestedFile>(`/api/ingestion/jobs/${body.job_id}/files`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listIngestedFiles(jobId: number): Promise<IngestedFile[]> {
  return apiFetch<IngestedFile[]>(`/api/ingestion/jobs/${jobId}/files`);
}

export function updateIngestedFile(id: number, body: Partial<IngestedFileCreate>): Promise<IngestedFile> {
  return apiFetch<IngestedFile>(`/api/ingestion/files/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createProcessingWorker(
  body: ProcessingWorkerCreate,
): Promise<ProcessingWorker> {
  return apiFetch<ProcessingWorker>('/api/ingestion/workers', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listProcessingWorkers(): Promise<ProcessingWorker[]> {
  return apiFetch<ProcessingWorker[]>('/api/ingestion/workers');
}

export function updateProcessingWorker(
  id: number,
  body: Partial<ProcessingWorkerCreate>,
): Promise<ProcessingWorker> {
  return apiFetch<ProcessingWorker>(`/api/ingestion/workers/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function getIngestionStats(): Promise<IngestionStats> {
  return apiFetch<IngestionStats>('/api/ingestion/stats/summary');
}

/* ============================================================================
   Project 6: Privacy-First Product Analytics
   ========================================================================== */

export interface AnalyticsEvent {
  id: number;
  project_id: string;
  session_id: string;
  anonymous_id: string;
  event_name: string;
  event_properties: Record<string, unknown>;
  user_properties: Record<string, unknown>;
  timestamp: string;
  consumed_at: string | null;
}

export interface AnalyticsEventCreate {
  project_id: string;
  session_id: string;
  anonymous_id: string;
  event_name: string;
  event_properties?: Record<string, unknown>;
  user_properties?: Record<string, unknown>;
  timestamp: string;
}

export interface ConsentRecord {
  id: number;
  anonymous_id: string;
  consent_status: string;
  consent_version: string | null;
  updated_at: string;
}

export interface ConsentRecordCreate {
  anonymous_id: string;
  consent_status?: string;
  consent_version?: string;
}

export interface ConsentRecordUpdate {
  consent_status?: string;
  consent_version?: string;
}

export interface DataRetentionPolicy {
  id: number;
  project_id: string;
  event_retention_days: number;
  raw_data_retention_days: number;
  is_active: boolean;
  created_at: string;
}

export interface DataRetentionPolicyCreate {
  project_id: string;
  event_retention_days?: number;
  raw_data_retention_days?: number;
  is_active?: boolean;
}

export interface DataRetentionPolicyUpdate {
  event_retention_days?: number;
  raw_data_retention_days?: number;
  is_active?: boolean;
}

export interface FunnelDefinition {
  id: number;
  project_id: string;
  name: string;
  steps: Record<string, unknown>[];
  created_at: string;
}

export interface FunnelDefinitionCreate {
  project_id: string;
  name: string;
  steps: Record<string, unknown>[];
}

export interface FunnelDefinitionUpdate {
  name?: string;
  steps?: Record<string, unknown>[];
}

export interface RetentionCohort {
  id: number;
  project_id: string;
  cohort_date: string;
  cohort_size: number;
  retention: Record<string, unknown>;
  computed_at: string;
}

export interface RetentionCohortCreate {
  project_id: string;
  cohort_date: string;
  cohort_size?: number;
  retention?: Record<string, unknown>;
}

export interface AnalyticsStats {
  total_events: number;
  total_projects: number;
  granted_consent: number;
  denied_consent: number;
}

export function ingestAnalyticsEvent(body: AnalyticsEventCreate): Promise<AnalyticsEvent> {
  return apiFetch<AnalyticsEvent>('/api/analytics/events', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listAnalyticsEvents({
  projectId,
  eventName,
  anonymousId,
  limit = 100,
}: {
  projectId: string;
  eventName?: string;
  anonymousId?: string;
  limit?: number;
}): Promise<AnalyticsEvent[]> {
  const params = new URLSearchParams({ project_id: projectId, limit: String(limit) });
  if (eventName) params.set('event_name', eventName);
  if (anonymousId) params.set('anonymous_id', anonymousId);
  return apiFetch<AnalyticsEvent[]>(`/api/analytics/events?${params}`);
}

export function getAnalyticsEventCount(
  projectId: string,
  eventName?: string,
): Promise<{ project_id: string; event_name: string | null; count: number }> {
  const params = new URLSearchParams({ project_id: projectId });
  if (eventName) params.set('event_name', eventName);
  return apiFetch<{ project_id: string; event_name: string | null; count: number }>(
    `/api/analytics/events/count?${params}`,
  );
}

export function setConsent(body: ConsentRecordCreate): Promise<ConsentRecord> {
  return apiFetch<ConsentRecord>('/api/analytics/consent', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getConsent(anonymousId: string): Promise<ConsentRecord> {
  return apiFetch<ConsentRecord>(`/api/analytics/consent/${anonymousId}`);
}

export function updateConsent(
  anonymousId: string,
  body: ConsentRecordUpdate,
): Promise<ConsentRecord> {
  return apiFetch<ConsentRecord>(`/api/analytics/consent/${anonymousId}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createRetentionPolicy(
  body: DataRetentionPolicyCreate,
): Promise<DataRetentionPolicy> {
  return apiFetch<DataRetentionPolicy>('/api/analytics/retention-policies', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listRetentionPolicies(): Promise<DataRetentionPolicy[]> {
  return apiFetch<DataRetentionPolicy[]>('/api/analytics/retention-policies');
}

export function updateRetentionPolicy(
  id: number,
  body: DataRetentionPolicyUpdate,
): Promise<DataRetentionPolicy> {
  return apiFetch<DataRetentionPolicy>(`/api/analytics/retention-policies/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createFunnel(body: FunnelDefinitionCreate): Promise<FunnelDefinition> {
  return apiFetch<FunnelDefinition>('/api/analytics/funnels', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listFunnels(projectId?: string): Promise<FunnelDefinition[]> {
  const params = new URLSearchParams();
  if (projectId) params.set('project_id', projectId);
  return apiFetch<FunnelDefinition[]>(
    `/api/analytics/funnels${params.toString() ? `?${params}` : ''}`,
  );
}

export function listRetentionCohorts(projectId: string): Promise<RetentionCohort[]> {
  return apiFetch<RetentionCohort[]>(
    `/api/analytics/retention-cohorts?project_id=${projectId}`,
  );
}

export function createRetentionCohort(
  body: RetentionCohortCreate,
): Promise<RetentionCohort> {
  return apiFetch<RetentionCohort>('/api/analytics/retention-cohorts', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getAnalyticsStats(): Promise<AnalyticsStats> {
  return apiFetch<AnalyticsStats>('/api/analytics/stats/summary');
}

/* ============================================================================
   Project 7: Continuous Website Accessibility Monitoring
   ========================================================================== */

export interface MonitoredWebsite {
  id: number;
  user_id: number;
  name: string;
  url: string;
  scan_interval_minutes: number;
  wcag_level: string;
  is_active: boolean;
  last_scan_at: string | null;
  created_at: string;
}

export interface MonitoredWebsiteCreate {
  name: string;
  url: string;
  scan_interval_minutes?: number;
  wcag_level?: string;
  is_active?: boolean;
}

export interface MonitoredWebsiteUpdate {
  name?: string;
  url?: string;
  scan_interval_minutes?: number;
  wcag_level?: string;
  is_active?: boolean;
}

export interface AccessibilityScan {
  id: number;
  website_id: number;
  status: string;
  pages_scanned: number;
  issues_found: number;
  wcag_level: string;
  score: number | null;
  summary: Record<string, unknown>;
  started_at: string;
  completed_at: string | null;
}

export interface AccessibilityScanCreate {
  website_id: number;
  wcag_level: string;
}

export interface AccessibilityIssue {
  id: number;
  scan_id: number;
  page_url: string;
  component_selector: string | null;
  rule_id: string;
  rule_name: string;
  wcag_level: string;
  severity: string;
  description: string;
  remediation: string | null;
  element_html: string | null;
  detected_at: string;
  is_resolved: boolean;
}

export interface AccessibilityIssueCreate {
  scan_id: number;
  page_url: string;
  component_selector?: string;
  rule_id: string;
  rule_name: string;
  wcag_level: string;
  severity: string;
  description: string;
  remediation?: string;
  element_html?: string;
}

export interface AccessibilityStats {
  total_websites: number;
  total_scans: number;
  total_issues: number;
  unresolved_issues: number;
}

export function listMonitoredWebsites({
  isActive,
}: { isActive?: boolean } = {}): Promise<MonitoredWebsite[]> {
  const params = new URLSearchParams();
  if (isActive != null) params.set('is_active', String(isActive));
  return apiFetch<MonitoredWebsite[]>(
    `/api/accessibility/websites${params.toString() ? `?${params}` : ''}`,
  );
}

export function createMonitoredWebsite(
  body: MonitoredWebsiteCreate,
): Promise<MonitoredWebsite> {
  return apiFetch<MonitoredWebsite>('/api/accessibility/websites', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getMonitoredWebsite(id: number): Promise<MonitoredWebsite> {
  return apiFetch<MonitoredWebsite>(`/api/accessibility/websites/${id}`);
}

export function updateMonitoredWebsite(
  id: number,
  body: MonitoredWebsiteUpdate,
): Promise<MonitoredWebsite> {
  return apiFetch<MonitoredWebsite>(`/api/accessibility/websites/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteMonitoredWebsite(id: number): Promise<void> {
  return apiFetch<void>(`/api/accessibility/websites/${id}`, { method: 'DELETE' });
}

export function createAccessibilityScan(
  body: AccessibilityScanCreate,
): Promise<AccessibilityScan> {
  return apiFetch<AccessibilityScan>(
    `/api/accessibility/websites/${body.website_id}/scans`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function listAccessibilityScans(
  websiteId: number,
  limit = 50,
): Promise<AccessibilityScan[]> {
  return apiFetch<AccessibilityScan[]>(
    `/api/accessibility/websites/${websiteId}/scans?limit=${limit}`,
  );
}

export function getAccessibilityScan(id: number): Promise<AccessibilityScan> {
  return apiFetch<AccessibilityScan>(`/api/accessibility/scans/${id}`);
}

export function updateAccessibilityScan(
  id: number,
  body: Partial<AccessibilityScanCreate>,
): Promise<AccessibilityScan> {
  return apiFetch<AccessibilityScan>(`/api/accessibility/scans/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createAccessibilityIssue(
  body: AccessibilityIssueCreate,
): Promise<AccessibilityIssue> {
  return apiFetch<AccessibilityIssue>(`/api/accessibility/scans/${body.scan_id}/issues`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listAccessibilityIssues(
  scanId: number,
  { severity, isResolved }: { severity?: string; isResolved?: boolean } = {},
): Promise<AccessibilityIssue[]> {
  const params = new URLSearchParams();
  if (severity) params.set('severity', severity);
  if (isResolved != null) params.set('is_resolved', String(isResolved));
  return apiFetch<AccessibilityIssue[]>(
    `/api/accessibility/scans/${scanId}/issues${params.toString() ? `?${params}` : ''}`,
  );
}

export function updateAccessibilityIssue(
  id: number,
  body: Partial<AccessibilityIssueCreate>,
): Promise<AccessibilityIssue> {
  return apiFetch<AccessibilityIssue>(`/api/accessibility/issues/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function getAccessibilityStats(): Promise<AccessibilityStats> {
  return apiFetch<AccessibilityStats>('/api/accessibility/stats/summary');
}

/* ============================================================================
   Project 8: Cross-Platform Inventory Reservation
   ========================================================================== */

export interface SalesChannel {
  id: number;
  name: string;
  channel_type: string;
  config: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
}

export interface SalesChannelCreate {
  name: string;
  channel_type: string;
  config?: Record<string, unknown>;
  is_active?: boolean;
}

export interface SalesChannelUpdate {
  name?: string;
  channel_type?: string;
  config?: Record<string, unknown>;
  is_active?: boolean;
}

export interface InventoryItem {
  id: number;
  channel_id: number;
  sku: string;
  name: string;
  total_quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  reorder_threshold: number;
  metadata: Record<string, unknown>;
  updated_at: string;
}

export interface InventoryItemCreate {
  channel_id: number;
  sku: string;
  name: string;
  total_quantity?: number;
  reserved_quantity?: number;
  available_quantity?: number;
  reorder_threshold?: number;
  metadata?: Record<string, unknown>;
}

export interface InventoryItemUpdate {
  sku?: string;
  name?: string;
  total_quantity?: number;
  reserved_quantity?: number;
  available_quantity?: number;
  reorder_threshold?: number;
  metadata?: Record<string, unknown>;
}

export interface InventoryReservation {
  id: number;
  item_id: number;
  channel_id: number;
  external_order_id: string | null;
  quantity: number;
  status: string;
  reserved_at: string;
  consumed_at: string | null;
  released_at: string | null;
}

export interface InventoryReservationCreate {
  item_id: number;
  channel_id: number;
  external_order_id?: string;
  quantity: number;
  expires_at?: string;
}

export interface InventoryReservationUpdate {
  status?: string;
  external_order_id?: string;
}

export interface StockReconciliation {
  id: number;
  item_id: number;
  expected_quantity: number;
  actual_quantity: number;
  discrepancy: number;
  reason: string | null;
  reconciled_by_user_id: number | null;
  reconciled_at: string;
}

export interface StockReconciliationCreate {
  item_id: number;
  expected_quantity: number;
  actual_quantity: number;
  reason?: string;
  reconciled_by_user_id?: number;
}

export interface InventoryStats {
  total_items: number;
  total_channels: number;
  active_reservations: number;
  low_stock_items: number;
}

export function listSalesChannels(): Promise<SalesChannel[]> {
  return apiFetch<SalesChannel[]>('/api/inventory/channels');
}

export function createSalesChannel(body: SalesChannelCreate): Promise<SalesChannel> {
  return apiFetch<SalesChannel>('/api/inventory/channels', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getSalesChannel(id: number): Promise<SalesChannel> {
  return apiFetch<SalesChannel>(`/api/inventory/channels/${id}`);
}

export function updateSalesChannel(id: number, body: SalesChannelUpdate): Promise<SalesChannel> {
  return apiFetch<SalesChannel>(`/api/inventory/channels/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteSalesChannel(id: number): Promise<void> {
  return apiFetch<void>(`/api/inventory/channels/${id}`, { method: 'DELETE' });
}

export function listInventoryItems({
  channelId,
  sku,
  lowStock,
}: {
  channelId?: number;
  sku?: string;
  lowStock?: boolean;
} = {}): Promise<InventoryItem[]> {
  const params = new URLSearchParams();
  if (channelId != null) params.set('channel_id', String(channelId));
  if (sku) params.set('sku', sku);
  if (lowStock != null) params.set('low_stock', String(lowStock));
  return apiFetch<InventoryItem[]>(
    `/api/inventory/items${params.toString() ? `?${params}` : ''}`,
  );
}

export function createInventoryItem(
  channelId: number,
  body: InventoryItemCreate,
): Promise<InventoryItem> {
  return apiFetch<InventoryItem>(`/api/inventory/channels/${channelId}/items`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getInventoryItem(id: number): Promise<InventoryItem> {
  return apiFetch<InventoryItem>(`/api/inventory/items/${id}`);
}

export function updateInventoryItem(
  id: number,
  body: InventoryItemUpdate,
): Promise<InventoryItem> {
  return apiFetch<InventoryItem>(`/api/inventory/items/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createInventoryReservation(
  body: InventoryReservationCreate,
): Promise<InventoryReservation> {
  return apiFetch<InventoryReservation>('/api/inventory/reservations', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listInventoryReservations({
  itemId,
  status,
}: { itemId?: number; status?: string } = {}): Promise<InventoryReservation[]> {
  const params = new URLSearchParams();
  if (itemId != null) params.set('item_id', String(itemId));
  if (status) params.set('status', status);
  return apiFetch<InventoryReservation[]>(
    `/api/inventory/reservations${params.toString() ? `?${params}` : ''}`,
  );
}

export function updateInventoryReservation(
  id: number,
  body: InventoryReservationUpdate,
): Promise<InventoryReservation> {
  return apiFetch<InventoryReservation>(`/api/inventory/reservations/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function createStockReconciliation(
  body: StockReconciliationCreate,
): Promise<StockReconciliation> {
  return apiFetch<StockReconciliation>('/api/inventory/reconciliations', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listStockReconciliations({ itemId }: { itemId?: number } = {}): Promise<StockReconciliation[]> {
  const params = new URLSearchParams();
  if (itemId != null) params.set('item_id', String(itemId));
  return apiFetch<StockReconciliation[]>(
    `/api/inventory/reconciliations${params.toString() ? `?${params}` : ''}`,
  );
}

export function getInventoryStats(): Promise<InventoryStats> {
  return apiFetch<InventoryStats>('/api/inventory/stats/summary');
}

/* ============================================================================
   Project 9: Offline-First Data Sync & Conflict Resolution
   ========================================================================== */

export interface SyncRecord {
  id: number;
  device_id: string;
  collection: string;
  record_id: string;
  version_vector: Record<string, unknown>;
  data: Record<string, unknown>;
  operation: string;
  status: string;
  conflict_with_record_id: string | null;
  synced_at: string | null;
  resolved_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface SyncRecordCreate {
  device_id: string;
  collection: string;
  record_id: string;
  version_vector?: Record<string, unknown>;
  data?: Record<string, unknown>;
  operation: string;
}

export interface SyncRecordUpdate {
  version_vector?: Record<string, unknown>;
  data?: Record<string, unknown>;
  operation?: string;
  status?: string;
  conflict_with_record_id?: string;
}

export interface SyncConflict {
  id: number;
  collection: string;
  record_id: string;
  local_version: Record<string, unknown>;
  remote_version: Record<string, unknown>;
  local_vector: Record<string, unknown>;
  remote_vector: Record<string, unknown>;
  resolution_strategy: string | null;
  resolved_data: Record<string, unknown> | null;
  status: string;
  created_at: string;
  resolved_at: string | null;
}

export interface SyncConflictCreate {
  collection: string;
  record_id: string;
  local_version?: Record<string, unknown>;
  remote_version?: Record<string, unknown>;
  local_vector?: Record<string, unknown>;
  remote_vector?: Record<string, unknown>;
  resolution_strategy?: string;
  resolved_data?: Record<string, unknown>;
}

export interface SyncConflictUpdate {
  resolution_strategy?: string;
  resolved_data?: Record<string, unknown>;
  status?: string;
}

export interface SyncStats {
  total_records: number;
  pending: number;
  synced: number;
  conflicts: number;
  open_conflicts: number;
}

export function createSyncRecord(body: SyncRecordCreate): Promise<SyncRecord> {
  return apiFetch<SyncRecord>('/api/sync/records', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listSyncRecords({
  deviceId,
  collection,
  status,
  limit = 100,
}: {
  deviceId?: string;
  collection?: string;
  status?: string;
  limit?: number;
} = {}): Promise<SyncRecord[]> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (deviceId) params.set('device_id', deviceId);
  if (collection) params.set('collection', collection);
  if (status) params.set('status', status);
  return apiFetch<SyncRecord[]>(`/api/sync/records?${params}`);
}

export function getSyncRecord(id: number): Promise<SyncRecord> {
  return apiFetch<SyncRecord>(`/api/sync/records/${id}`);
}

export function updateSyncRecord(id: number, body: SyncRecordUpdate): Promise<SyncRecord> {
  return apiFetch<SyncRecord>(`/api/sync/records/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function markSynced(id: number): Promise<SyncRecord> {
  return apiFetch<SyncRecord>(`/api/sync/records/${id}/sync`, { method: 'POST' });
}

export function markConflict(id: number, conflictWithRecordId: string): Promise<SyncRecord> {
  return apiFetch<SyncRecord>(
    `/api/sync/records/${id}/conflict?conflict_with_record_id=${encodeURIComponent(conflictWithRecordId)}`,
    { method: 'POST' },
  );
}

export function listSyncConflicts({
  collection,
  status,
}: { collection?: string; status?: string } = {}): Promise<SyncConflict[]> {
  const params = new URLSearchParams();
  if (collection) params.set('collection', collection);
  if (status) params.set('status', status);
  return apiFetch<SyncConflict[]>(
    `/api/sync/conflicts${params.toString() ? `?${params}` : ''}`,
  );
}

export function getSyncConflict(id: number): Promise<SyncConflict> {
  return apiFetch<SyncConflict>(`/api/sync/conflicts/${id}`);
}

export function resolveSyncConflict(
  id: number,
  body: SyncConflictUpdate,
): Promise<SyncConflict> {
  return apiFetch<SyncConflict>(`/api/sync/conflicts/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteSyncConflict(id: number): Promise<void> {
  return apiFetch<void>(`/api/sync/conflicts/${id}`, { method: 'DELETE' });
}

export function getSyncStats(): Promise<SyncStats> {
  return apiFetch<SyncStats>('/api/sync/stats/summary');
}

/* ============================================================================
   Project 10: Visual Workflow Execution & Automation
   ========================================================================== */

export interface Workflow {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  definition: Record<string, unknown>;
  status: string;
  trigger_type: string | null;
  trigger_config: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface WorkflowCreate {
  name: string;
  description?: string;
  definition?: Record<string, unknown>;
  trigger_type?: string;
  trigger_config?: Record<string, unknown>;
}

export interface WorkflowUpdate {
  name?: string;
  description?: string;
  definition?: Record<string, unknown>;
  status?: string;
  trigger_type?: string;
  trigger_config?: Record<string, unknown>;
}

export interface WorkflowExecution {
  id: number;
  workflow_id: number;
  trigger_payload: Record<string, unknown>;
  status: string;
  started_at: string;
  completed_at: string | null;
  context: Record<string, unknown>;
  error_message: string | null;
}

export interface WorkflowExecutionCreate {
  workflow_id: number;
  trigger_payload?: Record<string, unknown>;
  context?: Record<string, unknown>;
}

export interface WorkflowStepExecution {
  id: number;
  execution_id: number;
  step_id: string;
  step_type: string;
  status: string;
  input: Record<string, unknown>;
  output: Record<string, unknown> | null;
  error_message: string | null;
  attempt_number: number;
  max_retries: number;
  started_at: string | null;
  completed_at: string | null;
  depends_on: string[];
}

export interface WorkflowStepExecutionCreate {
  execution_id: number;
  step_id: string;
  step_type: string;
  input?: Record<string, unknown>;
  max_retries?: number;
  depends_on?: string[];
}

export interface WorkflowStats {
  total_workflows: number;
  active_workflows: number;
  total_executions: number;
  failed_executions: number;
}

export function listWorkflows({ status }: { status?: string } = {}): Promise<Workflow[]> {
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  return apiFetch<Workflow[]>(
    `/api/workflows${params.toString() ? `?${params}` : ''}`,
  );
}

export function createWorkflow(body: WorkflowCreate): Promise<Workflow> {
  return apiFetch<Workflow>('/api/workflows', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getWorkflow(id: number): Promise<Workflow> {
  return apiFetch<Workflow>(`/api/workflows/${id}`);
}

export function updateWorkflow(id: number, body: WorkflowUpdate): Promise<Workflow> {
  return apiFetch<Workflow>(`/api/workflows/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function deleteWorkflow(id: number): Promise<void> {
  return apiFetch<void>(`/api/workflows/${id}`, { method: 'DELETE' });
}

export function publishWorkflow(id: number): Promise<Workflow> {
  return apiFetch<Workflow>(`/api/workflows/${id}/publish`, { method: 'POST' });
}

export function archiveWorkflow(id: number): Promise<Workflow> {
  return apiFetch<Workflow>(`/api/workflows/${id}/archive`, { method: 'POST' });
}

export function createWorkflowExecution(
  body: WorkflowExecutionCreate,
): Promise<WorkflowExecution> {
  return apiFetch<WorkflowExecution>('/api/workflows/executions', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function listWorkflowExecutions({
  workflowId,
  status,
}: { workflowId?: number; status?: string } = {}): Promise<WorkflowExecution[]> {
  const params = new URLSearchParams();
  if (workflowId != null) params.set('workflow_id', String(workflowId));
  if (status) params.set('status', status);
  return apiFetch<WorkflowExecution[]>(
    `/api/workflows/executions${params.toString() ? `?${params}` : ''}`,
  );
}

export function getWorkflowExecution(id: number): Promise<WorkflowExecution> {
  return apiFetch<WorkflowExecution>(`/api/workflows/executions/${id}`);
}

export function createWorkflowStep(
  body: WorkflowStepExecutionCreate,
): Promise<WorkflowStepExecution> {
  return apiFetch<WorkflowStepExecution>(
    `/api/workflows/executions/${body.execution_id}/steps`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}

export function listWorkflowSteps(executionId: number): Promise<WorkflowStepExecution[]> {
  return apiFetch<WorkflowStepExecution[]>(
    `/api/workflows/executions/${executionId}/steps`,
  );
}

export function updateWorkflowStep(
  id: number,
  body: Partial<WorkflowStepExecutionCreate>,
): Promise<WorkflowStepExecution> {
  return apiFetch<WorkflowStepExecution>(`/api/workflows/steps/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function getWorkflowStats(): Promise<WorkflowStats> {
  return apiFetch<WorkflowStats>('/api/workflows/stats/summary');
}
