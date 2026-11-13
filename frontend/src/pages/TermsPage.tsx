import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

export function TermsPage() {
  return (
    <ProsePage
      kicker="Legal"
      title="Terms, in plain English"
      intro="The rules for using MANABI, what you can submit, and what happens to the work you post. If a sentence here is unclear, that is a bug worth reporting."
    >
      <ProseSection id="service" title="The service">
        <p>
          MANABI is a free catalog of project ideas for students and developers.
          Each idea is written up as a brief and labelled for learning, a
          hackathon or a resume. You can browse and claim briefs, submit a
          public GitHub repository, have it checked, and track progress from the
          repository itself. The platform also includes a catalog chat and a
          dashboard of your projects.
        </p>
        <p>
          MANABI is free to use and has no paid plans. It is provided as-is.
          Features can change, pause or disappear, and there is no uptime
          guarantee, support desk or service credit.
        </p>
      </ProseSection>

      <ProseSection id="accounts" title="Accounts">
        <p>
          Login runs through GitHub OAuth. Use your own account, keep it secure,
          and be responsible for the activity under it. If you believe someone
          else has access, tell us through the Contact page. Account data is
          handled as described in the Privacy page.
        </p>
      </ProseSection>

      <ProseSection id="use" title="Acceptable use">
        <ul className="list-disc space-y-1.5 pl-5">
          <li>
            Submit only repositories you own, or where you meet the contributor
            access rule the verification system checks.
          </li>
          <li>
            Do not invent commits, buy stars or reports, or otherwise try to
            game verification or ranking.
          </li>
          <li>
            Do not scrape, automate or bypass rate limits in a way that burdens
            the service or other users.
          </li>
          <li>
            Do not probe, access or change another person&apos;s account,
            projects or data. Do not test against repositories you do not own.
          </li>
          <li>
            Do not submit unlawful, harmful, deceptive or infringing content.
          </li>
          <li>
            Do not suggest a project idea or source you have no right to share.
          </li>
          <li>
            Do not attempt to enter the admin review queue or any other
            restricted area without authorization.
          </li>
        </ul>
        <p>
          MANABI may remove content, pause a project or limit access when one of
          these rules is broken.
        </p>
      </ProseSection>

      <ProseSection id="submissions" title="Submissions and verification">
        <p>
          Verification is a best-effort check, not an endorsement. It reads
          ownership signals, the README, the commit count and the relevance of
          the repository to the brief. An AI relevance check can be wrong, a
          pre-existing repository may need a higher score, and an admin may
          change a decision.
        </p>
        <p>
          Three reports can send a published project back to review. Keep your
          repository and local work as the source of truth. A verified badge is
          not legal proof of authorship, ownership or fitness for any purpose.
          You remain responsible for the repository you submit.
        </p>
      </ProseSection>

      <ProseSection id="content" title="Content and licence">
        <p>
          You keep ownership of the code and content in your repositories. By
          submitting a project, you allow MANABI to display the repository link,
          description, demo URL, progress and verification state publicly, and
          to use that information to operate the service.
        </p>
        <p>
          If you suggest a project idea, you allow MANABI to write it up and
          publish it as part of the catalog. The team may edit the wording, add
          a source or leave the idea out.
        </p>
        <p>
          Briefs are researched and written by the MANABI team. Where a brief
          comes from a published problem statement, the source belongs to the
          organisation that published it and stays credited and linked. The
          MANABI code is released under the MIT licence.
        </p>
      </ProseSection>

      <ProseSection id="third-parties" title="Third-party services">
        <p>
          MANABI depends on GitHub for login and public repository data, on a
          model provider for relevance and chat, and on hosting and database
          providers. Those services have their own terms and availability. When
          one is unavailable, a verification may go to review or a feature may
          pause. That is expected behaviour, not a guarantee of service.
        </p>
      </ProseSection>

      <ProseSection id="removal" title="Removal and termination">
        <p>
          You can remove your projects from the dashboard. MANABI may remove or
          pause content, or suspend access, for abuse, legal reasons, or to
          protect the service and its users. Requests to delete account data
          belong on the Contact page.
        </p>
      </ProseSection>

      <ProseSection id="liability" title="Disclaimers and liability">
        <p>
          MANABI is provided as-is and without warranties of any kind, express
          or implied. To the extent permitted by law, the maintainers are not
          liable for lost data, lost projects, lost opportunities, or any
          damages arising from use of the service. Nothing on this page is legal
          advice.
        </p>
      </ProseSection>

      <ProseSection id="changes" title="Changes and contact">
        <p>
          These terms may change. The updated version appears here with a new
          date, and continued use after a change means you accept it. Questions
          belong on the Contact page.
        </p>
        <p className="text-sm text-muted">Last updated November 2026.</p>
        <div>
          <Link to="/contact" className={buttonClasses('secondary')}>
            Contact us
          </Link>
        </div>
      </ProseSection>
    </ProsePage>
  );
}
