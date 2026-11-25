const STORAGE_KEY = 'manabi:visitor-id';
const VISITOR_ID_PATTERN = /^[A-Za-z0-9_-]{16,64}$/;

let memoryId: string | null = null;

function randomId(): string {
  if (typeof crypto !== 'undefined') {
    if (typeof crypto.randomUUID === 'function') {
      return crypto.randomUUID();
    }
    if (typeof crypto.getRandomValues === 'function') {
      const bytes = crypto.getRandomValues(new Uint8Array(16));
      return Array.from(bytes, (byte) =>
        byte.toString(16).padStart(2, '0'),
      ).join('');
    }
  }
  const fallback = `${Date.now().toString(36)}${Math.random()
    .toString(36)
    .slice(2)}`;
  return fallback.padEnd(32, '0').slice(0, 32);
}

/**
 * Coarse device hints sent with the heartbeat. They contain nothing unique:
 * screen size, CPU cores and timezone only separate devices that share one IP.
 */
export function getDeviceHints() {
  const screen =
    typeof window !== 'undefined' && window.screen
      ? `${window.screen.width}x${window.screen.height}`
      : '';
  const cores =
    typeof navigator !== 'undefined' ? navigator.hardwareConcurrency || 0 : 0;
  let timezone = '';
  try {
    timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
  } catch {
    timezone = '';
  }
  return { screen, cores, timezone };
}

/**
 * Legacy id used only to adopt this browser's existing presence row.
 *
 * Identity itself is derived on the server (see routers/visitors.py), so
 * clearing storage no longer creates a new visitor; this value is sent so an
 * old row is upgraded instead of duplicated. It is random, lives in
 * localStorage, and is never linked to an account unless the visitor logs in
 * (handled server-side). Storage can be unavailable in private mode, so the
 * id falls back to memory for the current page load.
 */
export function getVisitorId(): string {
  if (memoryId) return memoryId;

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored && VISITOR_ID_PATTERN.test(stored)) {
      memoryId = stored;
      return stored;
    }
    const created = randomId();
    localStorage.setItem(STORAGE_KEY, created);
    memoryId = created;
    return created;
  } catch {
    memoryId = randomId();
    return memoryId;
  }
}
