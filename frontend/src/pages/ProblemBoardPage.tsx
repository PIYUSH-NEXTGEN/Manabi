import { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { buttonClasses, Input, Skeleton } from '@/design/primitives';
import { ProblemCard } from '@/components/problems/ProblemCard';
import { FilterSelect } from '@/components/problems/FilterSelect';
import { TechChips } from '@/components/problems/TechChips';
import { useFacets } from '@/hooks/useFacets';
import { useInfiniteProblems } from '@/hooks/useInfiniteProblems';

const boardHeader =
  'font-mono text-[11px] font-bold uppercase tracking-widest';
const monoLabel = cx(boardHeader);

function BoardSkeletons() {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {Array.from({ length: 6 }, (_, index) => (
        <div
          key={index}
          className="border-[3px] border-ink bg-white p-4 shadow-hard"
        >
          <Skeleton className="mb-2 h-3 w-24" />
          <Skeleton className="mb-3 h-6 w-3/4" />
          <Skeleton className="mb-2 h-3 w-full" />
          <Skeleton className="h-3 w-2/3" />
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
  const tech = searchParams.getAll('tech');

  const filterKey = [
    q,
    field,
    domain,
    difficulty,
    source,
    tech.join(','),
  ].join('|');
  const filters = useMemo(
    () => ({ q, field, domain, difficulty, source, tech }),
    [filterKey],
  );

  const board = useInfiniteProblems(filters);
  const problems = board.data?.pages.flatMap((page) => page.items) ?? [];
  const total = board.data?.pages[0]?.total ?? 0;
  const hasFilters =
    Boolean(q || field || domain || difficulty || source) || tech.length > 0;

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

  function toggleTech(value: string) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      const current = next.getAll('tech');
      next.delete('tech');
      const updated = current.includes(value)
        ? current.filter((t) => t !== value)
        : [...current, value];
      for (const t of updated) next.append('tech', t);
      return next;
    });
  }

  function clearFilters() {
    setSearchParams({});
  }

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1200px,96vw)] py-12">
        <p className={monoLabel}>Problem board</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-none md:text-6xl">
          Problems
        </h1>
        <p className="mt-3 max-w-2xl text-lg leading-snug">
          Every real, unglamorous problem in the index. Filter it down, pick
          one, and build the thing.
        </p>

        <section
          aria-label="Search and filters"
          className="mt-8 border-[3px] border-ink bg-white p-4 shadow-hard"
        >
          <form
            noValidate
            onSubmit={(event) => event.preventDefault()}
            className="grid gap-4"
          >
            <Input
              label="Search"
              type="search"
              placeholder="Leaf blight, stock-outs, SLAs…"
              value={q}
              onChange={(event) => setParam('q', event.target.value)}
            />
          </form>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <FilterSelect
              label="Field"
              value={field}
              onChange={(value) => setParam('field', value)}
              options={facets.data?.fields ?? []}
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
          <div className="mt-4 flex flex-col gap-2">
            <span className="sr-only" id="tech-chips-label">
              Filter by tech
            </span>
            <TechChips
              options={(facets.data?.tech_tags ?? []).slice(0, 8)}
              selected={tech}
              onToggle={toggleTech}
            />
          </div>
        </section>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
          <p className="font-mono text-xs font-bold uppercase tracking-widest">
            {board.data ? `${total} problems in the index` : 'Counting…'}
          </p>
          {hasFilters ? (
            <button
              type="button"
              onClick={clearFilters}
              className={buttonClasses('secondary')}
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
          <section className="mt-6 border-[3px] border-ink bg-white p-6 shadow-hard">
            <p>
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

        {board.data && problems.length === 0 && hasFilters ? (
          <section className="mt-6 border-[3px] border-ink bg-white p-6 shadow-hard">
            <p>
              Nothing in the index matches those filters yet. Clear one or two
              and look again.
            </p>
          </section>
        ) : null}

        {problems.length > 0 ? (
          <div className="mt-6 grid items-stretch gap-6 md:grid-cols-2 xl:grid-cols-3">
            {problems.map((problem) => (
              <ProblemCard key={problem.id} problem={problem} className="h-full" />
            ))}
          </div>
        ) : null}

        {board.hasNextPage ? (
          <div className="mt-8 flex justify-center">
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
