import { Link } from 'react-router-dom';
import { Tag } from '@/design/primitives';
import { ProblemCard } from '@/components/problems/ProblemCard';
import { ProjectProgressBadge } from '@/components/problems/ProjectProgressBadge';
import type { ProjectOut, RecommendationItem } from '@/api/client';
import {
  projectOwnerUsername,
} from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { useMyProjects } from '@/hooks/useMyProjects';
import { useProjectProgress } from '@/hooks/useProjectProgress';
import { useRecommendations } from '@/hooks/useRecommendations';

function ReasonList({ reasons }: { reasons: RecommendationItem['reasons'] }) {
  if (reasons.length === 0) return null;

  return (
    <ul className="mt-3 space-y-1 font-mono text-[11px] font-bold uppercase tracking-widest text-ink/70">
      {reasons.map((reason) => (
        <li key={reason}>+ {reason}</li>
      ))}
    </ul>
  );
}

function MyProjectRow({ project }: { project: ProjectOut }) {
  const progress = useProjectProgress(project.id);
  const repoLabel = projectOwnerUsername(project.owner) ?? project.repo_url;

  return (
    <li className="flex items-center justify-between gap-3 px-4 py-3">
      <Link
        to={`/projects/${project.id}`}
        className="font-mono text-sm font-bold underline-offset-4 hover:underline"
      >
        {repoLabel}
      </Link>
      {progress.isLoading ? (
        <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/60">
          Checking GitHub…
        </span>
      ) : (
        <ProjectProgressBadge progress={progress.data ?? null} />
      )}
    </li>
  );
}

export function DashboardPage() {
  const me = useMe();
  const recommendations = useRecommendations();
  const projects = useMyProjects();

  const displayName = me.data?.name || me.data?.username;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <h1 className="font-display text-3xl uppercase leading-none md:text-4xl">
        Dashboard
      </h1>
      <p className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-ink/70">
        {displayName ? <>Logged in as {displayName}</> : 'Loading…'}
      </p>

      <section aria-label="Your projects" className="mt-8">
        <h2 className="font-display text-xl uppercase md:text-2xl">
          Your projects
        </h2>
        {projects.isLoading ? (
          <p className="mt-2 text-sm">Loading projects…</p>
        ) : projects.data && projects.data.length > 0 ? (
          <ul className="mt-3 divide-y-[3px] divide-ink border-[3px] border-ink bg-white">
            {projects.data.map((project) => (
              <MyProjectRow key={project.id} project={project} />
            ))}
          </ul>
        ) : (
          <p className="mt-3 border-[3px] border-ink bg-white p-4 text-sm leading-snug">
            No projects yet.{' '}
            <Link to="/problems" className="underline underline-offset-4">
              Pick a problem
            </Link>{' '}
            and submit your repo against it.
          </p>
        )}
        {projects.error ? (
          <p className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-red">
            {projects.error.detail}
          </p>
        ) : null}
      </section>

      <section aria-label="For you" className="mt-8">
        <h2 className="font-display text-xl uppercase md:text-2xl">For you</h2>
        {recommendations.isLoading ? (
          <p className="mt-2 text-sm">Loading recommendations…</p>
        ) : null}
        {recommendations.error ? (
          <p className="mt-2 font-mono text-[11px] font-bold uppercase tracking-widest text-red">
            {recommendations.error.detail}
          </p>
        ) : null}
        {recommendations.data && recommendations.data.items.length === 0 ? (
          <p className="mt-3 border-[3px] border-ink bg-white p-4 text-sm leading-snug">
            Nothing matched yet — try more problems and projects, and this
            fills up.
          </p>
        ) : null}
        {recommendations.data && recommendations.data.items.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 pt-4 sm:grid-cols-2 lg:grid-cols-3">
            {recommendations.data.items.map((item) => (
              <div key={item.problem.id} className="flex flex-col">
                <ProblemCard problem={item.problem} />
                <div className="flex items-center gap-2 px-1 pt-2">
                  <Tag>{`score ${item.score}`}</Tag>
                </div>
                <ReasonList reasons={item.reasons} />
              </div>
            ))}
          </div>
        ) : null}
      </section>
    </main>
  );
}
