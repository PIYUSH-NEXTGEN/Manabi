import { useQuery } from '@tanstack/react-query';
import { ApiError, getRecommendations, type RecommendationsOut } from '@/api/client';
import { useMe } from '@/hooks/useMe';

export function useRecommendations() {
  const me = useMe();

  return useQuery<RecommendationsOut, ApiError>({
    queryKey: ['recommendations', me.data?.id ?? 'anon'],
    queryFn: getRecommendations,
    enabled: Boolean(me.data),
    staleTime: 60_000,
  });
}
