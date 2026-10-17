import { useQuery } from '@tanstack/react-query';
import { ApiError, getStats, type StatsOut } from '@/api/client';

export function useStats() {
  return useQuery<StatsOut, ApiError>({
    queryKey: ['stats'],
    queryFn: getStats,
  });
}
