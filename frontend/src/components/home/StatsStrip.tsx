import type { ApiError, StatsOut } from '@/api/client';
import type { UseQueryResult } from '@tanstack/react-query';
import { CountUp } from './CountUp';

const STAT_ENTRIES: Array<{ key: keyof StatsOut; label: string }> = [
  { key: 'problems', label: 'Problems' },
  { key: 'sources', label: 'Sources' },
  { key: 'fields', label: 'Fields' },
  { key: 'projects', label: 'Projects' },
  { key: 'ml_questions', label: 'ML questions' },
];

export function StatsStrip({
  query,
}: {
  query: UseQueryResult<StatsOut, ApiError>;
}) {
  if (query.isLoading) {
    return (
      <section aria-busy="true" className="border-b-[3px] border-ink bg-ink">
        <div className="skeleton mx-auto h-28 w-[min(1200px,96vw)]" aria-hidden />
      </section>
    );
  }

  if (query.isError) {
    return (
      <section className="border-b-[3px] border-ink bg-ink">
        <p
          role="alert"
          className="mx-auto w-[min(1200px,96vw)] py-6 font-mono text-xs font-bold uppercase tracking-widest text-paper"
        >
          Stats unavailable — {query.error.detail}
        </p>
      </section>
    );
  }

  if (query.data == null) {
    return null;
  }

  const stats = query.data;

  return (
    <section
      aria-label="Platform stats"
      className="border-b-[3px] border-ink bg-ink text-paper"
    >
      <dl className="mx-auto grid w-[min(1200px,96vw)] grid-cols-2 gap-6 py-8 md:grid-cols-5">
        {STAT_ENTRIES.map((entry) => (
          <div key={entry.key} className="flex flex-col-reverse gap-1">
            <dt className="font-mono text-[11px] font-bold uppercase tracking-widest">
              {entry.label}
            </dt>
            <dd className="font-display text-4xl text-yellow md:text-5xl">
              <CountUp value={stats[entry.key]} />
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
