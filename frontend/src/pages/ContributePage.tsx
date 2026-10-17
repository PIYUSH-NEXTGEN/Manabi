import { Link } from 'react-router-dom';
import { buttonClasses, Stamp } from '@/design/primitives';
import { StaticShell } from './StaticShell';

export function ContributePage() {
  return (
    <StaticShell kicker="Contribute" title="Build on someone else's repo" wide>
      <div className="flex items-center gap-4">
        <Stamp tone="open" />
        <p className="font-mono text-[11px] font-bold uppercase tracking-widest">
          Projects marked open are looking for contributors
        </p>
      </div>

      <ol className="flex flex-col gap-4">
        <li className="border-t-[3px] border-ink pt-3">
          <p className="font-mono text-xs font-bold uppercase tracking-widest text-blue">
            01 — Find a live project
          </p>
          <p className="mt-1">
            Open a problem, scroll to its submitted projects, and look for the
            'Open for contributors' stamp.
          </p>
        </li>
        <li className="border-t-[3px] border-ink pt-3">
          <p className="font-mono text-xs font-bold uppercase tracking-widest text-blue">
            02 — Take a good-first-issue
          </p>
          <p className="mt-1">
            Each project page lists contributor issues straight from GitHub,
            good-first-issue first.
          </p>
        </li>
        <li className="border-t-[3px] border-ink pt-3">
          <p className="font-mono text-xs font-bold uppercase tracking-widest text-blue">
            03 — Open a PR like everywhere else
          </p>
          <p className="mt-1">
            MANABI does not fork your workflow. Commits show up on the project
            page automatically.
          </p>
        </li>
      </ol>

      <p>
        No project yet for a problem you like? Claim it and be the first —
        then tick 'open for contributors' when you submit.
      </p>

      <div className="flex flex-wrap gap-4">
        <Link to="/problems" className={buttonClasses('primary')}>
          Find a problem
        </Link>
        <Link to="/how-it-works" className={buttonClasses('secondary')}>
          How it works
        </Link>
      </div>
    </StaticShell>
  );
}
