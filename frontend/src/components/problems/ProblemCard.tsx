import { memo } from 'react';
import { Link } from 'react-router-dom';
import { ArrowUpRight, GitBranch, Star } from 'lucide-react';
import { cx } from '@/lib/cx';
import { fieldLabel } from '@/lib/fields';
import type { ProblemOut } from '@/api/client';

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  // Show the problem's field so card labels match the Field filter.
  const field = fieldLabel(String(problem.field ?? ''));

  const projectLabel =
    problem.project_count === 1
      ? '1 project'
      : `${problem.project_count} projects`;

  // Zero-star problems stay clean; the chip appears once someone stars.
  const starCount = problem.star_count ?? 0;

  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group relative flex h-full flex-col overflow-hidden border border-ink bg-sheet [transition:transform_400ms_cubic-bezier(0.22,1,0.36,1),box-shadow_400ms_cubic-bezier(0.22,1,0.36,1),border-color_400ms_cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-[6px] hover:border-accent hover:shadow-[0_26px_48px_-24px_rgba(10,10,25,0.5)] focus-visible:-translate-y-[6px] focus-visible:border-accent focus-visible:shadow-[0_26px_48px_-24px_rgba(10,10,25,0.5)]',
        className,
      )}
    >
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 -translate-x-[120%] skew-x-[-18deg] bg-[linear-gradient(100deg,transparent_40%,rgba(255,255,255,0.35)_50%,transparent_60%)] [transition:transform_900ms_cubic-bezier(0.22,1,0.36,1)] group-hover:translate-x-[120%]"
      />
      <header className="relative flex items-center border-b border-line px-4 py-2.5">
        <span className="font-mono text-label font-bold uppercase tracking-[0.18em] text-accent">
          {problem.difficulty}
        </span>
        <span
          aria-hidden
          className="absolute inset-x-0 bottom-[-1px] h-[2px] origin-left scale-x-0 bg-accent [transition:transform_300ms_cubic-bezier(0.22,1,0.36,1)] group-hover:scale-x-100"
        />
      </header>

      <div className="flex flex-1 flex-col p-4 sm:p-5">
        <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          {field}
        </p>
        <h3 className="mt-2 font-display text-body uppercase leading-[1.02] tracking-tight">
          {problem.title}
        </h3>
        <p className="mt-3 line-clamp-3 text-body leading-relaxed text-ink-soft">
          {problem.summary}
        </p>

        <div className="mt-auto flex items-center justify-between gap-3 border-t border-line pt-3 font-mono text-label font-bold uppercase tracking-[0.14em]">
          <span className="flex items-center gap-2.5">
            <span className="flex items-center gap-1 text-muted">
              <GitBranch aria-hidden size={11} strokeWidth={2.4} />
              {projectLabel}
            </span>
            {starCount > 0 ? (
              <span
                title={`${starCount} star${starCount === 1 ? '' : 's'}`}
                className="flex items-center gap-1 text-accent"
              >
                <Star
                  aria-hidden
                  size={11}
                  strokeWidth={2.4}
                  className="fill-accent"
                />
                {starCount}
              </span>
            ) : null}
          </span>
          <span className="flex items-center gap-1 text-accent transition-colors group-hover:text-ink">
            Open brief
            <ArrowUpRight
              aria-hidden
              size={12}
              strokeWidth={2.6}
              className="[transition:transform_300ms_cubic-bezier(0.22,1,0.36,1)] group-hover:-translate-y-1 group-hover:translate-x-1"
            />
          </span>
        </div>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
