import { safeExternalUrl } from '@/lib/url';
import { Link, useParams } from 'react-router-dom';
import type { ReactNode } from 'react';
import { cx } from '@/lib/cx';
import { Stamp, Tag, type Difficulty } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import { SubmitProjectPanel } from '@/components/problems/SubmitProjectPanel';
import { useProblem } from '@/hooks/useProblem';
import { projectOwnerUsername, type ProblemDetail } from '@/api/client';

const DIFFICULTY_FILL: Record<Difficulty, number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

const sectionHeading =
  'font-mono text-[11px] font-bold uppercase tracking-widest';

function DetailSkeleton() {
  return (
    <div className="mx-auto w-[min(1100px,96vw)] animate-pulse space-y-4 py-16">
      <div className="h-4 w-40 rounded bg-ink/20" />
      <div className="h-10 w-2/3 rounded bg-ink/20" />
      <div className="h-4 w-1/2 rounded bg-ink/20" />
      <div className="h-40 w-full rounded bg-ink/20" />
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
      <main className="border-b-[3px] border-ink bg-paper">
        <DetailSkeleton />
      </main>
    );
  }

  if (problem.isError) {
    if (problem.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <main className="border-b-[3px] border-ink">
        <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
          <h1 className="font-display text-3xl uppercase">
            Could not load this problem
          </h1>
          <p>{problem.error.message}</p>
          <Link
            to="/problems"
            className="font-mono text-xs font-bold underline"
          >
            Back to the board
          </Link>
        </div>
      </main>
    );
  }

  const data = problem.data;

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1100px,96vw)] py-12">
        <div className="grid gap-8 lg:grid-cols-[1.6fr_1fr]">
          <article>
            <p className={sectionHeading}>
              {data.field} · {data.domain ?? 'unclassed domain'}
            </p>
            <h1 className="mt-2 font-display text-4xl uppercase leading-tight">
              {data.title}
            </h1>
            <p className="mt-4 text-lg leading-snug">{data.summary}</p>
            <DetailStructuredCard data={data} />
          </article>

          <aside className="flex flex-col gap-6">
            <SubmitProjectPanel problemId={data.id} />
            <div className="flex flex-col gap-3">
              <h2 className={sectionHeading}>
                Projects in the wild ({data.projects.length})
              </h2>
              <ul className="flex list-none flex-col gap-2 divide-y divide-ink/10">
                {data.projects.map((project) => {
                  const owner = projectOwnerUsername(project.owner);
                  return (
                    <li
                      key={project.id}
                      className="flex flex-col gap-1 border-[3px] border-ink bg-white p-3 shadow-hard"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-mono text-xs font-bold">
                          {project.repo_name}
                        </span>
                <ProjectProgressBadge progress={project.progress} />
                      </div>
                      {owner ? (
                        <p className="font-mono text-[10px] uppercase tracking-widest text-ink/70">
                          by {owner} · {project.open_for_contributors ? 'open to contributors' : 'solo run'}
                        </p>
                      ) : null}
                      <Link
                        to={`/projects/${project.id}`}
                        className="font-mono text-[11px] font-bold uppercase tracking-widest text-blue underline underline-offset-4"
                      >
                        Open project →
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          </aside>
        </div>

        <section
          aria-label="Original statement"
          className="mt-10 border-[3px] border-ink bg-white p-4 shadow-hard"
        >
          <h2 className={sectionHeading}>Original statement</h2>
          <pre className="mt-2 max-h-96 whitespace-pre-wrap font-body text-sm leading-relaxed">
            {data.original_text}
          </pre>
        </section>
      </div>
    </main>
  );
}

function DetailStructuredCard({ data }: { data: ProblemDetail }) {
  const filled = DIFFICULTY_FILL[data.difficulty as Difficulty];
  const squares = `${'■'.repeat(filled)}${'□'.repeat(3 - filled)}`;

  return (
    <dl className="mt-8 divide-y divide-ink/10 border-[3px] border-ink bg-white shadow-hard">
      <DetailRow
        label={
          <dt className={`${sectionHeading} flex items-center gap-1.5`}>
            Who is affected
            {data.ai_fields.includes('who_affected') ? (
              <Stamp tone="ai-suggested" label="AI-SUGGESTED" rotate={-2} />
            ) : null}
          </dt>
        }
      >
        <p className="text-sm leading-snug">{data.who_affected}</p>
      </DetailRow>
      <DetailRow
        label={
          <dt className={`${sectionHeading} flex items-center gap-1.5`}>
            Why it matters
            {data.ai_fields.includes('why_matters') ? (
              <Stamp tone="ai-suggested" label="AI-SUGGESTED" rotate={-2} />
            ) : null}
          </dt>
        }
      >
        <p className="text-sm leading-snug">{data.why_matters}</p>
      </DetailRow>
      <DetailRow label={<dt className={sectionHeading}>Tech</dt>}>
        {data.tech_tags.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {data.tech_tags.map((tag) => (
              <Tag key={tag}>{tag}</Tag>
            ))}
          </div>
        ) : (
          <p className="text-sm">none of interest</p>
        )}
      </DetailRow>
      <DetailRow
        label={
          <dt className={`${sectionHeading} flex items-center gap-1.5`}>
            Datasets
          </dt>
        }
      >
        {data.datasets.length > 0 ? (
          <ul className="ml-4 list-disc text-sm leading-snug">
            {data.datasets.map((dataset) => {
              const name = typeof dataset.name === 'string' ? dataset.name : null;
              const url = typeof dataset.url === 'string' ? dataset.url : null;
              const safeUrl = url ? safeExternalUrl(url) : null;
              return (
                <li key={name ?? url ?? JSON.stringify(dataset)}>
                  {safeUrl && name ? (
                    <a href={safeUrl} target="_blank" rel="noreferrer" className="underline underline-offset-4">
                      {name}
                    </a>
                  ) : (
                    name ?? 'Unnamed dataset'
                  )}
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="text-sm">No dataset attached to this brief.</p>
        )}
      </DetailRow>
      <DetailRow
        label={
          <dt className={`${sectionHeading} flex items-center gap-1.5`}>
            Approaches worth trying
            {data.ai_fields.includes('approaches') ? (
              <Stamp tone="ai-suggested" label="AI-SUGGESTED" rotate={-2} />
            ) : null}
          </dt>
        }
      >
        <ol className="ml-4 list-decimal text-sm leading-snug">
          {data.approaches.map((approach) => (
            <li key={approach}>{approach}</li>
          ))}
        </ol>
      </DetailRow>
      <DetailRow
        label={
          <dt className={`${sectionHeading} flex items-center gap-1.5`}>
            Effort
            {data.ai_fields.includes('est_hours') ? (
              <Stamp tone="ai-suggested" label="AI-SUGGESTED" rotate={-2} />
            ) : null}
          </dt>
        }
      >
        <div className="flex items-center gap-2 font-mono text-xs font-bold uppercase tracking-widest">
          <span>
            <span aria-hidden>{squares}</span>
            <span className="sr-only">difficulty {data.difficulty}</span>
          </span>
          <span aria-hidden>·</span>
          <span>{data.est_hours} hours</span>
        </div>
      </DetailRow>
      <DetailRow label={<dt className={sectionHeading}>Source</dt>}>
        {safeExternalUrl(data.source_url) ? (
          <a
            href={safeExternalUrl(data.source_url) ?? undefined}
            target="_blank"
            rel="noreferrer"
            className="font-mono text-xs font-bold underline underline-offset-4"
          >
            {data.source_url?.replace(/^https?:\/\//, '')}
          </a>
        ) : (
          <span className="font-mono text-xs font-bold">
            {data.source_name} · no public link
          </span>
        )}
        <p className="mt-1 font-mono text-[10px] uppercase tracking-widest text-ink/70">
          Source: {data.source_name}
        </p>
      </DetailRow>
    </dl>
  );
}

interface DetailRowProps {
  label: ReactNode;
  children: ReactNode;
}

function DetailRow({ label, children }: DetailRowProps) {
  return (
    <div
      className={cx(
        'grid gap-2 px-4 py-4 sm:grid-cols-[180px_1fr] sm:items-baseline',
      )}
    >
      {label}
      <dd className="contents sm:block">{children}</dd>
    </div>
  );
}
