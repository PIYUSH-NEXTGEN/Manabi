import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { buttonClasses, Stamp } from '@/design';
import { useProject } from '@/hooks/useProject';
import { useStats } from '@/hooks/useStats';
import { CountUp } from './CountUp';

const STATUS_TONE = {
  active: 'active',
  stale: 'stale',
  not_started: 'not-started',
} as const;

function CommitMeter({ commits }: { commits: number }) {
  const filled = Math.min(10, Math.max(commits > 0 ? 1 : 0, Math.round(commits / 2)));
  return (
    <div role="img" aria-label={`${commits} commits`} className="mt-2 flex gap-1">
      {Array.from({ length: 10 }, (_, index) => (
        <span
          key={index}
          className={`block h-2.5 flex-1 border ${
            index < filled ? 'border-ink bg-ink' : 'border-line bg-transparent'
          }`}
        />
      ))}
    </div>
  );
}

function ProjectRecord() {
  const query = useProject(1);
  const project = query.data;
  const progress = project?.progress;

  return (
    <figure className="border border-ink bg-sheet">
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
          Project record
        </span>
        {progress ? (
          <Stamp tone={STATUS_TONE[progress.status]} />
        ) : (
          <span className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
            {query.isLoading ? 'Syncing' : 'No data'}
          </span>
        )}
      </div>

      <div className="p-5 sm:p-6">
        {query.isLoading ? (
          <div className="space-y-3" aria-busy="true">
            <div className="skeleton h-2.5 w-20" />
            <div className="skeleton h-8 w-3/4" />
            <div className="skeleton h-3 w-1/2" />
            <div className="skeleton mt-6 h-16 w-full" />
          </div>
        ) : project ? (
          <>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-muted">
              Repository
            </p>
            <p className="mt-2 break-words font-display text-3xl uppercase leading-[0.95] tracking-tight sm:text-4xl">
              {project.repo_name}
            </p>
            <p className="mt-1 font-mono text-[10px] font-bold uppercase tracking-[0.14em] text-muted">
              {project.repo_owner}
            </p>
            <p className="mt-4 text-sm leading-snug text-ink-soft">
              {project.problem_title}
            </p>

            {progress ? (
              <>
                <div className="mt-6 border-t border-ink pt-4">
                  <div className="flex items-baseline justify-between gap-3 font-mono text-[9px] font-bold uppercase tracking-[0.16em]">
                    <span className="text-muted">Commit activity</span>
                    <span>{progress.commit_count} commits</span>
                  </div>
                  <CommitMeter commits={progress.commit_count} />
                </div>

                <dl className="mt-5 grid grid-cols-2 border-t border-line">
                  <div className="border-b border-r border-line py-3 pr-3">
                    <dt className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                      README
                    </dt>
                    <dd className="mt-1 font-mono text-[11px] font-bold uppercase tracking-[0.1em]">
                      {progress.has_readme ? 'Present' : 'Missing'}
                    </dd>
                  </div>
                  <div className="border-b border-line py-3 pl-3">
                    <dt className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                      Open issues
                    </dt>
                    <dd className="mt-1 font-mono text-[11px] font-bold uppercase tracking-[0.1em]">
                      {progress.open_issues.length}
                    </dd>
                  </div>
                  <div className="border-r border-line py-3 pr-3">
                    <dt className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                      Last commit
                    </dt>
                    <dd className="mt-1 font-mono text-[11px] font-bold uppercase tracking-[0.1em]">
                      {progress.last_commit_at
                        ? new Date(progress.last_commit_at).toLocaleDateString('en-CA')
                        : 'Never'}
                    </dd>
                  </div>
                  <div className="py-3 pl-3">
                    <dt className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                      Access
                    </dt>
                    <dd className="mt-1 font-mono text-[11px] font-bold uppercase tracking-[0.1em]">
                      {project.open_for_contributors ? 'Open' : 'Solo'}
                    </dd>
                  </div>
                </dl>
              </>
            ) : (
              <p className="mt-5 border-t border-line pt-3 font-mono text-[10px] uppercase tracking-[0.14em] text-muted">
                No progress tracked yet.
              </p>
            )}

            <div className="mt-5 flex items-end justify-between gap-4 border-t border-line pt-4">
              <Link
                to={`/projects/${project.id}`}
                className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent underline decoration-accent/40 underline-offset-4 hover:text-ink"
              >
                Open project →
              </Link>
              <span aria-hidden className="barcode h-7 w-24 opacity-80" />
              <span aria-hidden className="block size-7 bg-accent" />
            </div>
          </>
        ) : (
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-muted">
              Repository
            </p>
            <p className="mt-2 font-display text-2xl uppercase leading-tight">
              Record unavailable
            </p>
            <p className="mt-3 text-sm leading-snug text-ink-soft">
              The projects API did not respond. Browse the archive while it
              comes back online.
            </p>
            <Link
              to="/problems"
              className="mt-5 inline-block border border-ink px-4 py-2 font-mono text-[10px] font-bold uppercase tracking-[0.16em] transition-colors hover:bg-ink hover:text-paper"
            >
              Browse problems
            </Link>
          </div>
        )}
      </div>

      <figcaption className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
        <span>Live record</span>
        <span>Pulled from GitHub</span>
      </figcaption>
    </figure>
  );
}

export function Hero() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = query.trim();
    navigate(trimmed ? `/problems?q=${encodeURIComponent(trimmed)}` : '/problems');
  }

  return (
    <section className="border-b border-ink bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid items-start gap-12 py-10 md:grid-cols-[1.12fr_0.88fr] md:gap-14 md:py-14">
          <div>
            <h1
              className="font-display uppercase leading-[0.82] tracking-[-0.035em]"
              style={{ fontSize: 'clamp(4rem, 11vw, 8.5rem)' }}
            >
              MANABI
            </h1>
            <p className="mt-5 max-w-xl font-display text-xl uppercase leading-[0.95] tracking-tight sm:text-2xl">
              Real problems.
              <span className="text-accent"> Real sources.</span>
            </p>

            <p className="mt-5 max-w-xl text-base leading-relaxed text-ink-soft sm:text-lg">
              A working archive of problem briefs published by real
              organisations — every record links back to its official source.
              Search it, open a brief, and start building; link a repo and
              MANABI tracks the commits.
            </p>

            <form
              role="search"
              noValidate
              onSubmit={handleSubmit}
              className="mt-7 flex w-full max-w-xl flex-col gap-3 sm:flex-row"
            >
              <label htmlFor="hero-search" className="sr-only">
                Search problem briefs
              </label>
              <input
                id="hero-search"
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search problems — leaf blight, SLAs…"
                className="field min-w-0 flex-1"
              />
              <button type="submit" className={buttonClasses('primary', 'shrink-0')}>
                Browse projects
              </button>
            </form>

            <dl className="mt-9 max-w-xl border-t border-ink">
              <div className="py-4">
                <dt className="font-mono text-[9px] font-bold uppercase leading-relaxed tracking-[0.16em] text-muted">
                  Problem briefs indexed
                </dt>
                <dd className="mt-1 font-display text-4xl leading-none text-accent md:text-5xl">
                  <StatsNumber />
                </dd>
              </div>
            </dl>
          </div>

          <ProjectRecord />
        </div>
      </div>
    </section>
  );
}

function StatsNumber() {
  const stats = useStats();
  if (!stats.data) {
    return <span aria-hidden>—</span>;
  }
  return <CountUp value={stats.data.problems} />;
}
