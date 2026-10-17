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
  difficulty: Difficulty;
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
  const filled = DIFFICULTY_FILL[difficulty];
  const squares = `${'■'.repeat(filled)}${'□'.repeat(3 - filled)}`;
  const meta = [domain, estHours != null ? `${estHours}h` : null]
    .filter(Boolean)
    .join(' · ');

  return (
    <article
      className={cx('flex h-full flex-col border-[3px] border-ink bg-white shadow-hard', className)}
    >
      <header className="flex items-center justify-between gap-3 border-b-[3px] border-ink bg-ink px-3 py-1.5 font-mono text-[11px] font-bold uppercase tracking-widest text-paper">
        <span>{sourceId ?? 'NO-ID'}</span>
        <span>{field}</span>
      </header>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <h3 className="font-display text-lg uppercase leading-tight">{title}</h3>
        {summary ? <p className="line-clamp-3 text-sm leading-snug">{summary}</p> : null}
        <div className="mt-auto flex items-center justify-between gap-3 pt-2 font-mono text-[11px] font-bold uppercase tracking-widest">
          <span>
            <span aria-hidden>{squares}</span>
            <span className="sr-only">{difficulty}</span>
          </span>
          <span>{meta}</span>
        </div>
      </div>
    </article>
  );
}
