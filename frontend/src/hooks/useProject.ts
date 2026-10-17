import { useQuery } from '@tanstack/react-query';
import { ApiError, getProject, type ProjectOut } from '@/api/client';

export function useProject(id: number | null) {
  return useQuery<ProjectOut, ApiError>({
    queryKey: ['project', id],
    queryFn: () => getProject(id as number),
    enabled: id != null,
  });
}
