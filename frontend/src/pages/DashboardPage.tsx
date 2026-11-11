import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Dialog, useToast } from '@/design/primitives';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import type {
  ProjectOut,
  ProjectPatch,
  CompletionChecklistItem,
} from '@/api/client';
import { ApiError } from '@/api/client';
import { useMe } from '@/hooks/useMe';
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
import { SOLUTION_SUMMARY_MAX } from '@/lib/limits';

const STATUS_TAGS: Record<ProjectOut['verification_status'], { label: string; tone: string }> = {
  verified: { label: 'verified · public', tone: 'text-accent' },
  needs_review: { label: 'pending review', tone: 'text-ink/60' },
  rejected: { label: 'rejected', tone: 'text-danger' },
};

function checkCompletionError(error: unknown): CompletionChecklistItem[] | null {
  if (error instanceof ApiError && error.status === 422 && error.code === 'not_ready_to_complete') {
    const detail = (error.payload as { detail?: { checklist?: unknown } } | undefined)?.detail;
    if (Array.isArray(detail?.checklist)) {
      return detail.checklist.filter(
        (item): item is CompletionChecklistItem =>
          typeof item?.item === 'string' && typeof item?.ok === 'boolean',
      );
    }
  }
  return null;
}

function EditProjectDialog({ project }: { project: ProjectOut }) {
  const patch = usePatchProject(project.id);
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [summary, setSummary] = useState(project.solution_summary ?? '');
  const [demoUrl, setDemoUrl] = useState(project.demo_url ?? '');
  const [openToContributors, setOpenToContributors] = useState(project.open_for_contributors);

  function handleOpenChange(next: boolean) {
    setOpen(next);
    if (next) {
      // Re-sync from the latest server copy every time the dialog opens.
      setSummary(project.solution_summary ?? '');
      setDemoUrl(project.demo_url ?? '');
      setOpenToContributors(project.open_for_contributors);
    }
  }

  function save() {
    const nextSummary = summary.trim();
    const nextDemoUrl = demoUrl.trim();
    const body: ProjectPatch = { open_for_contributors: openToContributors };
    let changed = openToContributors !== project.open_for_contributors;
    // Send only changed fields, and send "" to clear one. An omitted field
    // means "leave it alone", so undefined could never clear a value.
    if (nextSummary !== (project.solution_summary ?? '').trim()) {
      body.solution_summary = nextSummary;
      changed = true;
    }
    if (nextDemoUrl !== (project.demo_url ?? '').trim()) {
      body.demo_url = nextDemoUrl;
      changed = true;
    }
    if (!changed) {
      setOpen(false);
      return;
    }
    patch.mutate(body, {
      onSuccess: () => {
        setOpen(false);
        toast('Project saved.');
      },
      onError: (error) => {
        // The backend commits the edit before re-running the relevance check,
        // so rate-limit/GitHub errors mean saved-but-not-reverified.
        const savedAnyway =
          error instanceof ApiError && (error.status === 429 || error.status === 503);
        if (savedAnyway) {
          setOpen(false);
          toast(`${error.detail} Your changes were saved.`);
          return;
        }
        toast(
          error instanceof ApiError
            ? error.detail
            : 'Could not save the project. Try again.',
          'error',
        );
      },
    });
  }

  return (
    <Dialog
      open={open}
      onOpenChange={handleOpenChange}
      title={`Edit ${project.repo_name}`}
      triggerLabel="Edit"
    >
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
            maxLength={SOLUTION_SUMMARY_MAX}
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
  const [open, setOpen] = useState(false);
  const [demoUrl, setDemoUrl] = useState(project.demo_url ?? '');
  const [reflection, setReflection] = useState('');
  const [checklist, setChecklist] = useState<CompletionChecklistItem[] | null>(null);
  const [failure, setFailure] = useState<string | null>(null);

  function handleOpenChange(next: boolean) {
    setOpen(next);
    if (next) {
      setDemoUrl(project.demo_url ?? '');
      setReflection('');
      setChecklist(null);
      setFailure(null);
    }
  }

  function markComplete() {
    setChecklist(null);
    setFailure(null);
    complete.mutate(
      {
        demo_url: demoUrl.trim().length > 0 ? demoUrl.trim() : undefined,
        reflection: reflection.trim().length > 0 ? reflection.trim() : undefined,
      },
      {
        onSuccess: () => {
          setOpen(false);
          toast('Marked as completed. Nice ship.');
        },
        onError: (error) => {
          const items = checkCompletionError(error);
          if (items) {
            setChecklist(items);
          } else {
            setFailure(
              error instanceof ApiError
                ? error.status >= 500
                  ? 'GitHub is not reachable right now. Try again shortly.'
                  : error.detail
                : 'Could not mark as completed. Try again.',
            );
          }
        },
      },
    );
  }

  return (
    <Dialog
      open={open}
      onOpenChange={handleOpenChange}
      title={`Complete ${project.repo_name}`}
      triggerLabel="Mark complete"
    >
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
              Not ready yet. Missing:
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
  const [open, setOpen] = useState(false);
  const [failure, setFailure] = useState<string | null>(null);

  function handleOpenChange(next: boolean) {
    setOpen(next);
    if (next) setFailure(null);
  }

  return (
    <Dialog
      open={open}
      onOpenChange={handleOpenChange}
      title={`Remove ${project.repo_name}?`}
      triggerLabel="Remove"
    >
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
              onSuccess: () => {
                setOpen(false);
                toast(`${project.repo_name} removed.`);
              },
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

    </main>
  );
}
