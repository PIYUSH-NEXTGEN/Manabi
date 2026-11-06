import { useState, type ChangeEvent, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import {
  buttonClasses,
  Input,
  Skeleton,
  useToast,
} from '@/design/primitives';
import { ApiError, type ProjectOut } from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { useSubmitProject } from '@/hooks/useSubmitProject';

const GITHUB_REPO_URL_PATTERN =
  /^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/;
const panelHeading =
  'font-mono text-xs font-bold uppercase tracking-widest';
const invalidReason =
  'Use a GitHub repo URL like https://github.com/owner/name';
const SUMMARY_MIN = 40;
const SUMMARY_MAX = 800;

const ERROR_MESSAGES: Record<string, string> = {
  invalid_repo_url: 'Use a GitHub repo URL like https://github.com/owner/name.',
  invalid_summary: 'Describe how your project solves the problem in 40–800 characters.',
  repo_not_found: 'Repository not found on GitHub or not public.',
  fork_not_allowed: 'This is a fork — submit the original repo you built the solution in.',
  repo_not_available: 'This repository is archived or disabled and cannot accept submissions.',
  not_repo_owner: 'You can only submit repositories you own or have contributed to.',
  github_rate_limited: 'GitHub rate limit reached — try again in a few minutes.',
  github_unavailable: 'GitHub is not reachable right now — try again shortly.',
  not_relevant: 'Automatic check: this repo does not relate to the problem. You can edit and resubmit if that is wrong.',
  already_submitted: 'You already linked this repository to this problem.',
  repo_already_used: 'This repository is already linked to another problem.',
  repo_already_used_other_problem: 'This repository is already linked to another problem.',
  rate_limited: 'Too many submissions this hour — try again later.',
};

function errorMessageFor(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 429) return 'Too many attempts — wait a bit before trying again.';
    if (error.code && ERROR_MESSAGES[error.code]) return ERROR_MESSAGES[error.code];
    return error.detail;
  }
  return 'Something went wrong while submitting. Try again.';
}

function statusLabel(status: ProjectOut['verification_status']): string {
  switch (status) {
    case 'verified':
      return 'Verified against the problem — it is public.';
    case 'needs_review':
      return 'Submitted — an automatic check is pending human confirmation.';
    case 'rejected':
      return 'Rejected by the automatic relevance check.';
    default:
      return 'Submitted.';
  }
}

export function SubmitProjectPanel({ problemId }: { problemId: number }) {
  const me = useMe();
  const toast = useToast();

  const [repoUrl, setRepoUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [openForContributors, setOpenForContributors] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState<ProjectOut | null>(null);

  const submit = useSubmitProject(problemId);

  if (me.isPending) {
    return (
      <div className="flex flex-col gap-2">
        <Skeleton className="h-3 w-36" />
        <Skeleton className="h-10 w-full" />
      </div>
    );
  }

  if (!me.data) {
    return (
      <aside className="flex flex-col gap-3">
        <h2 className={panelHeading}>Submit a project</h2>
        <p className="text-sm leading-snug">
          Log in with GitHub to claim this problem and submit your repository.
        </p>
        <a
          href="/api/auth/github/login"
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          Log in with GitHub
        </a>
      </aside>
    );
  }

  function handleRepoUrlChange(event: ChangeEvent<HTMLInputElement>) {
    setRepoUrl(event.target.value);
  }

  function handleSummaryChange(event: ChangeEvent<HTMLTextAreaElement>) {
    setSummary(event.target.value);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitError(null);

    const normalized = repoUrl
      .trim()
      .replace(/\/+$/, '')
      .replace(/\.git$/, '');
    if (!GITHUB_REPO_URL_PATTERN.test(normalized)) {
      setValidationError(invalidReason);
      return;
    }
    if (summary.trim().length < SUMMARY_MIN) {
      setValidationError(
        `Add a summary of at least ${SUMMARY_MIN} characters explaining how the repo solves this problem.`,
      );
      return;
    }

    setValidationError(null);
    setSubmitError(null);
    submit.mutate(
      {
        repo_url: normalized,
        solution_summary: summary.trim(),
        open_for_contributors: openForContributors,
      },
      {
        onSuccess: (project) => {
          setSubmitted(project);
          setRepoUrl('');
          setSummary('');
          setOpenForContributors(false);
          toast('Submission received.');
        },
        onError: (error) => {
          setSubmitError(errorMessageFor(error));
        },
      },
    );
  }

  if (submitted) {
    return (
      <aside className="flex flex-col gap-3 border border-ink bg-sheet p-4">
        <h2 className={panelHeading}>Submitted</h2>
        <p className="text-sm leading-snug">{statusLabel(submitted.verification_status)}</p>
        <p className="text-sm leading-snug">
          {submitted.repo_url} is on the board with a progress badge.
        </p>
        <Link
          to={`/projects/${submitted.id}`}
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          Open project page
        </Link>
      </aside>
    );
  }

  return (
    <aside className="flex flex-col gap-3 border border-ink bg-sheet p-4">
      <h2 className={panelHeading}>Submit a project</h2>
      <form
        noValidate
        onSubmit={handleSubmit}
        className="flex flex-col gap-3"
      >
        <Input
          label="GitHub repo URL"
          type="url"
          placeholder="https://github.com/owner/name"
          value={repoUrl}
          onChange={handleRepoUrlChange}
        />
        <label
          htmlFor="solution-summary"
          className={cx(panelHeading, 'flex items-baseline justify-between')}
        >
          How it solves this problem
          <span
            className={cx(
              'normal-case tracking-normal',
              summary.trim().length > SUMMARY_MAX
                ? 'text-danger'
                : summary.trim().length >= SUMMARY_MIN
                  ? 'text-ink/60'
                  : 'text-ink/40',
            )}
          >
            {summary.trim().length}–{SUMMARY_MAX}
          </span>
        </label>
        <textarea
          id="solution-summary"
          value={summary}
          onChange={handleSummaryChange}
          rows={5}
          maxLength={800}
          placeholder={`What the repo does, how it addresses the problem, and where the data comes from (${SUMMARY_MIN}–${SUMMARY_MAX} characters).`}
          className="border border-ink bg-paper px-3 py-2 text-sm"
        />
        <p className="text-[13px] leading-snug text-ink-soft">
          Only the summary and stats are public — your repo README stays yours.
        </p>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={openForContributors}
            onChange={(event) => setOpenForContributors(event.target.checked)}
            className="size-4 accent-[var(--accent)]"
          />
          Open for contributors
        </label>
        {validationError ? (
          <p
            role="alert"
            className="font-mono text-[11px] font-bold uppercase tracking-widest text-danger"
          >
            {validationError}
          </p>
        ) : null}
        {submitError ? (
          <p
            role="alert"
            className="font-mono text-[11px] font-bold uppercase tracking-widest text-danger"
          >
            {submitError}
          </p>
        ) : null}
        <button
          type="submit"
          disabled={submit.isPending}
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          {submit.isPending ? 'Submitting…' : 'Submit project'}
        </button>
      </form>
    </aside>
  );
}
