import type { UseQueryResult } from '@tanstack/react-query';
import { motion } from 'motion/react';
import { Link } from 'react-router-dom';
import type { ApiError, ProblemsListOut } from '@/api/client';
import { buttonClasses, IndexCard, Skeleton, type Difficulty } from '@/design';
import { slideUpReveal } from '@/design/motion';

export function FeaturedProblems({
  query,
}: {
  query: UseQueryResult<ProblemsListOut, ApiError>;
}) {
  if (query.isLoading) {
    return (
      <section className="border-b border-ink">
        <div className="mx-auto grid w-[min(1240px,96vw)] gap-5 py-14 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 3 }, (_, index) => (
            <Skeleton key={index} className="h-64" />
          ))}
        </div>
      </section>
    );
  }

  if (query.isError) {
    return (
      <section className="border-b border-ink">
        <div
          role="alert"
          className="mx-auto my-12 flex w-[min(1240px,96vw)] flex-col items-start gap-4 border border-ink bg-sheet p-6"
        >
          <p className="font-mono text-[11px] font-bold uppercase tracking-[0.16em]">
            Could not load problems — {query.error.detail}
          </p>
          <button
            type="button"
            onClick={() => query.refetch()}
            className={buttonClasses('primary')}
          >
            Retry
          </button>
        </div>
      </section>
    );
  }

  if (query.data == null) {
    return null;
  }

  const items = query.data.items.slice(0, 3);

  if (items.length === 0) {
    return (
      <section className="border-b border-ink">
        <div className="mx-auto my-12 w-[min(1240px,96vw)] border border-ink bg-sheet p-6">
          <p className="text-sm">No problems on the board yet.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="border-b border-ink">
      <div className="mx-auto w-[min(1240px,96vw)] py-14">
        <div className="mb-8 flex flex-wrap items-end justify-between gap-4 border-b border-ink pb-4">
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-accent">
              01 / Index highlights
            </p>
            <h2 className="mt-2 font-display text-3xl uppercase leading-none tracking-tight md:text-4xl">
              Featured problems
            </h2>
          </div>
          <Link
            to="/problems"
            className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent underline decoration-accent/40 underline-offset-4 hover:text-ink"
          >
            See the board →
          </Link>
        </div>

        <div className="grid items-stretch gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((problem, index) => (
            <motion.div
              key={problem.id}
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.2 }}
              transition={{ delay: index * 0.06 }}
              className="h-full min-w-0"
            >
              <Link to={`/problems/${problem.id}`} className="block h-full">
                <IndexCard
                  sourceId={problem.source_id}
                  field={problem.field}
                  title={problem.title}
                  summary={problem.summary}
                  difficulty={problem.difficulty as Difficulty}
                  domain={problem.domain}
                  estHours={problem.est_hours}
                  className="flex h-full min-h-64 flex-col"
                />
              </Link>
            </motion.div>
          ))}
        </div>

        <div className="mt-10">
          <Link to="/problems" className={buttonClasses('secondary')}>
            Browse all problems
          </Link>
        </div>
      </div>
    </section>
  );
}
