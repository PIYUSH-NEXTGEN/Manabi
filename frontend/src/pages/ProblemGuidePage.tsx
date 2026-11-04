import type { ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { Skeleton, Tag } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { useProblem } from '@/hooks/useProblem';

const panelHeading = 'font-mono text-[10px] font-bold uppercase tracking-[0.18em]';

function GuideSkeleton() {
  return (
    <div className="mx-auto w-[min(900px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

function Phase({
  number,
  title,
  children,
}: {
  number: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="grid gap-4 border-t border-ink py-7 first:border-t-0 sm:grid-cols-[64px_minmax(0,1fr)] sm:gap-6">
      <span className="font-display text-4xl leading-none text-accent sm:text-5xl">
        {number}
      </span>
      <div>
        <h2 className={panelHeading}>{title}</h2>
        <div className="mt-3 space-y-3 text-sm leading-relaxed text-ink-soft">
          {children}
        </div>
      </div>
    </section>
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
      <main className="border-b border-ink bg-paper">
        <GuideSkeleton />
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
    <main className="border-b border-ink bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-10">
        <Link
          to={`/problems/${data.id}`}
          className="font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-accent underline decoration-accent/40 underline-offset-4 hover:text-ink"
        >
          ← Back to {data.title}
        </Link>

        <header className="mt-6 grid gap-6 border-b border-ink pb-8 md:grid-cols-[minmax(0,1fr)_280px]">
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-accent">
              Field manual / Brief {data.source_id ?? data.id}
            </p>
            <h1 className="mt-3 font-display uppercase leading-[0.92] tracking-[-0.02em]" style={{ fontSize: 'clamp(2rem, 4.6vw, 3.5rem)' }}>
              Build guide · {data.title}
            </h1>
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-ink-soft">
              These are starting phases, not a complete spec. Pick a phase,
              build it, ship it, then move to the next.
            </p>
          </div>
          <dl className="self-start border border-ink bg-sheet px-4 py-3 font-mono text-[10px] font-bold uppercase tracking-[0.1em]">
            <div className="flex items-center justify-between border-b border-line pb-2.5">
              <dt className="text-[9px] tracking-[0.16em] text-muted">Phases</dt>
              <dd>03</dd>
            </div>
            <div className="flex items-center justify-between border-b border-line py-2.5">
              <dt className="text-[9px] tracking-[0.16em] text-muted">Field</dt>
              <dd>{data.field.replace(/-/g, ' ')}</dd>
            </div>
            <div className="flex items-center justify-between py-2.5">
              <dt className="text-[9px] tracking-[0.16em] text-muted">Est. time</dt>
              <dd>{data.est_hours} h</dd>
            </div>
          </dl>
        </header>

        <div className="mt-8 grid gap-10 lg:grid-cols-[minmax(0,1fr)_280px] lg:gap-14">
          <div>
            <Phase number="01" title="Phase 1 · Start">
              <p>
                Understand the problem and set up your workspace. Pick the stack
                that fits you - the tags on the problem page are options, not
                rules. If it lists a backend language you can swap it for Python
                or Go, and the same goes for the database and frontend. Create a
                new repository, add a README, and commit the empty project.
              </p>
            </Phase>

            <Phase number="02" title="Phase 2 · Implement">
              <p>
                Build the core feature end to end. Work through the approaches
                below in order, committing after each one. Do not try to build
                everything at once - get one path working before you add more.
              </p>
              <ol className="space-y-2 border-t border-line pt-3">
                {data.approaches.map((approach, index) => (
                  <li key={index} className="flex gap-3">
                    <span className="font-mono text-[9px] font-bold tracking-[0.14em] text-accent">
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    <span>{approach}</span>
                  </li>
                ))}
              </ol>
            </Phase>

            <Phase number="03" title="Phase 3 · Ship">
              <p>
                Test the core flow, fix the bugs you find, and deploy. Add a
                README that explains how to run the project and what it does.
                Ship it to a host you control, share the link, and keep
                improving it based on what you learn.
              </p>
              <p>
                Ship the MVP first, then add whatever matters to you. Build what
                you want to learn and ship it.
              </p>
            </Phase>
          </div>

          <aside className="flex flex-col gap-6">
            {data.tech_tags.length > 0 ? (
              <div className="border border-ink bg-sheet p-4">
                <h2 className={panelHeading}>Suggested stack</h2>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {data.tech_tags.map((tag) => (
                    <Tag key={tag}>{tag}</Tag>
                  ))}
                </div>
              </div>
            ) : null}
            <div className="border-t border-ink pt-4">
              <p className={cx(panelHeading, 'text-muted')}>Source</p>
              <p className="mt-2 text-sm">{data.source_name}</p>
              <p className="mt-1 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                {data.source_id ?? 'No source id'}
              </p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
