import type { components, paths } from './schema';

type Schemas = components['schemas'];

export type ProblemOut = Schemas['ProblemOut'];
export type ProblemDetail = Schemas['ProblemDetail'];
export type ProblemsListOut = Schemas['ProblemsListOut'];
export type FacetsOut = Schemas['FacetsOut'];
export type Facet = Schemas['Facet'];
export type StatsOut = Schemas['StatsOut'];

export class ApiError extends Error {
  readonly status: number;
  readonly detail: string;
  /** Machine-readable error code from {"detail": {"code", "message"}} bodies. */
  readonly code: string | null;
  /** The raw parsed response body, for error payloads with extra fields
   * (e.g. the completion checklist). */
  readonly payload?: unknown;

  constructor(status: number, detail: string, code: string | null = null, payload?: unknown) {
    super(detail);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
    this.code = code;
    this.payload = payload;
  }
}

interface ErrorBody {
  detail?: unknown;
}

/** FastAPI can return the error detail as a plain string or as
 * {"code": ..., "message": ...}. Handle both. */
function parseErrorBody(body: ErrorBody): { detail: string; code: string | null } | null {
  if (typeof body.detail === 'string' && body.detail.length > 0) {
    return { detail: body.detail, code: null };
  }
  if (typeof body.detail === 'object' && body.detail !== null) {
    const object = body.detail as Record<string, unknown>;
    if (
      typeof object.code === 'string' &&
      typeof object.message === 'string' &&
      object.message.length > 0
    ) {
      return { detail: object.message, code: object.code };
    }
    return null;
  }
  return null;
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (init?.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(path, {
    ...init,
    credentials: 'include',
    headers,
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    let code: string | null = null;
    let payload: unknown;
    try {
      const body = (await response.json()) as ErrorBody;
      payload = body;
      const parsed = parseErrorBody(body);
      if (parsed) {
        detail = parsed.detail;
        code = parsed.code;
      }
    } catch {
      detail = `Request failed with status ${response.status}`;
    }
    throw new ApiError(response.status, detail, code, payload);
  }

  return (await response.json()) as T;
}

export type HealthResponse =
  paths['/api/health']['get']['responses']['200']['content']['application/json'];

export function getHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/api/health');
}

export interface ProblemsQuery {
  q?: string;
  field?: string;
  domain?: string;
  difficulty?: string;
  tech?: string[];
  source?: string;
  sort?: 'newest' | 'popular';
  distinct?: 'field' | 'domain';
  limit?: number;
  offset?: number;
}

export function getStats(): Promise<StatsOut> {
  return apiFetch<StatsOut>('/api/stats');
}

export function getProblems(query: ProblemsQuery = {}): Promise<ProblemsListOut> {
  const params = new URLSearchParams();
  if (query.q) params.set('q', query.q);
  if (query.field) params.set('field', query.field);
  if (query.domain) params.set('domain', query.domain);
  if (query.difficulty) params.set('difficulty', query.difficulty);
  for (const tech of query.tech ?? []) params.append('tech', tech);
  if (query.source) params.set('source', query.source);
  if (query.sort) params.set('sort', query.sort);
  if (query.distinct) params.set('distinct', query.distinct);
  if (query.limit != null) params.set('limit', String(query.limit));
  if (query.offset != null) params.set('offset', String(query.offset));
  const qs = params.toString();
  return apiFetch<ProblemsListOut>(`/api/problems${qs ? `?${qs}` : ''}`);
}

export function getFacets(): Promise<FacetsOut> {
  return apiFetch<FacetsOut>('/api/problems/facets');
}

export function getProblem(id: number): Promise<ProblemDetail> {
  return apiFetch<ProblemDetail>(`/api/problems/${id}`);
}

export interface MeOut {
  id: number;
  username: string;
  name: string | null;
  avatar_url: string | null;
  is_admin?: boolean;
}

export function getMe(): Promise<MeOut> {
  return apiFetch<MeOut>('/api/auth/me');
}

export function logout(): Promise<void> {
  return apiFetch<void>('/api/auth/logout', { method: 'POST' });
}

export function createProblem(body: ProblemIn): Promise<ProblemOut> {
  return apiFetch<ProblemOut>('/api/problems', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function postChat(body: ChatIn): Promise<ChatOut> {
  return apiFetch<ChatOut>('/api/chat', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function getRecommendations(): Promise<RecommendationsOut> {
  return apiFetch<RecommendationsOut>('/api/recommendations');
}

export function getMyProjects(): Promise<ProjectOut[]> {
  return apiFetch<ProjectOut[]>('/api/me/projects');
}

export type Progress = NonNullable<Schemas['ProjectOut']['progress']>;
export type ProjectOut = Schemas['ProjectOut'];
export type ProjectCreate = Schemas['ProjectCreate'];
export type ProblemIn = Schemas['ProblemIn'];
export type ChatIn = Schemas['ChatIn'];
export type ChatMessage = Schemas['ChatMessage'];
export type ChatOut = Schemas['ChatOut'];
export type ChatPageContext = Schemas['ChatPageContext'];
export type ChatProblemItem = Schemas['ChatProblemItem'];
export type RecommendationsOut = Schemas['RecommendationsOut'];
export type RecommendationItem = Schemas['RecommendationItem'];
export type AdminSubmissionOut = Schemas['AdminSubmissionOut'];
export type AdminSubmissionsOut = Schemas['AdminSubmissionsOut'];
export type AdminSubmissionActionOut = Schemas['AdminSubmissionActionOut'];
/** Checklist item inside the not_ready_to_complete error body. */
export interface CompletionChecklistItem {
  item: string;
  ok: boolean;
}

export type SubmissionStatusFilter =
  | 'verified'
  | 'needs_review'
  | 'rejected';

export function getAdminSubmissions(
  status: SubmissionStatusFilter = 'needs_review',
  limit = 50,
  offset = 0,
): Promise<AdminSubmissionsOut> {
  const params = new URLSearchParams({
    status,
    limit: String(limit),
    offset: String(offset),
  });
  return apiFetch<AdminSubmissionsOut>(`/api/admin/submissions?${params}`);
}

export function approveSubmission(
  id: number,
  note?: string,
): Promise<AdminSubmissionActionOut> {
  const qs = note ? `?note=${encodeURIComponent(note)}` : '';
  return apiFetch<AdminSubmissionActionOut>(
    `/api/admin/submissions/${id}/approve${qs}`,
    { method: 'POST' },
  );
}

export function rejectSubmission(
  id: number,
  note?: string,
): Promise<AdminSubmissionActionOut> {
  const qs = note ? `?note=${encodeURIComponent(note)}` : '';
  return apiFetch<AdminSubmissionActionOut>(
    `/api/admin/submissions/${id}/reject${qs}`,
    { method: 'POST' },
  );
}

export function projectOwnerUsername(owner: ProjectOut['owner']): string | null {
  return typeof owner.username === 'string' && owner.username.length > 0
    ? owner.username
    : null;
}

export function getProject(id: number): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/projects/${id}`);
}

export function getProjectProgress(
  id: number,
  refresh = false,
): Promise<Progress> {
  return apiFetch<Progress>(
    `/api/projects/${id}/progress${refresh ? '?refresh=true' : ''}`,
  );
}

export interface CommitSummary {
  sha: string;
  message: string;
  date: string;
}

export interface IssueSummary {
  number: number;
  title: string;
  url: string;
  labels: string[];
}

export function asCommitSummary(raw: unknown): CommitSummary | null {
  if (typeof raw !== 'object' || raw === null) return null;
  const record = raw as Record<string, unknown>;
  if (typeof record.sha !== 'string') return null;
  if (typeof record.message !== 'string') return null;
  if (typeof record.date !== 'string') return null;
  return { sha: record.sha, message: record.message, date: record.date };
}

export function asIssueSummary(raw: unknown): IssueSummary | null {
  if (typeof raw !== 'object' || raw === null) return null;
  const record = raw as Record<string, unknown>;
  if (typeof record.number !== 'number') return null;
  if (typeof record.title !== 'string') return null;
  if (typeof record.url !== 'string') return null;
  if (!Array.isArray(record.labels)) return null;
  const labels: string[] = [];
  for (const label of record.labels) {
    if (typeof label !== 'string') return null;
    labels.push(label);
  }
  return { number: record.number, title: record.title, url: record.url, labels };
}

export function submitProject(
  problemId: number,
  body: ProjectCreate,
): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/problems/${problemId}/projects`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export type ProjectPatch = Schemas['ProjectPatch'];
export type CompleteIn = Schemas['CompleteIn'];

export function deleteProject(id: number): Promise<void> {
  return apiFetch<void>(`/api/projects/${id}`, { method: 'DELETE' });
}

export function patchProject(id: number, body: ProjectPatch): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/projects/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export function completeProject(id: number, body: CompleteIn): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/projects/${id}/complete`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function reopenProject(id: number): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/projects/${id}/reopen`, { method: 'POST' });
}

export function reportProject(
  id: number,
  body: { reason?: string },
): Promise<{ ok: boolean; report_count: number }> {
  return apiFetch<{ ok: boolean; report_count: number }>(
    `/api/projects/${id}/report`,
    { method: 'POST', body: JSON.stringify(body) },
  );
}
