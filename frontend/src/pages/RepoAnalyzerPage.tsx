import { useState } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { GITHUB_REPO_URL_PATTERN } from '@/lib/repoUrl';
import { buttonClasses, Input } from '@/design/primitives';
import { StaticShell } from './StaticShell';

export function RepoAnalyzerPage() {
  const [repoUrl, setRepoUrl] = useState('');
  const [error, setError] = useState<string | undefined>(undefined);

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    const normalized = repoUrl.trim().replace(/\/$/, '');
    if (!GITHUB_REPO_URL_PATTERN.test(normalized)) {
      setError('Enter a valid GitHub repo URL like https://github.com/owner/name');
    }
  }

  return (
    <StaticShell kicker="Coming soon" title="Repo Analyzer">
      <div className="flex flex-wrap items-center gap-2">
        <span className="rounded-full bg-accent-soft px-2.5 py-1 font-mono text-label font-bold uppercase tracking-[0.1em] text-accent">
          Preview · not active yet
        </span>
      </div>

      <p className="text-body leading-relaxed">
        Paste a public GitHub repository link and MANABI will scan it for open
        pull requests, API endpoints, dependencies, and project structure so you
        can see at a glance what is inside before you start building.
      </p>

      <form
        noValidate
        onSubmit={handleSubmit}
        className="mt-6 flex flex-col gap-3"
      >
        <Input
          label="GitHub repo URL"
          type="url"
          placeholder="https://github.com/owner/name"
          value={repoUrl}
          onChange={(event) => setRepoUrl(event.target.value)}
          error={error}
        />
        <button
          type="submit"
          disabled
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          Analyze repo
        </button>
      </form>

      <p className="mt-8 border-t border-line pt-5 text-body leading-relaxed text-ink-soft">
        This tool is being built. In the meantime, browse{' '}
        <Link to="/problems" className="text-accent underline underline-offset-4">
          project ideas
        </Link>{' '}
        and link your own repository from a problem page.
      </p>
    </StaticShell>
  );
}
