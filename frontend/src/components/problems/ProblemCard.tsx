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

const DIFFICULTY_LABEL: Record<ProblemOut['difficulty'], string> = {
  beginner: 'beginner',
  intermediate: 'intermediate',
  advanced: 'advanced',
};

interface ProblemCardProps {
  problem: ProblemOut;
  className?: string;
}

function ProblemCardComponent({ problem, className }: ProblemCardProps) {
  const rawDomains = String(problem.domain ?? '')
    .split(',')
    .map((d) => d.trim())
    .filter(Boolean);
  let domains = Array.from(
    new Set(rawDomains.map((d) => ALLOWED_DOMAINS[d]).filter(Boolean)),
  ).slice(0, 4);
  if (domains.length === 0) {
    domains = ['web dev'];
  }

  return (
    <Link
      to={`/problems/${problem.id}`}
      className={cx(
        'group block border-[3px] border-ink bg-white shadow-hard transition-transform duration-100 hover:-translate-y-0.5',
        className,
      )}
    >
      <div className="flex h-[360px] w-full flex-col">
        <header className="p-4 flex flex-wrap items-center justify-between gap-2">
          {domains.map((domain) => (
            <span
              key={domain}
              className="font-mono text-[10px] font-bold uppercase tracking-widest border-b-2 border-ink pb-0.5 text-ink/60"
            >
              {domain}
            </span>
          ))}
          <span
            className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink"
          >
            {DIFFICULTY_LABEL[problem.difficulty]}
          </span>
        </header>
        <div className="flex-1 p-4">
          <h3 className="font-display text-xl uppercase leading-tight">
            {problem.title}
          </h3>
          <p className="mt-3 text-sm leading-relaxed line-clamp-4">
            {problem.summary}
          </p>
        </div>
      </div>
    </Link>
  );
}

export const ProblemCard = memo(ProblemCardComponent);
