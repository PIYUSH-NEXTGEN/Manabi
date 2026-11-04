import { Link, useParams } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { Button, Skeleton, Tag } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import { SubmitProjectPanel } from '@/components/problems/SubmitProjectPanel';
import { useProblem } from '@/hooks/useProblem';
import { projectOwnerUsername } from '@/api/client';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';

function ProjectSkeleton() {
  return (
    <div className="mx-auto w-[min(900px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

function futureIdeas(originalText: string | null | undefined): string[] {
  if (!originalText) return [];
  const section = originalText.match(
    /## (Possible future improvements|Stretch goals)[\s\S]*?(?=\n## |\z)/i,
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
        <ProjectSkeleton />
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
  const ideas = futureIdeas(data.original_text);
  const description = fullDescription(data.summary, data.who_affected, data.why_matters);

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1100px,96vw)] py-12">
        <section className="border-[3px] border-ink bg-white p-6 shadow-hard lg:p-8">
          <h1 className="font-display text-4xl uppercase leading-tight">
            {data.title}
          </h1>
          <p className="mt-4 text-lg leading-relaxed">{description}</p>

          <h2 className={cx(panelHeading, 'mt-8')}>Why it matters</h2>
          <p className="mt-2 text-sm leading-relaxed">{data.why_matters}</p>

          <h2 className={cx(panelHeading, 'mt-8')}>Tech stack</h2>
          <p className="mt-2 text-sm leading-relaxed">
            The stack below is a starting point, not a rule. If it lists a
            backend language you can swap it for another one - Python or Go,
            for example - and the same goes for the database, frontend, and
            anything else. Use what fits you.
          </p>
          {data.tech_tags.length > 0 ? (
            <div className="mt-3 flex flex-wrap gap-1.5">
              {data.tech_tags.map((tag) => (
                <Tag key={tag}>{tag}</Tag>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-sm">No stack listed.</p>
          )}

          <h2 className={cx(panelHeading, 'mt-8')}>What you can add later</h2>
          {ideas.length > 0 ? (
            <ul className="mt-2 list-disc ml-4 space-y-1 text-sm leading-relaxed">
              {ideas.map((idea) => (
                <li key={idea}>{idea}</li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-sm">
              Ship the MVP first, then add whatever matters to you. Build what
              you want to learn and ship it.
            </p>
          )}

          <div className="mt-8 flex justify-start">
            <Link to={`/problems/${data.id}/guide`}>
              <Button variant="primary">Build guide</Button>
            </Link>
          </div>
        </section>

        <aside className="mt-8 flex flex-col gap-6">
          <SubmitProjectPanel problemId={data.id} />
          <div className="flex flex-col gap-3">
            <h2 className={panelHeading}>
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
    </main>
  );
}
