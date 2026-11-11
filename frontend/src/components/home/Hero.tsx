import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'motion/react';
import { ArrowUpRight, Clock } from 'lucide-react';
import type { ProblemOut } from '@/api/client';
import { buttonClasses } from '@/design';
import { EASE_SNAP } from '@/design/motion';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { useProblems } from '@/hooks/useProblems';
import { useStats } from '@/hooks/useStats';
import { fieldLabel } from '@/lib/fields';
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

function domainLabel(value: string) {
  return value
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function DifficultyMeter({ level }: { level: ProblemOut['difficulty'] }) {
  return (
    <span className="flex shrink-0 items-center gap-1.5">
      <span aria-hidden className="flex gap-0.5">
        {Array.from({ length: 3 }, (_, index) => (
          <span
            key={index}
            className={cx(
              'block h-2.5 w-1 border border-ink',
              index < DIFFICULTY_FILL[level] ? 'bg-ink' : 'bg-transparent',
            )}
          />
        ))}
      </span>
      <span className="font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
        {level}
      </span>
    </span>
  );
}

function BriefShowcase() {
  const query = useProblems({
    sort: 'popular',
    distinct: 'field',
    limit: SHOWCASE_LIMIT,
  });
  const reduced = usePrefersReducedMotion();
  const [index, setIndex] = useState(0);
  const [held, setHeld] = useState(false);
  const [manualPause, setManualPause] = useState(false);

  const items = query.data?.items.slice(0, SHOWCASE_LIMIT) ?? [];
  const count = items.length;
  const paused = held || manualPause;

  useEffect(() => {
    if (paused || reduced || count < 2) return;
    const timer = window.setTimeout(() => {
      setIndex((value) => (value + 1) % count);
    }, CYCLE_MS);
    return () => window.clearTimeout(timer);
  }, [paused, reduced, count, index]);

  const current = count > 0 ? index % count : 0;
  const active = count > 0 ? items[current] : null;
  const showDomain =
    active != null &&
    active.domain.replace(/-/g, '') !== active.field.replace(/-/g, '');

  return (
    <figure
      className="relative border border-ink bg-sheet shadow-[8px_8px_0_0_var(--tint)] transition-shadow duration-200 hover:shadow-[10px_10px_0_0_var(--tint)] motion-reduce:transition-none"
      onMouseEnter={() => setHeld(true)}
      onMouseLeave={() => setHeld(false)}
    >
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.18em]">
          <span aria-hidden className="block size-1.5 bg-accent" />
          Brief index
        </span>
        <span className="font-mono text-label font-bold uppercase tabular-nums tracking-[0.16em] text-muted">
          {count > 0 ? `${pad(current + 1)} / ${pad(count)}` : 'No data'}
        </span>
      </div>

      <div className="flex min-h-[340px] flex-col p-5 sm:p-6" aria-busy={query.isLoading}>
        {query.isLoading ? (
          <div className="space-y-3" aria-hidden>
            <div className="flex items-center justify-between">
              <div className="skeleton h-2.5 w-20" />
              <div className="skeleton h-2.5 w-24" />
            </div>
            <div className="skeleton mt-3 h-8 w-3/4" />
            <div className="skeleton h-8 w-1/2" />
            <div className="skeleton mt-3 h-3 w-full" />
            <div className="skeleton h-3 w-2/3" />
            <div className="skeleton mt-auto h-9 w-full" />
          </div>
        ) : active ? (
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={active.id}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: reduced ? 0 : 0.38, ease: EASE_SNAP }}
              className="flex flex-1 flex-col"
            >
              <Link
                to={`/problems/${active.id}`}
                className="group/link flex h-full flex-col"
              >
                <div className="flex items-start justify-between gap-4">
                  <span className="font-mono text-label font-bold uppercase tracking-[0.18em] text-accent">
                    {fieldLabel(active.field)}
                  </span>
                  <DifficultyMeter level={active.difficulty} />
                </div>

                <h2 className="mt-5 line-clamp-3 font-display text-body uppercase leading-[1.02] tracking-tight">
                  {active.title}
                </h2>
                <p className="mt-3 line-clamp-3 text-body leading-snug text-ink-soft">
                  {active.summary}
                </p>

                {active.tech_tags.length > 0 ? (
                  <ul className="mt-4 flex flex-wrap gap-1.5">
                    {active.tech_tags.slice(0, 4).map((tag) => (
                      <li
                        key={tag}
                        className="border border-line px-1.5 py-0.5 font-mono text-label font-bold uppercase tracking-[0.12em] text-ink-soft transition-colors group-hover/link:border-ink/40"
                      >
                        {tag}
                      </li>
                    ))}
                  </ul>
                ) : null}

                <div className="mt-auto pt-6">
                  <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-line pt-3 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
                    <span className="flex flex-wrap items-center gap-x-3 gap-y-1">
                      <span className="flex items-center gap-1">
                        <Clock aria-hidden size={11} strokeWidth={2.4} />
                        {`~${active.est_hours}h`}
                      </span>
                      {showDomain ? <span>{domainLabel(active.domain)}</span> : null}
                      {active.project_count > 0 ? (
                        <span>{active.project_count} built</span>
                      ) : null}
                    </span>
                    <span className="flex items-center gap-1 text-ink transition-colors group-hover/link:text-accent">
                      Open brief
                      <ArrowUpRight
                        aria-hidden
                        size={12}
                        strokeWidth={2.6}
                        className="transition-transform duration-200 group-hover/link:-translate-y-0.5 group-hover/link:translate-x-0.5"
                      />
                    </span>
                  </div>
                </div>
              </Link>
            </motion.div>
          </AnimatePresence>
        ) : (
          <div className="flex flex-1 flex-col">
            <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
              Index
            </p>
            <p className="mt-2 font-display text-display uppercase leading-tight">
              Briefs unavailable
            </p>
            <p className="mt-3 max-w-xs text-body leading-snug text-ink-soft">
              The problems API did not respond. Open the board while it comes
              back online.
            </p>
            <Link
              to="/problems"
              className="mt-auto inline-flex w-fit items-center gap-1.5 border border-ink px-4 py-2 font-mono text-label font-bold uppercase tracking-[0.16em] transition-colors hover:bg-ink hover:text-paper"
            >
              Browse problems
              <ArrowUpRight aria-hidden size={12} strokeWidth={2.6} />
            </Link>
          </div>
        )}
      </div>

      <figcaption className="flex items-center gap-3 border-t border-line px-4 py-2.5">
        {count > 1 ? (
          <>
            <span className="flex flex-1 items-center gap-1" role="group" aria-label="Choose a brief">
              {items.map((item, itemIndex) => {
                const isActive = itemIndex === current;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setIndex(itemIndex)}
                    aria-label={`Show brief ${pad(itemIndex + 1)}: ${item.title}`}
                    aria-pressed={isActive}
                    className="group/tick relative flex-1 pt-1.5"
                  >
                    <span
                      className={cx(
                        'block h-1 transition-colors duration-150',
                        isActive ? 'bg-accent/25' : 'bg-line group-hover/tick:bg-ink/40',
                      )}
                    />
                    {isActive ? (
                      paused || reduced ? (
                        <span className="absolute inset-x-0 top-1.5 h-1 bg-accent" />
                      ) : (
                        <motion.span
                          key={item.id}
                          aria-hidden
                          className="absolute left-0 top-1.5 h-1 bg-accent"
                          initial={{ width: '0%' }}
                          animate={{ width: '100%' }}
                          transition={{ duration: CYCLE_MS / 1000, ease: 'linear' }}
                        />
                      )
                    ) : null}
                  </button>
                );
              })}
            </span>
            <button
              type="button"
              onClick={() => setManualPause((value) => !value)}
              className="shrink-0 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted underline underline-offset-2 transition-colors hover:text-ink"
            >
              {manualPause ? 'Play' : 'Pause'}
            </button>
          </>
        ) : (
          <span className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
            Live index
          </span>
        )}
      </figcaption>
    </figure>
  );
}

const HEADLINE_LINES = [
  { text: 'Pick a project.', accent: false },
  { text: 'Ship it.', accent: true },
  { text: 'Prove it.', accent: true },
];
const HEADLINE_STEP_MS = 1000;

/**
 * Three-step headline. Every line is in the DOM from the first paint (empty space
 * reserved), so the reveal only animates opacity/transform: no reflow, no jank.
 */
function HeroHeadline() {
  const reduced = usePrefersReducedMotion();

  return (
    <h1 className="font-display uppercase leading-[0.92] tracking-[-0.02em] text-display    ">
      {HEADLINE_LINES.map((line, index) => (
        <motion.span
          key={line.text}
          className={cx('block', line.accent && 'text-accent')}
          initial={reduced ? false : { opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={
            reduced
              ? { duration: 0 }
              : {
                  duration: 0.7,
                  delay: (index * HEADLINE_STEP_MS) / 1000,
                  ease: EASE_SNAP,
                }
          }
        >
          {line.text}{' '}
        </motion.span>
      ))}
    </h1>
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
            <HeroHeadline />

            <div className="mt-7 max-w-xl space-y-4 text-body leading-[1.7] text-ink-soft ">
              <p>
                Tired of Googling project ideas and still not knowing what to
                build? MANABI gives you real problems across every domain,
                filtered by difficulty.
              </p>
              <p>
                Pick one that fits your skills, from learning projects to
                resume and hackathon builds. Submit your repo on MANABI and
                show your work publicly.
              </p>
            </div>

            <form
              role="search"
              noValidate
              onSubmit={handleSubmit}
              className="mt-8 flex w-full max-w-xl flex-col gap-3 sm:flex-row"
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

            <dl className="mt-10 grid max-w-xl grid-cols-3 border-t border-ink">
              {HERO_STATS.map((stat) => (
                <div
                  key={stat.key}
                  className="border-r border-line py-5 pr-3 last:border-r-0 last:pr-0 [&:not(:first-child)]:pl-3"
                >
                  <dt className="font-mono text-label font-bold uppercase leading-relaxed tracking-[0.16em] text-muted">
                    {stat.label}
                  </dt>
                  <dd className="mt-1 font-display text-display leading-none text-accent ">
                    <StatsNumber statKey={stat.key} />
                  </dd>
                </div>
              ))}
            </dl>
          </div>

          <BriefShowcase />
        </div>
      </div>
    </section>
  );
}

const HERO_STATS = [
  { key: 'problems', label: 'Projects' },
  { key: 'fields', label: 'Fields' },
  { key: 'projects', label: 'Projects' },
] as const;

function StatsNumber({
  statKey,
}: {
  statKey: (typeof HERO_STATS)[number]['key'];
}) {
  const stats = useStats();
  if (!stats.data) {
    return <span aria-hidden>-</span>;
  }
  return <CountUp value={stats.data[statKey]} />;
}
