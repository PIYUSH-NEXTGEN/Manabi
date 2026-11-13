import { Link } from 'react-router-dom';
import { GithubMark } from '@/components/icons/GithubMark';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';

const linkClass =
  'text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink';

export function AboutPage() {
  return (
    <ProsePage
      kicker="About"
      title="About MANABI"
      intro="MANABI comes from the Japanese word for learning. It is a free catalog of project ideas for students and developers. Every idea is documented, sorted by field and goal, and ready to build for learning, a hackathon or your resume."
    >
      <ProseSection id="why" title="Why MANABI exists">
        <p>
          Finding a good project idea takes longer than it should. You search
          Google, ask an AI, and still end up with the same to-do app or a list
          of buzzwords with no scope, no data and no way to prove you built
          anything. The search is repeated for every hackathon, every semester
          and every resume update.
        </p>
        <p>
          MANABI is built to make that search short. Instead of generating
          another idea on demand, it keeps a curated set of ideas that are
          already worth building and already written up: what the problem is,
          who it affects, how big it is, and what stack gets you there.
        </p>
      </ProseSection>

      <ProseSection id="curation" title="Where the ideas come from">
        <p>
          The MANABI team puts the catalog together by hand. Some briefs come
          from quality problem statements published across the internet:
          hackathons, competitions, public programs and open challenges. Others
          are written by us from scratch. Every brief is documented by a person
          before it goes on the board, and its source stays attached so you can
          check where it came from.
        </p>
        <p>
          There is no scraping and no endless feed. If a brief is on MANABI, a
          person read it, sized it and decided it was worth a student&apos;s or
          developer&apos;s time.
        </p>
      </ProseSection>

      <ProseSection id="catalog" title="What the catalog covers">
        <p>
          The catalog spans seven fields: web development, app development, AI
          and machine learning, data science, cyber security, DevOps and cloud,
          and blockchain.
        </p>
        <p>
          Every brief is sorted into one of three goals: <em>resume</em>,{' '}
          <em>hackathon</em> or <em>learning</em>. Resume briefs are chosen to
          give you something concrete to talk about in an interview. Hackathon
          briefs fit a short build window and can include a team plan and a
          pitch guide.
          Learning briefs are marked beginner, intermediate or advanced, so you
          can pick the next step above what you already know.
        </p>
      </ProseSection>

      <ProseSection id="brief" title="What a brief contains">
        <p>
          A brief gives you enough context to start without another research
          pass. Each one includes:
        </p>
        <ul className="list-disc space-y-1.5 pl-5">
          <li>A summary, who is affected and why the problem matters</li>
          <li>Difficulty and an estimate of the hours involved</li>
          <li>A suggested stack, approaches and useful datasets</li>
          <li>The original problem statement and its source</li>
        </ul>
        <p>
          Track briefs go further. Learning briefs can include a phase-by-phase
          build guide and the concepts you will pick up. Hackathon briefs can
          include a role-based team plan and a pitch guide with likely judge
          questions. Resume briefs can include scope levels, target roles, CV
          bullet templates and interview questions with answers.
        </p>
      </ProseSection>

      <ProseSection id="how" title="How it works">
        <ol className="list-decimal space-y-2 pl-5">
          <li>
            <span className="text-ink">Browse and claim.</span> Filter the
            catalog by field, difficulty, domain, tech stack or goal. Open a
            brief and sign in with GitHub when you are ready to build it.
          </li>
          <li>
            <span className="text-ink">Build in public.</span> Work in a public
            repository you own. MANABI reads the README, commits and open issues,
            so progress comes from the repository itself.
          </li>
          <li>
            <span className="text-ink">Submit your repo.</span> Add the
            repository URL and a short description of what you built. MANABI
            checks ownership, the README, the commit count and whether the work
            matches the brief.
          </li>
          <li>
            <span className="text-ink">Show your work.</span> Verified projects
            are published on the brief&apos;s page for everyone to see. Once the
            submission is verified and the repository has at least five commits,
            you can mark it complete and add a demo link or a short reflection.
          </li>
        </ol>
      </ProseSection>

      <ProseSection id="verification" title="How verification works">
        <p>
          Verification is a best-effort check, not an endorsement. It accepts a
          repository only when one of these is true: you own it, you have push
          or admin access to the organisation that owns it, or you have at least
          three commits in it under your own account.
        </p>
        <p>
          The repository must be public, not a fork, not archived, and have a
          README and at least five commits. An automatic check then compares the
          brief with the README, the repository metadata and your description.
        </p>
        <p>
          If the check is unsure or unavailable, the submission goes to human
          review instead of receiving a verified badge. Three reports from other
          users also send a published project back to review.
        </p>
      </ProseSection>

      <ProseSection id="chat" title="Ask MANABI">
        <p>
          Not sure where to start? Ask MANABI is a chat assistant that answers
          from this catalog only. Tell it what you already know and how much time
          you have, and it suggests briefs that exist, with links. If nothing
          fits, it says so instead of inventing a project.
        </p>
        <p>
          Chat needs a GitHub login and is limited to 20 messages per account per
          rolling 24 hours. Messages are not saved.
        </p>
      </ProseSection>

      <ProseSection id="scope" title="What MANABI does not do">
        <p>
          MANABI does not host your code, run your project or promise a job. It
          links to GitHub and keeps the brief and the proof of work in one
          place. A verified badge means the submission passed the checks above;
          it does not mean the project is good, complete or useful.
        </p>
      </ProseSection>

      <ProseSection id="free" title="Free, and open source">
        <p>
          MANABI is completely free. There are no paid plans, no premium briefs
          and no locked features. It is meant to stay that way for everyone who
          builds here.
        </p>
        <p>
          The code is MIT-licensed and developed in the open. You can read it,
          report a bug, suggest an idea or open an issue in the{' '}
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
            className={`inline-flex items-center gap-1.5 ${linkClass}`}
          >
            <GithubMark size={13} />
            GitHub repository
          </a>
          . The{' '}
          <Link to="/contribute" className={linkClass}>
            Contribute page
          </Link>{' '}
          covers the ways to get involved.
        </p>
      </ProseSection>

      <ProseSection id="account" title="Account and data">
        <p>
          Browsing is open. Claiming a brief, submitting a repository, using the
          dashboard or Ask MANABI, and starring projects need a GitHub account.
          Your GitHub token stays on the server and is never sent to the
          browser. Chat messages are not saved. The{' '}
          <Link to="/privacy" className={linkClass}>
            Privacy page
          </Link>{' '}
          lists everything that is stored.
        </p>
      </ProseSection>

      <div className="flex flex-wrap gap-3 border-t border-line pt-8">
        <Link to="/problems" className={buttonClasses('primary')}>
          Browse problems
        </Link>
        <Link to="/faq" className={buttonClasses('secondary')}>
          Read the FAQ
        </Link>
      </div>
    </ProsePage>
  );
}
