import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

export function HowItWorksPage() {
  return (
    <StaticShell kicker="How it works" title="From idea to shipped code">
      <section className="mt-8 border-[3px] border-ink bg-white p-6 shadow-hard">
        <h2 className="font-mono text-xs font-bold uppercase tracking-widest">
          What MANABI is
        </h2>
        <p className="mt-2 text-sm leading-relaxed">
          MANABI is a catalog of real project problems. Each problem comes with
          a short description, who it affects, why it matters, and a suggested
          tech stack. You pick a problem, link your GitHub repository, and your
          progress gets tracked automatically.
        </p>
      </section>

      <section className="mt-8 border-[3px] border-ink bg-white p-6 shadow-hard">
        <h2 className="font-mono text-xs font-bold uppercase tracking-widest">
          How to use it
        </h2>
        <ol className="mt-4 list-decimal ml-6 space-y-3 text-sm leading-relaxed">
          <li>
            <span className="font-bold">Find a problem.</span> Browse the
            Projects page and pick one that interests you.
          </li>
          <li>
            <span className="font-bold">Open the problem page.</span> Read the
            description, why it matters, the tech stack, and what you can add
            later.
          </li>
          <li>
            <span className="font-bold">Link your repo.</span> Click Submit a
            project and paste your public GitHub repository URL.
          </li>
          <li>
            <span className="font-bold">Build and ship.</span> Work on the
            project in your repo. MANABI pulls commits, README status, and open
            issues from GitHub so your progress shows up on the problem page.
          </li>
          <li>
            <span className="font-bold">Use the build guide.</span> Each problem
            has a Build guide with phases to help you start, implement, and ship
            without getting stuck.
          </li>
        </ol>
      </section>

      <section className="mt-8 border-[3px] border-ink bg-white p-6 shadow-hard">
        <h2 className="font-mono text-xs font-bold uppercase tracking-widest">
          What you get
        </h2>
        <ul className="mt-4 list-disc ml-6 space-y-2 text-sm leading-relaxed">
          <li>A curated list of problems across domains like web dev, AI, ML,
            blockchain, cybersecurity, devops, data engineering, and systems.</li>
          <li>Progress tracking from your GitHub repository.</li>
          <li>A build guide with phases for every project.</li>
          <li>The option to mark your project as open for contributors.</li>
        </ul>
      </section>

      <div className="mt-10">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse projects
        </Link>
      </div>
    </StaticShell>
  );
}
