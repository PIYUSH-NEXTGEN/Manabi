import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

const linkClass =
  'text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink';

const GROUPS = [
  {
    id: 'start',
    title: 'Getting started',
    items: [
      {
        q: 'What is MANABI?',
        a: 'A catalog of real problems. You pick a brief, build the solution in a public GitHub repository, and MANABI checks the work and tracks progress from that repository.',
      },
      {
        q: 'Do I need an account?',
        a: 'You can browse without one. Claiming a brief, submitting a project, using the dashboard or Ask MANABI, and starring a project need a GitHub login.',
      },
      {
        q: 'Is MANABI free?',
        a: 'Yes. It is a free prototype and the code is MIT-licensed. There are no paid plans.',
      },
      {
        q: 'Do I have to use the suggested stack?',
        a: 'No. The stack and approaches are suggestions. Verification looks at whether the repository matches the problem, not whether you followed the suggested tools.',
      },
    ],
  },
  {
    id: 'catalog',
    title: 'The catalog',
    items: [
      {
        q: 'Are the problems real?',
        a: 'Yes. Briefs come from published problem statements, competitions and public programs. Each one is reviewed by hand and keeps its source attached. MANABI does not scrape or invent a source.',
      },
      {
        q: 'What is in a brief?',
        a: 'A summary, who is affected, why it matters, difficulty, an hour estimate, a suggested stack, approaches, datasets and the original source. Some briefs also have a build guide, team plan or resume notes.',
      },
      {
        q: 'What do the difficulty levels mean?',
        a: 'They describe scope, not skill level. Beginner is one flow in one stack. Intermediate adds persistence, authentication or an API. Advanced is systems work such as event delivery, consistency or offline sync.',
      },
      {
        q: 'What are the goal tracks?',
        a: 'Resume, Hackathon and Learning are labels for what a brief suits. They narrow the board; they do not change the brief.',
      },
    ],
  },
  {
    id: 'submit',
    title: 'Submitting a project',
    items: [
      {
        q: 'Which repositories can I submit?',
        a: 'A public repository you own or have the required access to. It cannot be a fork or archived, it needs a README and at least five commits, and a repository can only be linked to one problem.',
      },
      {
        q: 'Can I submit a private repository?',
        a: 'No. MANABI reads public repository data only. Your GitHub token is not used to read private repositories.',
      },
      {
        q: 'Can I submit a project I started before using MANABI?',
        a: 'Yes, if it is public and meets the submission rules. Repositories older than 180 days need a stronger match before they verify automatically, and often go to review.',
      },
      {
        q: 'Can I work in a team?',
        a: 'Yes. Each person uses their own GitHub account. For an organisation repository, push or admin access is enough. For someone else\'s repository, you need at least three commits under your account.',
      },
      {
        q: 'What are the limits?',
        a: 'Five submissions per rolling 24 hours, ten active projects, and ten submit attempts per hour. Chat has its own daily limit. A rate-limited response tells you how long to wait.',
      },
    ],
  },
  {
    id: 'verify',
    title: 'Verification and review',
    items: [
      {
        q: 'How does verification work?',
        a: 'MANABI checks ownership, the README, the commit count and the relevance of the repository to the brief. The relevance check compares the brief with the README, repository metadata and your description.',
      },
      {
        q: 'What does "verified" mean?',
        a: 'The submission passed those checks and becomes public. It is not an endorsement of the project\'s quality, and it does not mean the work is finished.',
      },
      {
        q: 'Why did my project go to review?',
        a: 'The relevance check was uncertain, the repository is older than 180 days, GitHub or the model was unavailable, or users reported the project. An admin can approve or reject it. A project in review re-checks itself at most once a day.',
      },
      {
        q: 'Why was my submission rejected?',
        a: 'Common reasons are a fork, an archived repository, no README, fewer than five commits, no ownership basis, or a repository already linked to another problem. The response includes the specific reason.',
      },
      {
        q: 'Can I edit or remove a submission?',
        a: 'Yes. From the dashboard you can edit the description, demo link and contributor setting, or remove the project. Editing the description runs the relevance check again.',
      },
    ],
  },
  {
    id: 'tracking',
    title: 'Tracking and completion',
    items: [
      {
        q: 'How does progress tracking work?',
        a: 'MANABI reads commits, README state and open issues through the GitHub API and caches the result for ten minutes. You can force a refresh from the project page. Repeat refreshes are rate-limited.',
      },
      {
        q: 'When can I mark a project complete?',
        a: 'When the submission is verified, the repository has a README, and it has at least five commits. You can add a demo link and a short reflection at that point, and reopen the project later if it is still moving.',
      },
      {
        q: 'How do contributors join a project?',
        a: 'Submit with "open for contributors" turned on. The project page then lists its GitHub issues, good-first-issue first, and contributors open pull requests as they would on any repository.',
      },
    ],
  },
  {
    id: 'data',
    title: 'Chat, data and rules',
    items: [
      {
        q: 'What does Ask MANABI do?',
        a: 'It answers from the catalog only. Tell it your stack and the time you have, and it suggests briefs that exist, with links. If nothing fits, it says so.',
      },
      {
        q: 'Is my chat stored?',
        a: 'No. Messages are sent to the model to produce a reply and are not written to the database. The daily message limit is tracked per account.',
      },
      {
        q: 'Where does my GitHub token go?',
        a: (
          <>
            It is stored on the server and used for GitHub API calls. It is never
            returned to the browser. The{' '}
            <Link to="/privacy" className={linkClass}>
              Privacy page
            </Link>{' '}
            lists everything that is stored.
          </>
        ),
      },
      {
        q: 'How do recommendations work?',
        a: 'They score briefs against the languages and topics on your GitHub profile. With no profile signals, the newest briefs are shown instead.',
      },
      {
        q: 'How do I report a project?',
        a: 'Sign in and use the report action on a published project. You can report a project once and cannot report your own. Three reports send it back to review.',
      },
      {
        q: 'How do I report a bug or a security issue?',
        a: (
          <>
            Use the{' '}
            <Link to="/contact" className={linkClass}>
              Contact page
            </Link>
            . Bugs can go in the public issue tracker. Security reports should
            ask for a private channel first.
          </>
        ),
      },
    ],
  },
];

export function FaqPage() {
  return (
    <ProsePage
      kicker="FAQ"
      title="Straight answers"
      intro="How the catalog, verification and tracking work. These answers match the behaviour the API enforces."
    >
      {GROUPS.map((group) => (
        <ProseSection key={group.id} id={group.id} title={group.title}>
          <FaqList items={group.items} />
        </ProseSection>
      ))}

      <div className="flex flex-wrap gap-3 border-t border-line pt-8">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
        <Link to="/about" className={buttonClasses('secondary')}>
          About MANABI
        </Link>
      </div>
    </ProsePage>
  );
}

function FaqList({
  items,
}: {
  items: { q: string; a: ReactNode }[];
}) {
  return (
    <div className="flex flex-col">
      {items.map((entry) => (
        <details
          key={entry.q}
          className="group border-t border-line py-4 first:border-t-0 first:pt-0"
        >
          <summary className="flex cursor-pointer list-none items-start justify-between gap-4 [&::-webkit-details-marker]:hidden">
            <span className="font-medium text-ink">{entry.q}</span>
            <Plus
              aria-hidden
              size={14}
              strokeWidth={2}
              className="mt-1 shrink-0 text-muted transition-transform duration-200 group-open:rotate-45"
            />
          </summary>
          <p className="mt-2 pr-6">{entry.a}</p>
        </details>
      ))}
    </div>
  );
}
