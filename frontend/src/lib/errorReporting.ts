import { apiUrl, getLastResponseRequestId } from '@/api/client';

export type ClientErrorEvent =
  | 'error'
  | 'unhandledrejection'
  | 'react_error_boundary';

interface ClientErrorExtra {
  component_stack?: string;
}

interface ClientErrorPayload {
  event: ClientErrorEvent;
  message: string;
  error_name: string;
  stack?: string;
  component_stack?: string;
  route: string;
  app_version: string;
  backend_request_id?: string;
}

const ENDPOINT = apiUrl('/api/client-errors');
const MAX_MESSAGE = 1000;
const MAX_STACK = 4000;
const MAX_COMPONENT_STACK = 4000;
const MAX_DEDUPE = 50;

const seen = new Set<string>();
let installed = false;

/**
 * Reporting is production-only: in dev and tests the console already shows the
 * error, and the E2E smoke test treats backend noise as a failure.
 */
function reportingEnabled(): boolean {
  return import.meta.env.PROD;
}

function truncate(value: string, max: number): string {
  return value.length > max ? value.slice(0, max) : value;
}

function currentRoute(): string {
  if (typeof window === 'undefined') return '';
  // Collapse ids so one broken detail page does not create a new error group.
  const path = window.location.pathname.replace(/\/\d+(?=\/|$)/g, '/:id');
  return truncate(path, 300);
}

function describe(error: unknown): { message: string; name: string; stack?: string } {
  if (error instanceof Error) {
    return { message: error.message, name: error.name, stack: error.stack };
  }
  if (typeof error === 'string') {
    return { message: error, name: 'Error' };
  }
  if (
    error !== null &&
    typeof error === 'object' &&
    'message' in error &&
    typeof (error as { message?: unknown }).message === 'string'
  ) {
    const candidate = error as { message: string; name?: unknown; stack?: unknown };
    return {
      message: candidate.message,
      name: typeof candidate.name === 'string' ? candidate.name : 'Error',
      stack: typeof candidate.stack === 'string' ? candidate.stack : undefined,
    };
  }
  try {
    return { message: JSON.stringify(error), name: 'Error' };
  } catch {
    return { message: String(error), name: 'Error' };
  }
}

export function reportClientError(
  event: ClientErrorEvent,
  error: unknown,
  extra: ClientErrorExtra = {},
): void {
  if (!reportingEnabled()) return;

  const detail = describe(error);
  const payload: ClientErrorPayload = {
    event,
    message: truncate(detail.message || 'Unknown client error', MAX_MESSAGE),
    error_name: truncate(detail.name || 'Error', 100),
    stack: detail.stack ? truncate(detail.stack, MAX_STACK) : undefined,
    component_stack: extra.component_stack
      ? truncate(extra.component_stack, MAX_COMPONENT_STACK)
      : undefined,
    route: currentRoute(),
    app_version: truncate(import.meta.env.VITE_APP_VERSION ?? '', 100) || 'web',
    backend_request_id: getLastResponseRequestId() ?? undefined,
  };

  const dedupeKey = `${payload.event}:${payload.error_name}:${payload.message}:${payload.route}`;
  if (seen.has(dedupeKey)) return;
  if (seen.size >= MAX_DEDUPE) {
    const oldest = seen.values().next().value;
    if (oldest) seen.delete(oldest);
  }
  seen.add(dedupeKey);

  const body = JSON.stringify(payload);
  try {
    if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
      const blob = new Blob([body], { type: 'application/json' });
      if (navigator.sendBeacon(ENDPOINT, blob)) return;
    }
  } catch {
    // Fall through to fetch.
  }
  void fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body,
    keepalive: true,
  }).catch(() => {
    // Losing a browser error report must never trigger another error loop.
  });
}

export function installGlobalErrorReporting(): void {
  if (installed || !reportingEnabled() || typeof window === 'undefined') return;
  installed = true;

  window.addEventListener('error', (event) => {
    // Resource-load events have no message and would report every broken
    // avatar as an application error.
    if (!event.error && !event.message) return;
    reportClientError('error', event.error ?? event.message);
  });

  window.addEventListener('unhandledrejection', (event) => {
    reportClientError('unhandledrejection', event.reason);
  });
}
