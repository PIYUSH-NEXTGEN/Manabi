import { useQuery } from '@tanstack/react-query';
import { ApiError, getFacets, type FacetsOut } from '@/api/client';

export function useFacets() {
  return useQuery<FacetsOut, ApiError>({
    queryKey: ['problems', 'facets'],
    queryFn: getFacets,
  });
}
