import { useState } from 'react';
import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { buttonClasses, Input } from '@/design/primitives';
import { StaticShell } from './StaticShell';

export function RepoAnalyzerPage() {
  const [repoUrl, setRepoUrl] = useState('');
  const [error, setError] = useState<string | undefined>(undefined);

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    const normalized = repoUrl.trim().replace(/\/$/, '');
    if (!/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(normalized)) {
      setError('Enter a valid GitHub repo URL like https://github.com/owner/name');
      return;
    }
    setError(undefined);
  }

  return (
    <StaticShell kicker="Coming soon" title="Repo Analyzer">
      <p className="text-sm leading-relaxed">
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
        {error ? (
          <p
            role="alert"
            className="font-mono text-[11px] font-bold uppercase tracking-widest text-red"
          >
            {error}
          </p>
        ) : null}
        <button
          type="submit"
          disabled
          className={cx(buttonClasses('primary'), 'self-start')}
        >
          Analyze repo
        </button>
      </form>

      <p className="mt-8 text-sm leading-relaxed text-ink/60">
        This tool is being built. In the meantime, browse{' '}
        <Link to="/problems" className="text-blue underline underline-offset-4">
          project ideas
        </Link>{' '}
        and link your own repository from a problem page.
      </p>
    </StaticShell>
  );
}
