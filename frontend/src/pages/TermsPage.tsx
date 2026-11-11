import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';
import {
  RefAside,
  RefIndex,
  RefItem,
  RefList,
  RefNote,
  RefSection,
} from './staticParts';

const CONTENTS = [
  { href: '#service', label: 'The service' },
  { href: '#accounts', label: 'Accounts' },
  { href: '#use', label: 'Acceptable use' },
  { href: '#submissions', label: 'Submissions and verification' },
  { href: '#content', label: 'Content and licence' },
  { href: '#third-parties', label: 'Third-party services' },
  { href: '#removal', label: 'Removal and termination' },
  { href: '#liability', label: 'Disclaimers and liability' },
  { href: '#changes', label: 'Changes and contact' },
];

export function TermsPage() {
  return (
    <StaticShell
      kicker="Legal"
      code="REF 05"
      title="Terms, in plain English"
      intro="The rules for using MANABI, the limits of a prototype, and what happens to the work you submit. If a sentence here is unclear, that is a bug worth reporting."
      wide
      aside={
        <>
          <RefAside title="In short">
            <RefList>
              <RefItem>
                Submit only repositories you own or have the required access to.
              </RefItem>
              <RefItem>
                Do not fabricate commits or game verification, stars or reports.
              </RefItem>
              <RefItem>Your code stays yours.</RefItem>
              <RefItem>
                This is a prototype: as-is, no SLA and no guarantee of uptime.
              </RefItem>
            </RefList>
          </RefAside>

          <RefAside title="On this page">
            <RefIndex items={CONTENTS} />
          </RefAside>

          <RefNote tone="accent">
            Last updated November 2026. Using MANABI means accepting these
            terms.
          </RefNote>
        </>
      }
    >
      <RefSection id="service" index="01" title="The service">
        <p>
          MANABI is a catalog of real problems with a path from brief to public
          proof: browse and claim briefs, submit a GitHub repository, have it
          verified, and track progress from the repository itself. It also
          includes a catalog chat and a dashboard of your projects.
        </p>
        <p>
          MANABI is a free prototype provided as-is. Features can change, pause
          or disappear. There is no uptime guarantee, support desk or service
          credit.
        </p>
      </RefSection>

      <RefSection id="accounts" index="02" title="Accounts">
        <p>
          Login runs through GitHub OAuth. Use your own account, keep it secure,
          and be responsible for the activity under it. If you believe someone
          else has access, tell us through the Contact page. Account data is
          handled as described in the Privacy page.
        </p>
      </RefSection>

      <RefSection id="use" index="03" title="Acceptable use">
        <RefList>
          <RefItem>
            Submit only repositories you own, or where you meet the contributor
            access rule the verification system checks.
          </RefItem>
          <RefItem>
            Do not invent commits, buy stars or reports, or otherwise try to
            game verification or ranking.
          </RefItem>
          <RefItem>
            Do not scrape, automate or bypass rate limits in a way that burdens
            the service or other users.
          </RefItem>
          <RefItem>
            Do not probe, access or change another person&apos;s account,
            projects or data. Do not test against repositories you do not own.
          </RefItem>
          <RefItem>
            Do not submit unlawful, harmful, deceptive or infringing content.
          </RefItem>
          <RefItem>
            Do not attempt to enter the admin review queue or any other
            restricted area without authorization.
          </RefItem>
        </RefList>
        <p>
          MANABI may remove content, pause a project or limit access when one of
          these rules is broken.
        </p>
      </RefSection>

      <RefSection id="submissions" index="04" title="Submissions and verification">
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
      </RefSection>

      <RefSection id="content" index="05" title="Content and licence">
        <p>
          You keep ownership of the code and content in your repositories. By
          submitting a project, you allow MANABI to display the repository
          link, description, demo URL, progress and verification state publicly,
          and to use that information to operate the service.
        </p>
        <p>
          Problem statements belong to the organisations that published them;
          MANABI credits and links each source. The MANABI code is released
          under the MIT licence.
        </p>
      </RefSection>

      <RefSection id="third-parties" index="06" title="Third-party services">
        <p>
          MANABI depends on GitHub for login and public repository data, on a
          model provider for relevance and chat, and on hosting and database
          providers. Those services have their own terms and availability. When
          one is unavailable, a verification may go to review or a feature may
          pause; that is expected behaviour, not a guarantee of service.
        </p>
      </RefSection>

      <RefSection id="removal" index="07" title="Removal and termination">
        <p>
          You can remove your projects from the dashboard. MANABI may remove or
          pause content, or suspend access, for abuse, legal reasons, or to
          protect the service and its users. Prototype data may be reset during
          development. Requests to delete account data belong on the Contact
          page.
        </p>
      </RefSection>

      <RefSection id="liability" index="08" title="Disclaimers and liability">
        <p>
          MANABI is provided as-is and without warranties of any kind, express
          or implied. To the extent permitted by law, the maintainers are not
          liable for lost data, lost projects, lost opportunities, or any
          damages arising from use of the service. Nothing on this page is legal
          advice.
        </p>
      </RefSection>

      <RefSection id="changes" index="09" title="Changes and contact">
        <p>
          These terms may change. The updated version appears here with a new
          date, and continued use after a change means you accept it. Questions
          belong on the Contact page.
        </p>
        <div>
          <Link to="/contact" className={buttonClasses('secondary')}>
            Contact us
          </Link>
        </div>
      </RefSection>
    </StaticShell>
  );
}