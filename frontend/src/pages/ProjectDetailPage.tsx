import { Link, useParams } from 'react-router-dom';
import type { ReactNode } from 'react';
import { cx } from '@/lib/cx';
import { safeExternalUrl } from '@/lib/url';
import { buttonClasses, Skeleton, Stamp, Tag, useToast } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import { useProject } from '@/hooks/useProject';
import { useRefreshProgress } from '@/hooks/useRefreshProgress';
import {
  asCommitSummary,
  asIssueSummary,
  projectOwnerUsername,
} from '@/api/client';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';
const smallMono = 'font-mono text-[10px] font-bold uppercase tracking-widest';

function ProjectSkeleton() {
  return (
    <div className="mx-auto w-[min(900px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-40 w-full" />
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

  if (project.isPending) {
    return (
      <main className="border-b-[3px] border-ink bg-paper">
        <ProjectSkeleton />
      </main>
    );
  }

  if (project.isError) {
    if (project.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <main className="border-b-[3px] border-ink">
        <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
          <h1 className="font-display text-3xl uppercase">
            Could not load this project
          </h1>
          <p>{project.error.message}</p>
          <Link
            to="/problems"
            className="font-mono text-xs font-bold underline"
          >
            Back to the board
          </Link>
        </div>
      </main>
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
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(900px,96vw)] py-12">
        <p className={panelHeading}>Project · {data.repo_owner}/{data.repo_name}</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-tight">
          {data.repo_name}
        </h1>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          <ProjectProgressBadge progress={progress} />
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
            className="text-blue underline underline-offset-4"
          >
            {data.problem_title}
          </Link>
        </p>

        <section
          aria-label="GitHub progress"
          className="mt-8 border-[3px] border-ink bg-white p-4 shadow-hard"
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
              Progress unknown — hit refresh to pull the latest data from
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
                  : '—'}
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
