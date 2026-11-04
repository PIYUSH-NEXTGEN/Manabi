import { cx } from '@/lib/cx';

export type Difficulty = 'beginner' | 'intermediate' | 'advanced';

const DIFFICULTY_FILL: Record<Difficulty, number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

interface IndexCardProps {
  sourceId?: string | null;
  field: string;
  title: string;
  summary?: string | null;
  difficulty?: Difficulty | null;
  domain?: string | null;
  estHours?: number | null;
  className?: string;
}

export function IndexCard({
  sourceId,
  field,
  title,
  summary,
  difficulty,
  domain,
  estHours,
  className,
}: IndexCardProps) {
  const filled = difficulty ? DIFFICULTY_FILL[difficulty] : 0;
  const meta = [domain, estHours != null ? `${estHours} h` : null]
    .filter(Boolean)
    .join(' · ');

  return (
    <article
      className={cx(
        'flex h-full flex-col border border-ink bg-sheet transition-colors duration-150 hover:border-accent',
        className,
      )}
    >
      <header className="flex items-center justify-between gap-3 border-b border-line px-4 py-2.5">
        <span className="flex items-center gap-2 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-ink">
          <span aria-hidden className="block size-2 bg-accent" />
          {sourceId ?? 'NO-ID'}
        </span>
        <span className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
          {field}
        </span>
      </header>
      <div className="flex flex-1 flex-col gap-3 p-4">
        <h3 className="font-display text-[1.15rem] uppercase leading-[1.02] tracking-tight">
          {title}
        </h3>
        {summary ? (
          <p className="line-clamp-3 text-[13px] leading-snug text-ink-soft">{summary}</p>
        ) : null}
        <div className="mt-auto flex items-end justify-between gap-3 border-t border-line pt-3 font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
          {difficulty ? (
            <span className="flex items-center gap-1.5">
              <span aria-hidden className="flex gap-0.5">
                {Array.from({ length: 3 }, (_, index) => (
                  <span
                    key={index}
                    className={cx(
                      'block size-2 border border-ink',
                      index < filled ? 'bg-ink' : 'bg-transparent',
                    )}
                  />
                ))}
              </span>
              <span className="sr-only">{difficulty}</span>
            </span>
          ) : (
            <span />
          )}
          <span className="text-muted">{meta || 'open brief'}</span>
        </div>
      </div>
    </article>
  );
}
