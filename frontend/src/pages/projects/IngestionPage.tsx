import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listIngestionJobs,
  createIngestionJob,
  IngestionJob,
  IngestionJobCreate,
  listIngestedFiles,
  IngestedFile,
  IngestedFileCreate,
  addIngestedFile,
  createProcessingWorker,
  ProcessingWorker,
  ProcessingWorkerCreate,
  listProcessingWorkers,
  getIngestionStats,
  IngestionStats,
} from '@/api/projects';

export function IngestionPage() {
  const [jobs, setJobs] = useState<IngestionJob[]>([]);
  const [files, setFiles] = useState<IngestedFile[]>([]);
  const [workers, setWorkers] = useState<ProcessingWorker[]>([]);
  const [stats, setStats] = useState<IngestionStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [j, f, w, s] = await Promise.all([
        listIngestionJobs(),
        listIngestedFiles(1),
        listProcessingWorkers(),
        getIngestionStats(),
      ]);
      setJobs(j);
      setFiles(f);
      setWorkers(w);
      setStats(s);
      setLoading(false);
    }
    load();
  }, []);

  async function handleCreateJob(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: IngestionJobCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
    };
    const created = await createIngestionJob(body);
    setJobs([created, ...jobs]);
  }

  async function handleAddFile(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: IngestedFileCreate = {
      job_id: 1,
      original_filename: (form.elements.namedItem('filename') as HTMLInputElement).value,
      stored_path: `/uploads/${(form.elements.namedItem('filename') as HTMLInputElement).value}`,
      file_size: Number((form.elements.namedItem('size') as HTMLInputElement).value) || 0,
      mime_type: (form.elements.namedItem('mime_type') as HTMLInputElement).value,
    };
    const created = await addIngestedFile(body);
    setFiles([created, ...files]);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">File Ingestion</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Jobs</p>
          <p className="font-display text-2xl">{stats?.total_jobs ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Pending</p>
          <p className="font-display text-2xl">{stats?.pending_jobs ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Files</p>
          <p className="font-display text-2xl">{stats?.total_files ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Duplicates Skipped</p>
          <p className="font-display text-2xl">{stats?.duplicate_files ?? 0}</p>
        </div>
      </div>

      <section aria-label="Create job" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Create Ingestion Job
        </h2>
        <form onSubmit={handleCreateJob} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Job name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Create Job</Button>
        </form>
      </section>

      <section aria-label="Files" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Ingested Files
        </h2>
        <form
          onSubmit={handleAddFile}
          className="grid grid-cols-1 gap-3 sm:grid-cols-5 max-w-xl mb-4"
        >
          <input
            name="filename"
            placeholder="filename.csv"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="size"
            type="number"
            placeholder="Size (bytes)"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <input
            name="mime_type"
            placeholder="text/csv"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <Button type="submit">Add File</Button>
        </form>
        <ul className="divide-y border border-ink bg-sheet">
          {files.map((f) => (
            <li key={f.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{f.original_filename}</span> — {f.file_size} bytes
              <span className="ml-2 font-bold text-[9px] border-[1px] border-ink px-1">{f.status}</span>
              {f.is_duplicate ? ' <span className="font-bold text-accent">DUPLICATE</span>' : null}
            </li>
          ))}
          {files.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No files yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Workers">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Processing Workers
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const form = e.currentTarget as HTMLFormElement;
            const body: ProcessingWorkerCreate = {
              worker_name: (form.elements.namedItem('worker_name') as HTMLInputElement).value,
            };
            createProcessingWorker(body).then((w) => setWorkers([w, ...workers]));
          }}
          className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl"
        >
          <input
            name="worker_name"
            placeholder="worker-1"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Add Worker</Button>
        </form>
        <ul className="mt-4 divide-y border border-ink bg-sheet">
          {workers.map((w) => (
            <li key={w.id} className="p-3 font-mono text-xs">
              {w.worker_name} — {w.status}
            </li>
          ))}
          {workers.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No workers yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
