import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import { motion } from "motion/react";
import { ArrowUpRight } from "lucide-react";
import { cx } from "@/lib/cx";
import { EASE_SNAP, slideUpReveal } from "@/design/motion";
import { Tag } from "@/design/primitives";
import { LoadErrorPanel, PageSkeleton } from "@/pages/detailStates";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { ProjectProgressBadge } from "@/components/problems/ProjectProgressBadge";
import { SubmitProjectPanel } from "@/components/problems/SubmitProjectPanel";
import { GithubMark } from "@/components/icons/GithubMark";
import { useProblem } from "@/hooks/useProblem";
import { fieldLabel } from "@/lib/fields";
import { projectOwnerUsername } from "@/api/client";
import type { ProblemOut } from "@/api/client";

const panelHeading =
  "font-mono text-[10px] font-bold uppercase tracking-[0.18em]";
const microLabel =
  "font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted";

type BuildGuidePhase = NonNullable<ProblemOut["build_guide"]>[number];

function descriptionParagraphs(
  summary: string,
  whoAffected: string,
  whyMatters: string,
): string[] {
  const paragraphs = summary
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim().replace(/\s+/g, " "))
    .filter(Boolean);
  paragraphs.push(
    `This project is for ${whoAffected.toLowerCase()}. ${whyMatters}`,
  );
  return paragraphs;
}

// Briefs without a curated guide get a stack-agnostic phase roadmap built
// from the existing approaches steps.
function guideFromApproaches(approaches: string[]): BuildGuidePhase[] {
  return approaches.map((step, index) => ({
    title: `Phase ${index + 1}`,
    summary: step,
    steps: [],
  }));
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
        <PageSkeleton width="w-[min(1240px,96vw)]" />
      </main>
    );
  }

  if (problem.isError) {
    if (problem.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <LoadErrorPanel
        title="Could not load this problem"
        message={problem.error.message}
        backTo="/problems"
        backLabel="Back to the board"
      />
    );
  }

  const data = problem.data;
  const isHackathon = data.goal === "hackathon";
  const isResume = data.goal === "resume";
  const paragraphs = descriptionParagraphs(
    data.summary,
    data.who_affected,
    data.why_matters,
  );
  const projectCount = data.project_count ?? data.projects.length;
  const completedCount = data.completed_count ?? 0;
  const buildingCount = projectCount - completedCount;
  const learningConcepts = data.learning_concepts ?? [];
  const guide = data.build_guide?.length
    ? data.build_guide
    : guideFromApproaches(data.approaches);
  const teamPlan = isHackathon ? data.team_plan : undefined;
  const pitchGuide = isHackathon ? data.pitch_guide : undefined;
  const resumeKit = isResume ? data.resume_kit : undefined;

  // Section numbers are assigned in render order, so the optional "what
  // you'll learn" section never leaves a gap in the numbering.
  let sectionCounter = 0;
  const nextSectionNumber = () =>
    String((sectionCounter += 1)).padStart(2, "0");

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
              style={{ fontSize: "clamp(2.25rem, 5vw, 4rem)" }}
            >
              {data.title}
            </h1>

            {isHackathon ? (
              <div className="mt-6 max-w-3xl space-y-6 border-l-2 border-accent/50 pl-5 text-base leading-relaxed text-ink-soft md:text-lg">
                <div>
                  <p className={cx(microLabel, "text-accent")}>The problem</p>
                  <p className="mt-2">{data.summary}</p>
                </div>
                <div>
                  <p className={cx(microLabel, "text-accent")}>
                    Who faces it, and how
                  </p>
                  <p className="mt-2">
                    {data.who_affected} {data.why_matters}
                  </p>
                </div>
                {data.approaches.length > 0 ? (
                  <div>
                    <p className={cx(microLabel, "text-accent")}>
                      How it gets fixed
                    </p>
                    <ul className="mt-2 space-y-2">
                      {data.approaches.map((approach) => (
                        <li key={approach} className="flex gap-3">
                          <span
                            aria-hidden
                            className="mt-[0.7em] block size-1.5 shrink-0 bg-accent/70"
                          />
                          {approach}
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="mt-6 max-w-3xl space-y-4 border-l-2 border-accent/50 pl-5 text-base leading-relaxed text-ink-soft md:text-lg">
                {paragraphs.map((paragraph) => (
                  <p key={paragraph}>{paragraph}</p>
                ))}
              </div>
            )}
          </div>

          <dl className="self-start border border-ink bg-sheet px-4 py-3">
            <div className="flex items-center justify-between border-b border-line pb-2.5">
              <dt className={microLabel}>File no.</dt>
              <dd className="font-mono text-sm font-bold tracking-[0.08em]">
                M-{String(data.id).padStart(3, "0")}
              </dd>
            </div>
            <SpecRow label="Field">{fieldLabel(data.field)}</SpecRow>
            <SpecRow label="Domain">{data.domain.replace(/-/g, " ")}</SpecRow>
            <SpecRow label="Difficulty">{data.difficulty}</SpecRow>
          </dl>
        </motion.header>

        <div className="mt-10 grid gap-12 lg:grid-cols-[minmax(0,1fr)_320px] lg:gap-16">
          <article>
            {isHackathon || isResume ? null : (
              <Section number={nextSectionNumber()} title="Why it matters">
                <p className="max-w-3xl border-l-2 border-line pl-5 text-base leading-relaxed text-ink-soft">
                  {data.why_matters}
                </p>
              </Section>
            )}

            {!isHackathon &&
            !isResume &&
            learningConcepts.length > 0 ? (
              <Section
                number={nextSectionNumber()}
                title="What concepts you'll learn"
              >
                <ul className="max-w-3xl space-y-2.5 text-sm leading-relaxed text-ink-soft">
                  {learningConcepts.map((concept) => (
                    <li key={concept} className="flex gap-3">
                      <span
                        aria-hidden
                        className="mt-2 block size-1.5 shrink-0 bg-accent"
                      />
                      {concept}
                    </li>
                  ))}
                </ul>
              </Section>
            ) : null}

            {isResume ? null : (
              <Section number={nextSectionNumber()} title="Tech stack">
                <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                  The stack below is a starting point, not a rule. If it lists a
                  backend language you can swap it for another one - Python or
                  Go, for example - and the same goes for the database,
                  frontend, and anything else. Use what fits you.
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
            )}

            {resumeKit ? (
              <>
                <Section number={nextSectionNumber()} title="MVP vs standout">
                  <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                    Two bars for the same project. The first level ships with
                    honest numbers; the second one is what most people skip -
                    and what makes a recruiter stop scrolling.
                  </p>
                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    {(resumeKit.scope_levels ?? []).map((scopeLevel) => (
                      <div
                        key={scopeLevel.level}
                        className="border border-ink bg-sheet p-5"
                      >
                        <p className={cx(microLabel, "text-accent")}>
                          {scopeLevel.level}
                        </p>
                        <p className="mt-2.5 text-sm leading-relaxed text-ink-soft">
                          {scopeLevel.text}
                        </p>
                        {(scopeLevel.checks ?? []).length > 0 ? (
                          <ul className="mt-4 max-w-2xl space-y-2">
                            {(scopeLevel.checks ?? []).map((check) => (
                              <li
                                key={check}
                                className="flex gap-3 text-sm leading-relaxed text-ink-soft"
                              >
                                <span
                                  aria-hidden
                                  className="mt-2 block size-1.5 shrink-0 bg-accent"
                                />
                                {check}
                              </li>
                            ))}
                          </ul>
                        ) : null}
                      </div>
                    ))}
                  </div>
                </Section>

                <Section number={nextSectionNumber()} title="Roles it helps with">
                  <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {(resumeKit.target_roles ?? []).map((targetRole) => (
                      <div
                        key={targetRole.role}
                        className="border border-line bg-sheet p-4"
                      >
                        <dt className="font-display text-sm uppercase tracking-tight text-ink">
                          {targetRole.role}
                        </dt>
                        <dd className="mt-2 text-sm leading-relaxed text-ink-soft">
                          {targetRole.how_it_helps}
                        </dd>
                      </div>
                    ))}
                  </dl>
                </Section>

                <Section
                  number={nextSectionNumber()}
                  title="Resume bullet template"
                >
                  <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                    Fill the braces with your own numbers from the run - never
                    invent them. The example shows what a filled bullet looks
                    like.
                  </p>
                  <ul className="mt-4 max-w-3xl space-y-4">
                    {(resumeKit.resume_bullets ?? []).map((resumeBullet) => (
                      <li
                        key={resumeBullet.bullet}
                        className="border border-line bg-sheet p-4"
                      >
                        <p className="font-mono text-[13px] leading-relaxed text-ink">
                          {resumeBullet.bullet}
                        </p>
                        {resumeBullet.example ? (
                          <p className="mt-2.5 text-sm leading-relaxed text-ink-soft">
                            <span
                              className={cx(microLabel, "mr-2 text-muted")}
                            >
                              Example
                            </span>
                            {resumeBullet.example}
                          </p>
                        ) : null}
                      </li>
                    ))}
                  </ul>
                </Section>

                <Section
                  number={nextSectionNumber()}
                  title="Interview talking points"
                >
                  <ul className="max-w-3xl space-y-4">
                    {(resumeKit.interview_points ?? []).map((interviewPoint) => (
                      <li
                        key={interviewPoint.question}
                        className="border-t border-line pt-4 first:border-t-0 first:pt-0"
                      >
                        <p className="text-sm font-bold leading-snug text-ink">
                          {interviewPoint.question}
                        </p>
                        <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
                          {interviewPoint.answer}
                        </p>
                      </li>
                    ))}
                  </ul>
                </Section>
              </>
            ) : null}

            {teamPlan ? (
              <Section number={nextSectionNumber()} title="Team plan">
                {teamPlan.note ? (
                  <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                    {teamPlan.note}
                  </p>
                ) : null}
                {(teamPlan.roles ?? []).length > 0 ? (
                  <dl className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {(teamPlan.roles ?? []).map((teamRole) => (
                      <div
                        key={teamRole.role}
                        className="border border-line bg-sheet p-4"
                      >
                        <dt className="font-display text-sm uppercase tracking-tight text-ink">
                          {teamRole.role}
                        </dt>
                        <dd className="mt-2 text-sm leading-relaxed text-ink-soft">
                          {teamRole.covers}
                        </dd>
                      </div>
                    ))}
                  </dl>
                ) : null}
                {(teamPlan.milestones ?? []).length > 0 ? (
                  <ol className="mt-5 max-w-3xl space-y-2.5">
                    {(teamPlan.milestones ?? []).map((milestone, index) => (
                      <li
                        key={milestone}
                        className="flex gap-3 text-sm leading-relaxed text-ink-soft"
                      >
                        <span className="shrink-0 font-mono text-[10px] font-bold leading-relaxed text-accent">
                          T+{String(index + 1).padStart(1, "0")}
                        </span>
                        {milestone}
                      </li>
                    ))}
                  </ol>
                ) : null}
              </Section>
            ) : null}

            {pitchGuide ? (
              <Section number={nextSectionNumber()} title="Pitch guide">
                {pitchGuide.one_liner ? (
                  <p className="max-w-3xl border-l-2 border-accent/60 pl-5 text-base font-bold leading-relaxed md:text-lg">
                    {pitchGuide.one_liner}
                  </p>
                ) : null}
                {(pitchGuide.beats ?? []).length > 0 ? (
                  <ol className="mt-5 flex list-none flex-col gap-4">
                    {(pitchGuide.beats ?? []).map((beat, index) => (
                      <li
                        key={`${beat.heading}-${index}`}
                        className="border border-line bg-sheet p-5"
                      >
                        <p className="flex items-baseline gap-3">
                          <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
                            {String(index + 1).padStart(2, "0")}
                          </span>
                          <span className="font-display text-sm uppercase tracking-tight text-ink">
                            {beat.heading}
                          </span>
                        </p>
                        <p className="mt-2.5 max-w-2xl text-sm leading-relaxed text-ink-soft">
                          {beat.text}
                        </p>
                      </li>
                    ))}
                  </ol>
                ) : null}
                {(pitchGuide.judge_questions ?? []).length > 0 ? (
                  <div className="mt-6">
                    <p className={panelHeading}>Questions the judges may ask</p>
                    <ul className="mt-4 max-w-3xl space-y-4">
                      {(pitchGuide.judge_questions ?? []).map(
                        (judgeQuestion) => (
                          <li
                            key={judgeQuestion.question}
                            className="border-t border-line pt-4 first:border-t-0 first:pt-0"
                          >
                            <p className="text-sm font-bold leading-snug text-ink">
                              {judgeQuestion.question}
                            </p>
                            <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
                              {judgeQuestion.answer}
                            </p>
                          </li>
                        ),
                      )}
                    </ul>
                  </div>
                ) : null}
              </Section>
            ) : null}

            <Section number={nextSectionNumber()} title="Build guide">
              <p className="max-w-3xl text-sm leading-relaxed text-ink-soft">
                Work through the phases in order - each one ends with something
                working. No phase assumes a particular language, framework, or
                database; pick tools you already know or want to learn, and swap
                anything at any point.
              </p>
              {guide.length > 0 ? (
                <ol className="mt-5 flex list-none flex-col gap-6">
                  {guide.map((phase, index) => (
                    <li
                      key={`${phase.title}-${index}`}
                      className="border border-line bg-sheet p-5"
                    >
                      <p className="flex items-baseline gap-3">
                        <span className="font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
                          {String(index + 1).padStart(2, "0")}
                        </span>
                        <span className="font-display text-base uppercase tracking-tight text-ink">
                          {phase.title}
                        </span>
                      </p>
                      {phase.summary ? (
                        <p className="mt-2.5 max-w-2xl text-sm leading-relaxed text-ink-soft">
                          {phase.summary}
                        </p>
                      ) : null}
                      {(phase.steps ?? []).length > 0 ? (
                        <ol className="mt-4 flex list-none flex-col gap-2.5">
                          {(phase.steps ?? []).map((step, stepIndex) => (
                            <li
                              key={step}
                              className="flex gap-3 text-sm leading-relaxed text-ink-soft"
                            >
                              <span className="shrink-0 font-mono text-[10px] font-bold leading-relaxed text-accent">
                                {index + 1}.{stepIndex + 1}
                              </span>
                              {step}
                            </li>
                          ))}
                        </ol>
                      ) : null}
                    </li>
                  ))}
                </ol>
              ) : (
                <p className="mt-4 max-w-3xl text-sm leading-relaxed text-ink-soft">
                  No phased guide for this brief yet. Start with the smallest
                  version where one core flow works end to end, then keep
                  iterating on what annoys you most.
                </p>
              )}
            </Section>
          </article>

          <aside className="flex flex-col gap-9 lg:sticky lg:top-24 lg:self-start">
            <SubmitProjectPanel problemId={data.id} />

            <section>
              <h2 className={cx(panelHeading, "border-b border-ink pb-2")}>
                Projects in the wild
                {buildingCount === 1 && completedCount === 0
                  ? " (1)"
                  : ` (${buildingCount} building${
                      completedCount > 0 ? ` · ${completedCount} completed` : ""
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
                          <GithubMark
                            size={13}
                            className="shrink-0 text-muted"
                          />
                          <span className="truncate font-mono text-xs font-bold">
                            {project.repo_name}
                          </span>
                          {completed ? (
                            <span
                              title={
                                project.demo_url != null
                                  ? `Demo: ${project.demo_url}`
                                  : "Marked as completed"
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
                        <p
                          className={cx(
                            microLabel,
                            "normal-case tracking-normal",
                          )}
                        >
                          by {owner} ·{" "}
                          {project.open_for_contributors
                            ? "open to contributors"
                            : "solo run"}
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
