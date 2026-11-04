import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listTenants,
  createTenant,
  Tenant,
  TenantCreate,
  listFindings,
  SecurityFinding,
  SecurityFindingCreate,
  createFinding,
  listRolePermissions,
  RolePermission,
  RolePermissionCreate,
  createRolePermission,
  getAuditSummary,
  AuditSummary,
} from '@/api/projects';

export function TenantSecurityPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [findings, setFindings] = useState<SecurityFinding[]>([]);
  const [rolePerms, setRolePerms] = useState<RolePermission[]>([]);
  const [summary, setSummary] = useState<AuditSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [t, f, rp, s] = await Promise.all([
        listTenants(),
        listFindings(1),
        listRolePermissions(),
        getAuditSummary(),
      ]);
      setTenants(t);
      setFindings(f);
      setRolePerms(rp);
      setSummary(s);
      setLoading(false);
    }
    load();
  }, []);

  async function handleCreateTenant(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: TenantCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      slug: (form.elements.namedItem('slug') as HTMLInputElement).value,
    };
    const created = await createTenant(body);
    setTenants([created, ...tenants]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Tenant Security Audit</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Tenants</p>
          <p className="font-display text-2xl">{tenants.length}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Open Findings</p>
          <p className="font-display text-2xl">{summary?.open_findings ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Critical</p>
          <p className="font-display text-2xl">{summary?.critical_findings ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">High</p>
          <p className="font-display text-2xl">{summary?.high_findings ?? 0}</p>
        </div>
      </div>

      <section aria-label="Create tenant" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Create Tenant
        </h2>
        <form onSubmit={handleCreateTenant} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Tenant name"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="slug"
            placeholder="tenant-slug"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Create</Button>
        </form>
      </section>

      <section aria-label="Tenants" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">Tenants</h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {tenants.map((t) => (
            <li key={t.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{t.name}</span> ({t.slug}) — plan: {t.plan}
            </li>
          ))}
          {tenants.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No tenants yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Security findings" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Security Findings
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const form = e.currentTarget as HTMLFormElement;
            const body: SecurityFindingCreate = {
              tenant_id: 1,
              check_type: (form.elements.namedItem('check_type') as HTMLInputElement).value,
              severity: (form.elements.namedItem('severity') as HTMLInputElement).value,
              title: (form.elements.namedItem('title') as HTMLInputElement).value,
              description: (form.elements.namedItem('description') as HTMLInputElement).value,
            };
            createFinding(body).then((f) => setFindings([f, ...findings]));
          }}
          className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl"
        >
          <input
            name="check_type"
            placeholder="Check type"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="severity"
            placeholder="critical/high/medium/low"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="title"
            placeholder="Title"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="description"
            placeholder="Description"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Log Finding</Button>
        </form>
        <ul className="mt-4 divide-y border-[3px] border-ink bg-white">
          {findings.map((f) => (
            <li key={f.id} className="p-3 font-mono text-xs">
              <span className={`font-bold text-red`}>{f.severity.toUpperCase()}</span> — {f.title}
              <span className="ml-2 font-bold text-[9px] border-[1px] border-ink px-1">{f.status}</span>
            </li>
          ))}
          {findings.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No findings yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Role permissions">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Role Permissions
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const form = e.currentTarget as HTMLFormElement;
            const body: RolePermissionCreate = {
              role: (form.elements.namedItem('role') as HTMLInputElement).value,
              permission: (form.elements.namedItem('permission') as HTMLInputElement).value,
            };
            createRolePermission(body).then((p) => setRolePerms([p, ...rolePerms]));
          }}
          className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl"
        >
          <input
            name="role"
            placeholder="admin/member/viewer"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="permission"
            placeholder="read:orders"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Add Permission</Button>
        </form>
        <ul className="mt-4 divide-y border-[3px] border-ink bg-white">
          {rolePerms.map((p) => (
            <li key={p.id} className="p-3 font-mono text-xs">
              {p.role} → {p.permission}{p.resource_type ? ` (${p.resource_type})` : ''}
            </li>
          ))}
          {rolePerms.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No role permissions yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
