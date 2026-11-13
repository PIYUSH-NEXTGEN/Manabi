import { Link } from 'react-router-dom';
import { GithubMark } from '@/components/icons/GithubMark';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';

export function ContributePage() {
  return (
    <ProsePage
      kicker="Contribute"
      title="Contribute to MANABI"
      intro="The catalog grows with the people who use it. You can suggest an idea, build a brief and show your repo, join a project that is open for contributors, or work on the platform itself."
    >
      <ProseSection id="ideas" title="Suggest a project idea">
        <p>
          If you know a problem worth building, send it in. Good sources are
          hackathon problem statements, open challenges, public programs and
          problems you have run into yourself.
        </p>
        <p>
          Include the source or a link, who the problem affects and why it
          matters, and roughly how big the build is. Send it through the{' '}
          <Link to="/contact" className="text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink">
            Contact page
          </Link>{' '}
          or open an issue in the{' '}
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink"
          >
            <GithubMark size={13} />
            GitHub repository
          </a>
          . The team reads each one and documents the ideas that fit the catalog.
        </p>
      </ProseSection>

      <ProseSection id="build" title="Build a brief and submit your repo">
        <p>
          This is the main way to contribute. Pick a brief, build it in a public
          repository you own, and submit the repo when there is real work in it.
        </p>
        <ol className="list-decimal space-y-2 pl-5">
          <li>
            <span className="text-ink">Claim a brief.</span> Sign in with GitHub
            and open the problem you want to build.
          </li>
          <li>
            <span className="text-ink">Build in public.</span> Commit as you go.
            A README, at least five commits and a working demo are what get a
            project through.
          </li>
          <li>
            <span className="text-ink">Submit the repo.</span> Add the URL and a
            short description of what you built. MANABI checks ownership,
            relevance and activity before it goes live.
          </li>
        </ol>
        <p>
          Verified projects are published on the brief page for everyone to see.
          Your work stops being a folder nobody opens.
        </p>
      </ProseSection>

      <ProseSection id="join" title="Join a project that is open">
        <p>
          Some submitted projects are marked open for contributors. You can join
          one without asking us for anything.
        </p>
        <ol className="list-decimal space-y-2 pl-5">
          <li>
            <span className="text-ink">Find an open project.</span> Open a
            problem and look for the &quot;Open for contributors&quot; label in
            its submitted projects.
          </li>
          <li>
            <span className="text-ink">Pick an issue.</span> The project page
            lists its GitHub issues, good-first-issue first. Read the
            maintainer&apos;s notes before you start.
          </li>
          <li>
            <span className="text-ink">Open a pull request.</span> Work in your
            fork and open a PR as you would on any repository. MANABI follows
            the commits from GitHub.
          </li>
        </ol>
        <p>
          The maintainer decides what gets merged. Keep the discussion in the
          issue and do not ask for access you do not need.
        </p>
      </ProseSection>

      <ProseSection id="code" title="Help build the platform">
        <p>
          MANABI is open source under the MIT license. Bug fixes, clearer error
          text, docs that match the app and test coverage are all useful. Large
          rewrites and features nobody asked for usually are not, so open an
          issue first if you are unsure.
        </p>
        <p>
          The repository has setup steps for both the FastAPI backend and the
          Vite frontend, plus a contributing guide and a code of conduct. Start
          with an issue or a small pull request.
        </p>
      </ProseSection>

      <ProseSection id="rules" title="A few ground rules">
        <p>
          Be honest about what you built. Do not submit someone else&apos;s
          repository, a fork, or a project that only borrows the brief&apos;s
          name. Reports from other users send a project back to review, and
          repeat cases can lose access.
        </p>
        <p>
          Be respectful in issues, pull requests and project pages. The code of
          conduct in the repository applies to every space around MANABI.
        </p>
      </ProseSection>

      <div className="flex flex-wrap gap-3 border-t border-line pt-8">
        <Link to="/problems" className={buttonClasses('primary')}>
          Find a problem
        </Link>
        <Link to="/faq" className={buttonClasses('secondary')}>
          Read the FAQ
        </Link>
      </div>
    </ProsePage>
  );
}
