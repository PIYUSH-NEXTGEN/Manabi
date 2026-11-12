import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AnimatePresence, motion } from 'motion/react';
import {
  ArrowRight,
  ArrowUpRight,
  Check,
  Clock,
} from 'lucide-react';
import type { ProblemOut } from '@/api/client';
import { EASE_SNAP } from '@/design/motion';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { useProblems } from '@/hooks/useProblems';
import { useStats } from '@/hooks/useStats';
import { FIELD_LABELS, FIELD_VALUES, fieldLabel } from '@/lib/fields';
import { CountUp } from './CountUp';

const SHOWCASE_LIMIT = 6;
const CYCLE_MS = 3000;

const DIFFICULTY_FILL: Record<ProblemOut['difficulty'], number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

const CHECKS = ['Own repo', 'README', '5+ commits'];

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
              index < DIFFICULTY_FILL[level] ? 'bg-ink' : 'bg-ink/15',
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

function StatValue({ value }: { value?: number }) {
  if (value == null) {
    return <span aria-hidden>–</span>;
  }
  return <CountUp value={value} />;
}

function BriefCarousel() {
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
      className="relative mx-auto w-full max-w-[560px]"
      onMouseEnter={() => setHeld(true)}
      onMouseLeave={() => setHeld(false)}
    >
      <div
        aria-hidden
        className="absolute -inset-8 -z-10 rounded-[3rem] bg-gradient-to-br from-sky/50 via-sky/15 to-lime/30 blur-2xl dark:from-sky/10 dark:via-transparent dark:to-lime/10"
      />

      <div className="overflow-hidden rounded-[2rem] border border-ink/10 bg-sheet shadow-lift transition-shadow duration-300 hover:shadow-[0_38px_90px_-42px_rgba(10,11,13,0.38)] motion-reduce:transition-none">
        <div className="flex items-center justify-between gap-3 border-b border-line px-5 py-4 sm:px-6">
          <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.16em] text-ink-soft">
            <span className="relative flex size-2">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-lime opacity-75 motion-reduce:animate-none" />
              <span className="relative inline-flex size-2 rounded-full bg-lime" />
            </span>
            Live brief
          </span>
          <span className="font-mono text-label font-bold uppercase tabular-nums tracking-[0.14em] text-muted">
            {count > 0 ? `${pad(current + 1)} / ${pad(count)}` : 'Index'}
          </span>
        </div>

        <div
          className="flex min-h-[360px] flex-col p-6 sm:p-8"
          aria-busy={query.isLoading}
        >
          {query.isLoading ? (
            <div className="space-y-3" aria-hidden>
              <div className="flex items-center justify-between">
                <div className="skeleton h-5 w-24 rounded-full" />
                <div className="skeleton h-2.5 w-28" />
              </div>
              <div className="skeleton mt-5 h-8 w-11/12" />
              <div className="skeleton h-8 w-3/4" />
              <div className="skeleton mt-4 h-3 w-full" />
              <div className="skeleton h-3 w-5/6" />
              <div className="skeleton mt-auto h-16 w-full" />
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
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="rounded-full bg-sky px-3 py-1 font-mono text-label font-bold uppercase tracking-[0.12em] text-[#0a0b0d]">
                    {fieldLabel(active.field)}
                  </span>
                  <DifficultyMeter level={active.difficulty} />
                </div>

                <Link
                  to={`/problems/${active.id}`}
                  className="group/brief mt-5 block"
                >
                  <h3 className="font-display text-[1.7rem] leading-[1.08] tracking-[-0.03em] text-ink sm:text-[2rem]">
                    {active.title}
                  </h3>
                  <p className="mt-3 line-clamp-3 text-body leading-relaxed text-ink-soft">
                    {active.summary}
                  </p>
                </Link>

                {active.tech_tags.length > 0 ? (
                  <ul className="mt-4 flex flex-wrap gap-1.5">
                    {active.tech_tags.slice(0, 4).map((tag) => (
                      <li
                        key={tag}
                        className="rounded-full border border-ink/10 px-2.5 py-0.5 font-mono text-label font-bold uppercase tracking-[0.1em] text-ink-soft"
                      >
                        {tag}
                      </li>
                    ))}
                  </ul>
                ) : null}

                <div className="mt-6 grid grid-cols-3 gap-2">
                  {CHECKS.map((label) => (
                    <div
                      key={label}
                      className="rounded-xl border border-line bg-paper/80 px-2 py-2.5 text-center"
                    >
                      <span className="mx-auto flex size-5 items-center justify-center rounded-full bg-lime text-[#0a0b0d]">
                        <Check aria-hidden size={11} strokeWidth={3} />
                      </span>
                      <span className="mt-1.5 block font-mono text-[0.6rem] font-bold uppercase tracking-[0.08em] text-ink-soft">
                        {label}
                      </span>
                    </div>
                  ))}
                </div>

                <div className="mt-auto flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-line pt-4">
                  <span className="flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-label font-bold uppercase tracking-[0.13em] text-muted">
                    <span className="flex items-center gap-1">
                      <Clock aria-hidden size={11} strokeWidth={2.4} />
                      {`~${active.est_hours}h`}
                    </span>
                    {showDomain ? <span>{domainLabel(active.domain)}</span> : null}
                    {active.project_count > 0 ? (
                      <span>{active.project_count} built</span>
                    ) : null}
                  </span>
                  <Link
                    to={`/problems/${active.id}`}
                    className="flex items-center gap-1 text-[0.8125rem] font-semibold text-ink transition-colors hover:text-sky-strong"
                  >
                    Open brief
                    <ArrowUpRight
                      aria-hidden
                      size={13}
                      strokeWidth={2.6}
                      className="transition-transform duration-200 group-hover/brief:-translate-y-0.5 group-hover/brief:translate-x-0.5"
                    />
                  </Link>
                </div>
              </motion.div>
            </AnimatePresence>
          ) : (
            <div className="flex flex-1 flex-col">
              <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
                The index
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

        <figcaption className="flex items-center gap-3 border-t border-line px-5 py-3.5 sm:px-6">
          {count > 1 ? (
            <>
              <span
                className="flex flex-1 items-center gap-1.5"
                role="group"
                aria-label="Choose a brief"
              >
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
                          isActive ? 'bg-sky' : 'bg-tint group-hover/tick:bg-ink/25',
                        )}
                      />
                      {isActive ? (
                        paused || reduced ? (
                          <span className="absolute inset-x-0 top-1.5 h-1 rounded-full bg-ink" />
                        ) : (
                          <motion.span
                            key={item.id}
                            aria-hidden
                            className="absolute left-0 top-1.5 h-1 rounded-full bg-ink"
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
      </div>
    </figure>
  );
}

export function ProjectsSection() {
  const stats = useStats();
  const reduced = usePrefersReducedMotion();

  const statItems = [
    { label: 'Briefs curated', value: stats.data?.problems },
    { label: 'Fields', value: stats.data?.fields },
    { label: 'Sources', value: stats.data?.sources },
    { label: 'Projects built', value: stats.data?.projects },
  ];

  return (
    <section
      id="index"
      className="relative scroll-mt-6 overflow-hidden border-b border-line bg-paper py-20 md:py-28"
    >
      <div
        aria-hidden
        className="pointer-events-none absolute -right-32 top-4 size-[32rem] rounded-full bg-sky/25 blur-3xl dark:bg-sky/10"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -bottom-24 -left-40 size-[26rem] rounded-full bg-lime/20 blur-3xl dark:bg-lime/5"
      />

      <div className="relative mx-auto w-[min(1240px,96vw)]">
        <div className="flex flex-wrap items-end justify-between gap-6 border-b border-line pb-8">
          <div className="max-w-3xl">
            <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
              <span className="text-ink">01</span> / The project board
            </p>
            <h2 className="mt-3 text-balance font-display text-display leading-[1.03] tracking-[-0.03em] text-ink">
              Find a project worth{' '}
              <span className="relative isolate inline-block whitespace-nowrap">
                <span
                  aria-hidden
                  className="absolute inset-x-0 bottom-1 -z-10 h-3 rounded-full bg-lime/80"
                />
                proving.
              </span>
            </h2>
          </div>
          <p className="max-w-sm text-body leading-relaxed text-ink-soft">
            Real problems from the field, scoped into briefs you can actually
            finish. Pick a lane, match your level, and ship something worth
            showing.
          </p>
        </div>

        <div className="mt-10 grid gap-12 lg:grid-cols-[0.86fr_1.14fr] lg:items-center lg:gap-16">
          <motion.div
            initial={reduced ? false : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.25 }}
            transition={{ duration: reduced ? 0 : 0.45, ease: EASE_SNAP }}
          >
            <p className="max-w-xl text-lead leading-relaxed text-ink-soft">
              Every brief starts with a real user, a clear outcome and a stack
              you can start from. Filter by field or difficulty, then turn the
              build into proof on your GitHub, your resume and your portfolio.
            </p>

            <dl className="mt-8 grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-2">
              {statItems.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-2xl border border-line bg-sky/20 px-4 py-4 dark:bg-sky/10"
                >
                  <dd className="font-display text-[2rem] leading-none tracking-[-0.03em] text-ink">
                    <StatValue value={stat.value} />
                  </dd>
                  <dt className="mt-2 font-mono text-label font-bold uppercase leading-snug tracking-[0.12em] text-muted">
                    {stat.label}
                  </dt>
                </div>
              ))}
            </dl>

            <div className="mt-7 flex flex-wrap items-center gap-3">
              <Link
                to="/problems"
                className="press group inline-flex items-center justify-center gap-2 rounded-full bg-lime px-5 py-3.5 text-[0.875rem] font-semibold text-[#0a0b0d] transition hover:-translate-y-px hover:brightness-95 active:translate-y-0 active:scale-[0.98]"
              >
                Browse all projects
                <ArrowRight
                  aria-hidden
                  size={15}
                  strokeWidth={2.5}
                  className="transition-transform duration-200 group-hover:translate-x-0.5"
                />
              </Link>
              <Link
                to="/about"
                className="press inline-flex items-center justify-center gap-2 rounded-full bg-sky px-5 py-3.5 text-[0.875rem] font-semibold text-[#0a0b0d] transition hover:-translate-y-px hover:bg-sky-strong active:translate-y-0 active:scale-[0.98]"
              >
                How the platform works
              </Link>
            </div>

            <div className="mt-8 flex flex-wrap items-center gap-2 border-t border-line pt-5">
              <span className="mr-1 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
                Fields
              </span>
              {FIELD_VALUES.slice(0, 4).map((field) => (
                <Link
                  key={field}
                  to={`/problems?field=${field}`}
                  className="rounded-full border border-ink/10 bg-tint px-3 py-1.5 text-[0.75rem] font-semibold text-ink-soft transition-colors hover:border-sky-strong hover:bg-sky/40 hover:text-ink dark:bg-sheet"
                >
                  {FIELD_LABELS[field]}
                </Link>
              ))}
              <Link
                to="/problems"
                className="rounded-full px-2 py-1.5 text-[0.75rem] font-semibold text-ink underline underline-offset-4 transition-colors hover:text-sky-strong"
              >
                +3 more
              </Link>
            </div>
          </motion.div>

          <BriefCarousel />
        </div>
      </div>
    </section>
  );
}
