import type { Progress } from '@/api/client';
import { Stamp } from '@/design/primitives';

const STATUS_STAMP = {
  not_started: { tone: 'not-started', label: 'not started' },
  active: { tone: 'active', label: 'active' },
  stale: { tone: 'stale', label: 'stale' },
} as const;

export function ProjectProgressBadge({
  progress,
}: {
  progress: Progress | null;
}) {
  if (!progress) {
    return (
      <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-red">
        Progress unknown
      </span>
    );
  }

  const stamp = STATUS_STAMP[progress.status];

  return (
    <span className="inline-flex items-center gap-1.5">
      <Stamp tone={stamp.tone} label={stamp.label} rotate={-2} />
      <span className="font-mono text-[10px] font-bold uppercase tracking-widest">
        {progress.commit_count} commits
      </span>
    </span>
  );
}
