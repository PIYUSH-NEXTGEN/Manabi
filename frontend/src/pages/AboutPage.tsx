import { Link } from 'react-router-dom';
import { ArrowUpRight } from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';
import {
  RefAside,
  RefFacts,
  RefItem,
  RefList,
  RefNote,
  RefSection,
} from './staticParts';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';

const STEPS = [
  {
    number: '01',
    title: 'Browse the index',
    copy: 'Search and filter the catalog by field, domain, difficulty, tech stack, or goal track. Every card opens a full brief, not a teaser.',
  },
  {
    number: '02',
    title: 'Claim a brief',
    copy: 'Read who is affected, why it matters, the suggested stack, the approaches and the datasets. Sign in with GitHub when you are ready to claim it.',
  },
  {
    number: '03',
    title: 'Submit a public repo',
    copy: 'Ownership, README, commit history and AI relevance are checked before anything goes public. Uncertain cases go to human review; a failed check never earns a badge.',
  },
  {
    number: '04',
    title: 'Let the repo prove it',
    copy: 'Commits, README state and open issues update from GitHub. Once the submission is verified and the repo has at least five commits, you can mark the project complete.',
  },
];

const INDEX_ITEMS = [
  {
    title: 'Problem index',
    copy: 'Seven fields, three difficulty levels and goal tracks for resumes, hackathons and learning. Briefs carry the source, stakeholders, approaches, stack and datasets.',
  },
  {
    title: 'Dashboard',
    copy: 'Every repo you submit, with its verification state and live progress. Recommendations are scored against the topics and languages on your GitHub profile.',
  },
  {
    title: 'Ask MANABI',
    copy: 'A catalog assistant that answers from the index only. Tell it your stack and the time you have; it points at briefs that exist or says plainly that nothing fits.',
  },
  {
    title: 'Contributor projects',
    copy: 'Projects marked open list good-first issues from GitHub, so another builder can join a real codebase instead of starting from an empty folder.',
  },
];

const PRINCIPLES = [
  {
    number: '01',
    title: 'Grounded briefs',
    copy: 'Every statement keeps its original source and context. If a detail is inferred, the brief says so.',
  },
  {
    number: '02',
    title: 'A path to execution',
    copy: 'Approaches, a suggested stack, an effort estimate and datasets ship with the brief. Swap what you know; the path stays.',
  },
  {
    number: '03',
    title: 'Proof over claims',
    copy: 'Verification reads ownership, README, commits and relevance. Public progress comes from the repo, not from a checkbox.',
  },
];

export function AboutPage() {
  return (
    <StaticShell
      kicker="About"
      code="REF 01"
      title="About MANABI"
      intro="MANABI is a working catalog of real problems. Browse briefs from seven fields, claim the one you can finish, and let a public GitHub repository prove the work. Curated briefs, a real verification gate, and progress that updates from the repo itself."
      aside={
        <>
          <RefAside title="At a glance">
            <RefFacts
              items={[
                { label: 'Fields', value: '7 specialisations' },
                { label: 'Difficulty', value: '3 levels' },
                {
                  label: 'Tracks',
                  value: 'Resume · Hackathon · Learning',
                },
                { label: 'Sign-in', value: 'GitHub OAuth' },
                { label: 'License', value: 'MIT' },
              ]}
            />
          </RefAside>

          <RefAside title="The short version">
            <p className="text-ink">
              Real problems. A public repo. Commits that prove the work.
            </p>
            <Link
              to="/problems"
              className={buttonClasses('primary', 'w-full justify-center')}
            >
              Browse the index
            </Link>
          </RefAside>

          <RefAside title="Open source">
            <p>
              MANABI is MIT-licensed and built in the open. Read the code, open
              an issue, or leave a star.
            </p>
            <a
              href={REPO_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.14em] text-accent transition-colors hover:text-ink"
            >
              <GithubMark size={13} />
              View the repository
              <ArrowUpRight aria-hidden size={12} strokeWidth={2.6} />
            </a>
          </RefAside>
        </>
      }
    >
      <RefSection id="why" index="01" title="Why MANABI exists">
        <p>
          Most project ideas are invented for a portfolio and forgotten by the
          next application. MANABI starts from problems that organisations,
          competitions and public programs have already published, adds the
          context a builder needs, and keeps a link back to the original.
        </p>
        <p>
          There is no scraping and no infinite feed. Briefs are curated and
          reviewed, and the source stays attached. The point is not to collect
          ideas. It is to make real work findable, finishable and visible.
        </p>
      </RefSection>

      <RefSection id="workflow" index="02" title="From brief to proof">
        <div className="flex flex-col">
          {STEPS.map((step) => (
            <div
              key={step.number}
              className="grid gap-2 border-t border-line py-4 first:border-t-0 first:pt-0 sm:grid-cols-[56px_minmax(0,1fr)] sm:gap-5"
            >
              <span
                aria-hidden
                className="font-display text-display leading-none text-accent"
              >
                {step.number}
              </span>
              <div>
                <h3 className="font-mono text-label font-bold uppercase tracking-[0.16em] text-ink">
                  {step.title}
                </h3>
                <p className="mt-1.5 text-body leading-relaxed">
                  {step.copy}
                </p>
              </div>
            </div>
          ))}
        </div>
      </RefSection>

      <RefSection id="index" index="03" title="What is in the index">
        <dl className="grid gap-x-8 sm:grid-cols-2">
          {INDEX_ITEMS.map((item) => (
            <div key={item.title} className="border-t border-line py-4">
              <dt className="font-mono text-label font-bold uppercase tracking-[0.14em] text-ink">
                {item.title}
              </dt>
              <dd className="mt-1.5 text-body leading-relaxed">
                {item.copy}
              </dd>
            </div>
          ))}
        </dl>
      </RefSection>

      <RefSection id="principles" index="04" title="What we optimise for">
        <ol className="grid gap-4 sm:grid-cols-3">
          {PRINCIPLES.map((principle) => (
            <li
              key={principle.number}
              className="flex flex-col rounded-card border border-line bg-sheet p-5 shadow-soft"
            >
              <span
                aria-hidden
                className="font-mono text-label font-bold tabular-nums tracking-[0.14em] text-accent"
              >
                {principle.number}
              </span>
              <h3 className="mt-2 font-mono text-label font-bold uppercase tracking-[0.14em] text-ink">
                {principle.title}
              </h3>
              <p className="mt-2 text-body leading-relaxed">
                {principle.copy}
              </p>
            </li>
          ))}
        </ol>
      </RefSection>

      <RefSection id="status" index="05" title="Status">
        <RefNote tone="accent">
          MANABI is a working prototype, not a company. The catalog, GitHub
          verification, progress tracking, dashboard and catalog chat are live.
          The Repo Analyzer is still being built, so its form is visible but
          disabled. Data may be reset while the project is under active
          development.
        </RefNote>
        <RefList>
          <RefItem>
            Verification is deliberately conservative: when GitHub or the
            relevance model is unsure, the submission goes to human review
            instead of receiving a badge.
          </RefItem>
          <RefItem>
            Reported projects return to review. Three independent reports are
            enough to pause a published project while an admin looks at it.
          </RefItem>
        </RefList>
      </RefSection>

      <div className="flex flex-wrap gap-3 border-t border-line pt-6">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
        <Link to="/faq" className={buttonClasses('secondary')}>
          Read the FAQ
        </Link>
      </div>
    </StaticShell>
  );
}