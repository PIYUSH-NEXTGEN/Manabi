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
        'flex h-full flex-col overflow-hidden rounded-card border border-line bg-sheet shadow-soft transition-[transform,box-shadow,border-color] duration-300 ease-out hover:-translate-y-0.5 hover:border-ink/20 hover:shadow-lift',
        className,
      )}
    >
      <header className="flex items-center justify-between gap-3 border-b border-line px-5 py-3">
        <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.16em] text-ink-soft">
          <span aria-hidden className="block size-1.5 rounded-full bg-accent" />
          {sourceId ?? 'NO-ID'}
        </span>
        <span className="text-label font-semibold text-muted">{field}</span>
      </header>
      <div className="flex flex-1 flex-col gap-3 p-5">
        <h3 className="font-display text-[1.0625rem] leading-snug text-ink">
          {title}
        </h3>
        {summary ? (
          <p className="line-clamp-3 text-body leading-relaxed text-ink-soft">
            {summary}
          </p>
        ) : null}
        <div className="mt-auto flex items-end justify-between gap-3 border-t border-line pt-3.5 font-mono text-label font-bold uppercase tracking-[0.12em]">
          {difficulty ? (
            <span className="flex items-center gap-1.5">
              <span aria-hidden className="flex gap-1">
                {Array.from({ length: 3 }, (_, index) => (
                  <span
                    key={index}
                    className={cx(
                      'block h-1.5 w-4 rounded-full',
                      index < filled ? 'bg-accent' : 'bg-tint',
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
