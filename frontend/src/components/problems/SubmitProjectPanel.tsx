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

export function SubmitProjectPanel({ problemId }: { problemId: number }) {
  const me = useMe();
  const toast = useToast();

  const [repoUrl, setRepoUrl] = useState('');
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

    setValidationError(null);
    setSubmitError(null);
    submit.mutate(
      {
        repo_url: normalized,
        open_for_contributors: openForContributors,
      },
      {
        onSuccess: (project) => {
          setSubmitted(project);
          setRepoUrl('');
          setOpenForContributors(false);
          toast('Project submitted — good luck with those green squares.');
        },
        onError: (error) => {
          setSubmitError(
            error instanceof ApiError
              ? error.detail
              : 'Something went wrong while submitting. Try again.',
          );
        },
      },
    );
  }

  if (submitted) {
    return (
      <aside className="flex flex-col gap-3 border-[3px] border-ink bg-white p-4 shadow-hard">
        <h2 className={panelHeading}>Submitted</h2>
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
    <aside className="flex flex-col gap-3 border-[3px] border-ink bg-white p-4 shadow-hard">
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
          error={validationError ?? undefined}
        />
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={openForContributors}
            onChange={(event) => setOpenForContributors(event.target.checked)}
            className="size-4 accent-blue"
          />
          Open for contributors
        </label>
        {submitError ? (
          <p
            role="alert"
            className="font-mono text-[11px] font-bold uppercase tracking-widest text-red"
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
