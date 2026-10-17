import { motion } from 'motion/react';
import { Link } from 'react-router-dom';
import { buttonClasses, IndexCard, type Difficulty } from '@/design';
import { letterDrop, wobble } from '@/design/motion';
import { useProblems } from '@/hooks/useProblems';
import { useStats } from '@/hooks/useStats';
import type { ProblemOut } from '@/api/client';

const WORDMARK = 'MANABI';
const STACK_ROTATIONS = [-3, 2, -1];

function HeroCard({ problem }: { problem: ProblemOut }) {
  return (
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
  );
}

function CardStack({ problems }: { problems: ProblemOut[] }) {
  return (
    <div className="relative hidden h-[430px] md:block">
      {problems.map((problem, index) => (
        <div
          key={problem.id}
          className="absolute w-[320px]"
          style={{
            top: index * 36,
            left: index * 28,
            zIndex: 10 - index,
            transform: `rotate(${STACK_ROTATIONS[index % STACK_ROTATIONS.length]}deg)`,
          }}
        >
          <HeroCard problem={problem} />
        </div>
      ))}
    </div>
  );
}

export function Hero() {
  const stats = useStats();
  const problems = useProblems({ sort: 'newest', limit: 6 });
  const cards = problems.data?.items.slice(0, 3) ?? [];

  return (
    <section className="border-b-[3px] border-ink">
      <div className="mx-auto grid w-[min(1200px,96vw)] gap-10 py-12 md:grid-cols-[1.1fr_1fr] md:py-16">
        <div className="flex flex-col gap-6">
          <h1
            aria-label={WORDMARK}
            className="flex font-display leading-[0.85] tracking-tight"
            style={{ fontSize: 'clamp(3rem, 12vw, 11rem)' }}
          >
            <span aria-hidden className="flex">
              {WORDMARK.split('').map((letter, index) => (
                <motion.span
                  key={`${letter}-${index}`}
                  custom={index}
                  variants={letterDrop}
                  initial="hidden"
                  animate="show"
                  className="inline-block"
                >
                  {letter}
                </motion.span>
              ))}
            </span>
          </h1>

          <p className="max-w-xl text-lg leading-snug">
            Real problem briefs with real sources. Claim one, link your repo,
            and build in public.
          </p>

          <div className="flex flex-wrap gap-4">
            <Link to="/problems" className={buttonClasses('primary')}>
              Browse problems
            </Link>
            <Link to="/ml" className={buttonClasses('secondary')}>
              Practice ML
            </Link>
          </div>

          <p className="font-mono text-xs font-bold uppercase tracking-widest">
            {stats.data
              ? `${stats.data.problems} problems on the board`
              : stats.isError
                ? 'Problem count unavailable'
                : 'Counting problems…'}
          </p>
        </div>

        <div className="relative">
          <motion.span
            variants={wobble}
            initial="rest"
            whileHover="hover"
            className="absolute -top-4 right-0 z-20 inline-block rotate-3 border-[3px] border-ink bg-yellow px-3 py-1 font-mono text-[11px] font-bold uppercase tracking-widest shadow-hard-sm"
          >
            Real problems only
          </motion.span>

          {cards.length > 0 ? (
            <>
              <CardStack problems={cards} />
              <div className="md:hidden">
                <HeroCard problem={cards[0]} />
              </div>
            </>
          ) : problems.isError ? (
            <p
              role="alert"
              className="border-[3px] border-ink bg-white p-4 font-mono text-xs uppercase shadow-hard"
            >
              {problems.error.detail}
            </p>
          ) : (
            <div className="hidden flex-col gap-4 md:flex">
              <div className="skeleton h-36 border-[3px] border-ink" aria-hidden />
              <div className="skeleton h-36 border-[3px] border-ink" aria-hidden />
              <div className="skeleton h-36 border-[3px] border-ink" aria-hidden />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
