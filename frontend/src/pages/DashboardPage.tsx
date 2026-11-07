import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Dialog, useToast } from '@/design/primitives';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import type { ProjectOut, CompletionChecklistItem } from '@/api/client';
import { ApiError } from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { useGithubHeatmap } from '@/hooks/useGithubHeatmap';
import { useLogout } from '@/hooks/useLogout';
import {
  useCompleteProject,
  useDeleteProject,
  useMyProjects,
  usePatchProject,
  useReopenProject,
} from '@/hooks/useMyProjects';
import { useProjectProgress } from '@/hooks/useProjectProgress';
import { cx } from '@/lib/cx';

const SUMMARY_MAX = 400;

const STATUS_TAGS: Record<ProjectOut['verification_status'], { label: string; tone: string }> = {
  verified: { label: 'verified · public', tone: 'text-accent' },
  needs_review: { label: 'pending review', tone: 'text-ink/60' },
  rejected: { label: 'rejected', tone: 'text-danger' },
};

function checkCompletionError(error: unknown): CompletionChecklistItem[] | null {
  if (error instanceof ApiError && error.status === 422 && error.code === 'not_ready_to_complete') {
    const detail = (error.payload as { detail?: { checklist?: unknown } } | undefined)?.detail;
    if (Array.isArray(detail?.checklist)) return detail.checklist as CompletionChecklistItem[];
  }
  return null;
}

function EditProjectDialog({ project }: { project: ProjectOut }) {
  const patch = usePatchProject(project.id);
  const toast = useToast();
  const [summary, setSummary] = useState(project.solution_summary ?? '');
  const [demoUrl, setDemoUrl] = useState(project.demo_url ?? '');
  const [openToContributors, setOpenToContributors] = useState(project.open_for_contributors);

  function save() {
    patch.mutate(
      {
        solution_summary: summary.trim().length > 0 ? summary.trim() : undefined,
        demo_url: demoUrl.trim().length > 0 ? demoUrl.trim() : undefined,
        open_for_contributors: openToContributors,
      },
      {
        onSuccess: () => toast('Project saved.'),
        onError: (error) =>
          toast(
            error instanceof ApiError
              ? error.detail
              : 'Could not save the project. Try again.',
            'error',
          ),
      },
    );
  }

  return (
    <Dialog title={`Edit ${project.repo_name}`} triggerLabel="Edit">
      <div className="flex flex-col gap-3">
        <label className="block" htmlFor={`summary-${project.id}`}>
          <span className={cx(fieldLabelClasses, 'block')}>
            Description (optional) ({summary.trim().length}/400)
          </span>
          <textarea
            id={`summary-${project.id}`}
            value={summary}
            onChange={(event) => setSummary(event.target.value)}
            rows={5}
            maxLength={SUMMARY_MAX}
            className="mt-1 w-full border border-ink bg-paper px-3 py-2 text-sm"
          />
          <span className="mt-1 block text-xs text-ink-soft">
            Editing the description re-runs the automatic relevance check at most
            once per day.
          </span>
        </label>
        <label className="block" htmlFor={`demo-${project.id}`}>
          <span className={fieldLabelClasses}>Demo URL (optional)</span>
          <input
            id={`demo-${project.id}`}
            type="url"
            value={demoUrl}
            onChange={(event) => setDemoUrl(event.target.value)}
            placeholder="https://…"
            className="mt-1 w-full border border-ink bg-paper px-3 py-2 text-sm"
          />
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={openToContributors}
            onChange={(event) => setOpenToContributors(event.target.checked)}
            className="size-4 accent-[var(--accent)]"
          />
          Open for contributors
        </label>
        <Button onClick={save} disabled={patch.isPending}>
          {patch.isPending ? 'Saving…' : 'Save changes'}
        </Button>
      </div>
    </Dialog>
  );
}

function CompleteChecklistRow({ checklist }: { checklist: CompletionChecklistItem[] }) {
  return (
    <ul className="space-y-1 text-sm">
      {checklist.map((item) => (
        <li key={item.item}>
          <span className={item.ok ? 'text-accent' : 'text-danger'}>
            {item.ok ? '✓' : '✗'}
          </span>{' '}
          {item.item}
        </li>
      ))}
    </ul>
  );
}

function CompleteProjectDialog({ project }: { project: ProjectOut }) {
  const complete = useCompleteProject(project.id);
  const toast = useToast();
  const [demoUrl, setDemoUrl] = useState(project.demo_url ?? '');
  const [reflection, setReflection] = useState('');
  const [checklist, setChecklist] = useState<CompletionChecklistItem[] | null>(null);
  const [failure, setFailure] = useState<string | null>(null);

  function markComplete() {
    setChecklist(null);
    setFailure(null);
    complete.mutate(
      {
        demo_url: demoUrl.trim().length > 0 ? demoUrl.trim() : undefined,
        reflection: reflection.trim().length > 0 ? reflection.trim() : undefined,
      },
      {
        onSuccess: () => toast('Marked as completed. Nice ship.'),
        onError: (error) => {
          const items = checkCompletionError(error);
          if (items) {
            setChecklist(items);
          } else {
            setFailure(
              error instanceof ApiError
                ? error.status >= 500
                  ? 'GitHub is not reachable right now — try again shortly.'
                  : error.detail
                : 'Could not mark as completed. Try again.',
            );
          }
        },
      },
    );
  }

  return (
    <Dialog title={`Complete ${project.repo_name}`} triggerLabel="Mark complete">
      <div className="flex flex-col gap-3">
        <p className="text-sm leading-snug">
          Completing needs a verified submission, a README and at least 5
          commits. MANABI checks GitHub again the moment you press the button.
        </p>
        <label className="block" htmlFor={`complete-demo-${project.id}`}>
          <span className={fieldLabelClasses}>Demo URL (optional)</span>
          <input
            id={`complete-demo-${project.id}`}
            type="url"
            value={demoUrl}
            onChange={(event) => setDemoUrl(event.target.value)}
            placeholder="https://…"
            className="mt-1 w-full border border-ink bg-paper px-3 py-2 text-sm"
          />
        </label>
        <label className="block" htmlFor={`complete-reflection-${project.id}`}>
          <span className={fieldLabelClasses}>What did you learn? (optional)</span>
          <textarea
            id={`complete-reflection-${project.id}`}
            value={reflection}
            onChange={(event) => setReflection(event.target.value)}
            rows={3}
            maxLength={800}
            className="mt-1 w-full border border-ink bg-paper px-3 py-2 text-sm"
          />
        </label>
        {checklist ? (
          <div className="border border-ink bg-sheet p-3">
            <p className="font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
              Not ready yet — missing:
            </p>
            <CompleteChecklistRow checklist={checklist} />
          </div>
        ) : null}
        {failure ? (
          <p role="alert" className="font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
            {failure}
          </p>
        ) : null}
        <Button onClick={markComplete} disabled={complete.isPending}>
          {complete.isPending ? 'Checking GitHub…' : 'Mark completed'}
        </Button>
      </div>
    </Dialog>
  );
}

function RemoveProjectDialog({ project }: { project: ProjectOut }) {
  const remove = useDeleteProject();
  const toast = useToast();
  const [failure, setFailure] = useState<string | null>(null);

  return (
    <Dialog title={`Remove ${project.repo_name}?`} triggerLabel="Remove">
      <div className="flex flex-col gap-3">
        <p className="text-sm leading-snug">
          This removes the submission from the board completely. Your GitHub
          repository itself is untouched.
        </p>
        {failure ? (
          <p role="alert" className="font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
            {failure}
          </p>
        ) : null}
        <Button
          onClick={() =>
            remove.mutate(project.id, {
              onSuccess: () => toast(`${project.repo_name} removed.`),
              onError: () =>
                setFailure('Could not remove the project. Try again.'),
            })
          }
          disabled={remove.isPending}
        >
          {remove.isPending ? 'Removing…' : 'Yes, remove it'}
        </Button>
      </div>
    </Dialog>
  );
}

function MyProjectRow({ project }: { project: ProjectOut }) {
  const progress = useProjectProgress(project.id);
  const reopen = useReopenProject(project.id);
  const toast = useToast();
  const statusTag = STATUS_TAGS[project.verification_status] ?? null;
  const completed = project.completed_at != null;

  function handleReopen() {
    reopen.mutate(undefined, {
      onSuccess: () => toast('Back to building.'),
      onError: () => toast('Could not reopen. Try again.', 'error'),
    });
  }

  return (
    <li className="flex flex-col gap-2 px-4 py-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <Link
            to={`/projects/${project.id}`}
            className="font-display text-base uppercase leading-tight underline-offset-4 hover:underline md:text-lg"
          >
            {project.repo_name}
          </Link>
          <p className="mt-0.5 truncate font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
            {project.problem_title}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {statusTag ? (
            <span
              className={cx(
                'font-mono text-[10px] font-bold uppercase tracking-widest',
                statusTag.tone,
              )}
            >
              {statusTag.label}
            </span>
          ) : null}
          {completed ? (
            <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent">
              ✓ Completed
            </span>
          ) : null}
          {progress.isLoading ? (
            <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
              Checking GitHub…
            </span>
          ) : (
            <ProjectProgressBadge progress={progress.data ?? null} />
          )}
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        {verifiedOrBetter(project) ? (
          <CompleteProjectDialog project={project} />
        ) : null}
        <EditProjectDialog project={project} />
        {completed ? (
          <Button variant="secondary" onClick={handleReopen} disabled={reopen.isPending}>
            Reopen
          </Button>
        ) : null}
        <RemoveProjectDialog project={project} />
      </div>
    </li>
  );
}

function verifiedOrBetter(project: ProjectOut): boolean {
  return project.verification_status === 'verified' && project.completed_at == null;
}

const HEAT_LEVEL_BG: Record<number, string> = {
  0: 'bg-ink/10',
  1: 'bg-accent/40',
  2: 'bg-accent/65',
  3: 'bg-accent/85',
  4: 'bg-accent',
};

const WEEKS = 13;

function GithubHeatmapSection({ username }: { username: string }) {
  const heatmap = useGithubHeatmap();

  const byDate = new Map<string, number>();
  if (heatmap.data) {
    for (const day of heatmap.data.days) {
      byDate.set(day.date, day.count);
    }
  }

  const today = new Date();
  const totalCells = WEEKS * 7;
  const cells: Array<{ date: string; count: number }> = [];
  for (let i = totalCells - 1; i >= 0; i -= 1) {
    const date = new Date(today);
    date.setUTCDate(today.getUTCDate() - i);
    const iso = date.toISOString().slice(0, 10);
    cells.push({ date: iso, count: byDate.get(iso) ?? 0 });
  }

  function level(count: number): number {
    if (count <= 0) return 0;
    if (count < 3) return 1;
    if (count < 6) return 2;
    if (count < 10) return 3;
    return 4;
  }

  return (
    <section aria-label="GitHub activity" className="mt-8">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="font-display text-xl uppercase md:text-2xl">GitHub activity</h2>
        {heatmap.data ? (
          <p className="font-mono text-[11px] font-bold uppercase tracking-widest text-ink/70">
            {`${heatmap.data.total} pushes · public · last ${WEEKS} weeks`}
          </p>
        ) : null}
      </div>
      {heatmap.isPending ? (
        <p className="mt-3 text-sm">Loading activity from GitHub…</p>
      ) : heatmap.error ? (
        <p className="mt-3 font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
          {heatmap.error.detail || 'Could not load GitHub activity.'}
        </p>
      ) : (
        <div className="mt-3 border border-ink bg-sheet p-4">
          <div
            className="grid gap-[3px]"
            style={{ gridTemplateColumns: `repeat(${WEEKS}, 1fr)` }}
          >
            {cells.map((cell) => (
              <span
                key={cell.date}
                aria-label={`${cell.date}: ${cell.count} pushes`}
                title={`${cell.date}: ${cell.count} ${cell.count === 1 ? 'push' : 'pushes'}`}
                className={cx(
                  'block aspect-square rounded-[1px]',
                  HEAT_LEVEL_BG[level(cell.count)],
                )}
              />
            ))}
          </div>
          <p className="mt-3 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
            Public pushes by {username} · updates from GitHub
          </p>
        </div>
      )}
    </section>
  );
}

const fieldLabelClasses = 'font-mono text-[11px] font-bold uppercase tracking-widest';

export function DashboardPage() {
  const me = useMe();
  const logout = useLogout();
  const projects = useMyProjects();

  const displayName = me.data?.name || me.data?.username;
  const rows = projects.data ?? [];
  const inReview = rows.filter((p) => p.verification_status === 'needs_review').length;
  const completedCount = rows.filter((p) => p.completed_at != null).length;
  const buildingCount = rows.length - completedCount;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl uppercase leading-none md:text-4xl">
            Dashboard
          </h1>
          <p className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-ink/70">
            {displayName ? `Logged in as ${displayName}` : 'Loading…'}
          </p>
        </div>
        {me.data ? (
          <Button
            variant="danger"
            size="small"
            onClick={() => logout.mutate()}
            disabled={logout.isPending}
          >
            {logout.isPending ? 'Signing out…' : 'Log out'}
          </Button>
        ) : null}
      </div>

      <section aria-label="Your projects" className="mt-8">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="font-display text-xl uppercase md:text-2xl">
            Your projects
          </h2>
          {rows.length > 0 ? (
            <p className="font-mono text-[11px] font-bold uppercase tracking-widest text-ink/70">
              {rows.length} total · {buildingCount} building · {inReview} in
              review · {completedCount} completed
            </p>
          ) : null}
        </div>
        {projects.isLoading ? (
          <p className="mt-2 text-sm">Loading projects…</p>
        ) : projects.data && projects.data.length > 0 ? (
          <ul className="mt-3 divide-y-[3px] divide-ink border border-ink bg-sheet">
            {projects.data.map((project) => (
              <MyProjectRow key={project.id} project={project} />
            ))}
          </ul>
        ) : (
          <p className="mt-3 border border-ink bg-sheet p-4 text-sm leading-snug">
            No projects yet.{' '}
            <Link to="/problems" className="underline underline-offset-4">
              Pick a problem
            </Link>{' '}
            and submit your repo against it.
          </p>
        )}
        {projects.error ? (
          <p className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
            {projects.error.detail}
          </p>
        ) : null}
      </section>

      {me.data ? <GithubHeatmapSection username={me.data.username} /> : null}
    </main>
  );
}
