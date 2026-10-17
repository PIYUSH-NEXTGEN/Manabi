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
    <div
      role="img"
      aria-label={`${commits} commits`}
      className="flex gap-1"
    >
      {Array.from({ length: 10 }, (_, index) => (
        <span
          key={index}
          className={`block size-3.5 border-[2px] border-ink ${
            index < filled ? 'bg-ink' : 'bg-white'
          }`}
        />
      ))}
    </div>
  );
}

function ProgressPanel({ project }: { project: ProjectOut }) {
  const progress = project.progress;

  return (
    <div className="border-[3px] border-ink bg-white p-5 text-ink shadow-hard-lg">
      <div className="flex items-start justify-between gap-3 border-b-[3px] border-ink pb-3">
        <div>
          <p className="font-mono text-[11px] font-bold uppercase tracking-widest">
            {project.repo_owner} / {project.repo_name}
          </p>
          <p className="mt-1 text-sm font-semibold">{project.problem_title}</p>
        </div>
        {progress ? <Stamp tone={STATUS_TONE[progress.status]} /> : null}
      </div>

      {progress ? (
        <div className="mt-4 flex flex-col gap-3">
          <SegmentedMeter commits={progress.commit_count} />
          <div className="flex flex-wrap gap-x-5 gap-y-1 font-mono text-[11px] font-bold uppercase tracking-widest">
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
        <p className="mt-4 font-mono text-[11px] uppercase tracking-widest">
          No progress tracked yet.
        </p>
      )}
    </div>
  );
}

export function BuildInPublic() {
  const query = useProject(1);

  return (
    <section className="border-b-[3px] border-ink bg-red text-white">
      <div className="mx-auto grid w-[min(1200px,96vw)] items-center gap-10 py-12 md:grid-cols-2">
        <div className="flex flex-col items-start gap-4">
          <p className="font-mono text-xs font-bold uppercase tracking-widest">
            Build in public
          </p>
          <h2 className="font-display text-3xl uppercase leading-none md:text-4xl">
            Link a repo. <span className="text-yellow">MANABI tracks it.</span>
          </h2>
          <p className="max-w-md text-sm leading-snug">
            Commits, README, and good-first-issues update themselves. Visitors
            see proof of work, not a claim of it.
          </p>
          <Link
            to="/problems"
            className="inline-flex items-center gap-2 border-[3px] border-ink bg-yellow px-5 py-2.5 font-mono text-xs font-bold uppercase tracking-widest text-ink shadow-hard press"
          >
            Claim a problem
          </Link>
        </div>

        <div>
          {query.isLoading ? (
            <div className="skeleton h-56 border-[3px] border-ink" aria-hidden />
          ) : query.data ? (
            <ProgressPanel project={query.data} />
          ) : (
            <p className="border-[3px] border-ink bg-white p-4 font-mono text-[11px] uppercase tracking-widest text-ink">
              Progress panel loads when the projects API is up.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
