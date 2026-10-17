import type { UseQueryResult } from '@tanstack/react-query';
import { motion } from 'motion/react';
import { Link } from 'react-router-dom';
import type { ApiError, ProblemsListOut } from '@/api/client';
import { buttonClasses, IndexCard, Skeleton, type Difficulty } from '@/design';
import { slideUpReveal } from '@/design/motion';

const CARD_OFFSETS = ['md:col-span-7', 'md:col-span-5', 'md:col-span-5', 'md:col-span-7', 'md:col-span-6', 'md:col-span-6'];
const CARD_NUDGES = ['md:translate-y-0', 'md:translate-y-6', 'md:translate-y-0', 'md:translate-y-6', 'md:translate-y-0', 'md:translate-y-6'];

export function FeaturedProblems({
  query,
}: {
  query: UseQueryResult<ProblemsListOut, ApiError>;
}) {
  if (query.isLoading) {
    return (
      <section className="border-b-[3px] border-ink">
        <div className="mx-auto grid w-[min(1200px,96vw)] gap-6 py-12 md:grid-cols-2">
          {Array.from({ length: 6 }, (_, index) => (
            <Skeleton key={index} className="h-44" />
          ))}
        </div>
      </section>
    );
  }

  if (query.isError) {
    return (
      <section className="border-b-[3px] border-ink">
        <div
          role="alert"
          className="mx-auto my-12 flex w-[min(1200px,96vw)] flex-col items-start gap-4 border-[3px] border-ink bg-white p-6 shadow-hard"
        >
          <p className="font-mono text-xs font-bold uppercase tracking-widest">
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

  const items = query.data.items;

  if (items.length === 0) {
    return (
      <section className="border-b-[3px] border-ink">
        <div className="mx-auto my-12 w-[min(1200px,96vw)] border-[3px] border-ink bg-white p-6 shadow-hard">
          <p className="text-sm">
            No problems on the board yet. Import one from a real source on the
            Ingest page.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1200px,96vw)] py-12">
        <div className="mb-8 flex items-end justify-between gap-4 border-b-[3px] border-ink pb-3">
          <h2 className="font-display text-3xl uppercase leading-none md:text-4xl">
            Featured problems
          </h2>
          <Link
            to="/problems"
            className="font-mono text-xs font-bold uppercase tracking-widest text-blue underline underline-offset-4"
          >
            See the board →
          </Link>
        </div>

        <div className="grid gap-x-6 gap-y-10 md:grid-cols-12">
          {items.map((problem, index) => (
            <motion.div
              key={problem.id}
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.2 }}
              transition={{ delay: (index % 2) * 0.06 }}
              className={[
                CARD_OFFSETS[index % CARD_OFFSETS.length],
                CARD_NUDGES[index % CARD_NUDGES.length],
              ].join(' ')}
            >
              <Link
                to={`/problems/${problem.id}`}
                className="block transition-transform duration-150 hover:-translate-y-1"
              >
                <IndexCard
                  sourceId={problem.source_id}
                  field={problem.field}
                  title={problem.title}
                  summary={problem.summary}
                  difficulty={problem.difficulty as Difficulty}
                  domain={problem.domain}
                  estHours={problem.est_hours}
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
