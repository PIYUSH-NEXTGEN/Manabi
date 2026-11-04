import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listApiSpecs,
  createApiSpec,
  ApiSpec,
  ApiSpecCreate,
  listApiComparisons,
  ApiContractComparison,
  listMonitoringTargets,
  createMonitoringTarget,
  ApiMonitoringTarget,
  ApiMonitoringTargetCreate,
  runContractCheck,
  listContractChecks,
  ApiContractCheck,
} from '@/api/projects';

export function ApiContractsPage() {
  const [specs, setSpecs] = useState<ApiSpec[]>([]);
  const [comparisons, setComparisons] = useState<ApiContractComparison[]>([]);
  const [targets, setTargets] = useState<ApiMonitoringTarget[]>([]);
  const [checks, setChecks] = useState<ApiContractCheck[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [s, c, t, ch] = await Promise.all([
        listApiSpecs(),
        listApiComparisons(),
        listMonitoringTargets(),
        listContractChecks(1, 10),
      ]);
      setSpecs(s);
      setComparisons(c);
      setTargets(t);
      setChecks(ch);
      setLoading(false);
    }
    load();
  }, []);

  async function handleCreateSpec(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: ApiSpecCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      version: (form.elements.namedItem('version') as HTMLInputElement).value,
      spec: { openapi: '3.0.0', info: { title: (form.elements.namedItem('name') as HTMLInputElement).value }, paths: {} },
    };
    const created = await createApiSpec(body);
    setSpecs([created, ...specs]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">API Contract Drift</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-3">
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Specs</p>
          <p className="font-display text-2xl">{specs.length}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Comparisons</p>
          <p className="font-display text-2xl">{comparisons.length}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Monitoring Targets</p>
          <p className="font-display text-2xl">{targets.length}</p>
        </div>
      </div>

      <section aria-label="Register spec" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Register API Spec
        </h2>
        <form onSubmit={handleCreateSpec} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Spec name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="version"
            placeholder="v1.0.0"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Register</Button>
        </form>
      </section>

      <section aria-label="Comparisons" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Contract Comparisons
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse border border-ink bg-sheet">
            <thead>
              <tr className="border-b border-ink">
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Spec A</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Spec B</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Breaking</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Non-breaking</th>
                <th className="p-3 font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">Created</th>
              </tr>
            </thead>
            <tbody>
              {comparisons.map((c) => (
                <tr key={c.id} className="border-b border-ink/20 hover:bg-ink/5">
                  <td className="p-3 font-mono text-xs">#{c.spec_a_id}</td>
                  <td className="p-3 font-mono text-xs">#{c.spec_b_id}</td>
                  <td className="p-3 font-mono text-xs">{c.breaking_changes_count}</td>
                  <td className="p-3 font-mono text-xs">{c.non_breaking_changes_count}</td>
                  <td className="p-3 font-mono text-xs">{new Date(c.created_at).toLocaleString()}</td>
                </tr>
              ))}
              {comparisons.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-3 font-mono text-xs text-center text-ink/50">
                    No comparisons yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-label="Monitoring targets" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Monitoring Targets
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const form = e.currentTarget as HTMLFormElement;
            const body: ApiMonitoringTargetCreate = {
              name: (form.elements.namedItem('name') as HTMLInputElement).value,
              base_url: (form.elements.namedItem('base_url') as HTMLInputElement).value,
            };
            createMonitoringTarget(body).then((t) => setTargets([t, ...targets]));
          }}
          className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl"
        >
          <input
            name="name"
            placeholder="Target name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="base_url"
            placeholder="https://api.example.com"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Add Target</Button>
        </form>
        <div className="mt-4 space-y-2">
          {targets.map((t) => (
            <div key={t.id} className="flex items-center justify-between p-3 border border-ink bg-sheet">
              <span className="font-mono text-xs">{t.name}</span>
              <Button
                onClick={() => runContractCheck(t.id).then((c) => setChecks([c, ...checks]))}
              >
                Check
              </Button>
            </div>
          ))}
        </div>
      </section>

      <section aria-label="Contract checks">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Recent Contract Checks
        </h2>
        <ul className="divide-y border border-ink bg-sheet">
          {checks.map((c) => (
            <li key={c.id} className="p-3 font-mono text-xs">
              Target #{c.target_id} — {c.status} ({c.breaking_changes_detected} breaking)
            </li>
          ))}
          {checks.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No checks yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
