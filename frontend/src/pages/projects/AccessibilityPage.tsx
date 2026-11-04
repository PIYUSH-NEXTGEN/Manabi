import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listMonitoredWebsites,
  createMonitoredWebsite,
  MonitoredWebsite,
  MonitoredWebsiteCreate,
  listAccessibilityScans,
  AccessibilityScan,
  AccessibilityScanCreate,
  createAccessibilityScan,
  createAccessibilityIssue,
  AccessibilityIssueCreate,
  getAccessibilityStats,
  AccessibilityStats,
} from '@/api/projects';

export function AccessibilityPage() {
  const [websites, setWebsites] = useState<MonitoredWebsite[]>([]);
  const [scans, setScans] = useState<AccessibilityScan[]>([]);
  const [stats, setStats] = useState<AccessibilityStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [ws, sc, st] = await Promise.all([
      listMonitoredWebsites(),
      listAccessibilityScans(1),
      getAccessibilityStats(),
    ]);
    setWebsites(ws);
    setScans(sc);
    setStats(st);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleCreateWebsite(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: MonitoredWebsiteCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      url: (form.elements.namedItem('url') as HTMLInputElement).value,
      wcag_level: 'AA',
    };
    const created = await createMonitoredWebsite(body);
    setWebsites([created, ...websites]);
  }

  async function handleCreateScan(e: React.FormEvent) {
    e.preventDefault();
    const body: AccessibilityScanCreate = {
      website_id: 1,
      wcag_level: 'AA',
    };
    await createAccessibilityScan(body);
    load();
  }

  async function handleCreateIssue(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: AccessibilityIssueCreate = {
      scan_id: 1,
      page_url: (form.elements.namedItem('page_url') as HTMLInputElement).value,
      rule_id: (form.elements.namedItem('rule_id') as HTMLInputElement).value,
      rule_name: (form.elements.namedItem('rule_name') as HTMLInputElement).value,
      wcag_level: 'AA',
      severity: (form.elements.namedItem('severity') as HTMLInputElement).value,
      description: (form.elements.namedItem('description') as HTMLInputElement).value,
    };
    await createAccessibilityIssue(body);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Accessibility Monitoring</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Websites</p>
          <p className="font-display text-2xl">{stats?.total_websites ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Scans</p>
          <p className="font-display text-2xl">{stats?.total_scans ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Issues</p>
          <p className="font-display text-2xl">{stats?.total_issues ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Unresolved</p>
          <p className="font-display text-2xl">{stats?.unresolved_issues ?? 0}</p>
        </div>
      </div>

      <section aria-label="Add website" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Add Website to Monitor
        </h2>
        <form onSubmit={handleCreateWebsite} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Site name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="url"
            placeholder="https://example.com"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Add</Button>
        </form>
      </section>

      <section aria-label="Websites" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">Monitored Websites</h2>
        <ul className="divide-y border border-ink bg-sheet">
          {websites.map((w) => (
            <li key={w.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{w.name}</span> — {w.url} ({w.wcag_level})
            </li>
          ))}
          {websites.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No websites yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Scans" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Accessibility Scans
        </h2>
        <form
          onSubmit={handleCreateScan}
          className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl mb-4"
        >
          <Button type="submit">Run Scan</Button>
        </form>
        <ul className="divide-y border border-ink bg-sheet">
          {scans.map((s) => (
            <li key={s.id} className="p-3 font-mono text-xs">
              Scan #{s.id} — {s.pages_scanned} pages, {s.issues_found} issues — {s.status}
            </li>
          ))}
          {scans.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No scans yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Issues">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Accessibility Issues
        </h2>
        <form
          onSubmit={handleCreateIssue}
          className="grid grid-cols-1 gap-3 sm:grid-cols-5 max-w-xl mb-4"
        >
          <input
            name="page_url"
            placeholder="Page URL"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="rule_id"
            placeholder="Rule ID (e.g. color-contrast)"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="rule_name"
            placeholder="Rule name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="severity"
            placeholder="critical/serious/moderate/minor"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="description"
            placeholder="Description"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Log Issue</Button>
        </form>
      </section>
    </main>
  );
}
