import { useSyncExternalStore } from 'react';
import { Link } from 'react-router-dom';
import { Button, buttonClasses } from '@/design/primitives';
import {
  getConsent,
  setConsent,
  subscribeConsent,
} from '@/lib/analytics';
import { ProsePage, ProseSection } from './staticParts';

function AnalyticsChoice() {
  const consent = useSyncExternalStore(
    subscribeConsent,
    getConsent,
    () => null,
  );
  const granted = consent === 'granted';

  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-3">
      <Button
        size="small"
        variant="secondary"
        onClick={() => setConsent(granted ? 'denied' : 'granted')}
      >
        {granted ? 'Turn analytics off' : 'Turn analytics on'}
      </Button>
      <span className="text-sm text-muted">
        Currently {consent === null ? 'not decided' : granted ? 'on' : 'off'}.
      </span>
    </div>
  );
}

export function PrivacyPage() {
  return (
    <ProsePage
      kicker="Legal"
      title="Privacy, in plain English"
      intro="What MANABI stores, why it stores it, and how to get it removed. This policy covers the web app and its API, not GitHub, the model provider, or any service you add on top of MANABI."
    >
      <ProseSection id="collect" title="What we collect">
        <ul className="list-disc space-y-2 pl-5">
          <li>
            <strong className="font-medium text-ink">Account data.</strong> Your
            GitHub numeric ID, username, display name and avatar URL, plus the
            time the account record was created.
          </li>
          <li>
            <strong className="font-medium text-ink">GitHub access token.</strong>{' '}
            Stored on the server so MANABI can call the GitHub API on your
            behalf. It is never returned to a browser.
          </li>
          <li>
            <strong className="font-medium text-ink">Profile signals.</strong>{' '}
            The languages and topics read from your GitHub profile to score
            recommendations.
          </li>
          <li>
            <strong className="font-medium text-ink">Submissions.</strong>{' '}
            Repository owner, name and URL, your description and demo URL,
            verification status, score and reason, ownership basis, repository
            creation date, completion details, reflection and the contributor
            setting.
          </li>
          <li>
            <strong className="font-medium text-ink">Progress data.</strong>{' '}
            Cached commits, README state and open issues for each submitted
            repository, with the time of the last GitHub check.
          </li>
          <li>
            <strong className="font-medium text-ink">Community actions.</strong>{' '}
            Stars, reports (the reason and the reporting account) and admin
            review notes.
          </li>
          <li>
            <strong className="font-medium text-ink">Session cookie.</strong> A
            signed cookie that keeps you logged in. It is set Secure and
            HttpOnly on an HTTPS deployment.
          </li>
          <li>
            <strong className="font-medium text-ink">Rate-limit records.</strong>{' '}
            Short-lived counters keyed to your account, or to an IP address for
            login attempts, so the API can name the wait instead of failing
            silently. Expired rows are removed.
          </li>
          <li>
            <strong className="font-medium text-ink">
              Anonymous presence id.
            </strong>{' '}
            A random id kept in your browser&apos;s local storage and used only
            to count how many people are online and how many unique browsers
            have visited. It is not linked to your account unless you log in,
            and we do not store your IP address for this.
          </li>
          <li>
            <strong className="font-medium text-ink">Chat.</strong> Messages are
            used to produce a reply and are not stored in the database.
          </li>
          <li>
            <strong className="font-medium text-ink">
              Optional analytics.
            </strong>{' '}
            Only if you allow it: pages visited, features used, your numeric
            account id, errors, and a text-masked session recording. See{' '}
            <a href="#analytics" className="underline underline-offset-4">
              analytics and recording
            </a>
            .
          </li>
        </ul>
      </ProseSection>

      <ProseSection id="why" title="How we use it">
        <ul className="list-disc space-y-1.5 pl-5">
          <li>To sign you in through GitHub and keep you signed in.</li>
          <li>
            To confirm repository ownership, compare a submission with the brief
            and decide whether it can be verified or needs review.
          </li>
          <li>
            To show commits, README status and open issues.
          </li>
          <li>
            To recommend briefs from the languages and topics on your profile.
          </li>
          <li>
            To run stars, reports, admin review, rate limits and abuse
            prevention.
          </li>
          <li>To answer a message you send through Contact or an issue.</li>
        </ul>
        <p>We do not use this data for advertising or profiling.</p>
      </ProseSection>

      <ProseSection id="sharing" title="Who can see it">
        <p>
          Your username, avatar, submitted repository, description, demo URL,
          progress and verification state are visible on public project pages.
          Reports and admin review notes are not public.
        </p>
        <ul className="list-disc space-y-2 pl-5">
          <li>
            <strong className="font-medium text-ink">
              Maintainers and admins.
            </strong>{' '}
            Can see the submission queue and review notes needed to moderate the
            service.
          </li>
          <li>
            <strong className="font-medium text-ink">The model provider.</strong>{' '}
            Receives the problem brief, a README excerpt, repository metadata
            and your description to evaluate relevance or answer a chat
            message. It does not receive your access token or session.
          </li>
          <li>
            <strong className="font-medium text-ink">GitHub.</strong> Handles
            OAuth and serves the public repository data MANABI reads.
          </li>
          <li>
            <strong className="font-medium text-ink">
              Hosting and database providers.
            </strong>{' '}
            Store the application database and may keep standard operational
            logs under their own policies.
          </li>
          <li>
            <strong className="font-medium text-ink">PostHog.</strong> Receives
            the optional analytics and session recordings described below, and
            nothing at all if you decline. Its servers are in the United
            States.
          </li>
        </ul>
      </ProseSection>

      <ProseSection id="analytics" title="Analytics and recording">
        <p>
          We use PostHog to understand which pages and features help people
          find a project to build, and to reproduce bugs from short session
          recordings. It is off until you choose. If you decline, the tool is
          never downloaded and nothing is sent.
        </p>
        <ul className="list-disc space-y-2 pl-5">
          <li>
            <strong className="font-medium text-ink">Events.</strong> Pages
            visited, filters and features used, stars, report and submission
            outcomes, and your numeric account id once you log in.
          </li>
          <li>
            <strong className="font-medium text-ink">Diagnostics.</strong>{' '}
            Errors, plus a few operational lines such as app start and render
            failure. Ordinary console output stays in your browser.
          </li>
          <li>
            <strong className="font-medium text-ink">Session replay.</strong>{' '}
            Clicks and page layout, kept for 30 days. Form inputs are masked and
            the chat panel is masked before anything leaves your browser; the
            text of a reply is never part of a recording.
          </li>
          <li>
            <strong className="font-medium text-ink">AI metadata.</strong>{' '}
            Latency, outcome and the number of turns in a chat. Your messages
            and the reply are not sent to PostHog.
          </li>
          <li>
            <strong className="font-medium text-ink">Storage.</strong> The
            choice and the analytics identifier live in your browser&apos;s
            local storage. Analytics sets no cookie.
          </li>
        </ul>
        <p>
          Your choice is remembered until you change it here. Turning analytics
          off deletes the stored identifier and stops all capture immediately.
        </p>
        <AnalyticsChoice />
      </ProseSection>

      <ProseSection id="never" title="What we never do">
        <ul className="list-disc space-y-1.5 pl-5">
          <li>Sell, rent or trade your data.</li>
          <li>Run ads or load analytics without asking you first.</li>
          <li>
            Use your GitHub token to read private repositories. MANABI works
            from public repository data.
          </li>
          <li>Use chat messages to build advertising profiles.</li>
          <li>
            Publish reports, review notes or another user&apos;s private account
            details.
          </li>
        </ul>
      </ProseSection>

      <ProseSection id="control" title="Retention and control">
        <p>
          Account and project records stay while the account or project exists.
          You can remove a project from the dashboard at any time. To request
          deletion of your account data, use the Contact page; a request may
          need verification so nobody else can delete your account.
        </p>
        <p>
          Review notes may be kept where they are needed to explain a moderation
          decision. Rate-limit rows expire with their window. Presence rows keep
          the random browser id and the last time it was seen so the all-time
          count stays accurate; they contain no IP address or account link
          unless you logged in. MANABI is a prototype, so data may also be reset
          during development. Do not store anything here that you cannot afford
          to lose.
        </p>
      </ProseSection>

      <ProseSection id="security" title="Security">
        <p>
          Sessions are signed, GitHub tokens are held on the server, and
          production uses HTTPS with Secure, HttpOnly cookies. No prototype can
          promise perfect security. If you find a vulnerability, ask for a
          private channel first; do not publish exploit details.
        </p>
      </ProseSection>

      <ProseSection id="changes" title="Changes and contact">
        <p>
          If this policy changes, the updated version appears here with a new
          date. Questions about data, deletion or a specific record belong on
          the Contact page.
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
