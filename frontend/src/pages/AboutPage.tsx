import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

const PRINCIPLES = [
  {
    number: '01',
    title: 'Grounded briefs',
    copy: 'Every brief keeps the original problem statement verbatim and links to the organisation that published it. Nothing goes live before review.',
  },
  {
    number: '02',
    title: 'A path to execution',
    copy: 'Each brief comes with a three-phase build guide — Start, Implement, Ship — and a suggested stack you can swap for your own.',
  },
  {
    number: '03',
    title: 'Proof of work',
    copy: 'Claim a brief, link a public repo, and commits, README status, and open issues update the project page on their own.',
  },
];

const IN_THE_INDEX = [
  {
    title: 'Problem index',
    copy: 'Briefs across web, mobile, ML and data, cloud, cybersecurity, systems, and blockchain — filterable by field, difficulty, and tech stack.',
  },
  {
    title: 'Build guides',
    copy: 'Three phases per brief, with the approach list and the deliverable you should be holding at the end of each phase.',
  },
  {
    title: 'Your dashboard',
    copy: 'Every repo you submit, tracked against GitHub, plus recommendations scored on the briefs you have already picked.',
  },
  {
    title: 'Ask MANABI',
    copy: 'A chat that answers only from the index: give it your stack and the time you have, and it points at briefs that exist.',
  },
];

export function AboutPage() {
  return (
    <StaticShell kicker="About" title="About MANABI">
      <p>
        MANABI is a catalog of real-world problems — from governments,
        companies, hackathons, and public programs — with a build path
        attached. Pick a brief, follow its guide, link your GitHub repository,
        and let the commits prove the work.
      </p>

      <div className="grid gap-5 md:grid-cols-3">
        {PRINCIPLES.map((principle) => (
          <div
            key={principle.number}
            className="flex flex-col gap-2 border border-ink bg-sheet p-4"
          >
            <span aria-hidden className="font-display text-4xl leading-none text-accent">
              {principle.number}
            </span>
            <h2 className="font-mono text-[11px] font-bold uppercase tracking-widest">
              {principle.title}
            </h2>
            <p>{principle.copy}</p>
          </div>
        ))}
      </div>

      <section aria-label="What is in the index" className="border-t border-ink pt-5">
        <h2 className="font-mono text-[11px] font-bold uppercase tracking-widest text-ink">
          What is in the index
        </h2>
        <dl className="mt-3 flex flex-col">
          {IN_THE_INDEX.map((item) => (
            <div
              key={item.title}
              className="grid gap-1 border-t border-line py-3 sm:grid-cols-[180px_minmax(0,1fr)] sm:gap-4"
            >
              <dt className="font-mono text-[10px] font-bold uppercase tracking-[0.14em] text-accent">
                {item.title}
              </dt>
              <dd>{item.copy}</dd>
            </div>
          ))}
        </dl>
      </section>

      <p className="border-l-[6px] border-accent pl-4">
        Built as a hackathon prototype: the index, build guides, GitHub
        tracking, and the chat are live. The Repo
        Analyzer is still being built, so its form does not submit yet.
      </p>

      <div className="flex flex-wrap gap-4">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
      </div>
    </StaticShell>
  );
}
