import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listWorkflows,
  createWorkflow,
  Workflow,
  WorkflowCreate,
  publishWorkflow,
  archiveWorkflow,
  listWorkflowExecutions,
  WorkflowExecution,
  WorkflowExecutionCreate,
  createWorkflowExecution,
  createWorkflowStep,
  WorkflowStepExecutionCreate,
  getWorkflowStats,
  WorkflowStats,
} from '@/api/projects';

export function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [executions, setExecutions] = useState<WorkflowExecution[]>([]);
  const [stats, setStats] = useState<WorkflowStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [wf, ex, st] = await Promise.all([
      listWorkflows(),
      listWorkflowExecutions(),
      getWorkflowStats(),
    ]);
    setWorkflows(wf);
    setExecutions(ex);
    setStats(st);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleCreateWorkflow(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: WorkflowCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      definition: { nodes: [], edges: [] },
    };
    const created = await createWorkflow(body);
    setWorkflows([created, ...workflows]);
  }

  async function handleExecute(workflowId: number) {
    const body: WorkflowExecutionCreate = { workflow_id: workflowId };
    const created = await createWorkflowExecution(body);
    setExecutions([created, ...executions]);
  }

  async function handlePublish(id: number) {
    await publishWorkflow(id);
    load();
  }

  async function handleArchive(id: number) {
    await archiveWorkflow(id);
    load();
  }

  async function handleCreateStep(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: WorkflowStepExecutionCreate = {
      execution_id: 1,
      step_id: (form.elements.namedItem('step_id') as HTMLInputElement).value,
      step_type: (form.elements.namedItem('step_type') as HTMLSelectElement).value,
    };
    await createWorkflowStep(body);
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Visual Workflow</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-yellow underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Workflows</p>
          <p className="font-display text-2xl">{stats?.total_workflows ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Active</p>
          <p className="font-display text-2xl">{stats?.active_workflows ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Executions</p>
          <p className="font-display text-2xl">{stats?.total_executions ?? 0}</p>
        </div>
        <div className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Failed</p>
          <p className="font-display text-2xl">{stats?.failed_executions ?? 0}</p>
        </div>
      </div>

      <section aria-label="Create workflow" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Create Workflow
        </h2>
        <form onSubmit={handleCreateWorkflow} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Workflow name"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Create</Button>
        </form>
      </section>

      <section aria-label="Workflows" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">Workflows</h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {workflows.map((w) => (
            <li key={w.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{w.name}</span> — {w.status}
              <div className="flex gap-1 mt-1">
                {w.status === 'draft' ? (
                  <Button onClick={() => handlePublish(w.id)}>Publish</Button>
                ) : (
                  <Button onClick={() => handleArchive(w.id)} variant="secondary">Archive</Button>
                )}
                <Button onClick={() => handleExecute(w.id)}>Execute</Button>
              </div>
            </li>
          ))}
          {workflows.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No workflows yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Executions">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Executions
        </h2>
        <ul className="divide-y border-[3px] border-ink bg-white">
          {executions.map((e) => (
            <li key={e.id} className="p-3 font-mono text-xs">
              Workflow #{e.workflow_id} — {e.status}
              <span className="ml-2 font-bold text-[9px] border-[1px] border-ink px-1">{e.status}</span>
            </li>
          ))}
          {executions.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No executions yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Step executions">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Step Executions
        </h2>
        <form
          onSubmit={handleCreateStep}
          className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl mb-4"
        >
          <input
            name="step_id"
            placeholder="Step ID"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
            required
          />
          <select
            name="step_type"
            className="border-[3px] border-ink bg-white p-2 font-mono text-sm"
          >
            <option value="http">HTTP</option>
            <option value="condition">Condition</option>
            <option value="delay">Delay</option>
            <option value="approval">Approval</option>
          </select>
          <Button type="submit">Add Step</Button>
        </form>
      </section>
    </main>
  );
}
