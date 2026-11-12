import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Skeleton, Tag, useToast } from '@/design/primitives';
import {
  useAdminSubmissions,
  useApproveSubmission,
  useRejectSubmission,
} from '@/hooks/useAdmin';
import { useMe } from '@/hooks/useMe';
import { ApiError, projectOwnerUsername } from '@/api/client';
import { safeExternalUrl } from '@/lib/url';
import { cx } from '@/lib/cx';

const sectionHeading =
  'font-mono text-label font-bold uppercase tracking-widest';

const FILTERS = [
  { key: 'needs_review', label: 'Needs review' },
  { key: 'rejected', label: 'Rejected' },
  { key: 'verified', label: 'Verified' },
] as const;

function OwnershipTag({ basis }: { basis: string }) {
  return <Tag>{basis.replace(/_/g, ' ')}</Tag>;
}

export function AdminReviewPage() {
  const me = useMe();
  const toast = useToast();
  const [statusFilter, setStatusFilter] = useState<
    (typeof FILTERS)[number]['key']
  >('needs_review');
  const submissions = useAdminSubmissions(statusFilter);
  const approve = useApproveSubmission();
  const reject = useRejectSubmission();

  if (me.isPending) {
    return (
      <main className="mx-auto w-[min(1100px,96vw)] space-y-3 py-16">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-40" />
      </main>
    );
  }

  if (!me.data?.is_admin) {
    return (
      <main className="mx-auto w-[min(760px,96vw)] py-16">
        <h1 className="font-display text-display leading-[1.02] tracking-[-0.03em]">Submissions</h1>
        <p className="mt-4 rounded-panel border border-line bg-sheet p-4">
          Admin access required. Add your GitHub username to
          {' '}
          <code>ADMIN_GITHUB_USERNAMES</code> to use this page.
        </p>
      </main>
    );
  }

  function runApprove(id: number) {
    approve.mutate(
      { id },
      {
        onSuccess: () => toast('Submission verified.'),
        onError: (error) =>
          toast(error instanceof ApiError ? error.detail : error.message, 'error'),
      },
    );
  }

  function runReject(id: number) {
    reject.mutate(
      { id },
      {
        onSuccess: () => toast('Submission rejected.'),
        onError: (error) =>
          toast(error instanceof ApiError ? error.detail : error.message, 'error'),
      },
    );
  }

  return (
    <main className="mx-auto w-[min(1200px,96vw)] py-12">
      <p className="font-mono text-label font-bold uppercase tracking-widest text-accent">
        Admin
      </p>
      <h1 className="mt-2 font-display text-display leading-[1.02] tracking-[-0.03em]">Submissions</h1>
      <p className="mt-3 max-w-2xl text-body leading-relaxed text-ink-soft">
        Project submissions against problems. Automatic checks first, humans
        for the edge cases.
      </p>

      <div className="mt-4 flex gap-2">
        {FILTERS.map((filter) => (
          <button
            key={filter.key}
            type="button"
            onClick={() => setStatusFilter(filter.key)}
            className={cx(
              buttonClass,
              statusFilter === filter.key && 'bg-ink text-paper',
            )}
          >
            {filter.label}
          </button>
        ))}
      </div>

      {submissions.isError ? (
        <p role="alert" className="mt-6 rounded-panel border border-line bg-sheet p-4">
          Could not load the queue. {submissions.error.detail}
        </p>
      ) : submissions.isPending ? (
        <Skeleton className="mt-6 h-48" />
      ) : submissions.data.items.length === 0 ? (
        <p className="mt-6 rounded-panel border border-line bg-sheet p-4">
          Nothing in this queue.
        </p>
      ) : (
        <p className="mt-3 font-mono text-label font-bold uppercase tracking-widest text-ink/70">
          {submissions.data.total} total
        </p>
      )}

      {!submissions.isError && !submissions.isPending && submissions.data.items.length > 0 ? (
        <ul className="mt-3 flex list-none flex-col gap-4">
          {submissions.data.items.map((submission) => {
            const repoUrl = safeExternalUrl(`https://github.com/${submission.repo_owner}/${submission.repo_name}`);
            const submitter = projectOwnerUsername({
              username: submission.submitter,
              avatar_url: submission.submitter_avatar_url,
            });
            return (
              <li
                key={submission.id}
                className="rounded-card border border-line bg-sheet p-5 shadow-soft"
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h2 className="font-display text-[1.0625rem] leading-snug text-ink">
                      {submission.problem_title}
                    </h2>
                    <p className="mt-1 font-mono text-body">
                      {repoUrl ? (
                        <a
                          href={repoUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="text-accent underline underline-offset-4"
                        >
                          {submission.repo_owner}/{submission.repo_name} ↗
                        </a>
                      ) : (
                        `${submission.repo_owner}/${submission.repo_name}`
                      )}
                    </p>
                    <p className="mt-1 text-body">
                      by {submitter ?? submission.submitter}
                      {submission.demo_url ? ' · has demo link' : ''}
                      {submission.open_for_contributors ? ' · open to contributors' : ''}
                    </p>
                  </div>
                  <div className="flex shrink-0 flex-wrap flex-col items-end gap-1">
                    {submission.ownership_basis ? (
                      <OwnershipTag basis={submission.ownership_basis} />
                    ) : null}
                    {submission.relevance_score != null ? (
                      <Tag>{`relevance ${submission.relevance_score.toFixed(2)}`}</Tag>
                    ) : null}
                    {submission.report_count > 0 ? (
                      <Tag>{`${submission.report_count} report${submission.report_count === 1 ? '' : 's'}`}</Tag>
                    ) : null}
                  </div>
                </div>

                {submission.solution_summary ? (
                  <p className="mt-3 border-l-2 border-line pl-3 text-body leading-snug">
                    {submission.solution_summary}
                  </p>
                ) : null}
                {submission.relevance_reason ? (
                  <p className={`${sectionHeading} mt-3`}>
                    LLM: {submission.relevance_reason}
                  </p>
                ) : null}

                {statusFilter === 'needs_review' ? (
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Button onClick={() => runApprove(submission.id)}>
                      Approve
                    </Button>
                    <Button
                      variant="secondary"
                      className="text-danger hover:border-danger/40 hover:text-danger"
                      onClick={() => runReject(submission.id)}
                    >
                      Reject
                    </Button>
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
      ) : null}

      <p className="mt-8">
        <Link
          to="/problems"
          className="inline-flex rounded-full border border-line bg-sheet px-4 py-2.5 text-[0.8125rem] font-semibold text-ink hover:border-ink/25"
        >
          Back to the board
        </Link>
      </p>
    </main>
  );
}

const buttonClass =
  'rounded-full border border-line px-3.5 py-1.5 text-[0.8125rem] font-semibold text-ink hover:border-ink/25 hover:bg-tint/60';
