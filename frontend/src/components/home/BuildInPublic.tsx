import type { ProjectOut } from '@/api/client';
import { Stamp } from '@/design/primitives';
import { useProject } from '@/hooks/useProject';
import { Link } from 'react-router-dom';

const STATUS_TONE = {
  active: 'active',
  stale: 'stale',
  not_started: 'not-started',
} as const;

function SegmentedMeter({ commits }: { commits: number }) {
  const filled = Math.min(10, Math.max(commits > 0 ? 1 : 0, Math.round(commits / 2)));
  return (
    <div role="img" aria-label={`${commits} commits`} className="flex gap-1">
      {Array.from({ length: 10 }, (_, index) => (
        <span
          key={index}
          className={`block size-3 border ${
            index < filled ? 'border-ink bg-ink' : 'border-line bg-transparent'
          }`}
        />
      ))}
    </div>
  );
}

function ProgressPanel({ project }: { project: ProjectOut }) {
  const progress = project.progress;

  return (
    <div className="border border-ink bg-paper p-5 text-ink">
      <div className="flex items-start justify-between gap-3 border-b border-line pb-3">
        <div>
          <p className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
            {project.repo_owner} / {project.repo_name}
          </p>
          <p className="mt-1 text-sm font-semibold">{project.problem_title}</p>
        </div>
        {progress ? <Stamp tone={STATUS_TONE[progress.status]} /> : null}
      </div>

      {progress ? (
        <div className="mt-4 flex flex-col gap-3">
          <SegmentedMeter commits={progress.commit_count} />
          <div className="flex flex-wrap gap-x-5 gap-y-1 font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
            <span>{progress.commit_count} commits</span>
            <span>README {progress.has_readme ? '✓' : '□'}</span>
            <span>
              Last commit{' '}
              {progress.last_commit_at
                ? new Date(progress.last_commit_at).toLocaleDateString('en-CA')
                : 'never'}
            </span>
          </div>
        </div>
      ) : (
        <p className="mt-4 font-mono text-[10px] uppercase tracking-[0.14em] text-muted">
          No progress tracked yet.
        </p>
      )}
    </div>
  );
}

export function BuildInPublic() {
  const query = useProject(1);

  return (
    <section className="border-b border-ink bg-olive text-paper">
      <div className="mx-auto grid w-[min(1240px,96vw)] items-center gap-10 py-14 md:grid-cols-2">
        <div className="flex flex-col items-start gap-4">
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/60">
            02 / Public record
          </p>
          <h2 className="font-display text-3xl uppercase leading-[0.92] tracking-tight md:text-4xl">
            Link a repo.
            <br />
            <span className="text-accent-soft">MANABI tracks it.</span>
          </h2>
          <p className="max-w-md text-sm leading-relaxed text-paper/80">
            Commits, README, and good-first-issues update themselves. Visitors
            see proof of work, not a claim of it.
          </p>
          <Link to="/problems" className="mt-2 inline-flex border border-paper bg-accent px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-paper transition-colors hover:border-accent hover:bg-paper hover:text-ink">
            Claim a problem
          </Link>
        </div>

        <div>
          {query.isLoading ? (
            <div className="skeleton h-56 border border-paper/40" aria-hidden />
          ) : query.data ? (
            <ProgressPanel project={query.data} />
          ) : (
            <p className="border border-paper/40 p-4 font-mono text-[10px] uppercase tracking-[0.14em]">
              Progress panel loads when the projects API is up.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
