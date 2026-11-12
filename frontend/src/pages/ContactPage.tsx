import { ArrowUpRight } from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { buttonClasses } from '@/design/primitives';
import { ProsePage, ProseSection } from './staticParts';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';
const GITHUB_ISSUES_URL =
  import.meta.env.VITE_GITHUB_ISSUES_URL || `${REPO_URL}/issues`;
const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL;
const SECURITY_URL = `${REPO_URL}/blob/main/SECURITY.md`;

const INCLUDED = [
  'The page, problem or project link you are writing about.',
  'What you expected and what actually happened.',
  'Steps to reproduce it, plus your browser and operating system if it is a UI bug.',
  'For verification errors, the error code and message from the response. Remove tokens, cookies and personal data first.',
];

const linkClass =
  'text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink';

export function ContactPage() {
  return (
    <ProsePage
      kicker="Contact"
      title="Talk to us"
      intro="Open an issue for bugs and concrete requests. Use email for account, data or security matters. Both reach the people maintaining MANABI, not a ticket queue."
    >
      <ProseSection id="issues" title="GitHub issues">
        <p>
          Best for anything with a URL we can inspect: bugs, broken briefs, copy
          errors, feature requests, and verification questions that can be
          discussed in public.
        </p>
        <div>
          <a
            href={GITHUB_ISSUES_URL}
            target="_blank"
            rel="noreferrer"
            className={buttonClasses('primary')}
          >
            <GithubMark size={14} />
            Open an issue
            <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
          </a>
        </div>
      </ProseSection>

      <ProseSection id="email" title="Email">
        {CONTACT_EMAIL ? (
          <>
            <p>
              Use email for account data, deletion requests, security reports,
              or anything you would rather not post publicly.
            </p>
            <p className="break-all font-medium text-ink">{CONTACT_EMAIL}</p>
            <div>
              <a
                href={`mailto:${CONTACT_EMAIL}`}
                className={buttonClasses('secondary')}
              >
                Write to us
                <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
              </a>
            </div>
          </>
        ) : (
          <>
            <p>
              This deployment has no private address configured. Open a minimal
              issue and ask for a private channel. Do not put sensitive details
              in the issue itself.
            </p>
            <div>
              <a
                href={GITHUB_ISSUES_URL}
                target="_blank"
                rel="noreferrer"
                className={buttonClasses('secondary')}
              >
                Request a private channel
                <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
              </a>
            </div>
          </>
        )}
      </ProseSection>

      <ProseSection id="include" title="What to include">
        <p>A useful report is short and specific. Include:</p>
        <ul className="list-disc space-y-1.5 pl-5">
          {INCLUDED.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <p>
          Public issues are public. Never paste a token, session cookie or
          another person&apos;s data into one.
        </p>
      </ProseSection>

      <ProseSection id="security" title="Security reports">
        <p>
          If something looks like a real vulnerability, do not publish the
          details. Ask for a private channel first and include only enough to
          establish contact. The security policy covers scope, what we fix
          first, and the issues already accepted.
        </p>
        <p>
          <a href={SECURITY_URL} className={linkClass}>
            Read the security policy
          </a>
        </p>
      </ProseSection>

      <ProseSection id="expect" title="What to expect">
        <p>
          MANABI is maintained by a small team. Public issues get public
          answers, which is also how the changelog stays honest. There is no
          support SLA and no bounty program.
        </p>
      </ProseSection>
    </ProsePage>
  );
}
