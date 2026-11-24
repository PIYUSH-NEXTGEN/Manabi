import { useToast } from '@/design/primitives';
import { ApiError } from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { isPostHogConfigured, posthog } from '@/lib/posthog';
import {
  useStarProblem,
  useStarProject,
  useUnstarProblem,
  useUnstarProject,
} from '@/hooks/useMyProjects';

export type StarKind = 'problem' | 'project';

const STAR_EVENTS = {
  problem: { starred: 'problem_starred', unstarred: 'problem_unstarred' },
  project: { starred: 'project_starred', unstarred: 'project_unstarred' },
} as const;

/**
 * Star/unstar behavior shared by the problem, project and mini star buttons.
 * Only the markup differs between them (button size, label casing), so this
 * keeps the 409 handling and toast copy in one place.
 */
export function useStarToggle(kind: StarKind, id: number, starred: boolean) {
  const me = useMe();
  const toast = useToast();
  const starProblem = useStarProblem(id);
  const unstarProblem = useUnstarProblem(id);
  const starProject = useStarProject(id);
  const unstarProject = useUnstarProject(id);

  const noun = kind;
  const star = kind === 'problem' ? starProblem : starProject;
  const unstar = kind === 'problem' ? unstarProblem : unstarProject;

  function toggle() {
    if (starred) {
      unstar.mutate(undefined, {
        onSuccess: () => {
          if (isPostHogConfigured) {
            posthog.capture(STAR_EVENTS[kind].unstarred, { target_id: id });
          }
        },
        onError: () => toast(`Could not un-star the ${noun}. Try again.`, 'error'),
      });
      return;
    }
    star.mutate(undefined, {
      onSuccess: () => {
        if (isPostHogConfigured) {
          posthog.capture(STAR_EVENTS[kind].starred, { target_id: id });
        }
        toast('Starred. Thanks for the signal.');
      },
      onError: (error) => {
        if (error instanceof ApiError && error.status === 409) {
          toast(`You already starred this ${noun}.`, 'error');
        } else {
          toast(`Could not star the ${noun}. Try again.`, 'error');
        }
      },
    });
  }

  return {
    loggedIn: Boolean(me.data),
    pending: star.isPending || unstar.isPending,
    toggle,
  };
}
