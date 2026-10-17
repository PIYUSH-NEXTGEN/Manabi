import { useQuery } from '@tanstack/react-query';
import { ApiError, getMe, type MeOut } from '@/api/client';

export function useMe() {
  return useQuery<MeOut, ApiError>({
    queryKey: ['auth', 'me'],
    queryFn: getMe,
    retry: false,
    staleTime: 60_000,
  });
}
