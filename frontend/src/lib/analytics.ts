import type { PostHog } from 'posthog-js';
import {
  isPostHogConfigured,
  loadPosthog,
  loadedPosthog,
  unloadPosthog,
} from '@/lib/posthog';

/** Where the visitor's analytics decision is remembered. */
export const ANALYTICS_CONSENT_KEY = 'manabi-analytics-consent';

export type ConsentChoice = 'granted' | 'denied';
type Properties = Record<string, unknown>;
type QueuedEvent = { event: string; properties?: Properties };
type LogAttributes = Record<string, string | number | boolean>;

const MAX_QUEUED_EVENTS = 25;

let consent: ConsentChoice | null = null;
let consentRead = false;
let queue: QueuedEvent[] = [];
const listeners = new Set<() => void>();

function storage(): Storage | null {
  if (typeof window === 'undefined') return null;
  try {
    return window.localStorage;
  } catch {
    // Private mode or a blocked storage partition: stay undecided and ask again.
    return null;
  }
}

/** Current decision, read from storage on first use. Null means "not asked". */
export function getConsent(): ConsentChoice | null {
  if (!consentRead) {
    const raw = storage()?.getItem(ANALYTICS_CONSENT_KEY);
    consent = raw === 'granted' || raw === 'denied' ? raw : null;
    consentRead = true;
  }
  return consent;
}

export function subscribeConsent(listener: () => void): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

function notifyConsent(): void {
  for (const listener of listeners) listener();
}

function captureWith(
  client: PostHog,
  event: string,
  properties?: Properties,
): void {
  try {
    client.capture(event, properties);
  } catch {
    // Analytics must never break a user action.
  }
}

async function loadAndFlushQueue(): Promise<void> {
  const client = await loadPosthog();
  if (!client) return;

  const pending = queue;
  queue = [];
  for (const item of pending) captureWith(client, item.event, item.properties);
}

export function setConsent(choice: ConsentChoice): void {
  consent = choice;
  consentRead = true;

  try {
    storage()?.setItem(ANALYTICS_CONSENT_KEY, choice);
  } catch {
    // The choice still applies for this tab.
  }

  notifyConsent();

  if (choice === 'granted') {
    void loadAndFlushQueue();
    trackPageview(currentPath());
  } else {
    queue = [];
    unloadPosthog();
  }
}

/** Withdraws the stored decision so the banner asks again. */
export function clearConsent(): void {
  consent = null;
  consentRead = true;
  queue = [];

  try {
    storage()?.removeItem(ANALYTICS_CONSENT_KEY);
  } catch {
    // Nothing else to undo.
  }

  unloadPosthog();
  notifyConsent();
}

function currentPath(): string {
  return typeof window === 'undefined' ? '/' : window.location.pathname;
}

/** Captures nothing unless PostHog is configured and consent is granted. */
export function track(event: string, properties?: Properties): void {
  if (!isPostHogConfigured || getConsent() !== 'granted') return;

  const client = loadedPosthog();
  if (client) {
    captureWith(client, event, properties);
    return;
  }

  // A click that happens in the moment between "Allow" and the SDK finishing
  // its download should still count.
  if (queue.length < MAX_QUEUED_EVENTS) queue.push({ event, properties });
  void loadAndFlushQueue();
}

export function trackPageview(path: string): void {
  track('$pageview', {
    route: path,
    $current_url: typeof window === 'undefined' ? undefined : window.location.href,
  });
}

export function identifyUser(
  id: number | string,
  properties?: Properties,
): void {
  if (!isPostHogConfigured || getConsent() !== 'granted') return;

  void loadPosthog().then((client) => {
    if (!client || getConsent() !== 'granted') return;
    try {
      client.identify(String(id), properties);
    } catch {
      // Identity is best-effort.
    }
  });
}

/** Forgets the analytics identity, e.g. after logout or an account switch. */
export function resetAnalytics(): void {
  queue = [];
  unloadPosthog();
}

/** Runs at startup: returning visitors who already agreed resume immediately. */
export function initAnalytics(): void {
  if (!isPostHogConfigured || getConsent() !== 'granted') return;
  void loadAndFlushQueue();
}

function logEvent(
  level: 'info' | 'warn' | 'error',
  message: string,
  attributes?: LogAttributes,
): void {
  if (!isPostHogConfigured || getConsent() !== 'granted') return;

  void loadPosthog().then((client) => {
    if (!client || getConsent() !== 'granted') return;
    try {
      client.logger[level](message, attributes);
    } catch {
      // Logs are best-effort.
    }
  });
}

/** The only browser logs exported to PostHog; console output stays local. */
export const analyticsLogs = {
  applicationStarted(): void {
    logEvent('info', 'application_started', { runtime: 'browser' });
  },
  preparationFailed(): void {
    logEvent('warn', 'application_preparation_failed', {
      preparation: 'mock_worker',
    });
  },
  uiRenderFailed(): void {
    logEvent('error', 'ui_render_failed', {
      error_source: 'react_error_boundary',
    });
  },
};

export { isPostHogConfigured };
