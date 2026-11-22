import { useQuery } from '@tanstack/react-query';
import { ApiError, getProjectProgress, type Progress } from '@/api/client';

export function useProjectProgress(
  projectId: number,
  options: { enabled?: boolean } = {},
) {
  return useQuery<Progress, ApiError>({
    queryKey: ['project', projectId, 'progress'],
    queryFn: () => getProjectProgress(projectId, false),
    refetchOnWindowFocus: false,
    enabled: options.enabled ?? true,
  });
}
