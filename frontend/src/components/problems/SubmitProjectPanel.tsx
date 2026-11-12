import { useEffect, useRef, useState, type ChangeEvent, type FormEvent } from 'react';
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
import { GITHUB_REPO_URL_PATTERN, stripGitSuffix } from '@/lib/repoUrl';
import { SOLUTION_SUMMARY_MAX } from '@/lib/limits';
import { SubmittingCard } from './SubmittingCard';
import { RetryCountdown } from '@/components/common/RetryCountdown';

const panelHeading =
  'font-mono text-label font-bold uppercase tracking-widest';
const invalidReason =
  'Use a GitHub repo URL like https://github.com/owner/name';

const ERROR_MESSAGES: Record<string, string> = {
  invalid_repo_url: 'Use a GitHub repo URL like https://github.com/owner/name.',
  invalid_summary: 'Keep the description to at most 400 characters.',
  invalid_demo_url: 'The deployed link must be a plain http(s) URL, at most 500 characters.',
  repo_not_found: 'Repository not found on GitHub or not public.',
  fork_not_allowed: 'This is a fork. Submit the original repo you built the solution in.',
  repo_not_available: 'This repository is archived or disabled and cannot accept submissions.',
  not_repo_owner: 'You can only submit repositories you own',
  github_rate_limited: 'GitHub rate limit reached. Try again in a few minutes.',
  github_unavailable: 'GitHub is not reachable right now. Try again shortly.',
  not_relevant: 'Your project was rejected by the automatic relevance check. The reasons below explain everything that can cause a rejection.',
  readme_required: 'Your project was rejected: the repository has no README. Add one that explains the project, then submit again.',
  too_few_commits: 'Your project was rejected: the repository does not have enough commit history yet.',
  already_submitted: 'You already linked this repository to this problem.',
  repo_already_used: 'This repository is already linked to another problem.',
  repo_already_used_other_problem: 'This repository is already linked to another problem.',
  rate_limited: 'Too many submissions this hour. Try again later.',
};

function errorMessageFor(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 429) {
      // The backend's 429 message already says when to come back.
      return error.detail || 'Too many attempts. Wait a bit before trying again.';
    }
    if (error.code && ERROR_MESSAGES[error.code]) return ERROR_MESSAGES[error.code];
    return error.detail;
  }
  return 'Something went wrong while submitting. Try again.';
}

function rejectReasons(error: unknown): string[] {
  if (error instanceof ApiError && error.payload && typeof error.payload === 'object') {
    const detail = (error.payload as { detail?: unknown }).detail;
    if (detail && typeof detail === 'object') {
      const candidates = (detail as { reasons?: unknown }).reasons;
      if (Array.isArray(candidates)) {
        return candidates.filter((reason): reason is string => typeof reason === 'string');
      }
    }
  }
  return [];
}

function statusLabel(status: ProjectOut['verification_status']): string {
  switch (status) {
    case 'verified':
      return 'Verified against the problem. It is now public.';
    case 'needs_review':
      return 'Submitted. It is awaiting review and will go public once the check confirms it.';
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
  const [demoUrl, setDemoUrl] = useState('');
  const [openForContributors, setOpenForContributors] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitRetryAfter, setSubmitRetryAfter] = useState<number | null>(null);
  const [submitReasons, setSubmitReasons] = useState<string[]>([]);
  const [submitted, setSubmitted] = useState<ProjectOut | null>(null);

  const submit = useSubmitProject(problemId);

  // On narrow screens the panel sits below the whole brief, so a rejection
  // would otherwise sit at the very bottom out of view. Pull the panel back
  // into sight as soon as a result lands (and while the checks run).
  const panelRef = useRef<HTMLElement | null>(null);
  const scrollToPanel = () =>
    panelRef.current?.scrollIntoView?.({ behavior: 'smooth', block: 'center' });
  useEffect(() => {
    if (submit.isPending) scrollToPanel();
  }, [submit.isPending]);
  useEffect(() => {
    if (submitError) scrollToPanel();
  }, [submitError]);
  useEffect(() => {
    if (submitted) scrollToPanel();
  }, [submitted]);

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
        <p className="text-body leading-snug">
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

  function handleDemoUrlChange(event: ChangeEvent<HTMLInputElement>) {
    setDemoUrl(event.target.value);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitError(null);
    setSubmitReasons([]);

    const normalized = stripGitSuffix(
      repoUrl.trim().replace(/\/+$/, ''),
    );
    if (!GITHUB_REPO_URL_PATTERN.test(normalized)) {
      setValidationError(invalidReason);
      return;
    }
    const demo = demoUrl.trim();
    if (demo && !/^https?:\/\/\S+$/i.test(demo)) {
      setValidationError('The deployed link must start with http:// or https://');
      return;
    }

    setValidationError(null);
    setSubmitError(null);
    setSubmitRetryAfter(null);
    submit.mutate(
      {
        repo_url: normalized,
        solution_summary: summary.trim() ? summary.trim() : undefined,
        demo_url: demo ? demo : undefined,
        open_for_contributors: openForContributors,
      },
      {
        onSuccess: (project) => {
          setSubmitted(project);
          setRepoUrl('');
          setSummary('');
          setDemoUrl('');
          setOpenForContributors(false);
          toast('Submission received.');
        },
        onError: (error) => {
          setSubmitError(errorMessageFor(error));
          setSubmitReasons(rejectReasons(error));
          setSubmitRetryAfter(
            error instanceof ApiError ? error.retryAfterSeconds : null,
          );
        },
      },
    );
  }

  if (submitted) {
    return (
      <aside ref={panelRef} className="flex flex-col gap-3 rounded-card border border-line bg-sheet p-5 shadow-soft">
        <h2 className={panelHeading}>Submitted</h2>
        <p className="text-body leading-snug">{statusLabel(submitted.verification_status)}</p>
        <p className="text-body leading-snug">
          Your repository has been added to the problem board with a progress badge.
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
    <aside
      ref={panelRef}
      className="flex flex-col gap-3 rounded-card border border-line bg-sheet p-5 shadow-soft"
    >
      <h2 className={panelHeading}>Submit a project</h2>
      {submit.isPending ? (
        <SubmittingCard />
      ) : (
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
          Description (optional)
          <span
            className={cx(
              'normal-case tracking-normal',
              summary.trim().length > SOLUTION_SUMMARY_MAX ? 'text-danger' : 'text-ink/40',
            )}
          >
            {summary.trim().length}/{SOLUTION_SUMMARY_MAX}
          </span>
        </label>
        <textarea
          id="solution-summary"
          value={summary}
          onChange={handleSummaryChange}
          rows={5}
          maxLength={SOLUTION_SUMMARY_MAX}
          className="field w-full"
        />
        <Input
          label="Deployed link (optional)"
          type="url"
          placeholder="https://your-project.example.com"
          value={demoUrl}
          onChange={handleDemoUrlChange}
        />
        <label className="flex items-center gap-2 text-body">
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
            className="font-mono text-label font-bold uppercase tracking-widest text-danger"
          >
            {validationError}
          </p>
        ) : null}
        {submitError ? (
          <div
            role="alert"
            className="flex flex-col gap-2 rounded-panel border border-danger/40 bg-danger-soft p-3.5"
          >
            <p className="font-mono text-label font-bold uppercase tracking-widest text-danger">
              {submitReasons.length > 0 ? 'Your project was rejected' : 'Submission failed'}
            </p>
            <p className="text-body leading-snug">{submitError}</p>
            {submitRetryAfter != null ? (
              <RetryCountdown seconds={submitRetryAfter} />
            ) : null}
            {submitReasons.length > 0 ? (
              <div className="flex flex-col gap-1.5">
                <p className="font-mono text-label uppercase tracking-widest text-ink-soft">
                  Why this can happen
                </p>
                <ul className="flex list-disc flex-col gap-1.5 pl-5 text-body leading-snug">
                  {submitReasons.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        ) : null}
        <button
          type="submit"
          disabled={submit.isPending}
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          Submit project
        </button>
      </form>
      )}
    </aside>
  );
}
