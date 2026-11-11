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
  { href: '#scope', label: 'Scope' },
  { href: '#collect', label: 'What we collect' },
  { href: '#why', label: 'How we use it' },
  { href: '#sharing', label: 'Who can see it' },
  { href: '#never', label: 'What we never do' },
  { href: '#control', label: 'Retention and control' },
  { href: '#security', label: 'Security' },
  { href: '#changes', label: 'Changes and contact' },
];

export function PrivacyPage() {
  return (
    <StaticShell
      kicker="Legal"
      code="REF 04"
      title="Privacy, in plain English"
      intro="What MANABI stores, why it stores it, and how to get it removed. Short enough to finish, specific enough to check against the code."
      aside={
        <>
          <RefAside title="In short">
            <RefList>
              <RefItem>No ads, analytics or data sales.</RefItem>
              <RefItem>Chat messages are not stored.</RefItem>
              <RefItem>
                Your GitHub token stays on the server and is never sent to the
                browser.
              </RefItem>
              <RefItem>
                Remove projects from your dashboard, or ask for account
                deletion through Contact.
              </RefItem>
            </RefList>
          </RefAside>

          <RefAside title="On this page">
            <RefIndex items={CONTENTS} />
          </RefAside>

          <RefNote tone="accent">
            Last updated November 2026. If this policy changes, the date here
            changes with it.
          </RefNote>
        </>
      }
    >
      <RefSection id="scope" index="01" title="Scope">
        <p>
          This policy covers the MANABI web app and its API: the problem
          catalog, GitHub login, project submissions and verification, progress
          tracking, the dashboard, stars, reports, admin review and the catalog
          chat. It does not cover GitHub itself, the model provider, or any
          service you add on top of MANABI.
        </p>
      </RefSection>

      <RefSection id="collect" index="02" title="What we collect">
        <RefList>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Account data.
            </span>{' '}
            Your GitHub numeric ID, username, display name and avatar URL, plus
            the time the account record was created.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              GitHub access token.
            </span>{' '}
            Stored server-side so MANABI can call the GitHub API on your behalf.
            It is never returned to a browser.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Profile signals.
            </span>{' '}
            The languages and topics read from your GitHub profile to score
            recommendations.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Submissions.
            </span>{' '}
            Repository owner, name and URL, your description and demo URL,
            verification status, score and reason, ownership basis, repository
            creation date, completion details, reflection and the contributor
            setting.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Progress data.
            </span>{' '}
            Cached commits, README state and open issues for each submitted
            repository, with the time of the last GitHub check.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Community actions.
            </span>{' '}
            Stars, reports (the reason and the reporting account) and admin
            review notes.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Session cookie.
            </span>{' '}
            A signed cookie that keeps you logged in. It is set Secure and
            HttpOnly on an HTTPS deployment.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Rate-limit records.
            </span>{' '}
            Short-lived counters keyed to your account, or to an IP address for
            login attempts, so the API can name the wait instead of failing
            silently. Expired rows are removed.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Chat.
            </span>{' '}
            Messages are used to produce a reply and are not stored in the
            database.
          </RefItem>
        </RefList>
      </RefSection>

      <RefSection id="why" index="03" title="How we use it">
        <RefList>
          <RefItem>To sign you in through GitHub and keep you signed in.</RefItem>
          <RefItem>
            To confirm repository ownership, compare a submission with the brief
            and decide whether it can be verified or needs review.
          </RefItem>
          <RefItem>
            To show commits, README status and open issues, and to let a project
            owner mark work complete.
          </RefItem>
          <RefItem>
            To recommend briefs from the languages and topics on your profile.
          </RefItem>
          <RefItem>
            To run stars, reports, admin review, rate limits and abuse
            prevention.
          </RefItem>
          <RefItem>
            To answer a message you send through Contact or an issue.
          </RefItem>
        </RefList>
        <p>We do not use this data for advertising or profiling.</p>
      </RefSection>

      <RefSection id="sharing" index="04" title="Who can see it">
        <p>
          Your username, avatar, submitted repository, description, demo URL,
          progress and verification state are visible on public project pages.
          Reports and admin review notes are not public.
        </p>
        <RefList>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Maintainers and admins.
            </span>{' '}
            Can see the submission queue and review notes needed to moderate the
            service.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              The model provider.
            </span>{' '}
            Receives the problem brief, a README excerpt, repository metadata
            and your description to evaluate relevance or answer a chat
            message. It does not receive your access token or session.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              GitHub.
            </span>{' '}
            Handles OAuth and serves the public repository data MANABI reads.
          </RefItem>
          <RefItem>
            <span className="font-mono text-[10px] font-bold uppercase tracking-[0.1em] text-ink">
              Hosting and database providers.
            </span>{' '}
            Store the application database and may keep standard operational
            logs under their own policies.
          </RefItem>
        </RefList>
      </RefSection>

      <RefSection id="never" index="05" title="What we never do">
        <RefList>
          <RefItem>Sell, rent or trade your data.</RefItem>
          <RefItem>Run ads or third-party tracking cookies.</RefItem>
          <RefItem>
            Use your GitHub token to read private repositories. MANABI works
            from public repository data.
          </RefItem>
          <RefItem>Use chat messages to build advertising profiles.</RefItem>
          <RefItem>
            Publish reports, review notes or another user&apos;s private account
            details.
          </RefItem>
        </RefList>
      </RefSection>

      <RefSection id="control" index="06" title="Retention and control">
        <p>
          Account and project records stay while the account or project exists.
          You can remove a project from the dashboard at any time. To request
          deletion of your account data, use the Contact page; a request may
          need verification so nobody else can delete your account.
        </p>
        <p>
          Review notes may be kept where they are needed to explain a
          moderation decision. Rate-limit rows expire with their window. MANABI
          is a prototype, so data may also be reset during development. Do not
          store anything here that you cannot afford to lose.
        </p>
      </RefSection>

      <RefSection id="security" index="07" title="Security">
        <p>
          Sessions are signed, GitHub tokens are held server-side, and
          production uses HTTPS with Secure, HttpOnly cookies. No prototype can
          promise perfect security. If you find a vulnerability, ask for a
          private channel first; do not publish exploit details.
        </p>
      </RefSection>

      <RefSection id="changes" index="08" title="Changes and contact">
        <p>
          If this policy changes, the updated version appears here with a new
          date. Questions about data, deletion or a specific record belong on
          the Contact page.
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