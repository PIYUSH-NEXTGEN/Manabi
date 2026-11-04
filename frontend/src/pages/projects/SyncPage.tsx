import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  createSyncRecord,
  SyncRecordCreate,
  listSyncRecords,
  SyncRecord,
  markSynced,
  markConflict,
  listSyncConflicts,
  SyncConflict,
  resolveSyncConflict,
  SyncConflictUpdate,
  getSyncStats,
  SyncStats,
} from '@/api/projects';

export function SyncPage() {
  const [records, setRecords] = useState<SyncRecord[]>([]);
  const [conflicts, setConflicts] = useState<SyncConflict[]>([]);
  const [stats, setStats] = useState<SyncStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [rec, conf, st] = await Promise.all([
      listSyncRecords(),
      listSyncConflicts(),
      getSyncStats(),
    ]);
    setRecords(rec);
    setConflicts(conf);
    setStats(st);
    setLoading(false);
  }

  async function handleCreateRecord(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: SyncRecordCreate = {
      device_id: (form.elements.namedItem('device_id') as HTMLInputElement).value,
      collection: (form.elements.namedItem('collection') as HTMLInputElement).value,
      record_id: (form.elements.namedItem('record_id') as HTMLInputElement).value,
      operation: (form.elements.namedItem('operation') as HTMLSelectElement).value,
      data: { value: (form.elements.namedItem('data_value') as HTMLInputElement).value },
    };
    const created = await createSyncRecord(body);
    setRecords([created, ...records]);
  }

  async function handleSync(id: number) {
    await markSynced(id);
    load();
  }

  async function handleMarkConflict(id: number, recordId: string) {
    await markConflict(id, recordId);
    load();
  }

  async function handleResolveConflict(id: number) {
    const body: SyncConflictUpdate = { status: 'resolved', resolved_data: { merged: true } };
    await resolveSyncConflict(id, body);
    load();
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Offline Sync</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-5">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Records</p>
          <p className="font-display text-2xl">{stats?.total_records ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Pending</p>
          <p className="font-display text-2xl">{stats?.pending ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Synced</p>
          <p className="font-display text-2xl">{stats?.synced ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Conflicts</p>
          <p className="font-display text-2xl">{stats?.conflicts ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Open Conflicts</p>
          <p className="font-display text-2xl">{stats?.open_conflicts ?? 0}</p>
        </div>
      </div>

      <section aria-label="Create sync record" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Create Sync Record
        </h2>
        <form
          onSubmit={handleCreateRecord}
          className="grid grid-cols-1 gap-3 sm:grid-cols-6 max-w-xl"
        >
          <input
            name="device_id"
            placeholder="Device ID"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="collection"
            placeholder="Collection"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <input
            name="record_id"
            placeholder="Record ID"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <select
            name="operation"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          >
            <option value="create">Create</option>
            <option value="update">Update</option>
            <option value="delete">Delete</option>
          </select>
          <input
            name="data_value"
            placeholder="Data value"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          />
          <Button type="submit">Create</Button>
        </form>
      </section>

      <section aria-label="Sync records" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Sync Records
        </h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {records.map((r) => (
            <li key={r.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{r.device_id}</span> / {r.collection} / {r.record_id}
              <span className="ml-2 font-bold text-[9px] border-[1px] border-ink px-1">{r.status}</span>
              <div className="flex gap-1 mt-1">
                {r.status === 'pending' ? (
                  <>
                    <Button onClick={() => handleSync(r.id)}>Sync</Button>
                    <Button
                      onClick={() => handleMarkConflict(r.id, r.record_id + '-conflict')}
                      variant="secondary"
                    >
                      Mark Conflict
                    </Button>
                  </>
                ) : null}
              </div>
            </li>
          ))}
          {records.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No records yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Conflicts">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Sync Conflicts
        </h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {conflicts.map((c) => (
            <li key={c.id} className="p-3 font-mono text-xs">
              {c.collection} / {c.record_id} — {c.status}
              <Button
                onClick={() => handleResolveConflict(c.id)}
                disabled={c.status === 'resolved'}
              >
                Resolve
              </Button>
            </li>
          ))}
          {conflicts.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No conflicts yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
