import { memo } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import type { ProblemOut } from '@/api/client';

const ALLOWED_DOMAINS: Record<string, string> = {
  'web-fullstack': 'web dev',
  mobile: 'app dev',
  ml: 'ml/data sci',
  'computer-vision': 'ml/data sci',
  'nlp-llm': 'ml/data sci',
  ai: 'ai',
  blockchain: 'blockchain',
  web3: 'blockchain',
  cybersecurity: 'cybersecurity',
  'devops-cloud': 'devops/cloud',
  cloud: 'devops/cloud',
  'data-engineering': 'data engineering',
  databases: 'data engineering',
  'iot-embedded': 'system programming',
  'distributed-systems': 'system programming',
  systems: 'system programming',
  healthcare: 'web dev',
  education: 'web dev',
  agriculture: 'web dev',
  fintech: 'web dev',
  climate: 'web dev',
  governance: 'web dev',
  transport: 'web dev',
  'disaster-management': 'web dev',
  industry: 'web dev',
  'social-impact': 'web dev',
  'developer-tools': 'web dev',
  other: 'web dev',
};

const DIFFICULTY_FILL: Record<ProblemOut['difficulty'], number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function DifficultyMeter({ difficulty }: { difficulty: ProblemOut['difficulty'] }) {
  const filled = DIFFICULTY_FILL[difficulty];
  return (
    <span className="flex items-center gap-1.5" title={difficulty}>
      <span aria-hidden className="flex gap-0.5">
        {Array.from({ length: 3 }, (_, index) => (
          <span
            key={index}
            className={cx(
              'block size-2 border border-ink',
              index < filled ? 'bg-ink' : 'bg-transparent',
            )}
          />
        ))}
      </span>
      <span className="sr-only">{difficulty}</span>
    </span>
  );
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  const rawDomains = String(problem.domain ?? '')
    .split(',')
    .map((d) => d.trim())
    .filter(Boolean);
  let domains = Array.from(
    new Set(rawDomains.map((d) => ALLOWED_DOMAINS[d]).filter(Boolean)),
  ).slice(0, 2);
  if (domains.length === 0) {
    domains = ['web dev'];
  }

  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group flex h-full flex-col border border-ink bg-sheet transition-colors duration-150 hover:border-accent',
        className,
      )}
    >
      <header className="flex flex-wrap items-center justify-between gap-x-3 gap-y-2 border-b border-line px-4 py-2.5">
        <span className="flex flex-wrap items-center gap-x-3 gap-y-1">
          {domains.map((domain) => (
            <span
              key={domain}
              className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted"
            >
              {domain}
            </span>
          ))}
        </span>
        <DifficultyMeter difficulty={problem.difficulty} />
      </header>

      <div className="flex flex-1 flex-col p-4">
        <p className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-accent">
          {problem.source_id ?? `BRIEF-${problem.id}`}
        </p>
        <h3 className="mt-2 font-display text-[1.2rem] uppercase leading-[1.02] tracking-tight">
          {problem.title}
        </h3>
        <p className="mt-3 line-clamp-4 text-[13px] leading-relaxed text-ink-soft">
          {problem.summary}
        </p>
        <div className="mt-auto flex items-center justify-between gap-3 border-t border-line pt-3 font-mono text-[9px] font-bold uppercase tracking-[0.16em]">
          <span className="text-muted">{problem.field}</span>
          <span className="text-accent transition-colors group-hover:text-ink">
            Open brief →
          </span>
        </div>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
