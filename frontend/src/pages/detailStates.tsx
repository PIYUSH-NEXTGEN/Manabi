import { Link } from 'react-router-dom';

import { Skeleton } from '@/design/primitives';

/** Loading and load-error blocks shared by the problem/project detail pages. */

export function PageSkeleton({ width }: { width: string }) {
  return (
    <div className={`mx-auto ${width} space-y-4 py-16`}>
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-16 w-2/3" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

export function LoadErrorPanel({
  title,
  message,
  backTo,
  backLabel,
}: {
  title: string;
  message: string;
  backTo: string;
  backLabel: string;
}) {
  return (
    <main className="border-b border-line">
      <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
        <h1 className="font-display text-display leading-tight text-ink">{title}</h1>
        <p className="text-body leading-relaxed text-ink-soft">{message}</p>
        <Link
          to={backTo}
          className="inline-flex rounded-full border border-line bg-sheet px-4 py-2.5 text-[0.875rem] font-semibold text-ink hover:border-ink/25"
        >
          {backLabel}
        </Link>
      </div>
    </main>
  );
}
