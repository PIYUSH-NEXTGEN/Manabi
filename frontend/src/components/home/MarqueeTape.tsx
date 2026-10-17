import type { UseQueryResult } from '@tanstack/react-query';
import type { ApiError, FacetsOut } from '@/api/client';
import { Marquee } from '@/design/primitives';

export function MarqueeTape({
  query,
}: {
  query: UseQueryResult<FacetsOut, ApiError>;
}) {
  if (query.isLoading) {
    return (
      <div aria-busy="true" className="border-y-[3px] border-ink">
        <div className="skeleton h-10" aria-hidden />
      </div>
    );
  }

  const sources = query.data?.sources ?? [];
  if (query.isError || sources.length === 0) {
    return null;
  }

  return <Marquee items={sources.map((source) => source.value)} label="Sources" />;
}
