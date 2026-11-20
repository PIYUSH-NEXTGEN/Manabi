import type { components } from './schema';

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
  /** Seconds until the rate limit frees up, from the Retry-After header. */
  readonly retryAfterSeconds: number | null;
  /** The raw parsed response body, for error payloads with extra fields. */
  readonly payload?: unknown;

  constructor(
    status: number,
    detail: string,
    code: string | null = null,
    payload?: unknown,
    retryAfterSeconds: number | null = null,
  ) {
    super(detail);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
    this.code = code;
    this.retryAfterSeconds = retryAfterSeconds;
    this.payload = payload;
  }
}

interface ErrorBody {
  detail?: unknown;
}

/** Normal requests get 20s; LLM/GitHub-backed writes explicitly allow longer. */
const DEFAULT_TIMEOUT_MS = 20_000;

// The backend mints/echoes X-Request-ID on every response. Keeping the most
// recent one lets a client-side error report point at the backend log line
// for the call that preceded it.
let lastResponseRequestId: string | null = null;

export function getLastResponseRequestId(): string | null {
  return lastResponseRequestId;
}

interface ApiFetchOptions extends RequestInit {
  timeoutMs?: number;
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

export async function apiFetch<T>(
  path: string,
  options: ApiFetchOptions = {},
): Promise<T> {
  const {
    timeoutMs = DEFAULT_TIMEOUT_MS,
    signal: externalSignal,
    ...init
  } = options;
  const headers = new Headers(init.headers);
  if (init.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const controller = new AbortController();
  let timedOut = false;
  const timer = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, timeoutMs);
  const abortFromCaller = () => controller.abort();
  if (externalSignal) {
    if (externalSignal.aborted) controller.abort();
    else externalSignal.addEventListener('abort', abortFromCaller);
  }

  let response: Response;
  try {
    response = await fetch(path, {
      ...init,
      credentials: 'include',
      headers,
      signal: controller.signal,
    });
  } catch {
    if (timedOut) {
      throw new ApiError(
        0,
        'The server took too long to respond. Try again.',
        'timeout',
      );
    }
    if (externalSignal?.aborted) {
      throw new ApiError(0, 'The request was cancelled.', 'aborted');
    }
    throw new ApiError(
      0,
      'Could not reach the server. Check your connection and try again.',
      'network_error',
    );
  } finally {
    clearTimeout(timer);
    externalSignal?.removeEventListener('abort', abortFromCaller);
  }

  lastResponseRequestId = response.headers.get('X-Request-ID');

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
    const retryHeader = response.headers.get('Retry-After');
    const retryAfterSeconds =
      retryHeader !== null && /^\d+$/.test(retryHeader)
        ? Number(retryHeader)
        : null;
    throw new ApiError(response.status, detail, code, payload, retryAfterSeconds);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  try {
    return (await response.json()) as T;
  } catch {
    throw new ApiError(
      response.status,
      'The server returned an unreadable response. Try again.',
      'invalid_response',
    );
  }
}

export interface ProblemsQuery {
  q?: string;
  field?: string;
  difficulty?: string;
  goal?: 'resume' | 'hackathon' | 'learning';
  tech?: string[];
  source?: string;
  sort?: 'newest' | 'popular' | 'discover';
  seed?: number;
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
  if (query.difficulty) params.set('difficulty', query.difficulty);
  if (query.goal) params.set('goal', query.goal);
  for (const tech of query.tech ?? []) params.append('tech', tech);
  if (query.source) params.set('source', query.source);
  if (query.sort) params.set('sort', query.sort);
  if (query.seed != null) params.set('seed', String(query.seed));
  if (query.distinct) params.set('distinct', query.distinct);
  if (query.limit != null) params.set('limit', String(query.limit));
  if (query.offset != null) params.set('offset', String(query.offset));
  const qs = params.toString();
  return apiFetch<ProblemsListOut>(`/api/problems${qs ? `?${qs}` : ''}`);
}

export interface FacetsQuery {
  q?: string;
  field?: string;
  source?: string;
  goal?: 'resume' | 'hackathon' | 'learning';
}

export function getFacets(query: FacetsQuery = {}): Promise<FacetsOut> {
  const params = new URLSearchParams();
  if (query.q) params.set('q', query.q);
  if (query.field) params.set('field', query.field);
  if (query.source) params.set('source', query.source);
  if (query.goal) params.set('goal', query.goal);
  const search = params.toString();
  return apiFetch<FacetsOut>(`/api/problems/facets${search ? `?${search}` : ''}`);
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

export function postChat(body: ChatIn): Promise<ChatOut> {
  return apiFetch<ChatOut>('/api/chat', {
    method: 'POST',
    body: JSON.stringify(body),
    timeoutMs: 75_000,
  });
}

export function getMyProjects(): Promise<ProjectOut[]> {
  return apiFetch<ProjectOut[]>('/api/me/projects');
}

export type Progress = NonNullable<Schemas['ProjectOut']['progress']>;
export type ProjectOut = Schemas['ProjectOut'];
export type ProjectCreate = Schemas['ProjectCreate'];
export type ChatIn = Schemas['ChatIn'];
export type ChatMessage = Schemas['ChatMessage'];
export type ChatOut = Schemas['ChatOut'];
export type ChatProblemItem = Schemas['ChatProblemItem'];
export type AdminSubmissionOut = Schemas['AdminSubmissionOut'];
export type AdminSubmissionsOut = Schemas['AdminSubmissionsOut'];
export type AdminSubmissionActionOut = Schemas['AdminSubmissionActionOut'];
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
    { timeoutMs: 75_000 },
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
    timeoutMs: 60_000,
  });
}

export type ProjectPatch = Schemas['ProjectPatch'];

export function deleteProject(id: number): Promise<void> {
  return apiFetch<void>(`/api/projects/${id}`, { method: 'DELETE' });
}

export function patchProject(id: number, body: ProjectPatch): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/api/projects/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
    timeoutMs: 75_000,
  });
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

export function starProject(id: number): Promise<{ ok: boolean; star_count: number }> {
  return apiFetch<{ ok: boolean; star_count: number }>(
    `/api/projects/${id}/star`,
    { method: 'POST' },
  );
}

export function unstarProject(id: number): Promise<void> {
  return apiFetch<void>(`/api/projects/${id}/star`, { method: 'DELETE' });
}

export function starProblem(id: number): Promise<{ ok: boolean; star_count: number }> {
  return apiFetch<{ ok: boolean; star_count: number }>(
    `/api/problems/${id}/star`,
    { method: 'POST' },
  );
}

export function unstarProblem(id: number): Promise<void> {
  return apiFetch<void>(`/api/problems/${id}/star`, { method: 'DELETE' });
}
