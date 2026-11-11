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
    <main className="border-b border-ink">
      <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
        <h1 className="font-display text-display uppercase">{title}</h1>
        <p>{message}</p>
        <Link to={backTo} className="font-mono text-label font-bold underline">
          {backLabel}
        </Link>
      </div>
    </main>
  );
}
