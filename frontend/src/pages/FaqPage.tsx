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
        a: 'A free catalog of project ideas for students and developers. Every idea is documented as a brief, sorted by field, goal and difficulty, and ready to build for learning, a hackathon or your resume. Build one in a public GitHub repo, submit it, and your work is shown on the platform.',
      },
      {
        q: 'What does MANABI mean?',
        a: 'MANABI comes from the Japanese word for learning. The name fits. The platform is about learning by building real projects, not collecting tutorial certificates.',
      },
      {
        q: 'Do I need an account?',
        a: 'You can browse without one. Claiming a brief, submitting a project, using the dashboard or Ask MANABI, and starring a project need a GitHub login.',
      },
      {
        q: 'Is MANABI free?',
        a: 'Yes, completely free. There are no paid plans, no premium briefs and no locked features. The code is open source and MIT-licensed.',
      },
      {
        q: 'Do I have to use the suggested stack?',
        a: 'No. The stack and approaches are suggestions. Verification looks at whether the repository matches the problem, not whether you followed the suggested tools.',
      },
      {
        q: 'How long does it take to find an idea?',
        a: 'Usually one visit. Filter by field, goal and difficulty, open two or three briefs, and pick one. If you would rather describe what you know, ask the chat assistant for a shortlist.',
      },
    ],
  },
  {
    id: 'catalog',
    title: 'The catalog',
    items: [
      {
        q: 'Where do the project ideas come from?',
        a: 'The MANABI team curates them by hand. Some come from quality problem statements published across the internet: hackathons, competitions, public programs and open challenges. Others are written by us. Every brief is documented by a person and keeps its source attached. MANABI does not scrape sources or invent one.',
      },
      {
        q: 'Which fields are covered?',
        a: 'Seven for now: web development, app development, AI and machine learning, data science, cyber security, DevOps and cloud, and blockchain. Each field also carries a domain, such as healthcare, education, agriculture or fintech, so you can find a problem area you care about.',
      },
      {
        q: 'What is in a brief?',
        a: 'A summary, who is affected, why it matters, difficulty, an hour estimate, a suggested stack, approaches, datasets and the original source. Track briefs go further.',
      },
      {
        q: 'Which briefs are "quality"?',
        a: 'A brief goes in when the problem is real, the scope fits the stated difficulty, and there is a clear way to build and show it. Briefs that cannot be scoped or verified stay out.',
      },
      {
        q: 'Can I suggest a project idea?',
        a: (
          <>
            Yes. Send it through the{' '}
            <Link to="/contact" className={linkClass}>
              Contact page
            </Link>{' '}
            or open an issue on GitHub with the source and why it is worth
            building. The team reviews suggestions, documents the good ones and
            adds them to the catalog.
          </>
        ),
      },
    ],
  },
  {
    id: 'tracks',
    title: 'Goals and difficulty',
    items: [
      {
        q: 'What are the goal tracks?',
        a: 'Resume, Hackathon and Learning are the three major categories. They describe what a brief suits. They narrow the board and each one unlocks extra material on the brief page.',
      },
      {
        q: 'What does each track add?',
        a: 'Resume briefs can include scope levels, target roles, CV bullet templates and interview questions. Hackathon briefs can include a role-based team plan and a pitch guide with likely judge questions. Learning briefs can include a build guide and the concepts you will practise.',
      },
      {
        q: 'What do the difficulty levels mean?',
        a: 'The Learning track is split into beginner, intermediate and advanced. The levels describe scope, not skill level. Beginner is one flow in one stack. Intermediate adds persistence, authentication or an API. Advanced is systems work such as event delivery, consistency or offline sync.',
      },
      {
        q: 'Can a brief be in more than one category?',
        a: 'Each brief carries one goal on the board, so the filters stay simple and predictable. A project built from a learning brief can still go on a resume. The track describes the brief, not what you can do with the project.',
      },
    ],
  },
  {
    id: 'submit',
    title: 'Submitting a project',
    items: [
      {
        q: 'What happens when I submit my repository?',
        a: 'MANABI checks that the repo is yours, public and has a README with at least five commits, then compares your description and README with the brief. A clear match is verified and published on the brief page. An unclear match goes to human review.',
      },
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
        a: 'The submission passed those checks and becomes public on the brief page. It is not an endorsement of the project\'s quality, and it does not mean the work is finished.',
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
];

export function FaqPage() {
  return (
    <ProsePage
      kicker="FAQ"
      title="Straight answers"
      intro="How the catalog, the goal tracks, verification and tracking work. These answers match the behaviour the API enforces."
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
