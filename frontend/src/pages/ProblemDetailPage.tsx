import type { ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  GitBranch,
} from 'lucide-react';
import { cx } from '@/lib/cx';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import { buttonClasses, Skeleton, Tag } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import { SubmitProjectPanel } from '@/components/problems/SubmitProjectPanel';
import { GithubMark } from '@/components/icons/GithubMark';
import { useProblem } from '@/hooks/useProblem';
import { projectOwnerUsername } from '@/api/client';

const panelHeading = 'font-mono text-[10px] font-bold uppercase tracking-[0.18em]';
const microLabel = 'font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted';

function ProjectSkeleton() {
  return (
    <div className="mx-auto w-[min(1240px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-16 w-2/3" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

function futureIdeas(originalText: string | null | undefined): string[] {
  if (!originalText) return [];
  const section = originalText.match(
    /## (Possible future improvements|Stretch goals)[\s\S]*?(?=\n## |$)/i,
  );
  if (!section) return [];
  return section[0]
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('-'))
    .map((line) => line.slice(1).trim())
    .filter(Boolean);
}

function fullDescription(summary: string, whoAffected: string, whyMatters: string): string {
  return `${summary} This project is for ${whoAffected.toLowerCase()}. ${whyMatters}`;
}

function Section({
  number,
  title,
  children,
}: {
  number: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <motion.section
      variants={slideUpReveal}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.2 }}
      className="border-t border-ink py-8 first:border-t-0 first:pt-0"
    >
      <div className="flex items-baseline gap-3">
        <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
          {number}
        </span>
        <h2 className={panelHeading}>{title}</h2>
      </div>
      <div className="mt-4">{children}</div>
    </motion.section>
  );
}

function SpecRow({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-t border-line py-2.5 first:border-t-0">
      <dt className={microLabel}>{label}</dt>
      <dd className="text-right font-mono text-[10px] font-bold uppercase tracking-widest">
        {children}
      </dd>
    </div>
  );
}

export function ProblemDetailPage() {
  const { id } = useParams();
  const problemId = Number(id);

  if (!Number.isInteger(problemId) || problemId <= 0) {
    return <NotFoundPage />;
  }

  return <DetailView problemId={problemId} />;
}

function DetailView({ problemId }: { problemId: number }) {
  const problem = useProblem(problemId);

  if (problem.isPending) {
    return (
      <main className="border-b border-ink bg-paper">
        <ProjectSkeleton />
      </main>
    );
  }

  if (problem.isError) {
    if (problem.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <main className="border-b border-ink">
        <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
          <h1 className="font-display text-3xl uppercase">
            Could not load this problem
          </h1>
          <p>{problem.error.message}</p>
          <Link to="/problems" className="font-mono text-xs font-bold underline">
            Back to the board
          </Link>
        </div>
      </main>
    );
  }

  const data = problem.data;
  const ideas = futureIdeas(data.original_text);
  const description = fullDescription(data.summary, data.who_affected, data.why_matters);
  const projectCount = data.project_count ?? data.projects.length;
  const completedCount = data.completed_count ?? 0;
  const buildingCount = projectCount - completedCount;

  return (
    <main className="border-b border-ink bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-8 md:py-10">
        <motion.header
          variants={slideUpReveal}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.35, ease: EASE_SNAP }}
          className="grid gap-8 border-b border-ink py-9 md:grid-cols-[minmax(0,1fr)_290px] md:gap-12"
        >
          <div>
            <p className="flex flex-wrap items-center gap-2 font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-accent">
              <span aria-hidden className="block size-2 bg-accent" />
              Problem brief / {data.source_id ?? `NO. ${data.id}`}
            </p>
            <h1
              className="mt-4 font-display uppercase leading-[0.9] tracking-[-0.02em]"
              style={{ fontSize: 'clamp(2.25rem, 5vw, 4rem)' }}
            >
              {data.title}
            </h1>

            <p className="mt-6 max-w-3xl border-l-2 border-accent/50 pl-5 text-base leading-relaxed text-ink-soft md:text-lg">
              {description}
            </p>

            <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
              <span className="flex items-center gap-1.5">
                <GitBranch aria-hidden size={12} strokeWidth={2.4} />
                {buildingCount === 1
                  ? `1 building${completedCount === 1 ? ' · 1 completed' : ''}`
                  : `${buildingCount} building${completedCount > 0 ? ` · ${completedCount} completed` : ''}`}
              </span>
            </div>
          </div>

          <dl className="self-start border border-ink bg-sheet px-4 py-3">
            <div className="flex items-center justify-between border-b border-line pb-2.5">
              <dt className={microLabel}>File no.</dt>
              <dd className="font-mono text-sm font-bold tracking-[0.08em]">
                M-{String(data.id).padStart(3, '0')}
              </dd>
            </div>
            <SpecRow label="Field">{data.field.replace(/-/g, ' ')}</SpecRow>
            <SpecRow label="Domain">{data.domain.replace(/-/g, ' ')}</SpecRow>
            <SpecRow label="Difficulty">{data.difficulty}</SpecRow>
          </dl>
        </motion.header>

        <div className="mt-10 grid gap-12 lg:grid-cols-[minmax(0,1fr)_320px] lg:gap-16">
          <article>
            <Section number="01" title="Why it matters">
              <p className="max-w-3xl border-l-2 border-line pl-5 text-base leading-relaxed text-ink-soft">
                {data.why_matters}
              </p>

            </Section>

            <Section number="02" title="Tech stack">
              <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                The stack below is a starting point, not a rule. If it lists a
                backend language you can swap it for another one - Python or Go,
                for example - and the same goes for the database, frontend, and
                anything else. Use what fits you.
              </p>
              {data.tech_tags.length > 0 ? (
                <div className="mt-4 flex flex-wrap gap-1.5">
                  {data.tech_tags.map((tag) => (
                    <Tag key={tag}>{tag}</Tag>
                  ))}
                </div>
              ) : (
                <p className="mt-3 text-sm">No stack listed.</p>
              )}
            </Section>

            <Section number="03" title="What you can add later">
              {ideas.length > 0 ? (
                <ul className="max-w-3xl space-y-2 text-sm leading-relaxed text-ink-soft">
                  {ideas.map((idea) => (
                    <li key={idea} className="flex gap-3">
                      <span aria-hidden className="mt-2 block size-1.5 shrink-0 bg-accent" />
                      {idea}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                  Ship the MVP first, then add whatever matters to you. Build
                  what you want to learn and ship it.
                </p>
              )}
            </Section>

            <motion.section
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.2 }}
              className="mt-2 flex flex-wrap items-center justify-between gap-5 border border-ink bg-sheet p-5 sm:p-6"
            >
              <div className="max-w-md">
                <p className={cx(microLabel, 'flex items-center gap-2')}>
                  <BookOpen aria-hidden size={12} strokeWidth={2.4} className="text-accent" />
                  Field manual
                </p>
                <h2 className={cx(panelHeading, 'mt-2')}>Three phases to ship</h2>
                <p className="mt-2 text-sm leading-relaxed text-ink-soft">
                  Start, implement, ship. The approaches above become your
                  checklist, with a place to stop at each phase.
                </p>
              </div>
              <Link
                to={`/problems/${data.id}/guide`}
                className={buttonClasses('primary', 'group shrink-0')}
              >
                Build guide
                <ArrowRight
                  aria-hidden
                  size={14}
                  strokeWidth={2.6}
                  className="transition-transform group-hover:translate-x-0.5"
                />
              </Link>
            </motion.section>
          </article>

          <aside className="flex flex-col gap-9 lg:sticky lg:top-24 lg:self-start">
            <SubmitProjectPanel problemId={data.id} />

            <section>
              <h2 className={cx(panelHeading, 'border-b border-ink pb-2')}>
                Projects in the wild
                {buildingCount === 1 && completedCount === 0
                  ? ' (1)'
                  : ` (${buildingCount} building${
                      completedCount > 0 ? ` · ${completedCount} completed` : ''
                    })`}
              </h2>
              <ul className="flex list-none flex-col">
                {data.projects.map((project) => {
                  const owner = projectOwnerUsername(project.owner);
                  const completed = project.completed_at != null;
                  return (
                    <li
                      key={project.id}
                      className="flex flex-col gap-2 border-b border-line py-3.5"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="flex min-w-0 items-center gap-2">
                          <GithubMark size={13} className="shrink-0 text-muted" />
                          <span className="truncate font-mono text-xs font-bold">
                            {project.repo_name}
                          </span>
                          {completed ? (
                            <span
                              title={
                                project.demo_url != null
                                  ? `Demo: ${project.demo_url}`
                                  : 'Marked as completed'
                              }
                              className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent"
                            >
                              ✓ Completed
                            </span>
                          ) : null}
                        </span>
                        <ProjectProgressBadge progress={project.progress} />
                      </div>
                      {owner ? (
                        <p className={cx(microLabel, 'normal-case tracking-normal')}>
                          by {owner} ·{' '}
                          {project.open_for_contributors
                            ? 'open to contributors'
                            : 'solo run'}
                        </p>
                      ) : null}
                      <Link
                        to={`/projects/${project.id}`}
                        className="group inline-flex w-fit items-center gap-1 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-accent underline decoration-accent/40 underline-offset-4 hover:text-ink"
                      >
                        Open project
                        <ArrowUpRight
                          aria-hidden
                          size={11}
                          strokeWidth={2.6}
                          className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
                        />
                      </Link>
                    </li>
                  );
                })}
                {data.projects.length === 0 ? (
                  <li className="border-b border-line py-3 text-sm text-ink-soft">
                    No projects linked yet. Be the first.
                  </li>
                ) : null}
              </ul>
            </section>
          </aside>
        </div>
      </div>
    </main>
  );
}
