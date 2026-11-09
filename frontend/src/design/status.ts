import type { Progress } from '@/api/client';

/** Presentation for Progress.status (the stamp tone doubles as the label). */
export const PROGRESS_STAMPS = {
  not_started: { tone: 'not-started', label: 'not started' },
  active: { tone: 'active', label: 'active' },
  stale: { tone: 'stale', label: 'stale' },
} as const satisfies Record<Progress['status'], { tone: string; label: string }>;
