import { StaticShell } from './StaticShell';

const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL;
const GITHUB_ISSUES_URL = import.meta.env.VITE_GITHUB_ISSUES_URL;

export function ContactPage() {
  return (
    <StaticShell kicker="Contact" title="Talk to us">
      <p>
        Bugs, breaks, and bad copy: open a GitHub issue — issues are the
        changelog. Anything else that needs a reply: email.
      </p>

      {GITHUB_ISSUES_URL || CONTACT_EMAIL ? (
        <ul className="flex flex-col gap-3">
          {GITHUB_ISSUES_URL ? (
            <li className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
              <p className="font-mono text-[11px] font-bold uppercase tracking-widest">
                GitHub issues
              </p>
              <a
                href={GITHUB_ISSUES_URL}
                target="_blank"
                rel="noreferrer"
                className="mt-1 inline-block text-blue underline underline-offset-4"
              >
                {GITHUB_ISSUES_URL} ↗
              </a>
            </li>
          ) : null}
          {CONTACT_EMAIL ? (
            <li className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
              <p className="font-mono text-[11px] font-bold uppercase tracking-widest">
                Email
              </p>
              <a
                href={`mailto:${CONTACT_EMAIL}`}
                className="mt-1 inline-block text-blue underline underline-offset-4"
              >
                {CONTACT_EMAIL}
              </a>
            </li>
          ) : null}
        </ul>
      ) : (
        <p
          role="status"
          className="border-[3px] border-ink bg-white p-4 shadow-hard-sm font-mono text-[11px] font-bold uppercase tracking-widest"
        >
          Contact details are not configured yet — no fake form here.
        </p>
      )}

      <p className="font-mono text-[11px] uppercase tracking-widest text-ink">
        There is no contact form. Forms eat messages; links do not.
      </p>
    </StaticShell>
  );
}
