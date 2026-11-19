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
import { useMe } from '@/hooks/useMe';
import { useInvalidateCatalogData } from '@/lib/queryCache';

export function useMyProjects() {
  const me = useMe();

  return useQuery<ProjectOut[], ApiError>({
    queryKey: ['me', 'projects', me.data?.id ?? 'anon'],
    queryFn: getMyProjects,
    enabled: Boolean(me.data),
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
