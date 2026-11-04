import { Link, useParams } from 'react-router-dom';
import { Skeleton, Tag } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { useProblem } from '@/hooks/useProblem';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';

function GuideSkeleton() {
  return (
    <div className="mx-auto w-[min(900px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

export function ProblemGuidePage() {
  const { id } = useParams();
  const problemId = Number(id);

  if (!Number.isInteger(problemId) || problemId <= 0) {
    return <NotFoundPage />;
  }

  return <GuideView problemId={problemId} />;
}

function GuideView({ problemId }: { problemId: number }) {
  const problem = useProblem(problemId);

  if (problem.isPending) {
    return (
      <main className="border-b-[3px] border-ink bg-paper">
        <GuideSkeleton />
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
            Could not load this guide
          </h1>
          <p>{problem.error.message}</p>
          <Link
            to={`/problems/${problemId}`}
            className="font-mono text-xs font-bold underline"
          >
            Back to the problem
          </Link>
        </div>
      </main>
    );
  }

  const data = problem.data;

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1100px,96vw)] py-12">
        <Link
          to={`/problems/${data.id}`}
          className="font-mono text-xs font-bold uppercase tracking-widest text-blue underline underline-offset-4"
        >
          ← Back to {data.title}
        </Link>

        <section className="mt-6 border-[3px] border-ink bg-white p-6 shadow-hard lg:p-8">
          <h1 className="font-display text-4xl uppercase leading-tight">
            Build guide · {data.title}
          </h1>
          <p className="mt-2 text-sm leading-relaxed text-ink/70">
            These are starting phases, not a complete spec. Pick a phase, build
            it, ship it, then move to the next.
          </p>

          <div className="mt-8 space-y-8">
            <div className="border-[3px] border-ink bg-white p-4 shadow-hard">
              <h2 className={panelHeading}>Phase 1 · Start</h2>
              <p className="mt-2 text-sm leading-relaxed">
                Understand the problem and set up your workspace. Pick the stack
                that fits you - the tags on the problem page are options, not
                rules. If it lists a backend language you can swap it for Python
                or Go, and the same goes for the database and frontend. Create a
                new repository, add a README, and commit the empty project.
              </p>
            </div>

            <div className="border-[3px] border-ink bg-white p-4 shadow-hard">
              <h2 className={panelHeading}>Phase 2 · Implement</h2>
              <p className="mt-2 text-sm leading-relaxed">
                Build the core feature end to end. Work through the approaches
                below in order, committing after each one. Do not try to build
                everything at once - get one path working before you add more.
              </p>
              <ol className="mt-3 list-decimal ml-4 space-y-1 text-sm leading-relaxed">
                {data.approaches.map((approach, index) => (
                  <li key={index}>{approach}</li>
                ))}
              </ol>
            </div>

            <div className="border-[3px] border-ink bg-white p-4 shadow-hard">
              <h2 className={panelHeading}>Phase 3 · Ship</h2>
              <p className="mt-2 text-sm leading-relaxed">
                Test the core flow, fix the bugs you find, and deploy. Add a
                README that explains how to run the project and what it does.
                Ship it to a host you control, share the link, and keep
                improving it based on what you learn.
              </p>
              <p className="mt-3 text-sm leading-relaxed">
                Ship the MVP first, then add whatever matters to you. Build what
                you want to learn and ship it.
              </p>
            </div>
          </div>

          {data.tech_tags.length > 0 && (
            <div className="mt-6 flex flex-wrap gap-1.5">
              <span className={panelHeading}>Suggested stack</span>
              {data.tech_tags.map((tag) => (
                <Tag key={tag}>{tag}</Tag>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
