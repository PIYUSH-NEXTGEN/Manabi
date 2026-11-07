import { useQuery } from '@tanstack/react-query';
import { ApiError, getGithubHeatmap, type HeatmapOut } from '@/api/client';

export function useGithubHeatmap() {
  return useQuery<HeatmapOut, ApiError>({
    queryKey: ['github', 'heatmap'],
    queryFn: getGithubHeatmap,
    staleTime: 5 * 60 * 1000,
    refetchInterval: 15 * 60 * 1000,
  });
}
