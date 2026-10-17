import { StaticShell } from './StaticShell';

export function TermsPage() {
  return (
    <StaticShell kicker="Legal" title="Terms, in plain English" wide>
      <dl className="flex flex-col gap-4">
        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            01 — What this is
          </dt>
          <dd className="mt-1">
            A hackathon prototype, provided as-is. No warranties, no uptime
            promises, no support desk. There is no company behind this — a
            small team built it in a weekend.
          </dd>
        </div>

        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            02 — Who owns what
          </dt>
          <dd className="mt-1">
            Problem statements belong to the organisations that published
            them; MANABI credits and links each source. Your code stays
            exactly yours — MANABI only reads public repo data to display
            progress.
          </dd>
        </div>

        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            03 — Your account
          </dt>
          <dd className="mt-1">
            Login is GitHub OAuth. You are responsible for the projects you
            submit and the answers you give. Be honest with both.
          </dd>
        </div>

        <div className="border-t-[3px] border-ink pt-3">
          <dt className="font-mono text-xs font-bold uppercase tracking-widest">
            04 — Data
          </dt>
          <dd className="mt-1">
            Prototype data may be reset or deleted at any time without
            notice. See the Privacy page for exactly what is stored.
          </dd>
        </div>
      </dl>

      <p className="font-mono text-[11px] uppercase tracking-widest">
        Questions → the Contact page, not a lawyer.
      </p>
    </StaticShell>
  );
}
