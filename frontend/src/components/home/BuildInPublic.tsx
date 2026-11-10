import { useQuery } from '@tanstack/react-query';
import type { ProjectOut } from '@/api/client';
import { getProblem, getProblems } from '@/api/client';
import { Stamp } from '@/design/primitives';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import { cx } from '@/lib/cx';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  ArrowUpRight,
  BrainCircuit,
  FileText,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { PROGRESS_STAMPS } from '@/design/status';
import { VerificationConsole } from './VerificationConsole';

const STEPS = [
  {
    step: '01',
    icon: ShieldCheck,
    title: 'Your own repo',
    copy: 'A public GitHub repo you own. Forks and other people’s repos don’t count.',
  },
  {
    step: '02',
    icon: FileText,
    title: 'README + 5 commits',
    copy: 'Your repo needs a README and at least 5 commits.',
  },
  {
    step: '03',
    icon: BrainCircuit,
    title: 'AI checks relevance',
    copy: 'AI reads your README and checks it matches the brief.',
  },
  {
    step: '04',
    icon: RefreshCw,
    title: 'Tracked after approval',
    copy: 'Commits, README and open issues update from GitHub.',
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
          <Stamp tone={PROGRESS_STAMPS[progress.status].tone} />
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

/**
 * Find a real project record to show in the panel without a hard-coded id:
 * the board's first problem that has any public project, then that problem's
 * detail (which embeds the projects). Prefers a record that already carries
 * GitHub progress so the meter has data to render.
 */
function useShowcaseProject() {
  const problems = useQuery({
    queryKey: ['problems', 'showcase'],
    queryFn: () => getProblems({ limit: 20 }),
  });

  const candidate = problems.data?.items.find((p) => p.project_count > 0);
  const detail = useQuery({
    queryKey: ['problem', 'showcase', candidate?.id],
    queryFn: () => getProblem(candidate!.id),
    enabled: candidate != null,
  });

  const projects = detail.data?.projects ?? [];
  const project =
    projects.find((p) => p.progress != null) ?? projects[0] ?? null;

  return {
    isLoading: problems.isLoading || (candidate != null && detail.isLoading),
    isError: problems.isError || (candidate != null && detail.isError),
    project,
  };
}

export function BuildInPublic() {
  const query = useShowcaseProject();

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
                <span className="text-accent-soft">02</span> / Submission
              </p>
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/45">
                Checked, not claimed
              </p>
            </div>

            <h2 className="mt-7 font-display text-4xl uppercase leading-[0.9] tracking-tight sm:text-5xl">
              Submit a repo.
              <br />
              <span className="text-accent-soft">We check the work.</span>
            </h2>
            <p className="mt-5 max-w-md text-sm leading-relaxed text-paper/75">
              Every project is checked before it goes public: your own repo, a
              README, real commits, then an AI relevance check. Only what passes
              gets tracked.
            </p>

            <ul className="mt-8 grid gap-px border border-paper/25 bg-paper/25 sm:grid-cols-2">
              {STEPS.map(({ step, icon: Icon, title, copy }) => (
                <li key={step} className="bg-olive p-4">
                  <div className="flex items-center justify-between gap-2">
                    <Icon
                      aria-hidden
                      size={18}
                      strokeWidth={2.2}
                      className="text-accent-soft"
                    />
                    <span className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/35">
                      {step}
                    </span>
                  </div>
                  <h3 className="mt-3 font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
                    {title}
                  </h3>
                  <p className="mt-1.5 text-[13px] leading-snug text-paper/65">
                    {copy}
                  </p>
                </li>
              ))}
            </ul>

            <p className="mt-4 border-l-2 border-accent-soft/60 pl-3 text-[12px] leading-relaxed text-paper/60">
              If the AI can’t judge, a keyword check takes over. It can send work
              to human review, but never mark it verified.
            </p>

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
            <div className="flex flex-col gap-5">
              <VerificationConsole />
              {query.isLoading ? (
                <div className="skeleton h-52 border border-paper/40" aria-hidden />
              ) : query.project ? (
                <ProgressPanel project={query.project} />
              ) : query.isError ? (
                <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/45">
                  Live example unavailable — the projects API is down.
                </p>
              ) : null}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
