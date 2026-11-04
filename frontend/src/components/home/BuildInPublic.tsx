import type { ProjectOut } from '@/api/client';
import { Stamp } from '@/design/primitives';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import { cx } from '@/lib/cx';
import { useProject } from '@/hooks/useProject';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  ArrowUpRight,
  CircleDot,
  FileText,
  GitCommitHorizontal,
} from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';

const STATUS_TONE = {
  active: 'active',
  stale: 'stale',
  not_started: 'not-started',
} as const;

const FEATURES = [
  {
    icon: GitCommitHorizontal,
    title: 'Commits',
    copy: 'Pulled from the repo on every sync.',
  },
  {
    icon: FileText,
    title: 'README',
    copy: 'Checked so the project documents itself.',
  },
  {
    icon: CircleDot,
    title: 'Open issues',
    copy: 'Contributors see where they can help.',
  },
];

function SegmentedMeter({ commits }: { commits: number }) {
  const filled = Math.min(10, Math.max(commits > 0 ? 1 : 0, Math.round(commits / 2)));
  return (
    <div role="img" aria-label={`${commits} commits`} className="flex gap-1">
      {Array.from({ length: 10 }, (_, index) => (
        <motion.span
          key={index}
          initial={{ opacity: 0.2, scaleY: 0.4 }}
          whileInView={{ opacity: 1, scaleY: 1 }}
          viewport={{ once: true }}
          transition={{ delay: index * 0.035, duration: 0.28, ease: EASE_SNAP }}
          className={cx(
            'block h-3 flex-1 border',
            index < filled ? 'border-ink bg-ink' : 'border-line bg-transparent',
          )}
        />
      ))}
    </div>
  );
}

function ProgressPanel({ project }: { project: ProjectOut }) {
  const progress = project.progress;
  const lastCommit = progress?.last_commit_at
    ? new Date(progress.last_commit_at).toLocaleDateString('en-CA')
    : 'never';

  return (
    <div className="border border-paper/25 bg-paper text-ink shadow-[6px_6px_0_0_rgba(23,21,15,0.28)] sm:shadow-[14px_14px_0_0_rgba(23,21,15,0.28)]">
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
          Project record
        </span>
        {progress ? (
          <Stamp tone={STATUS_TONE[progress.status]} />
        ) : (
          <span className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
            No data
          </span>
        )}
      </div>

      <div className="p-5 sm:p-6">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="truncate font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
              {project.repo_owner} / {project.repo_name}
            </p>
            <p className="mt-1 text-sm font-semibold leading-snug">
              {project.problem_title}
            </p>
          </div>
          <span aria-hidden className="mt-1 block size-2.5 shrink-0 bg-accent" />
        </div>

        {progress ? (
          <>
            <div className="mt-5 flex items-end justify-between gap-3 border-t border-line pt-4">
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                Commit activity
              </p>
              <p className="font-display text-3xl leading-none">
                {progress.commit_count}
              </p>
            </div>

            <div className="mt-3">
              <SegmentedMeter commits={progress.commit_count} />
            </div>

            <div className="mt-4 flex flex-wrap gap-x-5 gap-y-1 font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
              <span>README {progress.has_readme ? '✓' : '□'}</span>
              <span>Last commit {lastCommit}</span>
              <span>
                {progress.open_issues.length} open{' '}
                {progress.open_issues.length === 1 ? 'issue' : 'issues'}
              </span>
            </div>
          </>
        ) : (
          <p className="mt-5 border-t border-line pt-3 font-mono text-[10px] uppercase tracking-[0.14em] text-muted">
            No progress tracked yet.
          </p>
        )}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
        <span>Live record</span>
        <span className="flex items-center gap-1.5">
          <GithubMark size={12} />
          Pulled from GitHub
        </span>
      </div>
    </div>
  );
}

export function BuildInPublic() {
  const query = useProject(1);

  return (
    <section className="relative overflow-hidden border-b border-ink bg-olive text-paper">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(90deg, rgba(234,229,219,0.07) 0 1px, transparent 1px 96px)',
        }}
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] py-16 md:py-20">
        <div className="grid items-center gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:gap-16">
          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-paper/25 pb-3">
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/60">
                <span className="text-accent-soft">02</span> / Public record
              </p>
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/45">
                Proof, not promises
              </p>
            </div>

            <h2 className="mt-7 font-display text-4xl uppercase leading-[0.9] tracking-tight sm:text-5xl">
              Link a repo.
              <br />
              <span className="text-accent-soft">MANABI tracks it.</span>
            </h2>
            <p className="mt-5 max-w-md text-sm leading-relaxed text-paper/75">
              Commits, README, and good-first-issues update themselves. Visitors
              see proof of work, not a claim of it.
            </p>

            <ul className="mt-8 grid gap-px border border-paper/25 bg-paper/25 sm:grid-cols-3">
              {FEATURES.map(({ icon: Icon, title, copy }) => (
                <li key={title} className="bg-olive p-4">
                  <Icon
                    aria-hidden
                    size={18}
                    strokeWidth={2.2}
                    className="text-accent-soft"
                  />
                  <h3 className="mt-3 font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
                    {title}
                  </h3>
                  <p className="mt-1.5 text-[13px] leading-snug text-paper/65">
                    {copy}
                  </p>
                </li>
              ))}
            </ul>

            <Link
              to="/problems"
              className="group mt-8 inline-flex items-center gap-2 border border-paper bg-paper px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-ink transition-colors hover:border-accent hover:bg-accent hover:text-paper"
            >
              Claim a problem
              <ArrowUpRight
                aria-hidden
                size={14}
                strokeWidth={2.6}
                className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
              />
            </Link>
          </motion.div>

          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            transition={{ delay: 0.1 }}
          >
            {query.isLoading ? (
              <div className="skeleton h-64 border border-paper/40" aria-hidden />
            ) : query.data ? (
              <ProgressPanel project={query.data} />
            ) : (
              <div className="border border-paper/40 p-5">
                <p className="font-mono text-[10px] font-bold uppercase tracking-[0.14em] text-paper/70">
                  Progress panel loads when the projects API is up.
                </p>
                <Link
                  to="/problems"
                  className="mt-4 inline-flex items-center gap-1.5 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent-soft underline underline-offset-4 hover:text-paper"
                >
                  Browse the index
                  <ArrowUpRight aria-hidden size={12} strokeWidth={2.6} />
                </Link>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
