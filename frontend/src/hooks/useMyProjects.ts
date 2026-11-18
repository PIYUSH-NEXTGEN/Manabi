import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
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

export function useMyProjects() {
  const me = useMe();

  return useQuery<ProjectOut[], ApiError>({
    queryKey: ['me', 'projects', me.data?.id ?? 'anon'],
    queryFn: getMyProjects,
    enabled: Boolean(me.data),
  });
}

function useInvalidateProjects() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: ['me'] });
    void queryClient.invalidateQueries({ queryKey: ['project'] });
    void queryClient.invalidateQueries({ queryKey: ['problem'] });
    // Board cards, their counts and the facets all live under ['problems'].
    void queryClient.invalidateQueries({ queryKey: ['problems'] });
  };
}

export function useDeleteProject() {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (id: number) => deleteProject(id),
    onSuccess: invalidate,
  });
}

export function usePatchProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (body: ProjectPatch) => patchProject(projectId, body),
    onSuccess: invalidate,
  });
}

export function useReportProject(projectId: number) {
  return useMutation({
    mutationFn: (reason: string) => reportProject(projectId, { reason }),
  });
}

export function useStarProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: () => starProject(projectId),
    onSuccess: invalidate,
  });
}

export function useUnstarProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: () => unstarProject(projectId),
    onSuccess: invalidate,
  });
}

export function useStarProblem(problemId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: () => starProblem(problemId),
    onSuccess: invalidate,
  });
}

export function useUnstarProblem(problemId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: () => unstarProblem(problemId),
    onSuccess: invalidate,
  });
}
