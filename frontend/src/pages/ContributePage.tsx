import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

export function ContributePage() {
  return (
    <ProsePage
      kicker="Contribute"
      title="Build on someone else's repo"
      intro="Some MANABI projects are open for contributors. You can join one, take a good-first issue, and open a pull request without leaving the GitHub workflow you already use."
    >
      <ProseSection id="join" title="How to join">
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
      </ProseSection>

      <ProseSection id="none" title="If no project fits">
        <p>
          Claim the problem yourself and build the first version. When you
          submit, turn on &quot;open for contributors&quot; so the next person
          can join your repository instead of starting from an empty folder.
        </p>
      </ProseSection>

      <ProseSection id="rules" title="What to expect">
        <p>
          MANABI lists the issues; the repository maintainer decides what gets
          merged. Be respectful, keep the discussion in the issue, and do not
          ask for access you do not need.
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
