import { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  GraduationCap,
  Search,
  SlidersHorizontal,
  Trophy,
  X,
  FileBadge,
} from 'lucide-react';
import { cx } from '@/lib/cx';
import type { ProblemOut } from '@/api/client';
import { EASE_SNAP } from '@/design/motion';
import { buttonClasses, Input, Skeleton } from '@/design/primitives';
import { ProblemCard } from '@/components/problems/ProblemCard';
import { FilterSelect } from '@/components/problems/FilterSelect';
import { useFacets } from '@/hooks/useFacets';
import { fieldLabel } from '@/lib/fields';
import { useInfiniteProblems } from '@/hooks/useInfiniteProblems';

const microLabel = 'font-mono text-[9px] font-bold uppercase tracking-[0.16em]';

type GoalKey = 'resume' | 'hackathon' | 'learning';

const GOAL_OPTIONS: {
  value: GoalKey;
  label: string;
  description: string;
  icon: typeof Trophy;
}[] = [
  {
    value: 'resume',
    label: 'Resume',
    description: 'Interview-ready builds that show recruiters proof of work.',
    icon: FileBadge,
  },
  {
    value: 'hackathon',
    label: 'Hackathon',
    description: 'Deadline-tight briefs for team sprints and demo days.',
    icon: Trophy,
  },
  {
    value: 'learning',
    label: 'Learning',
    description: 'Skill-builder projects to grow at your own pace.',
    icon: GraduationCap,
  },
];

function goalOf(problem: ProblemOut): GoalKey | undefined {
  return problem.goal ?? undefined;
}

function BoardSkeletons() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 2xl:grid-cols-3">
      {Array.from({ length: 6 }, (_, index) => (
        <div key={index} className="border border-line bg-sheet">
          <div className="flex items-center justify-between border-b border-line px-4 py-2.5">
            <Skeleton className="h-2.5 w-16" />
            <Skeleton className="h-2.5 w-8" />
          </div>
          <div className="p-5">
            <Skeleton className="mb-2 h-2.5 w-20" />
            <Skeleton className="mb-3 h-6 w-4/5" />
            <Skeleton className="mb-2 h-3 w-full" />
            <Skeleton className="h-3 w-2/3" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function ProblemBoardPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const facets = useFacets();

  const q = searchParams.get('q') ?? '';
  const field = searchParams.get('field') ?? '';
  const domain = searchParams.get('domain') ?? '';
  const difficulty = searchParams.get('difficulty') ?? '';
  const source = searchParams.get('source') ?? '';
  const goalParam = searchParams.get('goal');
  const goal =
    GOAL_OPTIONS.find((option) => option.value === goalParam)?.value ?? '';

  const filterKey = [q, field, domain, difficulty, source].join('|');
  const filters = useMemo(
    () => ({ q, field, domain, difficulty, source }),
    [filterKey],
  );

  const board = useInfiniteProblems(filters);
  const problems = board.data?.pages.flatMap((page) => page.items) ?? [];
  const total = board.data?.pages[0]?.total ?? 0;
  const visibleProblems = goal
    ? problems.filter((problem) => goalOf(problem) === goal)
    : problems;
  const shownTotal = goal ? visibleProblems.length : total;
  const hasFilters = Boolean(q || field || domain || difficulty || source);

  const activeFilters: { key: string; label: string; value: string }[] = [
    ...(q ? [{ key: 'q', label: 'search', value: q }] : []),
    ...(field ? [{ key: 'field', label: 'field', value: fieldLabel(field) }] : []),
    ...(domain ? [{ key: 'domain', label: 'domain', value: domain }] : []),
    ...(difficulty
      ? [{ key: 'difficulty', label: 'difficulty', value: difficulty }]
      : []),
    ...(source ? [{ key: 'source', label: 'source', value: source }] : []),
  ];

  function setParam(key: string, value: string) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) {
        next.set(key, value);
      } else {
        next.delete(key);
      }
      return next;
    });
  }

  function removeFilter(key: string) {
    setParam(key, '');
  }

  function clearFilters() {
    setSearchParams({});
  }

  return (
    <main className="border-b border-ink bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-10 md:py-12">


        <div className="mt-8 flex flex-wrap items-end justify-between gap-6 border-b border-ink pb-8">
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-accent">
              Collection 01
            </p>
            <h1
              className="mt-2 font-display uppercase leading-[0.86] tracking-[-0.03em]"
              style={{ fontSize: 'clamp(3rem, 8vw, 5.5rem)' }}
            >
              Projects
            </h1>
          </div>
          <p className="max-w-md text-sm leading-relaxed text-ink-soft">
            Every brief is written and reviewed by the MANABI team. Filter it
            down, pick the one you can finish, and build the thing.
          </p>
        </div>

        <div className="mt-8" role="group" aria-label="Project tracks">
          <p className={cx(microLabel, 'text-muted')}>Browse by track</p>
          <div className="mt-3 grid gap-5 sm:grid-cols-3">
            {GOAL_OPTIONS.map((option) => {
              const active = goal === option.value;
              const Icon = option.icon;
              const count = problems.filter(
                (problem) => goalOf(problem) === option.value,
              ).length;
              return (
                <button
                  key={option.value}
                  type="button"
                  aria-pressed={active}
                  onClick={() => setParam('goal', active ? '' : option.value)}
                  className={cx(
                    'flex flex-col gap-2 border border-ink bg-sheet px-5 py-5 text-left transition-colors',
                    active
                      ? 'bg-ink text-paper'
                      : 'text-ink hover:bg-tint',
                  )}
                >
                  <span className="flex items-center gap-2 font-mono text-[10px] font-bold uppercase tracking-[0.16em]">
                    <Icon
                      aria-hidden
                      size={14}
                      strokeWidth={2.4}
                      className={active ? 'text-accent-soft' : 'text-accent'}
                    />
                    {option.label}
                  </span>
                  <span
                    className={cx(
                      'text-sm leading-snug',
                      active ? 'text-paper/75' : 'text-ink-soft',
                    )}
                  >
                    {option.description}
                  </span>
                  <span
                    className={cx(microLabel, active ? 'text-paper/55' : 'text-muted')}
                  >
                    {board.data ? `${count} projects` : 'Counting…'}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-8 grid gap-8 lg:grid-cols-[276px_minmax(0,1fr)] lg:gap-10">
          <aside className="lg:sticky lg:top-24 lg:self-start">
            <section
              aria-label="Search and filters"
              className="border border-ink bg-sheet"
            >
              <div className="flex items-center justify-between border-b border-line px-4 py-2.5">
                <h2 className={cx(microLabel, 'flex items-center gap-2')}>
                  <SlidersHorizontal
                    aria-hidden
                    size={12}
                    strokeWidth={2.4}
                    className="text-accent"
                  />
                  Filter index
                </h2>
              </div>

              <div className="p-4">
                <form
                  noValidate
                  onSubmit={(event) => event.preventDefault()}
                >
                  <div className="relative">
                    <Search
                      aria-hidden
                      size={14}
                      strokeWidth={2.4}
                      className="pointer-events-none absolute left-3 top-[2.3rem] text-muted"
                    />
                    <Input
                      label="Search"
                      type="search"
                      placeholder="Leaf blight, stock-outs, SLAs…"
                      value={q}
                      onChange={(event) => setParam('q', event.target.value)}
                      style={{ paddingLeft: '2.25rem' }}
                    />
                  </div>
                </form>

                <div className="mt-4 flex flex-col gap-4">
                  <FilterSelect
                    label="Field"
                    value={field}
                    onChange={(value) => setParam('field', value)}
                    options={facets.data?.fields ?? []}
                    labelFor={fieldLabel}
                  />
                  <FilterSelect
                    label="Difficulty"
                    value={difficulty}
                    onChange={(value) => setParam('difficulty', value)}
                    options={facets.data?.difficulties ?? []}
                  />
                  <FilterSelect
                    label="Domain"
                    value={domain}
                    onChange={(value) => setParam('domain', value)}
                    options={facets.data?.domains ?? []}
                  />
                </div>
              </div>
            </section>
          </aside>

          <div className="min-w-0">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line pb-3">
              <p className={cx(microLabel, 'text-muted')}>
                {board.data
                  ? `${shownTotal} projects in the index`
                  : 'Counting…'}
              </p>
            </div>

            {hasFilters ? (
              <div className="flex flex-wrap items-center gap-2 border-b border-line py-3">
                <span className={cx(microLabel, 'text-muted')}>
                  Filtered by
                </span>
                {activeFilters.map((filter) => (
                  <button
                    key={`${filter.key}-${filter.value}`}
                    type="button"
                    onClick={() => removeFilter(filter.key)}
                    aria-label={`Remove ${filter.label}: ${filter.value}`}
                    className="group inline-flex items-center gap-1.5 border border-ink bg-sheet px-2 py-1 font-mono text-[9px] font-bold uppercase tracking-[0.12em] transition-colors hover:bg-ink hover:text-paper"
                  >
                    <span className="text-muted group-hover:text-paper/70">
                      {filter.label}
                    </span>
                    {filter.value}
                    <X aria-hidden size={10} strokeWidth={3} />
                  </button>
                ))}
                <button
                  type="button"
                  onClick={clearFilters}
                  className="inline-flex items-center border border-ink px-2.5 py-1.5 font-mono text-[9px] font-bold uppercase tracking-[0.12em] transition-colors hover:bg-ink hover:text-paper"
                >
                  Clear filters
                </button>
              </div>
            ) : null}

            {board.isPending || board.isPlaceholderData ? (
              <div className="mt-6">
                <BoardSkeletons />
              </div>
            ) : null}

            {board.isError && !board.isPlaceholderData && !board.data ? (
              <section className="mt-6 border border-ink bg-sheet p-6">
                <p className="max-w-2xl text-sm leading-relaxed">
                  The board could not be loaded. That is almost certainly a
                  backend or network problem and it will not fix itself by
                  refreshing faster.
                </p>
                <button
                  type="button"
                  onClick={() => board.refetch()}
                  className={cx(buttonClasses('primary'), 'mt-4')}
                >
                  Try again
                </button>
              </section>
            ) : null}

            {board.data &&
            visibleProblems.length === 0 &&
            (!goal ? hasFilters : true) ? (
              <section className="mt-6 border border-line bg-sheet p-6">
                {goal ? (
                  <p className="text-sm leading-relaxed">
                    No projects in this track yet. New briefs land here as
                    soon as they're tagged for the{' '}
                    {goal === 'resume'
                      ? 'resume'
                      : goal === 'hackathon'
                        ? 'hackathon'
                        : 'learning'}{' '}
                    track.
                  </p>
                ) : (
                  <p className="text-sm leading-relaxed">
                    Nothing in the index matches those filters yet. Clear one
                    or two and look again.
                  </p>
                )}
              </section>
            ) : null}

            {visibleProblems.length > 0 ? (
              <div className="mt-6 grid items-stretch gap-5 sm:grid-cols-2 2xl:grid-cols-3">
                {visibleProblems.map((problem, index) => (
                  <motion.div
                    key={problem.id}
                    initial={{ opacity: 0, y: 14 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                      duration: 0.32,
                      delay: Math.min(index * 0.035, 0.28),
                      ease: EASE_SNAP,
                    }}
                    className="h-full min-w-0"
                  >
                    <ProblemCard problem={problem} className="h-full" />
                  </motion.div>
                ))}
              </div>
            ) : null}

            {board.hasNextPage && !goal ? (
              <div className="mt-10 flex justify-center">
                <button
                  type="button"
                  onClick={() => board.fetchNextPage()}
                  disabled={board.isFetchingNextPage}
                  className={buttonClasses('primary')}
                >
                  {board.isFetchingNextPage ? 'Loading…' : 'Load more'}
                </button>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </main>
  );
}
