import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  completeProject,
  deleteProject,
  getMyProjects,
  patchProject,
  reopenProject,
  reportProject,
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

export function useCompleteProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (body: { demo_url?: string; reflection?: string }) =>
      completeProject(projectId, body),
    onSuccess: invalidate,
  });
}

export function useReopenProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: () => reopenProject(projectId),
    onSuccess: invalidate,
  });
}

export function useReportProject(projectId: number) {
  return useMutation({
    mutationFn: (reason: string) => reportProject(projectId, { reason }),
  });
}
