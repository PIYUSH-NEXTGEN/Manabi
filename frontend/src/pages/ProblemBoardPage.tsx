import { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'motion/react';
import { cx } from '@/lib/cx';
import type { ProblemOut } from '@/api/client';
import { EASE_SNAP } from '@/design/motion';
import { buttonClasses, Input, Skeleton } from '@/design/primitives';
import { ProblemCard } from '@/components/problems/ProblemCard';
import { FilterSelect } from '@/components/problems/FilterSelect';
import { useFacets } from '@/hooks/useFacets';
import { fieldLabel } from '@/lib/fields';
import { useInfiniteProblems } from '@/hooks/useInfiniteProblems';

type GoalKey = 'resume' | 'hackathon' | 'learning';

const GOAL_OPTIONS: { value: GoalKey; label: string }[] = [
  { value: 'resume', label: 'Resume' },
  { value: 'hackathon', label: 'Hackathon' },
  { value: 'learning', label: 'Learning' },
];

function goalOf(problem: ProblemOut): GoalKey | undefined {
  return problem.goal ?? undefined;
}

function BoardSkeletons() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
      {Array.from({ length: 6 }, (_, index) => (
        <div
          key={index}
          className="overflow-hidden rounded-card border border-line bg-sheet"
        >
          <div className="flex items-center justify-between border-b border-line px-4 py-3">
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

  function clearFilters() {
    setSearchParams({});
  }

  return (
    <main className="border-b border-line bg-paper">
      <div className="mx-auto w-[min(1120px,94vw)] py-12 md:py-16">
        <header className="max-w-2xl">
          <h1 className="font-display text-display leading-[1.02] tracking-[-0.03em] text-ink">
            Projects
          </h1>
          <p className="mt-4 text-lead leading-relaxed text-ink-soft">
            Every brief is written and reviewed by the MANABI team. Filter it
            down, pick the one you can finish, and build the thing.
          </p>
        </header>

        <section
          aria-label="Search and filters"
          className="mt-8 border-y border-line py-5"
        >
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-[minmax(0,1.4fr)_repeat(3,minmax(0,1fr))]">
            <Input
              label="Search"
              type="search"
              placeholder="Leaf blight, stock-outs, SLAs…"
              value={q}
              onChange={(event) => setParam('q', event.target.value)}
            />
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

          <div className="mt-5 flex flex-wrap items-center gap-2">
            <span className="mr-1 text-sm text-muted">Goal</span>
            {GOAL_OPTIONS.map((option) => {
              const active = goal === option.value;
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
                    'inline-flex items-center gap-2 rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors',
                    active
                      ? 'border-ink bg-ink text-paper'
                      : 'border-line bg-paper text-ink-soft hover:border-ink/30 hover:text-ink',
                  )}
                >
                  {option.label}
                  <span
                    className={cx(
                      'text-xs',
                      active ? 'text-paper/70' : 'text-muted',
                    )}
                  >
                    {board.data
                      ? `${count} ${count === 1 ? 'project' : 'projects'}`
                      : 'Counting…'}
                  </span>
                </button>
              );
            })}
          </div>
        </section>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm text-muted">
            {board.data ? `${shownTotal} projects in the index` : 'Counting…'}
          </p>
          {hasFilters ? (
            <button
              type="button"
              onClick={clearFilters}
              className="text-sm text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink"
            >
              Clear filters
            </button>
          ) : null}
        </div>

        {board.isPending || board.isPlaceholderData ? (
          <div className="mt-6">
            <BoardSkeletons />
          </div>
        ) : null}

        {board.isError && !board.isPlaceholderData && !board.data ? (
          <section className="mt-6 border-y border-line py-6">
            <p className="max-w-2xl text-body leading-relaxed text-ink-soft">
              The board could not be loaded. That is almost certainly a backend
              or network problem and it will not fix itself by refreshing
              faster.
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
          <section className="mt-6 border-y border-line py-6">
            {goal ? (
              <p className="text-body leading-relaxed text-ink-soft">
                No projects in this track yet. New briefs land here as soon as
                they&apos;re tagged for the{' '}
                {goal === 'resume'
                  ? 'resume'
                  : goal === 'hackathon'
                    ? 'hackathon'
                    : 'learning'}{' '}
                track.
              </p>
            ) : (
              <p className="text-body leading-relaxed text-ink-soft">
                Nothing in the index matches those filters yet. Clear one or two
                and look again.
              </p>
            )}
          </section>
        ) : null}

        {visibleProblems.length > 0 ? (
          <div className="mt-6 grid items-stretch gap-5 sm:grid-cols-2 xl:grid-cols-3">
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
    </main>
  );
}
