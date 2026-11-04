import type { ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  ArrowLeft,
  ArrowUpRight,
  Check,
  ListOrdered,
  Timer,
} from 'lucide-react';
import { cx } from '@/lib/cx';
import { slideUpReveal } from '@/design/motion';
import { Skeleton, Tag } from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { useProblem } from '@/hooks/useProblem';

const panelHeading = 'font-mono text-[10px] font-bold uppercase tracking-[0.18em]';
const microLabel = 'font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted';

const PHASE_LINKS = [
  { index: 1, label: 'Start' },
  { index: 2, label: 'Implement' },
  { index: 3, label: 'Ship' },
];

function GuideSkeleton() {
  return (
    <div className="mx-auto w-[min(1240px,96vw)] space-y-4 py-16">
      <Skeleton className="h-3 w-40" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}

function Phase({
  id,
  number,
  title,
  leaveWith,
  children,
}: {
  id: string;
  number: string;
  title: string;
  leaveWith: string[];
  children: ReactNode;
}) {
  return (
    <motion.section
      id={id}
      variants={slideUpReveal}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.15 }}
      className="scroll-mt-24 border-t border-ink py-8 first:border-t-0 first:pt-0"
    >
      <div className="grid gap-5 sm:grid-cols-[64px_minmax(0,1fr)] sm:gap-7">
        <span className="font-display text-4xl leading-none text-accent sm:text-5xl">
          {number}
        </span>
        <div>
          <h2 className={panelHeading}>{title}</h2>
          <div className="mt-3 space-y-3 text-sm leading-relaxed text-ink-soft">
            {children}
          </div>

          <div className="mt-5 border border-line bg-sheet p-4">
            <p className={microLabel}>You leave with</p>
            <ul className="mt-2.5 space-y-1.5">
              {leaveWith.map((item) => (
                <li key={item} className="flex items-start gap-2 text-[13px] leading-snug">
                  <Check
                    aria-hidden
                    size={12}
                    strokeWidth={3}
                    className="mt-1 shrink-0 text-accent"
                  />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </motion.section>
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
      <div className="mx-auto w-[min(1240px,96vw)] py-8 md:py-10">
        <Link
          to={`/problems/${data.id}`}
          className="group inline-flex items-center gap-1.5 font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-accent underline decoration-accent/40 underline-offset-4 hover:text-ink"
        >
          <ArrowLeft
            aria-hidden
            size={12}
            strokeWidth={2.6}
            className="transition-transform group-hover:-translate-x-0.5"
          />
          Back to {data.title}
        </Link>

        <header className="mt-6 grid gap-6 border-b border-ink pb-8 md:grid-cols-[minmax(0,1fr)_280px]">
          <div>
            <p className="flex flex-wrap items-center gap-2 font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-accent">
              <span aria-hidden className="block size-2 bg-accent" />
              Field manual / Brief {data.source_id ?? data.id}
            </p>
            <h1
              className="mt-4 font-display uppercase leading-[0.92] tracking-[-0.02em]"
              style={{ fontSize: 'clamp(2rem, 4.6vw, 3.5rem)' }}
            >
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
              <dd className="flex items-center gap-1.5">
                <Timer aria-hidden size={11} strokeWidth={2.4} />
                {data.est_hours} h
              </dd>
            </div>
          </dl>
        </header>

        <div className="mt-10 grid gap-12 lg:grid-cols-[minmax(0,1fr)_280px] lg:gap-16">
          <div>
            <Phase
              id="phase-1"
              number="01"
              title="Phase 1 · Start"
              leaveWith={[
                'A repository with a README and one commit',
                'The stack you actually want to use',
                'One sentence that defines done',
              ]}
            >
              <p>
                Understand the problem and set up your workspace. Pick the stack
                that fits you - the tags on the problem page are options, not
                rules. If it lists a backend language you can swap it for Python
                or Go, and the same goes for the database and frontend. Create a
                new repository, add a README, and commit the empty project.
              </p>
            </Phase>

            <Phase
              id="phase-2"
              number="02"
              title="Phase 2 · Implement"
              leaveWith={[
                'The core flow working end to end',
                'A commit per approach, so the history reads',
                'The edge cases you found, written down',
              ]}
            >
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

            <Phase
              id="phase-3"
              number="03"
              title="Phase 3 · Ship"
              leaveWith={[
                'A deployed link you can share',
                'A README someone else can follow',
                'A short list of what comes next',
              ]}
            >
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

            <motion.div
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.2 }}
              className="mt-2 flex flex-wrap items-center justify-between gap-4 border border-ink bg-sheet p-5"
            >
              <p className="max-w-sm text-sm leading-relaxed text-ink-soft">
                When the repo exists, link it to this brief so progress tracks
                itself.
              </p>
              <Link
                to={`/problems/${data.id}`}
                className="group inline-flex items-center gap-1.5 border border-ink px-4 py-2.5 font-mono text-[10px] font-bold uppercase tracking-[0.16em] transition-colors hover:bg-ink hover:text-paper"
              >
                Open the brief
                <ArrowUpRight
                  aria-hidden
                  size={13}
                  strokeWidth={2.6}
                  className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
                />
              </Link>
            </motion.div>
          </div>

          <aside className="flex flex-col gap-6 lg:sticky lg:top-24 lg:self-start">
            <nav
              aria-label="On this page"
              className="border border-ink bg-sheet p-4"
            >
              <h2 className={cx(panelHeading, 'flex items-center gap-2')}>
                <ListOrdered
                  aria-hidden
                  size={12}
                  strokeWidth={2.4}
                  className="text-accent"
                />
                On this page
              </h2>
              <ul className="mt-3 space-y-2">
                {PHASE_LINKS.map((phase) => (
                  <li key={phase.index}>
                    <a
                      href={`#phase-${phase.index}`}
                      className="group flex items-baseline gap-2 font-mono text-[10px] font-bold uppercase tracking-[0.14em] text-ink-soft transition-colors hover:text-accent"
                    >
                      <span className="text-accent">
                        {String(phase.index).padStart(2, '0')}
                      </span>
                      {phase.label}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>

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
