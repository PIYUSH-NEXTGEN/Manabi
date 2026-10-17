import { memo } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { IndexCard, Tag, type Difficulty } from '@/design/primitives';
import type { ProblemOut } from '@/api/client';

const MAX_SHOWED_TAGS = 3;

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  const tags = problem.tech_tags.slice(0, MAX_SHOWED_TAGS);
  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group block h-full border-[3px] border-ink bg-white shadow-hard transition-transform duration-100 hover:-translate-y-0.5',
        className,
      )}
    >
      <IndexCard
        sourceId={problem.source_id}
        field={problem.field}
        title={problem.title}
        summary={problem.summary}
        difficulty={problem.difficulty as Difficulty}
        domain={problem.domain}
        estHours={problem.est_hours}
        className="border-0 shadow-none"
      />
      <div className="flex items-center justify-between gap-2 border-t-[3px] border-ink px-3 py-2">
        {tags.length > 0 ? (
          <div className="flex min-w-0 flex-wrap gap-1.5">
            {tags.map((tag) => (
              <Tag key={tag}>{tag}</Tag>
            ))}
          </div>
        ) : (
          <span className="font-mono text-[11px] font-bold uppercase tracking-widest text-ink/60">
            No stack listed
          </span>
        )}
        <p className="shrink-0 font-mono text-[11px] font-bold uppercase tracking-widest text-ink/60">
          {problem.project_count === 1
            ? '1 project'
            : `${problem.project_count} projects`}
        </p>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
