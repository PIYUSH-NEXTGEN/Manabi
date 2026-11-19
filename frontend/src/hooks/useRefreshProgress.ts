import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getProjectProgress,
  type Progress,
  type ProjectOut,
} from '@/api/client';
import { useInvalidateCatalogData } from '@/lib/queryCache';

export function useRefreshProgress(projectId: number) {
  const queryClient = useQueryClient();
  const invalidate = useInvalidateCatalogData();

  return useMutation<Progress, Error>({
    mutationFn: () => getProjectProgress(projectId, true),
    onSuccess: (progress) => {
      queryClient.setQueryData<ProjectOut>(['project', projectId], (old) =>
        old
          ? { ...old, progress, progress_updated_at: new Date().toISOString() }
          : old,
      );
      // A refresh can also change ownership/verification status and counts.
      invalidate();
    },
  });
}
