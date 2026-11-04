import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listWebhookEndpoints,
  createWebhookEndpoint,
  WebhookEndpoint,
  WebhookEndpointCreate,
  listWebhookEvents,
  WebhookEvent,
  listWebhookDeliveries,
  WebhookDelivery,
  retryWebhookDelivery,
  getDeliveryStats,
  DeliveryStats,
} from '@/api/projects';

export function WebhooksPage() {
  const [endpoints, setEndpoints] = useState<WebhookEndpoint[]>([]);
  const [events, setEvents] = useState<WebhookEvent[]>([]);
  const [deliveries, setDeliveries] = useState<WebhookDelivery[]>([]);
  const [stats, setStats] = useState<DeliveryStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [eps, evs, dels, st] = await Promise.all([
      listWebhookEndpoints(),
      listWebhookEvents(1, 20),
      listWebhookDeliveries({ limit: 20 }),
      getDeliveryStats(),
    ]);
    setEndpoints(eps);
    setEvents(evs);
    setDeliveries(dels);
    setStats(st);
    setLoading(false);
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: WebhookEndpointCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      url: (form.elements.namedItem('url') as HTMLInputElement).value,
      event_types: ['order.created', 'payment.received'],
    };
    const created = await createWebhookEndpoint(body);
    setEndpoints([created, ...endpoints]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Webhook Reliability</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-3">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Total Endpoints</p>
          <p className="font-display text-2xl">{endpoints.length}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Total Deliveries</p>
          <p className="font-display text-2xl">{stats?.total_deliveries ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Success Rate</p>
          <p className="font-display text-2xl">{stats?.success_rate ?? 0}%</p>
        </div>
      </div>

      <section aria-label="Register endpoint" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Register Webhook Endpoint
        </h2>
        <form onSubmit={handleCreate} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Endpoint name"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="url"
            placeholder="https://example.com/hooks"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Register</Button>
        </form>
      </section>

      <section aria-label="Recent deliveries" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Recent Deliveries
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse border-[3px] border-ink bg-white">
            <thead>
              <tr className="border-b-[3px] border-ink">
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                  Endpoint
                </th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                  Status
                </th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                  HTTP
                </th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                  Attempt
                </th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
                  Created
                </th>
              </tr>
            </thead>
            <tbody>
              {deliveries.map((d) => (
                <tr key={d.id} className="border-b border-ink/20 hover:bg-ink/5">
                  <td className="p-3 font-mono text-xs">#{d.endpoint_id}</td>
                  <td className="p-3 font-mono text-xs">{d.status}</td>
                  <td className="p-3 font-mono text-xs">{d.http_status ?? '—'}</td>
                  <td className="p-3 font-mono text-xs">#{d.attempt_number}</td>
                  <td className="p-3 font-mono text-xs">{new Date(d.created_at).toLocaleString()}</td>
                  <td className="p-3">
                    {d.status === 'failed' || d.status === 'dead_letter' ? (
                      <Button
                        onClick={() => retryWebhookDelivery(d.id).then(() => load())}
                      >
                        Retry
                      </Button>
                    ) : null}
                  </td>
                </tr>
              ))}
              {deliveries.length === 0 && (
                <tr>
                  <td colSpan={6} className="p-3 font-mono text-xs text-center text-ink/50">
                    No deliveries yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-label="Recent events">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Recent Events
        </h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {events.map((e) => (
            <li key={e.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{e.event_type}</span> on endpoint{' '}
              <span className="font-bold">#{e.endpoint_id}</span> — {new Date(e.received_at).toLocaleString()}
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
