import type { Progress } from '@/api/client';
import { PROGRESS_STAMPS } from '@/design/status';
import { Stamp } from '@/design/primitives';

export function ProjectProgressBadge({
  progress,
}: {
  progress: Progress | null;
}) {
  if (!progress) {
    return (
      <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-danger">
        Progress unknown
      </span>
    );
  }

  const stamp = PROGRESS_STAMPS[progress.status];

  return (
    <span className="inline-flex items-center gap-1.5">
      <Stamp tone={stamp.tone} label={stamp.label} rotate={-2} />
      <span className="font-mono text-[10px] font-bold uppercase tracking-widest">
        {progress.commit_count} commits
      </span>
    </span>
  );
}
