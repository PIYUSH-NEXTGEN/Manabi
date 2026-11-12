import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';
import { RefAside, RefIndex, RefNote, RefSection } from './staticParts';

const GROUPS = [
  {
    id: 'catalog',
    index: '01',
    title: 'The catalog',
    items: [
      {
        q: 'What is in a brief?',
        a: 'A summary, who is affected, why it matters, the difficulty, an effort estimate, a suggested stack, the approaches to take, datasets, and a link to the original source. It is enough to start without another research pass.',
      },
      {
        q: 'Are these real problems?',
        a: 'Yes. Briefs come from published problem statements, competitions and public programs. MANABI keeps the original statement and the source attached, and does not scrape or invent a source. Curation is manual.',
      },
      {
        q: 'What do the difficulty levels mean?',
        a: 'Scope, not a skill gate. Beginner is one flow in one stack, intermediate adds persistence, auth or an API, and advanced is systems work such as event delivery, consistency or offline sync.',
      },
      {
        q: 'What are the goal tracks?',
        a: 'Resume, Hackathon and Learning are labels for the outcome a brief suits. They narrow the board; they do not change the brief itself.',
      },
      {
        q: 'Do I need an account?',
        a: 'Browsing is open. Claiming a problem, submitting a repository, opening your dashboard, using Ask MANABI and starring projects need a GitHub login.',
      },
    ],
  },
  {
    id: 'submitting',
    index: '02',
    title: 'Submitting a project',
    items: [
      {
        q: 'Which repositories can I submit?',
        a: 'Public repositories you own: your account is the owner, you have push or admin access to the organisation repository, or you have at least three commits under your own account. Forks, archived repositories, repositories without a README and repositories with fewer than five commits are rejected. One repository can be linked to one problem.',
      },
      {
        q: 'How does verification work?',
        a: 'Four gates: ownership, a README, at least five commits, and an AI relevance check that compares the brief with the README, repository metadata and your description. A keyword check takes over if the model fails, and that fallback can never auto-verify.',
      },
      {
        q: 'Why did my project go to review?',
        a: 'The relevance check was uncertain, the repository is older than 180 days, GitHub or the model was unavailable, or users reported the project. An admin can approve or reject it, and a project in review re-checks itself at most once a day.',
      },
      {
        q: 'What are the limits?',
        a: 'Five submissions per rolling 24 hours, ten active projects, and ten submit attempts per hour. Chat has its own daily allowance. A rate-limited response names the wait, and the interface shows a live countdown.',
      },
    ],
  },
  {
    id: 'tracking',
    index: '03',
    title: 'Tracking and completion',
    items: [
      {
        q: 'How does progress tracking work?',
        a: 'MANABI reads commits, README state and open issues through the GitHub API and caches the result for ten minutes. You can force a refresh from the project page; repeat refreshes are rate-limited.',
      },
      {
        q: 'When can I mark a project complete?',
        a: 'When the submission is verified, the repository has a README, and it has at least five commits. You can add a demo URL and a short reflection at that point, and reopen the project later if it is still moving.',
      },
      {
        q: 'Can I edit or remove a project?',
        a: 'The dashboard lets you edit the description, demo URL and contributor setting, or remove the project. Editing the description re-runs the relevance check immediately.',
      },
      {
        q: 'How do contributors join?',
        a: 'Submit with “open for contributors” turned on. The project page then lists its GitHub issues, good-first-issue first, and contributors can open pull requests as they would on any repository. MANABI follows the commits.',
      },
    ],
  },
  {
    id: 'chat-data',
    index: '04',
    title: 'Chat, data and rules',
    items: [
      {
        q: 'What does Ask MANABI do?',
        a: 'It answers from the catalog only. Give it your stack and the time you have, and it suggests briefs that exist, with links. If nothing fits, it says so instead of inventing a project.',
      },
      {
        q: 'Is my chat stored?',
        a: 'No. Messages are sent to the model to produce a reply and are not written to the database. The daily message limit is tracked per account.',
      },
      {
        q: 'Where does my GitHub token go?',
        a: 'It is stored server-side and used for GitHub API calls; it is never returned to the browser. The Privacy page lists everything MANABI stores.',
      },
    ],
  },
];

const CONTENTS = GROUPS.map((group) => ({
  href: `#${group.id}`,
  label: group.title,
}));

export function FaqPage() {
  return (
    <StaticShell
      kicker="FAQ"
      code="REF 02"
      title="Straight answers"
      intro="How the catalog, verification and tracking actually work. No support script, no hidden rules: this is the same behaviour the API enforces."
      aside={
        <>
          <RefAside title="On this page">
            <RefIndex items={CONTENTS} />
          </RefAside>

          <RefAside title="Still stuck?">
            <p>
              If the answer is not here, the Contact page has a real channel.
              Bugs and concrete questions can be discussed in the open.
            </p>
            <Link
              to="/contact"
              className={buttonClasses('secondary', 'w-full justify-center')}
            >
              Contact us
            </Link>
          </RefAside>

          <RefNote>
            Verification and rate limits live in the API. This page explains
            them; it does not replace them.
          </RefNote>
        </>
      }
    >
      {GROUPS.map((group) => (
        <RefSection
          key={group.id}
          id={group.id}
          index={group.index}
          title={group.title}
        >
          <div className="flex flex-col">
            {group.items.map((entry) => (
              <details
                key={entry.q}
                className="group border-t border-line py-3.5 first:border-t-0 first:pt-0"
              >
                <summary className="flex cursor-pointer list-none items-start gap-3 [&::-webkit-details-marker]:hidden">
                  <Plus
                    aria-hidden
                    size={13}
                    strokeWidth={2.6}
                    className="mt-0.5 shrink-0 text-accent transition-transform duration-200 group-open:rotate-45"
                  />
                  <span className="font-mono text-label font-bold uppercase leading-snug tracking-[0.12em] text-ink">
                    {entry.q}
                  </span>
                </summary>
                <p className="mt-2 pl-[25px] text-body leading-relaxed text-ink-soft">
                  {entry.a}
                </p>
              </details>
            ))}
          </div>
        </RefSection>
      ))}

      <div className="flex flex-wrap gap-3 border-t border-line pt-6">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
        <Link to="/about" className={buttonClasses('secondary')}>
          How MANABI works
        </Link>
      </div>
    </StaticShell>
  );
}