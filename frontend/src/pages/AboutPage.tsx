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
      intro="MANABI is a catalog of real problems for students and early-career developers. Pick a brief, build the solution in a public GitHub repository, and the site tracks the work from that repository."
    >
      <ProseSection id="what" title="What MANABI is">
        <p>
          Most project ideas are invented for a portfolio and forgotten by the
          next application. MANABI starts from problems that organisations,
          competitions and public programs have already published. Each one is
          reviewed by hand and written up as a brief you can start from.
        </p>
        <p>
          The catalog covers seven fields: web development, app development, AI
          and machine learning, data science, cyber security, DevOps and cloud,
          and blockchain. Every brief is marked beginner, intermediate or
          advanced, and labelled for a resume, a hackathon or learning.
        </p>
        <p>
          There is no scraping and no endless feed. Every brief keeps its source
          attached, so you can check where the problem came from.
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
          Some briefs also include a build guide, a team plan for a hackathon,
          or notes you can use on a resume.
        </p>
      </ProseSection>

      <ProseSection id="how" title="How it works">
        <ol className="list-decimal space-y-2 pl-5">
          <li>
            <span className="text-ink">Browse and claim.</span> Filter the
            catalog by field, difficulty, tech stack or goal. Open a brief and
            sign in with GitHub when you are ready to claim it.
          </li>
          <li>
            <span className="text-ink">Build in public.</span> Work in a public
            repository you own. MANABI reads the README, commits and open issues,
            so progress comes from the repository itself.
          </li>
          <li>
            <span className="text-ink">Submit for verification.</span> Add the
            repository URL and a short description. MANABI checks ownership, the
            README, the commit count and whether the work matches the brief.
          </li>
          <li>
            <span className="text-ink">Mark it complete.</span> Once the
            submission is verified and the repository has at least five commits,
            you can mark the project complete and add a demo link or a short
            reflection.
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

      <ProseSection id="scope" title="What MANABI does not do">
        <p>
          MANABI does not host your code, run your project or promise a job. It
          links to GitHub and keeps the brief and the proof of work in one
          place. A verified badge means the submission passed the checks above;
          it does not mean the project is good, complete or useful.
        </p>
      </ProseSection>

      <ProseSection id="account" title="Account, data and status">
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
        <p>
          MANABI is a working prototype, not a company. The catalog,
          verification, progress tracking, dashboard and catalog chat are live,
          and the code is MIT-licensed. Data may be reset while the project is
          under active development, so do not store anything here that you
          cannot afford to lose.
        </p>
        <p>
          You can read the code, report a bug or open an issue in the{' '}
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
            className={`inline-flex items-center gap-1.5 ${linkClass}`}
          >
            <GithubMark size={13} />
            GitHub repository
          </a>
          .
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
