import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  ingestAnalyticsEvent,
  AnalyticsEventCreate,
  listAnalyticsEvents,
  AnalyticsEvent,
  setConsent,
  ConsentRecordCreate,
  createRetentionPolicy,
  DataRetentionPolicyCreate,
  listRetentionPolicies,
  DataRetentionPolicy,
  listFunnels,
  getAnalyticsStats,
  AnalyticsStats,
} from '@/api/projects';

export function AnalyticsPage() {
  const [stats, setStats] = useState<AnalyticsStats | null>(null);
  const [events, setEvents] = useState<AnalyticsEvent[]>([]);
  const [consent, setConsentRecord] = useState<{ anonymous_id: string; consent_status: string } | null>(null);
  const [policies, setPolicies] = useState<DataRetentionPolicy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [st, ev, pol] = await Promise.all([
        getAnalyticsStats(),
        listAnalyticsEvents({ projectId: 'demo', limit: 20 }),
        listRetentionPolicies(),
        listFunnels('demo'),
      ]);
      setStats(st);
      setEvents(ev);
      setPolicies(pol);
      setLoading(false);
    }
    load();
  }, []);

  async function handleTrack(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: AnalyticsEventCreate = {
      project_id: 'demo',
      session_id: 'session-' + Date.now(),
      anonymous_id: 'anon-' + Date.now(),
      event_name: (form.elements.namedItem('event_name') as HTMLInputElement).value,
      timestamp: new Date().toISOString(),
    };
    await ingestAnalyticsEvent(body);
    const ev = await listAnalyticsEvents({ projectId: 'demo', limit: 1 });
    setEvents(ev);
  }

  async function handleConsent(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: ConsentRecordCreate = {
      anonymous_id: (form.elements.namedItem('anonymous_id') as HTMLInputElement).value,
      consent_status: (form.elements.namedItem('consent_status') as HTMLSelectElement).value,
    };
    const c = await setConsent(body);
    setConsentRecord({ anonymous_id: c.anonymous_id, consent_status: c.consent_status });
  }

  async function handlePolicy(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: DataRetentionPolicyCreate = {
      project_id: (form.elements.namedItem('project_id') as HTMLInputElement).value,
      event_retention_days: Number((form.elements.namedItem('event_retention_days') as HTMLInputElement).value) || 90,
      raw_data_retention_days: Number((form.elements.namedItem('raw_data_retention_days') as HTMLInputElement).value) || 30,
    };
    const p = await createRetentionPolicy(body);
    setPolicies([p, ...policies]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Privacy Analytics</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Events</p>
          <p className="font-display text-2xl">{stats?.total_events ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Projects</p>
          <p className="font-display text-2xl">{stats?.total_projects ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Consent Granted</p>
          <p className="font-display text-2xl">{stats?.granted_consent ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Consent Denied</p>
          <p className="font-display text-2xl">{stats?.denied_consent ?? 0}</p>
        </div>
      </div>

      <section aria-label="Track event" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Track Anonymous Event
        </h2>
        <form onSubmit={handleTrack} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="event_name"
            placeholder="page_view / button_click"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Track</Button>
        </form>
      </section>

      <section aria-label="Consent" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Consent Management
        </h2>
        <form
          onSubmit={handleConsent}
          className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl"
        >
          <input
            name="anonymous_id"
            placeholder="Anonymous ID"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <select
            name="consent_status"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          >
            <option value="granted">Granted</option>
            <option value="denied">Denied</option>
          </select>
          <Button type="submit">Set Consent</Button>
        </form>
        {consent && (
          <div className="mt-4 p-3 border-[3px] border-ink bg-white">
            <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">
              Consent for {consent.anonymous_id}
            </p>
            <p className="font-mono text-xs">{consent.consent_status}</p>
          </div>
        )}
      </section>

      <section aria-label="Retention policies" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Data Retention Policies
        </h2>
        <form
          onSubmit={handlePolicy}
          className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl"
        >
          <input
            name="project_id"
            placeholder="Project ID"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="event_retention_days"
            type="number"
            placeholder="90"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          />
          <input
            name="raw_data_retention_days"
            type="number"
            placeholder="30"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          />
          <Button type="submit">Create Policy</Button>
        </form>
        <ul className="mt-4 divide-y border-[3px] border-ink bg-white">
          {policies.map((p) => (
            <li key={p.id} className="p-3 font-mono text-xs">
              {p.project_id} — events: {p.event_retention_days}d, raw: {p.raw_data_retention_days}d
            </li>
          ))}
          {policies.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No policies yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Recent events">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Recent Events (Anonymous)
        </h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {events.map((e) => (
            <li key={e.id} className="p-3 font-mono text-xs">
              {e.event_name} — anon:{e.anonymous_id.slice(0, 8)}… — {new Date(e.timestamp).toLocaleString()}
            </li>
          ))}
          {events.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No events yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
