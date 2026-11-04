import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listIncidents,
  createIncident,
  Incident,
  IncidentCreate,
  getIncidentStats,
  IncidentStats,
} from '@/api/projects';

export function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [stats, setStats] = useState<IncidentStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [inc, st] = await Promise.all([listIncidents(), getIncidentStats()]);
      setIncidents(inc);
      setStats(st);
      setLoading(false);
    }
    load();
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: IncidentCreate = {
      title: (form.elements.namedItem('title') as HTMLInputElement).value,
      description: (form.elements.namedItem('description') as HTMLInputElement).value,
      severity: (form.elements.namedItem('severity') as HTMLSelectElement).value,
      tags: ((form.elements.namedItem('tags') as HTMLInputElement).value)
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean),
    };
    const created = await createIncident(body);
    setIncidents([created, ...incidents]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Incident Response</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-5">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Total</p>
          <p className="font-display text-2xl">{stats?.total_incidents ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Open</p>
          <p className="font-display text-2xl">{stats?.open ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Investigating</p>
          <p className="font-display text-2xl">{stats?.investigating ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Resolved</p>
          <p className="font-display text-2xl">{stats?.resolved ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Critical</p>
          <p className="font-display text-2xl">{stats?.critical ?? 0}</p>
        </div>
      </div>

      <section aria-label="Create incident" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Declare Incident
        </h2>
        <form onSubmit={handleCreate} className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl">
          <input
            name="title"
            placeholder="Incident title"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="description"
            placeholder="What happened?"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <select
            name="severity"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          >
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <input
            name="tags"
            placeholder="tags (comma-separated)"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          />
          <Button type="submit">Declare</Button>
        </form>
      </section>

      <section aria-label="Incidents" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">Active Incidents</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse border-[3px] border-ink bg-white">
            <thead>
              <tr className="border-b-[3px] border-ink">
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Title</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Severity</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Status</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Assignee</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Started</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map((inc) => (
                <tr key={inc.id} className="border-b border-ink/20 hover:bg-ink/5 cursor-pointer">
                  <td className="p-3 font-mono text-xs font-bold">{inc.title}</td>
                  <td className="p-3 font-mono text-xs">{inc.severity}</td>
                  <td className="p-3 font-mono text-xs">{inc.status}</td>
                  <td className="p-3 font-mono text-xs">{inc.assignee_user_id ?? '—'}</td>
                  <td className="p-3 font-mono text-xs">{new Date(inc.started_at).toLocaleString()}</td>
                </tr>
              ))}
              {incidents.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-3 font-mono text-xs text-center text-ink/50">
                    No incidents yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
