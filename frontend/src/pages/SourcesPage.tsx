import { safeExternalUrl } from '@/lib/url';
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import type { ApiError, ProblemsListOut, FacetsOut } from '@/api/client';
import type { UseQueryResult } from '@tanstack/react-query';
import { useFacets } from '@/hooks/useFacets';
import { useProblems } from '@/hooks/useProblems';
import { Skeleton } from '@/design/primitives';
import { StaticShell } from './StaticShell';

interface SourceRow {
  name: string;
  count: number;
  url: string | null;
  note: string | null;
}

function mergeSources(
  facets: FacetsOut | undefined,
  problems: ProblemsListOut | undefined,
): SourceRow[] {
  if (!facets) {
    return [];
  }
  const urlNotes = new Map<string, { url: string | null; note: string | null }>();
  for (const problem of problems?.items ?? []) {
    const existing = urlNotes.get(problem.source_name);
    if (!existing || (!existing.url && problem.source_url)) {
      urlNotes.set(problem.source_name, {
        url: problem.source_url ?? existing?.url ?? null,
        note: problem.source_note ?? existing?.note ?? null,
      });
    }
  }

  return facets.sources.map((facet) => ({
    name: facet.value,
    count: facet.count,
    url: urlNotes.get(facet.value)?.url ?? null,
    note: urlNotes.get(facet.value)?.note ?? null,
  }));
}

function SourceList({
  facets,
  problems,
}: {
  facets: UseQueryResult<FacetsOut, ApiError>;
  problems: UseQueryResult<ProblemsListOut, ApiError>;
}) {
  if (facets.isLoading || problems.isLoading) {
    return (
      <div aria-busy="true" className="flex flex-col gap-3">
        <Skeleton className="h-14" />
        <Skeleton className="h-14" />
        <Skeleton className="h-14" />
      </div>
    );
  }

  if (facets.isError) {
    return (
      <p role="alert" className="border-[3px] border-ink bg-white p-4 shadow-hard-sm">
        Could not load sources — {facets.error.detail}
      </p>
    );
  }

  const rows = mergeSources(facets.data, problems.data);

  if (rows.length === 0) {
    return (
      <p className="border-[3px] border-ink bg-white p-4">
        No sources yet. Once problems are imported from a source, it shows up
        here with its own entry.
      </p>
    );
  }

  return (
    <dl className="flex flex-col">
      {rows.map((row) => (
        <div
          key={row.name}
          className="flex flex-col gap-1 border-[3px] border-ink bg-white p-4 shadow-hard-sm md:flex-row md:items-start md:justify-between"
        >
          <div>
            <dt className="font-mono text-sm font-bold uppercase tracking-widest">
              {row.name}
            </dt>
            {row.note ? <dd className="mt-1 text-xs">{row.note}</dd> : null}
            {safeExternalUrl(row.url) ? (
              <dd className="mt-1 text-xs">
                <a
                  href={safeExternalUrl(row.url) ?? undefined}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue underline underline-offset-4"
                >
                  {row.url} ↗
                </a>
              </dd>
            ) : null}
          </div>
          <dd className="shrink-0 font-mono text-[11px] font-bold uppercase tracking-widest">
            {row.count} {row.count === 1 ? 'problem' : 'problems'}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function SourcesPage() {
  const facets = useFacets();
  const problems = useProblems({ limit: 100 });
  const location = useLocation();

  useEffect(() => {
    if (location.hash === '#credits') {
      document.getElementById('credits')?.scrollIntoView();
    }
  }, [location.hash]);

  return (
    <StaticShell kicker="Sources" title="Sources" wide>
      <p>
        Every problem card links back to the organisation that published it.
        Where a source states a link or a status note, it is shown here
        unchanged.
      </p>

      <SourceList facets={facets} problems={problems} />

      <section
        id="credits"
        className="border-[3px] border-ink bg-yellow p-5 shadow-hard"
      >
        <h2 className="font-display text-xl uppercase">Data &amp; credits</h2>
        <p className="mt-2">
          Problem text belongs to the publishing organisations. MANABI stores
          the original statement verbatim next to every brief and credits the
          source on each card. Nothing here claims ownership of the source
          content — it indexes it, with a link back.
        </p>
      </section>
    </StaticShell>
  );
}
