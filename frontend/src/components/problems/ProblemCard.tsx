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
        'group relative flex h-full flex-col overflow-hidden rounded-card border border-line bg-sheet shadow-soft transition-[transform,box-shadow,border-color] duration-300 ease-out hover:-translate-y-1 hover:border-ink/20 hover:shadow-lift focus-visible:-translate-y-1 focus-visible:border-accent/50 focus-visible:shadow-lift',
        className,
      )}
    >
      <header className="flex items-center justify-between gap-3 px-5 pt-5">
        <span className="rounded-full bg-accent-soft px-2.5 py-1 font-mono text-label font-bold uppercase tracking-[0.12em] text-accent">
          {problem.difficulty}
        </span>
        <span className="text-label font-semibold text-muted">{field}</span>
      </header>

      <div className="flex flex-1 flex-col p-5">
        <h3 className="font-display text-[1.125rem] leading-snug tracking-[-0.015em] text-ink">
          {problem.title}
        </h3>
        <p className="mt-3 line-clamp-3 text-body leading-relaxed text-ink-soft">
          {problem.summary}
        </p>

        <div className="mt-auto flex items-center justify-between gap-3 border-t border-line pt-3.5 font-mono text-label font-bold uppercase tracking-[0.12em]">
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
          <span className="flex items-center gap-1 text-ink transition-colors group-hover:text-accent">
            Open brief
            <ArrowUpRight
              aria-hidden
              size={12}
              strokeWidth={2.6}
              className="transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
            />
          </span>
        </div>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
