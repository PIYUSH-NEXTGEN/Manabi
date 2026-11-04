import { Link } from 'react-router-dom';

const PROJECTS = [
  {
    to: '/projects/webhooks',
    title: 'Webhook Reliability & Event Delivery',
    tagline: 'Reliable event delivery, retry strategies, idempotency, dead-letter queues',
    field: 'Developer Infrastructure',
  },
  {
    to: '/projects/api-contracts',
    title: 'API Contract Drift & Breaking Change Detection',
    tagline: 'OpenAPI parsing, schema comparison, dependency graphs, automated contract testing',
    field: 'Developer Tools',
  },
  {
    to: '/projects/tenant-security',
    title: 'Multi-Tenant Security & Authorization Audit',
    tagline: 'RBAC/ABAC, tenant isolation, permission graphs, automated security testing',
    field: 'Cybersecurity',
  },
  {
    to: '/projects/incidents',
    title: 'Real-Time Incident Response & Investigation',
    tagline: 'Event correlation, WebSockets, distributed event ingestion, timeline reconstruction',
    field: 'Enterprise Infrastructure',
  },
  {
    to: '/projects/ingestion',
    title: 'Large-Scale File Ingestion & Processing',
    tagline: 'Resumable uploads, streaming, background workers, deduplication, job orchestration',
    field: 'Backend Infrastructure',
  },
  {
    to: '/projects/analytics',
    title: 'Privacy-First Product Analytics',
    tagline: 'High-volume event ingestion, aggregation, data retention, consent management',
    field: 'Data Infrastructure',
  },
  {
    to: '/projects/accessibility',
    title: 'Continuous Website Accessibility Monitoring',
    tagline: 'Browser automation, DOM analysis, accessibility rules, scheduled crawling',
    field: 'Web Infrastructure',
  },
  {
    to: '/projects/inventory',
    title: 'Cross-Platform Inventory Reservation',
    tagline: 'Concurrency control, database transactions, distributed synchronization, idempotency',
    field: 'Enterprise Systems',
  },
  {
    to: '/projects/sync',
    title: 'Offline-First Data Sync & Conflict Resolution',
    tagline: 'Conflict resolution, synchronization protocols, version vectors, CRDTs',
    field: 'Distributed Systems',
  },
  {
    to: '/projects/workflows',
    title: 'Visual Workflow Execution & Automation',
    tagline: 'Workflow orchestration, dependency graphs, durable execution, state management',
    field: 'Developer Infrastructure',
  },
];

export function ProjectsOverviewPage() {
  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <h1 className="font-display text-4xl uppercase leading-none md:text-6xl">
        Advanced{' '}
        <span className="text-accent">Project Ideas</span>
      </h1>
      <p className="mt-4 font-mono text-[12px] font-bold uppercase tracking-widest text-ink/70">
        Ten portfolio-grade project domains — system design, distributed architecture, data
        consistency, performance, security, and complex real-world workflows.
      </p>

      <section aria-label="Project domains" className="mt-12">
        <h2 className="font-display text-2xl uppercase md:text-3xl">
          Choose a domain
        </h2>
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
          {PROJECTS.map((p) => (
            <Link
              key={p.to}
              to={p.to}
              className="group block border border-line bg-sheet p-6 transition-colors duration-150 hover:border-accent"
            >
              <h3 className="font-display text-xl uppercase leading-none">
                {p.title}
              </h3>
              <p className="mt-2 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                {p.field}
              </p>
              <p className="mt-3 text-sm leading-relaxed text-ink/80">{p.tagline}</p>
              <span className="mt-4 inline-block font-mono text-[10px] font-bold uppercase tracking-widest text-accent underline-offset-4 hover:underline">
                Open project &rarr;
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section aria-label="About" className="mt-16 border-t border-ink pt-8">
        <h2 className="font-display text-xl uppercase md:text-2xl">
          What makes these advanced
        </h2>
        <ul className="mt-4 space-y-3 font-mono text-[11px] leading-relaxed text-ink/80">
          <li>· Solve problems developers, businesses, or organizations actually face</li>
          <li>· Engineering depth for internship and placement interviews</li>
          <li>· Real product potential — not just portfolio demos</li>
          <li>· Distinctive technical challenge in each domain</li>
          <li>· Feasible as serious independent projects with well-defined scope</li>
        </ul>
      </section>
    </main>
  );
}
