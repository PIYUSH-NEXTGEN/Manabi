import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'motion/react';
import { ArrowRight, ArrowUpRight, Clock } from 'lucide-react';
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
    <span className="flex shrink-0 items-center gap-2">
      <span aria-hidden className="flex gap-1">
        {Array.from({ length: 3 }, (_, index) => (
          <span
            key={index}
            className={cx(
              'block h-1.5 w-5 rounded-full',
              index < DIFFICULTY_FILL[level] ? 'bg-accent' : 'bg-tint',
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
      className="relative overflow-hidden rounded-card border border-line bg-sheet shadow-lift transition-shadow duration-300 hover:shadow-[0_36px_80px_-38px_rgba(48,39,27,0.42)] motion-reduce:transition-none"
      onMouseEnter={() => setHeld(true)}
      onMouseLeave={() => setHeld(false)}
    >
      <div className="flex items-center justify-between gap-3 border-b border-line px-5 py-3">
        <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.16em] text-ink-soft">
          <span aria-hidden className="block size-1.5 rounded-full bg-accent" />
          Brief index
        </span>
        <span className="font-mono text-label font-bold uppercase tabular-nums tracking-[0.14em] text-muted">
          {count > 0 ? `${pad(current + 1)} / ${pad(count)}` : 'No data'}
        </span>
      </div>

      <div className="flex min-h-[300px] flex-col p-6 sm:p-8" aria-busy={query.isLoading}>
        {query.isLoading ? (
          <div className="space-y-3" aria-hidden>
            <div className="flex items-center justify-between">
              <div className="skeleton h-2.5 w-20" />
              <div className="skeleton h-2.5 w-24" />
            </div>
            <div className="skeleton mt-3 h-7 w-3/4" />
            <div className="skeleton h-7 w-1/2" />
            <div className="skeleton mt-3 h-3 w-full" />
            <div className="skeleton h-3 w-2/3" />
            <div className="skeleton mt-auto h-9 w-full" />
          </div>
        ) : active ? (
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={active.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: reduced ? 0 : 0.38, ease: EASE_SNAP }}
              className="flex flex-1 flex-col"
            >
              <Link
                to={`/problems/${active.id}`}
                className="group/link flex h-full flex-col"
              >
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <span className="rounded-full bg-accent-soft px-2.5 py-1 font-mono text-label font-bold uppercase tracking-[0.12em] text-accent">
                    {fieldLabel(active.field)}
                  </span>
                  <DifficultyMeter level={active.difficulty} />
                </div>

                <h3 className="mt-5 line-clamp-3 font-display text-[1.5rem] leading-[1.15] tracking-[-0.02em] text-ink">
                  {active.title}
                </h3>
                <p className="mt-3 line-clamp-3 text-body leading-relaxed text-ink-soft">
                  {active.summary}
                </p>

                {active.tech_tags.length > 0 ? (
                  <ul className="mt-4 flex flex-wrap gap-1.5">
                    {active.tech_tags.slice(0, 4).map((tag) => (
                      <li
                        key={tag}
                        className="rounded-full border border-line px-2 py-0.5 font-mono text-label font-bold uppercase tracking-[0.1em] text-ink-soft"
                      >
                        {tag}
                      </li>
                    ))}
                  </ul>
                ) : null}

                <div className="mt-auto pt-6">
                  <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-line pt-3.5 font-mono text-label font-bold uppercase tracking-[0.13em] text-muted">
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
            <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
              Index
            </p>
            <p className="mt-2 font-display text-[1.5rem] leading-snug text-ink">
              Briefs unavailable
            </p>
            <p className="mt-3 max-w-xs text-body leading-relaxed text-ink-soft">
              The problems API did not respond. Open the board while it comes
              back online.
            </p>
            <Link
              to="/problems"
              className="mt-auto inline-flex w-fit items-center gap-1.5 rounded-full border border-line bg-sheet px-4 py-2.5 text-[0.8125rem] font-semibold text-ink transition-colors hover:border-ink/25"
            >
              Browse problems
              <ArrowUpRight aria-hidden size={12} strokeWidth={2.6} />
            </Link>
          </div>
        )}
      </div>

      <figcaption className="flex items-center gap-3 border-t border-line px-5 py-3">
        {count > 1 ? (
          <>
            <span className="flex flex-1 items-center gap-1.5" role="group" aria-label="Choose a brief">
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
                        'block h-1 rounded-full transition-colors duration-150',
                        isActive ? 'bg-accent/25' : 'bg-tint group-hover/tick:bg-ink/25',
                      )}
                    />
                    {isActive ? (
                      paused || reduced ? (
                        <span className="absolute inset-x-0 top-1.5 h-1 rounded-full bg-accent" />
                      ) : (
                        <motion.span
                          key={item.id}
                          aria-hidden
                          className="absolute left-0 top-1.5 h-1 rounded-full bg-accent"
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
              className="shrink-0 rounded-full px-2 py-1 text-[0.75rem] font-semibold text-muted underline underline-offset-4 transition-colors hover:text-ink"
            >
              {manualPause ? 'Play' : 'Pause'}
            </button>
          </>
        ) : (
          <span className="font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
            Live index
          </span>
        )}
      </figcaption>
    </figure>
  );
}

const HEADLINE_LINES = ['Pick a project.', 'Ship it. Prove it.'];
const HEADLINE_MARK = '#';
const HEADLINE_STEP_MS = 700;

/** Two-line centered headline, revealed without layout shift. */
function HeroHeadline() {
  const reduced = usePrefersReducedMotion();

  return (
    <h1 className="text-balance font-display text-hero leading-[1.03] tracking-[-0.035em] text-white">
      {HEADLINE_LINES.map((line, index) => (
        <motion.span
          key={line}
          className="block"
          initial={reduced ? false : { opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={
            reduced
              ? { duration: 0 }
              : {
                  duration: 0.8,
                  delay: 0.12 + (index * HEADLINE_STEP_MS) / 1000,
                  ease: EASE_SNAP,
                }
          }
        >
          {index === 0 ? (
            <span aria-hidden className="mr-[0.14em] text-white/70">
              {HEADLINE_MARK}
            </span>
          ) : null}
          {line}{' '}
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
    <>
      <section className="relative isolate flex min-h-[100svh] flex-col overflow-hidden bg-[#05283a]">
        <img
          src="/hero-sea-meadow.jpg"
          alt=""
          aria-hidden
          draggable={false}
          className="absolute inset-0 size-full object-cover object-[50%_42%] sm:object-[50%_48%] xl:object-[50%_56%]"
        />
        {/* The scene is the design: only enough scrim to hold the copy and the
            navigation at a comfortable contrast. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(3,24,35,0.55)_0%,rgba(3,24,35,0.10)_28%,rgba(3,24,35,0.08)_62%,rgba(3,24,35,0.45)_100%)]"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-[radial-gradient(58%_50%_at_50%_50%,rgba(3,24,35,0.42),transparent_78%)]"
        />

        <div className="relative mx-auto flex w-[min(1240px,94vw)] flex-1 flex-col justify-center pb-14 pt-36 text-center sm:pb-20">
          <div className="mx-auto max-w-4xl">
            <HeroHeadline />

            <p className="mx-auto mt-6 max-w-2xl text-balance text-lead leading-relaxed text-white/85">
              Tired of Googling project ideas and still not knowing what to build?
              MANABI is a curated index of real problems across every domain,
              filtered by difficulty. Pick one that fits your skills, then prove it
              with a public repo.
            </p>

            <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">
              <Link
                to="/problems"
                className="group inline-flex items-center justify-center gap-2 rounded-full bg-white px-6 py-3.5 text-[0.9375rem] font-semibold text-[#0a2938] transition-colors hover:bg-white/90"
              >
                Explore Projects
                <ArrowRight
                  aria-hidden
                  size={16}
                  strokeWidth={2.4}
                  className="transition-transform duration-200 group-hover:translate-x-0.5"
                />
              </Link>
              <Link
                to="/about"
                className="inline-flex items-center justify-center rounded-full border border-white/50 px-6 py-3.5 text-[0.9375rem] font-semibold text-white transition-colors hover:border-white/80 hover:bg-white/10"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section
        id="index"
        className="scroll-mt-6 border-b border-line bg-paper py-16 md:py-20"
      >
        <div className="mx-auto w-[min(1240px,96vw)]">
          <div className="flex flex-wrap items-end justify-between gap-8 border-b border-line pb-8">
            <div className="max-w-2xl">
              <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
                <span className="text-accent">01</span> / The index
              </p>
              <h2 className="mt-3 text-balance font-display text-display leading-[1.05] tracking-[-0.03em] text-ink">
                A brief for the thing you keep meaning to build.
              </h2>
            </div>

            <dl className="flex flex-wrap items-end gap-8">
              {HERO_STATS.map((stat) => (
                <div key={stat.key}>
                  <dt className="font-mono text-label font-bold uppercase leading-snug tracking-[0.14em] text-muted">
                    {stat.label}
                  </dt>
                  <dd className="mt-1 font-display text-[1.75rem] leading-none text-ink">
                    <StatsNumber statKey={stat.key} />
                  </dd>
                </div>
              ))}
            </dl>
          </div>

          <form
            role="search"
            noValidate
            onSubmit={handleSubmit}
            className="mt-8 flex w-full max-w-3xl flex-col gap-2 rounded-pill border border-line bg-sheet p-1.5 shadow-soft transition-colors focus-within:border-ink/25 sm:flex-row sm:items-center"
          >
            <label htmlFor="index-search" className="sr-only">
              Search problem briefs
            </label>
            <input
              id="index-search"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search the index: leaf blight, SLAs…"
              className="min-w-0 flex-1 rounded-full bg-transparent px-4 py-2.5 text-body text-ink outline-none placeholder:text-muted"
            />
            <button
              type="submit"
              className="inline-flex shrink-0 items-center justify-center rounded-full bg-ink px-5 py-2.5 text-[0.8125rem] font-semibold text-paper transition-colors hover:bg-ink/90"
            >
              Browse projects
            </button>
          </form>

          <div className="mt-10 grid items-start gap-10 lg:grid-cols-[0.8fr_1.2fr] lg:gap-16">
            <div>
              <p className="max-w-md text-body leading-relaxed text-ink-soft">
                Every brief is written and reviewed by the MANABI team, with the
                stakeholders, scope and starting stack attached. Filter the index
                by field and difficulty, or search for the problem you recognise.
              </p>
              <div className="mt-7 flex flex-wrap items-center gap-3">
                <Link to="/problems" className={buttonClasses('primary')}>
                  Browse the index
                  <ArrowUpRight aria-hidden size={14} strokeWidth={2.6} />
                </Link>
                <Link to="/about" className={buttonClasses('secondary')}>
                  How MANABI works
                </Link>
              </div>
              <ul className="mt-8 flex flex-col gap-2.5 border-t border-line pt-6 text-body leading-snug text-ink-soft">
                <li>Real problems, sourced and reviewed, never scraped.</li>
                <li>Progress read from your public GitHub repo.</li>
                <li>A verification gate that can say no.</li>
              </ul>
            </div>

            <BriefShowcase />
          </div>
        </div>
      </section>
    </>
  );
}

const HERO_STATS = [
  { key: 'problems', label: 'Briefs curated' },
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
