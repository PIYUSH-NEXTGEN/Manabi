import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

const FAQS = [
  {
    q: 'What is in a brief?',
    a: 'A real problem statement trimmed into a short brief: a summary, who it affects, why it matters, a difficulty level, an effort estimate, a suggested stack, and the approaches to take.',
  },
  {
    q: 'Are these problems real?',
    a: 'Yes. Every card keeps the original statement verbatim and links to the organisation that published it. If a source has no link, the card says so.',
  },
  {
    q: 'What do beginner, intermediate, and advanced mean?',
    a: 'Scope, not a skill gate. Beginner is one flow in one stack, intermediate adds persistence, auth, or an API, and advanced is systems work — event delivery, consistency, offline sync. Pick where you want to stretch.',
  },
  {
    q: 'Do I need an account?',
    a: 'Browsing is open. Claiming a problem, submitting a project, and opening your dashboard need a GitHub login.',
  },
  {
    q: 'How does progress tracking work?',
    a: 'After you link a public repo, MANABI reads commits, README status, and open issues through the GitHub API and caches the result for 10 minutes. You can refresh manually.',
  },
  {
    q: 'What does Ask MANABI do?',
    a: 'It answers from the catalog only: tell it your stack and the time you have, and it suggests briefs that exist, with a link to each one. It will say so plainly when nothing fits.',
  },
  {
    q: 'What does it cost?',
    a: 'Nothing. This is a hackathon prototype.',
  },
  {
    q: 'What happens to my data?',
    a: 'See Privacy. GitHub tokens stay on the server and are never returned to the browser, and chat messages are not stored.',
  },
];

export function FaqPage() {
  return (
    <StaticShell kicker="FAQ" title="Straight answers">
      <dl className="flex flex-col gap-4">
        {FAQS.map((entry) => (
          <div
            key={entry.q}
            className="flex flex-col gap-2 border border-ink bg-sheet p-4"
          >
            <dt className="font-mono text-xs font-bold uppercase tracking-widest">
              {entry.q}
            </dt>
            <dd>{entry.a}</dd>
          </div>
        ))}
      </dl>

      <div className="flex flex-wrap gap-4">
        <Link to="/problems" className={buttonClasses('secondary')}>
          Browse problems
        </Link>
      </div>
    </StaticShell>
  );
}
