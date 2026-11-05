import { memo } from 'react';
import { Link } from 'react-router-dom';
import { ArrowUpRight, GitBranch } from 'lucide-react';
import { cx } from '@/lib/cx';
import type { ProblemOut } from '@/api/client';

const prettify = (value: string) => value.replace(/-/g, ' ').trim();

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  // Show the problem's field so card labels match the Field filter.
  const field = prettify(String(problem.field ?? ''));

  const projectLabel =
    problem.project_count === 1
      ? '1 project'
      : `${problem.project_count} projects`;

  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group flex h-full flex-col border border-ink bg-sheet transition-[transform,box-shadow,border-color] duration-200 ease-out hover:-translate-y-1 hover:border-accent hover:shadow-[7px_7px_0_0_var(--accent)] focus-visible:-translate-y-1 focus-visible:shadow-[7px_7px_0_0_var(--accent)]',
        className,
      )}
    >
      <header className="flex items-center border-b border-line px-4 py-2.5">
        <span className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-accent">
          {problem.difficulty}
        </span>
      </header>

      <div className="flex flex-1 flex-col p-4 sm:p-5">
        <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
          {field}
        </p>
        <h3 className="mt-2 font-display text-[1.25rem] uppercase leading-[1.02] tracking-tight">
          {problem.title}
        </h3>
        <p className="mt-3 line-clamp-3 text-[13px] leading-relaxed text-ink-soft">
          {problem.summary}
        </p>

        <div className="mt-auto flex items-center justify-between gap-3 border-t border-line pt-3 font-mono text-[9px] font-bold uppercase tracking-[0.14em]">
          <span className="flex items-center gap-1 text-muted">
            <GitBranch aria-hidden size={11} strokeWidth={2.4} />
            {projectLabel}
          </span>
          <span className="flex items-center gap-1 text-accent transition-colors group-hover:text-ink">
            Open brief
            <ArrowUpRight
              aria-hidden
              size={12}
              strokeWidth={2.6}
              className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
            />
          </span>
        </div>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
