import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import type { ReactNode } from 'react';
import { Star } from 'lucide-react';
import { cx } from '@/lib/cx';
import { safeExternalUrl } from '@/lib/url';
import { buttonClasses, Button, Stamp, Tag, useToast } from '@/design/primitives';
import { LoadErrorPanel, PageSkeleton } from '@/pages/detailStates';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import { useProject } from '@/hooks/useProject';
import { useRefreshProgress } from '@/hooks/useRefreshProgress';
import { useMe } from '@/hooks/useMe';
import {
  useReportProject,
  useStarProject,
  useUnstarProject,
} from '@/hooks/useMyProjects';
import {
  asCommitSummary,
  asIssueSummary,
  ApiError,
  projectOwnerUsername,
} from '@/api/client';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';
const smallMono = 'font-mono text-[10px] font-bold uppercase tracking-widest';

function StarButton({
  projectId,
  starCount,
  starredByMe,
}: {
  projectId: number;
  starCount: number;
  starredByMe: boolean;
}) {
  const me = useMe();
  const star = useStarProject(projectId);
  const unstar = useUnstarProject(projectId);
  const toast = useToast();

  function toggle() {
    if (starredByMe) {
      unstar.mutate(undefined, {
        onError: () => toast('Could not un-star the project. Try again.', 'error'),
      });
      return;
    }
    star.mutate(undefined, {
      onSuccess: () => toast('Starred. Thanks for the signal.'),
      onError: (err) => {
        if (err instanceof ApiError && err.status === 409) {
          toast('You already starred this project.', 'error');
        } else {
          toast('Could not star the project. Try again.', 'error');
        }
      },
    });
  }

  if (!me.data) {
    return (
      <a
        href="/api/auth/github/login"
        title="Log in to star this project"
        aria-label="Log in to star this project"
        className={cx(buttonClasses('secondary', 'px-3 py-2'), 'press')}
      >
        <Star aria-hidden className="size-3.5" />
        {starCount > 0 ? starCount : 'Star'}
      </a>
    );
  }

  return (
    <Button
      variant="secondary"
      size="small"
      onClick={toggle}
      disabled={star.isPending || unstar.isPending}
      aria-pressed={starredByMe}
      aria-label={starredByMe ? 'Un-star this project' : 'Star this project'}
      title={starredByMe ? 'Click to remove your star' : 'Click to star this project'}
    >
      <Star
        aria-hidden
        className={cx('size-3.5', starredByMe && 'fill-accent text-accent')}
      />
      {starCount > 0 ? starCount : 'Star'}
    </Button>
  );
}

function ReportRow({ projectId, isOwner }: { projectId: number; isOwner?: boolean }) {
  const me = useMe();
  const report = useReportProject(projectId);
  const toast = useToast();
  const [reason, setReason] = useState('');
  const [error, setError] = useState<string | null>(null);

  if (!me.data || isOwner) return null;

  function report_it() {
    if (reason.trim().length < 10) {
      setError('Add a short reason (10+ characters) so the maintainers know what is wrong.');
      return;
    }
    setError(null);
    report.mutate(reason.trim(), {
      onSuccess: () => {
        toast('Report sent. Thanks. A maintainer will take a look.');
        setReason('');
      },
      onError: (err) => {
        if (err instanceof ApiError) {
          if (err.status === 409) {
            setError('You already reported this project.');
          } else if (err.status === 422) {
            setError('You cannot report your own submission.');
          } else if (err.status === 429) {
            setError('Too many reports this hour. Try again later.');
          } else {
            setError(err.detail);
          }
        } else {
          setError('Could not send the report. Try again.');
        }
      },
    });
  }

  return (
    <div className="mt-6 border-t border-line pt-4">
      <label
        htmlFor="report-reason"
        className={cx(smallMono, 'block')}
      >
        Something wrong with this submission?
      </label>
      <textarea
        id="report-reason"
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        rows={2}
        placeholder="Reports go to a maintainer, not to the repo owner."
        className="mt-2 w-[min(420px,100%)] border border-ink bg-paper px-3 py-2 text-sm"
      />
      {error ? (
        <p role="alert" className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-danger">
          {error}
        </p>
      ) : null}
      <button
        type="button"
        onClick={report_it}
        disabled={report.isPending}
        className={cx(buttonClasses('secondary'), 'mt-2')}
      >
        {report.isPending ? 'Sending…' : 'Report submission'}
      </button>
    </div>
  );
}

export function ProjectDetailPage() {
  const { id } = useParams();
  const projectId = Number(id);

  if (!Number.isInteger(projectId) || projectId <= 0) {
    return <NotFoundPage />;
  }

  return <ProjectView projectId={projectId} />;
}

function ProjectView({ projectId }: { projectId: number }) {
  const project = useProject(projectId);
  const refresh = useRefreshProgress(projectId);
  const toast = useToast();
  const me = useMe();

  if (project.isPending) {
    return (
      <main className="border-b border-ink bg-paper">
        <PageSkeleton width="w-[min(900px,96vw)]" />
      </main>
    );
  }

  if (project.isError) {
    if (project.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <LoadErrorPanel
        title="Could not load this project"
        message={project.error.message}
        backTo="/problems"
        backLabel="Back to the board"
      />
    );
  }

  const data = project.data;
  const owner = projectOwnerUsername(data.owner);
  const progress = data.progress;
  const commits = (progress?.recent_commits ?? [])
    .map((raw) => asCommitSummary(raw))
    .filter((commit): commit is NonNullable<typeof commit> => commit !== null);
  const issues = (progress?.open_issues ?? [])
    .map((raw) => asIssueSummary(raw))
    .filter((issue): issue is NonNullable<typeof issue> => issue !== null);

  function handleRefresh() {
    refresh.mutate(undefined, {
      onSuccess: () => {
        toast('Progress refreshed from GitHub.');
      },
      onError: () => {
        toast('GitHub did not respond. Try again in a minute.', 'error');
      },
    });
  }

  return (
    <main className="border-b border-ink">
      <div className="mx-auto w-[min(900px,96vw)] py-12">
        <p className={panelHeading}>Project · {data.repo_owner}/{data.repo_name}</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-tight">
          {data.repo_name}
        </h1>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          <StarButton
            projectId={projectId}
            starCount={data.star_count ?? 0}
            starredByMe={Boolean(data.starred_by_me)}
          />
          <ProjectProgressBadge progress={progress} />
          {data.completed_at != null ? (
            <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent">
              ✓ Completed
            </span>
          ) : null}
          {data.open_for_contributors ? (
            <Tag>open for contributors</Tag>
          ) : null}
          {owner ? (
            <span className={smallMono}>by {owner}</span>
          ) : null}
        </div>

        <p className="mt-3">
          {safeExternalUrl(data.repo_url) ? (
            <a
              href={safeExternalUrl(data.repo_url) ?? undefined}
              target="_blank"
              rel="noreferrer"
              className="font-mono text-xs font-bold underline underline-offset-4"
            >
              {data.repo_url} ↗
            </a>
          ) : (
            <span className="font-mono text-xs font-bold">{data.repo_url}</span>
          )}
        </p>
        <p className={cx(smallMono, 'mt-1')}>
          Problem:{' '}
          <Link
            to={`/problems/${data.problem_id}`}
            className="text-accent underline underline-offset-4"
          >
            {data.problem_title}
          </Link>
        </p>

        {data.solution_summary ? (
          <section aria-label="Solution summary" className="mt-6 border border-ink bg-sheet p-4">
            <h2 className={panelHeading}>How it solves this problem</h2>
            <p className="mt-2 text-sm leading-relaxed text-ink-soft">
              {data.solution_summary}
            </p>
            {data.demo_url && safeExternalUrl(data.demo_url) ? (
              <a
                href={safeExternalUrl(data.demo_url) ?? undefined}
                target="_blank"
                rel="noreferrer"
                className="font-mono text-xs font-bold underline underline-offset-4"
              >
                Live demo ↗
              </a>
            ) : null}
            {data.reflection ? (
              <p className="mt-2 text-sm leading-relaxed text-ink-soft">
                “{data.reflection}”
              </p>
            ) : null}
          </section>
        ) : null}

        <section
          aria-label="GitHub progress"
          className="mt-8 border border-ink bg-sheet p-4"
        >
          <div className="flex items-center justify-between gap-3">
            <h2 className={panelHeading}>Progress</h2>
            <button
              type="button"
              onClick={handleRefresh}
              disabled={refresh.isPending}
              className={cx(buttonClasses('secondary'))}
            >
              {refresh.isPending ? 'Checking GitHub…' : 'Refresh progress'}
            </button>
          </div>

          {progress ? null : (
            <p className="mt-3 text-sm leading-snug">
              Progress unknown. Hit refresh to pull the latest data from
              GitHub.
            </p>
          )}

          {progress ? (
            <dl className="mt-3 grid grid-cols-2 gap-3 md:grid-cols-4">
              <Stat label="Status">
                <Stamp
                  tone={
                    progress.status === 'active'
                      ? 'active'
                      : progress.status === 'stale'
                        ? 'stale'
                        : 'not-started'
                  }
                  rotate={-2}
                />
              </Stat>
              <Stat label="Commits">
                {progress.commit_count}
              </Stat>
              <Stat label="Last commit">
                {progress.last_commit_at
                  ? progress.last_commit_at.slice(0, 10)
                  : '-'}
              </Stat>
              <Stat label="README">
                {progress.has_readme ? 'Yes' : 'No'}
              </Stat>
            </dl>
          ) : null}

          <h3 className={cx(panelHeading, 'mt-6')}>Recent commits</h3>
          {commits.length > 0 ? (
            <ul className="mt-2 ml-4 list-disc space-y-1 text-sm leading-snug">
              {commits.map((commit) => (
                <li key={commit.sha}>
                  <span className="font-mono text-xs">{commit.sha.slice(0, 7)}</span>{' '}
                  {commit.message}{' '}
                  <span className={cx(smallMono, 'text-ink/60')}>
                    {commit.date}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-sm">No commits recorded yet.</p>
          )}

          <h3 className={cx(panelHeading, 'mt-6')}>Open issues</h3>
          {issues.length > 0 ? (
            <ul className="mt-2 space-y-2">
              {issues.map((issue) => (
                <li key={issue.number} className="text-sm">
                  {safeExternalUrl(issue.url) ? (
                    <a
                      href={safeExternalUrl(issue.url) ?? undefined}
                      target="_blank"
                      rel="noreferrer"
                      className="font-mono text-xs underline underline-offset-4"
                    >
                      #{issue.number} {issue.title}
                    </a>
                  ) : (
                    <span className="font-mono text-xs">
                      #{issue.number} {issue.title}
                    </span>
                  )}
                  {issue.labels.length > 0 ? (
                    <span className="ml-2 inline-flex gap-1">
                      {issue.labels.map((label) => (
                        <Tag key={label}>{label}</Tag>
                      ))}
                    </span>
                  ) : null}
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-sm">No open issues right now.</p>
          )}

          <ReportRow projectId={data.id} isOwner={owner != null && owner === (me.data?.username ?? null)} />
        </section>
      </div>
    </main>
  );
}

function Stat({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div>
      <dt className={smallMono}>{label}</dt>
      <dd className="mt-1 text-sm">{children}</dd>
    </div>
  );
}
