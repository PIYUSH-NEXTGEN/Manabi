import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

const PRINCIPLES = [
  {
    number: '01',
    title: 'Grounded problems',
    copy: 'Every card links to its real source and keeps the original statement verbatim.',
  },
  {
    number: '02',
    title: 'A path to execution',
    copy: 'Claim a problem, link your repo, and let progress track itself.',
  },
  {
    number: '03',
    title: 'Production-style ML practice',
    copy: 'Real debugging scenarios, graded against a hidden rubric — not puzzles.',
  },
];

export function AboutPage() {
  return (
    <StaticShell kicker="About" title="About MANABI">
      <p>
        MANABI is where students and developers find real-world problems to
        build — not tutorial clones. Briefs come from governments, companies,
        and hackathons; your GitHub becomes the proof of work.
      </p>

      <div className="grid gap-5 md:grid-cols-3">
        {PRINCIPLES.map((principle) => (
          <div
            key={principle.number}
            className="flex flex-col gap-2 border-[3px] border-ink bg-white p-4 shadow-hard-sm"
          >
            <span aria-hidden className="font-display text-4xl leading-none text-blue">
              {principle.number}
            </span>
            <h2 className="font-mono text-[11px] font-bold uppercase tracking-widest">
              {principle.title}
            </h2>
            <p>{principle.copy}</p>
          </div>
        ))}
      </div>

      <p className="border-l-[6px] border-yellow pl-4">
        Prototype built at a hackathon. The problems are real and credited;
        everything else is still landing step by step.
      </p>

      <div>
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
      </div>
    </StaticShell>
  );
}
