import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'motion/react';
import { buttonClasses } from '@/design';
import { EASE_SNAP } from '@/design/motion';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { useProblems } from '@/hooks/useProblems';
import { useStats } from '@/hooks/useStats';
import type { ProblemOut } from '@/api/client';
import { CountUp } from './CountUp';

const SHOWCASE_LIMIT = 6;
const CYCLE_MS = 3000;

const DIFFICULTY_FILL: Record<ProblemOut['difficulty'], number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

function pad(value: number) {
  return String(value).padStart(2, '0');
}

function DifficultyMeter({ difficulty }: { difficulty: ProblemOut['difficulty'] }) {
  const filled = DIFFICULTY_FILL[difficulty];
  return (
    <span className="flex items-center gap-1.5" title={difficulty}>
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
  );
}

function BriefShowcase() {
  const query = useProblems({ sort: 'popular', limit: SHOWCASE_LIMIT });
  const reduced = usePrefersReducedMotion();
  const [index, setIndex] = useState(0);
  const [held, setHeld] = useState(false);
  const [manualPause, setManualPause] = useState(false);

  const items = query.data?.items.slice(0, SHOWCASE_LIMIT) ?? [];
  const count = items.length;
  const paused = held || manualPause;

  useEffect(() => {
    if (paused || reduced || count < 2) return;
    const timer = window.setInterval(() => {
      setIndex((current) => (current + 1) % count);
    }, CYCLE_MS);
    return () => window.clearInterval(timer);
  }, [paused, reduced, count]);

  const current = count > 0 ? index % count : 0;
  const active = count > 0 ? items[current] : null;

  return (
    <figure
      className="border border-ink bg-sheet"
      onMouseEnter={() => setHeld(true)}
      onMouseLeave={() => setHeld(false)}
    >
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
          Brief in focus
        </span>
        <span className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
          {count > 0 ? `${pad(current + 1)} / ${pad(count)}` : 'No data'}
        </span>
      </div>

      <div className="min-h-[300px] p-5 sm:p-6" aria-busy={query.isLoading}>
        {query.isLoading ? (
          <div className="space-y-3" aria-hidden>
            <div className="skeleton h-2.5 w-20" />
            <div className="skeleton h-8 w-3/4" />
            <div className="skeleton h-3 w-full" />
            <div className="skeleton h-3 w-1/2" />
            <div className="skeleton mt-8 h-9 w-full" />
          </div>
        ) : active ? (
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={active.id}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: reduced ? 0 : 0.42, ease: EASE_SNAP }}
            >
              <Link to={`/problems/${active.id}`} className="group block">
                <div className="flex items-center justify-between gap-3">
                  <p className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-accent">
                    {active.source_id ?? `BRIEF-${active.id}`}
                  </p>
                  <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                    {active.field}
                  </p>
                </div>
                <h2 className="mt-2 line-clamp-3 font-display text-2xl uppercase leading-[0.98] tracking-tight sm:text-3xl">
                  {active.title}
                </h2>
                <p className="mt-3 line-clamp-3 text-sm leading-snug text-ink-soft">
                  {active.summary}
                </p>
                <div className="mt-6 flex items-center justify-between gap-3 border-t border-line pt-3 font-mono text-[9px] font-bold uppercase tracking-[0.16em]">
                  <DifficultyMeter difficulty={active.difficulty} />
                  <span className="text-accent transition-colors group-hover:text-ink">
                    Open brief →
                  </span>
                </div>
              </Link>
            </motion.div>
          </AnimatePresence>
        ) : (
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-muted">
              Index
            </p>
            <p className="mt-2 font-display text-2xl uppercase leading-tight">
              Briefs unavailable
            </p>
            <p className="mt-3 text-sm leading-snug text-ink-soft">
              The problems API did not respond. Open the board while it comes
              back online.
            </p>
            <Link
              to="/problems"
              className="mt-5 inline-block border border-ink px-4 py-2 font-mono text-[10px] font-bold uppercase tracking-[0.16em] transition-colors hover:bg-ink hover:text-paper"
            >
              Browse problems
            </Link>
          </div>
        )}
      </div>

      <figcaption className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
        <span>Curated by MANABI</span>
        {count > 1 ? (
          <span className="flex items-center gap-3">
            <span className="flex items-center gap-1">
              {items.map((item, itemIndex) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setIndex(itemIndex)}
                  aria-label={`Show brief ${itemIndex + 1}`}
                  aria-pressed={itemIndex === current}
                  className={cx(
                    'block size-2 border border-ink transition-colors',
                    itemIndex === current ? 'bg-ink' : 'bg-transparent hover:bg-tint',
                  )}
                />
              ))}
            </span>
            <button
              type="button"
              onClick={() => setManualPause((value) => !value)}
              className="underline underline-offset-2 transition-colors hover:text-ink"
            >
              {manualPause ? 'Play' : 'Pause'}
            </button>
          </span>
        ) : null}
      </figcaption>
    </figure>
  );
}

export function Hero() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = query.trim();
    navigate(trimmed ? `/problems?q=${encodeURIComponent(trimmed)}` : '/problems');
  }

  return (
    <section className="border-b border-ink bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid items-start gap-12 py-10 md:grid-cols-[1.12fr_0.88fr] md:gap-14 md:py-14">
          <div>
            <h1
              className="font-display uppercase leading-[0.82] tracking-[-0.035em]"
              style={{ fontSize: 'clamp(4rem, 11vw, 8.5rem)' }}
            >
              MANABI
            </h1>
            <p className="mt-5 max-w-xl font-display text-xl uppercase leading-[0.95] tracking-tight sm:text-2xl">
              Real problems.
              <span className="text-accent"> Handpicked by us.</span>
            </p>

            <p className="mt-5 max-w-xl text-base leading-relaxed text-ink-soft sm:text-lg">
              Every brief here is written and reviewed by the MANABI team:
              real work, scoped so you can actually finish it. Search the
              library, open a brief, link your repo, and MANABI tracks the
              commits.
            </p>

            <form
              role="search"
              noValidate
              onSubmit={handleSubmit}
              className="mt-7 flex w-full max-w-xl flex-col gap-3 sm:flex-row"
            >
              <label htmlFor="hero-search" className="sr-only">
                Search problem briefs
              </label>
              <input
                id="hero-search"
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search problems: leaf blight, SLAs…"
                className="field min-w-0 flex-1"
              />
              <button type="submit" className={buttonClasses('primary', 'shrink-0')}>
                Browse projects
              </button>
            </form>

            <dl className="mt-9 max-w-xl border-t border-ink">
              <div className="py-4">
                <dt className="font-mono text-[9px] font-bold uppercase leading-relaxed tracking-[0.16em] text-muted">
                  Problem briefs curated
                </dt>
                <dd className="mt-1 font-display text-4xl leading-none text-accent md:text-5xl">
                  <StatsNumber />
                </dd>
              </div>
            </dl>
          </div>

          <BriefShowcase />
        </div>
      </div>
    </section>
  );
}

function StatsNumber() {
  const stats = useStats();
  if (!stats.data) {
    return <span aria-hidden>—</span>;
  }
  return <CountUp value={stats.data.problems} />;
}
