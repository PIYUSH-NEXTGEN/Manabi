import {
  ArrowUpRight,
  LockKeyhole,
  Mail,
} from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';
import {
  RefAside,
  RefFacts,
  RefItem,
  RefLink,
  RefList,
  RefNote,
  RefSection,
} from './staticParts';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';
const GITHUB_ISSUES_URL =
  import.meta.env.VITE_GITHUB_ISSUES_URL || `${REPO_URL}/issues`;
const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL;
const SECURITY_URL = `${REPO_URL}/blob/main/SECURITY.md`;

const INCLUDED = [
  'The page, problem, or project link you are writing about.',
  'What you expected and what actually happened.',
  'Steps to reproduce it, plus your browser and operating system if it is a UI bug.',
  'For verification errors, the error code and message from the response. Remove tokens, cookies and personal data first.',
];

export function ContactPage() {
  return (
    <StaticShell
      kicker="Contact"
      code="REF 03"
      title="Talk to us"
      intro="Open issues for bugs and concrete requests. A private channel for account, data and security matters. Both reach the people maintaining MANABI, not a ticket queue."
      aside={
        <>
          <RefAside title="Channels">
            <RefFacts
              items={[
                { label: 'Issues', value: 'Open · public' },
                {
                  label: 'Email',
                  value: CONTACT_EMAIL ? 'Configured' : 'Not configured',
                },
                { label: 'Response', value: 'Best effort' },
                { label: 'SLA', value: 'None' },
                { label: 'Security', value: 'Private first' },
              ]}
            />
          </RefAside>

          <RefAside title="Repository">
            <RefList>
              <RefItem>
                <RefLink href={GITHUB_ISSUES_URL}>Issue tracker</RefLink>
              </RefItem>
              <RefItem>
                <RefLink href={SECURITY_URL}>Security policy</RefLink>
              </RefItem>
              <RefItem>
                <RefLink href={REPO_URL}>Source code</RefLink>
              </RefItem>
            </RefList>
          </RefAside>

          <RefNote>
            Public issues are public. Never paste a token, session cookie, or
            another person&apos;s data into one.
          </RefNote>
        </>
      }
    >
      <div className="grid gap-4 md:grid-cols-2">
        <article className="flex flex-col border border-ink bg-sheet">
          <header className="flex items-center justify-between gap-3 border-b border-line px-4 py-2.5">
            <span className="font-mono text-label font-bold uppercase tracking-[0.16em] text-accent">
              Open · public
            </span>
            <GithubMark size={14} className="text-ink" />
          </header>
          <div className="flex flex-1 flex-col p-5">
            <h2 className="font-display text-body uppercase leading-none tracking-tight">
              GitHub issues
            </h2>
            <p className="mt-3 text-body leading-relaxed text-ink-soft">
              Bugs, broken briefs, copy errors, feature requests and
              verification questions that can be discussed in public.
            </p>
            <p className="mt-2 text-body leading-relaxed text-ink-soft">
              Best for anything with a URL we can inspect.
            </p>
            <a
              href={GITHUB_ISSUES_URL}
              target="_blank"
              rel="noreferrer"
              className={buttonClasses('primary', 'mt-5 w-full justify-center')}
            >
              Open an issue
              <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
            </a>
          </div>
        </article>

        <article className="flex flex-col border border-ink bg-sheet">
          <header className="flex items-center justify-between gap-3 border-b border-line px-4 py-2.5">
            <span className="font-mono text-label font-bold uppercase tracking-[0.16em] text-ink-soft">
              Private
            </span>
            {CONTACT_EMAIL ? (
              <Mail aria-hidden size={14} strokeWidth={2.2} className="text-ink" />
            ) : (
              <LockKeyhole
                aria-hidden
                size={14}
                strokeWidth={2.2}
                className="text-ink"
              />
            )}
          </header>
          <div className="flex flex-1 flex-col p-5">
            <h2 className="font-display text-body uppercase leading-none tracking-tight">
              {CONTACT_EMAIL ? 'Email' : 'Private follow-up'}
            </h2>
            {CONTACT_EMAIL ? (
              <>
                <p className="mt-3 text-body leading-relaxed text-ink-soft">
                  Account data, security reports, or anything you would rather
                  not post publicly.
                </p>
                <p className="mt-2 break-all font-mono text-label tracking-[0.02em] text-ink">
                  {CONTACT_EMAIL}
                </p>
                <a
                  href={`mailto:${CONTACT_EMAIL}`}
                  className={buttonClasses(
                    'secondary',
                    'mt-5 w-full justify-center',
                  )}
                >
                  Write to us
                  <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
                </a>
              </>
            ) : (
              <>
                <p className="mt-3 text-body leading-relaxed text-ink-soft">
                  This deployment has no private address configured. Open a
                  minimal issue and ask for a private channel. Do not put
                  sensitive details in the issue itself.
                </p>
                <a
                  href={GITHUB_ISSUES_URL}
                  target="_blank"
                  rel="noreferrer"
                  className={buttonClasses(
                    'secondary',
                    'mt-5 w-full justify-center',
                  )}
                >
                  Request a private channel
                  <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
                </a>
              </>
            )}
          </div>
        </article>
      </div>

      <RefSection id="include" index="01" title="What to include">
        <RefList>
          {INCLUDED.map((item) => (
            <RefItem key={item}>{item}</RefItem>
          ))}
        </RefList>
      </RefSection>

      <RefSection id="security" index="02" title="Security reports">
        <p>
          If something looks like a real vulnerability, do not publish the
          details. Ask for a private channel first and include only enough to
          establish contact. The security policy covers scope, what we fix
          first, and the issues already accepted.
        </p>
        <RefLink href={SECURITY_URL}>Read the security policy</RefLink>
      </RefSection>

      <RefSection id="expect" index="03" title="What to expect">
        <p>
          MANABI is maintained by a small team. Public issues get public
          answers, which is also how the changelog stays honest. There is no
          support SLA and no bounty program.
        </p>
      </RefSection>
    </StaticShell>
  );
}