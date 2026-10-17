import { StaticShell } from './StaticShell';

const WE_STORE = [
  'Your GitHub username, display name, and avatar — shown on projects you submit.',
  'Links to the public repos you submit, plus automatically tracked progress (commits, README, open issues).',
  'Your ML practice answers and the feedback they got.',
  'A GitHub token on the server side. It is never returned to any browser.',
];

export function PrivacyPage() {
  return (
    <StaticShell kicker="Legal" title="Privacy, in plain English">
      <dl className="flex flex-col gap-4">
        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            What we store
          </dt>
          <dd>
            <ul className="mt-2 list-none flex flex-col gap-2">
              {WE_STORE.map((item) => (
                <li key={item} className="flex gap-2">
                  <span aria-hidden>■</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </dd>
        </div>

        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            What we do not do
          </dt>
          <dd className="mt-1">
            No analytics, no ads, no tracking cookies, no selling anything to
            anyone. Login runs through GitHub OAuth; a signed session cookie
            keeps you logged in and nothing else rides on it.
          </dd>
        </div>

        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            The honest part
          </dt>
          <dd className="mt-1">
            This is a hackathon prototype. Data lives in one database that can
            be cleared at any time. Do not submit anything you would be upset
            to lose.
          </dd>
        </div>
      </dl>
    </StaticShell>
  );
}
