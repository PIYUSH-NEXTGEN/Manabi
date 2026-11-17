import { useQuery } from '@tanstack/react-query';
import { ApiError, getFacets, type FacetsOut, type FacetsQuery } from '@/api/client';

export function useFacets(filters: FacetsQuery = {}) {
  return useQuery<FacetsOut, ApiError>({
    queryKey: ['problems', 'facets', filters],
    queryFn: () => getFacets(filters),
  });
}
