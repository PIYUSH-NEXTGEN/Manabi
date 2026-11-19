import { useQueryClient } from '@tanstack/react-query';

/**
 * Invalidate every cache that can change when a project is submitted, edited,
 * removed, verified, reported, starred, or refreshed.
 *
 * Server mutations already return the changed row, but derived data lives in
 * other queries: board cards/counts, facets, problem detail project lists,
 * the dashboard, stats, and the project's verification status. Centralizing
 * the keys here prevents a mutation from updating one view while leaving
 * another showing stale authorization/visibility state.
 */
const CATALOG_QUERY_KEYS = [
  ['me'],
  ['project'],
  ['problem'],
  ['problems'],
  ['stats'],
] as const;

export function useInvalidateCatalogData() {
  const queryClient = useQueryClient();

  return () => {
    for (const queryKey of CATALOG_QUERY_KEYS) {
      void queryClient.invalidateQueries({ queryKey });
    }
  };
}
