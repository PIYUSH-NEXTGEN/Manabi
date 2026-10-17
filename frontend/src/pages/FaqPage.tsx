import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

const FAQS = [
  {
    q: 'Are these problems real?',
    a: 'Yes. Every card links to its source and the original statement is shown verbatim. If a source has no link, the card says so.',
  },
  {
    q: 'Do I need an account?',
    a: 'Browsing is open. Claiming a problem, submitting a project, and getting ML answers graded need a GitHub login.',
  },
  {
    q: 'How does progress tracking work?',
    a: 'After you link a repo, MANABI reads commits, README, and good-first-issues through the GitHub API and caches the result for 10 minutes. You can refresh manually.',
  },
  {
    q: 'Who grades my ML answers?',
    a: 'An AI model grades your answer against a hidden rubric. You see which points you covered — never a raw pass/fail.',
  },
  {
    q: 'What does it cost?',
    a: 'Nothing. This is a hackathon prototype.',
  },
  {
    q: 'What happens to my data?',
    a: 'See Privacy. GitHub tokens stay on the server and are never returned to the browser.',
  },
];

export function FaqPage() {
  return (
    <StaticShell kicker="FAQ" title="Straight answers">
      <dl className="flex flex-col gap-4">
        {FAQS.map((entry) => (
          <div
            key={entry.q}
            className="flex flex-col gap-2 border-[3px] border-ink bg-white p-4 shadow-hard-sm"
          >
            <dt className="font-mono text-xs font-bold uppercase tracking-widest">
              {entry.q}
            </dt>
            <dd>{entry.a}</dd>
          </div>
        ))}
      </dl>

      <div>
        <Link to="/problems" className={buttonClasses('secondary')}>
          Browse problems
        </Link>
      </div>
    </StaticShell>
  );
}
