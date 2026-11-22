import { useMutation, useQuery } from '@tanstack/react-query';
import {
  deleteProject,
  getMyProjects,
  patchProject,
  reportProject,
  starProblem,
  starProject,
  unstarProblem,
  unstarProject,
  type ApiError,
  type ProjectOut,
  type ProjectPatch,
} from '@/api/client';
import { useInvalidateCatalogData } from '@/lib/queryCache';

/**
 * The dashboard list is keyed without the user id so `RequireAuth` can start
 * the fetch while it is still resolving the session, instead of waiting for
 * `/api/auth/me` and then starting a second round trip.
 */
export const MY_PROJECTS_QUERY_KEY = ['me', 'projects'] as const;

export function useMyProjects() {
  return useQuery<ProjectOut[], ApiError>({
    queryKey: MY_PROJECTS_QUERY_KEY,
    queryFn: getMyProjects,
  });
}

export function useDeleteProject() {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: (id: number) => deleteProject(id),
    onSuccess: invalidate,
  });
}

export function usePatchProject(projectId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: (body: ProjectPatch) => patchProject(projectId, body),
    onSuccess: invalidate,
  });
}

export function useReportProject(projectId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: (reason: string) => reportProject(projectId, { reason }),
    // The third report can move the project back to human review.
    onSuccess: invalidate,
  });
}

export function useStarProject(projectId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: () => starProject(projectId),
    onSuccess: invalidate,
  });
}

export function useUnstarProject(projectId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: () => unstarProject(projectId),
    onSuccess: invalidate,
  });
}

export function useStarProblem(problemId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: () => starProblem(problemId),
    onSuccess: invalidate,
  });
}

export function useUnstarProblem(problemId: number) {
  const invalidate = useInvalidateCatalogData();
  return useMutation({
    mutationFn: () => unstarProblem(problemId),
    onSuccess: invalidate,
  });
}
