import { useQuery } from '@tanstack/react-query';
import { ApiError, getMyProjects, type ProjectOut } from '@/api/client';
import { useMe } from '@/hooks/useMe';

export function useMyProjects() {
  const me = useMe();

  return useQuery<ProjectOut[], ApiError>({
    queryKey: ['me', 'projects', me.data?.id ?? 'anon'],
    queryFn: getMyProjects,
    enabled: Boolean(me.data),
  });
}
