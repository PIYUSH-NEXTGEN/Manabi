import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

const STEPS = [
  {
    n: '01',
    title: 'Find a problem',
    body: 'Browse the Projects page and pick one that interests you.',
  },
  {
    n: '02',
    title: 'Open the problem page',
    body: 'Read the description, why it matters, the tech stack, and what you can add later.',
  },
  {
    n: '03',
    title: 'Link your repo',
    body: 'Click Submit a project and paste your public GitHub repository URL.',
  },
  {
    n: '04',
    title: 'Build and ship',
    body: 'Work on the project in your repo. MANABI pulls commits, README status, and open issues from GitHub so your progress shows up on the problem page.',
  },
  {
    n: '05',
    title: 'Use the build guide',
    body: 'Each problem has a Build guide with phases to help you start, implement, and ship without getting stuck.',
  },
];

export function HowItWorksPage() {
  return (
    <StaticShell kicker="How it works" title="From idea to shipped code">
      <section className="border-t border-ink pt-6">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
            00
          </span>
          <h2 className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
            What MANABI is
          </h2>
        </div>
        <p className="mt-3 max-w-2xl">
          MANABI is a catalog of real project problems. Each problem comes with
          a short description, who it affects, why it matters, and a suggested
          tech stack. You pick a problem, link your GitHub repository, and your
          progress gets tracked automatically.
        </p>
      </section>

      <section className="mt-10 border-t border-ink pt-6">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
            01
          </span>
          <h2 className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
            How to use it
          </h2>
        </div>
        <ol className="mt-4">
          {STEPS.map((step) => (
            <li
              key={step.n}
              className="grid gap-2 border-t border-line py-4 sm:grid-cols-[48px_minmax(0,1fr)] sm:gap-4"
            >
              <span className="font-display text-xl leading-none text-accent/80">
                {step.n}
              </span>
              <div>
                <h3 className="font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
                  {step.title}
                </h3>
                <p className="mt-1.5 max-w-2xl">{step.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="mt-10 border-t border-ink pt-6">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
            02
          </span>
          <h2 className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
            What you get
          </h2>
        </div>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          <li className="flex gap-3 border-t border-line pt-3">
            <span aria-hidden className="mt-2 block size-1.5 shrink-0 bg-accent" />
            A curated list of problems across domains like web dev, AI, ML,
            blockchain, cybersecurity, devops, data engineering, and systems.
          </li>
          <li className="flex gap-3 border-t border-line pt-3">
            <span aria-hidden className="mt-2 block size-1.5 shrink-0 bg-accent" />
            Progress tracking from your GitHub repository.
          </li>
          <li className="flex gap-3 border-t border-line pt-3">
            <span aria-hidden className="mt-2 block size-1.5 shrink-0 bg-accent" />
            A build guide with phases for every project.
          </li>
          <li className="flex gap-3 border-t border-line pt-3">
            <span aria-hidden className="mt-2 block size-1.5 shrink-0 bg-accent" />
            The option to mark your project as open for contributors.
          </li>
        </ul>
      </section>

      <div className="mt-10 border-t border-ink pt-6">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse projects
        </Link>
      </div>
    </StaticShell>
  );
}
