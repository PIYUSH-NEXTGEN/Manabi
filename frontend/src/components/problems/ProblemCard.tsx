import { memo } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { IndexCard, Tag, type Difficulty } from '@/design/primitives';
import type { ProblemOut } from '@/api/client';

const MAX_SHOWED_TAGS = 4;

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group block border-[3px] border-ink bg-white shadow-hard transition-transform duration-100 hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-lg active:translate-x-0.5 active:translate-y-0.5 active:shadow-sm',
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
      />
      <div className="flex flex-col gap-2 border-t-[3px] border-ink p-3">
        <div className="flex flex-wrap gap-1.5">
          {problem.tech_tags.slice(0, MAX_SHOWED_TAGS).map((tag) => (
            <Tag key={tag}>{tag}</Tag>
          ))}
        </div>
        <p className="font-mono text-[11px] font-bold uppercase tracking-widest">
          {problem.project_count === 1
            ? '1 project'
            : `${problem.project_count} projects`}
        </p>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
