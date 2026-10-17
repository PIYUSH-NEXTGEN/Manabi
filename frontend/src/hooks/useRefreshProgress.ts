import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getProjectProgress,
  type Progress,
  type ProjectOut,
} from '@/api/client';

export function useRefreshProgress(projectId: number) {
  const queryClient = useQueryClient();

  return useMutation<Progress, Error>({
    mutationFn: () => getProjectProgress(projectId, true),
    onSuccess: (progress) => {
      queryClient.setQueryData<ProjectOut>(['project', projectId], (old) =>
        old
          ? { ...old, progress, progress_updated_at: new Date().toISOString() }
          : old,
      );
    },
  });
}
