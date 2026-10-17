import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useState, type ChangeEvent, type FormEvent, type ReactNode } from 'react';
import { cx } from '@/lib/cx';
import {
  buttonClasses,
  Input,
  Stamp,
  useToast,
} from '@/design/primitives';
import { useMe } from '@/hooks/useMe';
import {
  ApiError,
  createProblem,
  ingestStatement,
  type IngestOut,
  type ProblemCardDraft,
} from '@/api/client';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';
const smallMono = 'font-mono text-[10px] font-bold uppercase tracking-widest';

const FIELD_LABELS: Record<string, string> = {
  title: 'Title',
  summary: 'Summary',
  who_affected: 'Who is affected',
  why_matters: 'Why it matters',
  field: 'Field',
  domain: 'Domain',
  difficulty: 'Difficulty',
  est_hours: 'Estimated hours',
  tech_tags: 'Tech',
  datasets: 'Datasets',
  approaches: 'Approaches',
  source_name: 'Source name',
  source_id: 'Source id',
  source_url: 'Source URL',
  source_note: 'Source note',
  ai_fields: 'AI fields',
};

function Row({ label, value }: { label: ReactNode; value: string }) {
  return (
    <div className="grid gap-1 py-3 sm:grid-cols-[190px_1fr] sm:gap-3">
      <dt className={smallMono}>{label}</dt>
      <dd className="text-sm leading-snug whitespace-pre-wrap">{value}</dd>
    </div>
  );
}

function StampLabel({ text }: { text: string }) {
  return (
    <span className="flex flex-wrap items-center gap-1.5">
      {text}
      <Stamp tone="ai-suggested" label="AI-SUGGESTED" rotate={-2} />
    </span>
  );
}

function DraftPreview({
  draft,
  evidence,
}: {
  draft: ProblemCardDraft;
  evidence: Record<string, string>;
}) {
  const sortedEntries = Object.entries(evidence).sort(([a], [b]) =>
    a.localeCompare(b),
  );

  return (
    <section
      aria-label="Structured draft"
      className="border-[3px] border-ink bg-white p-4 shadow-hard"
    >
      <h2 className={panelHeading}>Structured draft — verify before publishing</h2>
      <dl className="mt-2 divide-y divide-ink/10">
        <Row label="Title" value={draft.title} />
        <Row label="Summary" value={draft.summary} />
        <Row
          label={<StampLabel text="Who is affected" />}
          value={draft.who_affected}
        />
        <Row
          label={<StampLabel text="Why it matters" />}
          value={draft.why_matters}
        />
        <Row
          label={<StampLabel text="Approaches" />}
          value={draft.approaches.join('\n')}
        />
        <Row
          label={<StampLabel text="Difficulty · hours" />}
          value={`${draft.difficulty}${draft.est_hours != null ? ` · ${draft.est_hours}h` : ''}`}
        />
        <Row label="Tech" value={draft.tech_tags.join(', ') || 'none'} />
        <Row
          label="Source"
          value={
            [
              draft.source_name,
              draft.source_id,
              draft.source_url,
              draft.source_note,
            ]
              .filter(Boolean)
              .join(' · ') || 'none'
          }
        />
      </dl>

      <h3 className={cx(panelHeading, 'mt-4')}>
        Evidence (citations behind each AI-drafted field)
      </h3>
      <ul className="ml-4 mt-2 list-disc space-y-1 text-sm leading-snug">
        {(
          sortedEntries.length > 0
            ? sortedEntries
            : [['—', 'No evidence returned for this statement.']]
        ).map(([field, citation]) => (
          <li key={field}>
            <span className={smallMono}>
              {FIELD_LABELS[field] ?? field}
            </span>
            : {citation}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function IngestPage() {
  const me = useMe();
  const toast = useToast();
  const queryClient = useQueryClient();

  const [text, setText] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [result, setResult] = useState<IngestOut | null>(null);
  const [ingestError, setIngestError] = useState<string | null>(null);
  const [publishedProblemId, setPublishedProblemId] = useState<number | null>(
    null,
  );

  const ingest = useMutation<IngestOut, Error>({
    mutationFn: () =>
      ingestStatement({
        text: text.trim() || undefined,
        url: sourceUrl.trim() || undefined,
      }),
    onSuccess: (value) => {
      setResult(value);
      setIngestError(null);
    },
    onError: (error) => {
      setIngestError(
        error instanceof ApiError
          ? error.detail
          : 'Storing this statement failed. Try again.',
      );
    },
  });

  const publish = useMutation({
    mutationFn: (value: IngestOut) =>
      createProblem({
        ...value.draft,
        datasets: value.draft.datasets.map((dataset) => ({
          name:
            typeof dataset.name === 'string' && dataset.name.length > 0
              ? dataset.name
              : 'Unnamed dataset',
          url: typeof dataset.url === 'string' ? dataset.url : null,
        })),
        ai_fields: Object.keys(value.evidence),
      }),
    onSuccess: (problem) => {
      setPublishedProblemId(problem.id);
      queryClient.invalidateQueries({ queryKey: ['problems'] });
      queryClient.setQueryData(['problem', problem.id], problem);
      toast('Published to the board — anyone can claim it now.');
    },
    onError: (error) => {
      toast(
        error instanceof ApiError
          ? error.detail
          : 'Publishing failed — try again.',
        'error',
      );
    },
  });

  function handleIngest(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setValidationError(null);
    setIngestError(null);
    setResult(null);
    setPublishedProblemId(null);

    if (!text.trim() && !sourceUrl.trim()) {
      setValidationError(
        'Paste the problem statement text, or give a URL to it.',
      );
      return;
    }
    if (!me.data) {
      setIngestError(
        'Log in with GitHub first — the backend rate-limits AI ingestion per user.',
      );
      return;
    }
    ingest.mutate();
  }

  function handleTextChange(event: ChangeEvent<HTMLTextAreaElement>) {
    setText(event.target.value);
  }

  function handleUrlChange(event: ChangeEvent<HTMLInputElement>) {
    setSourceUrl(event.target.value);
  }

  function handlePublish() {
    if (result) publish.mutate(result);
  }

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(900px,96vw)] py-12">
        <p className={smallMono}>Problem ingestion</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-none md:text-6xl">
          Ingest
        </h1>
        <p className="mt-3 max-w-2xl text-lg leading-snug">
          Paste a real problem statement (or a URL to one). The AI drafts a
          structured card, with citations for every invented field. You verify,
          then publish it to the board.
        </p>

        <form
          noValidate
          onSubmit={handleIngest}
          className="mt-8 flex flex-col gap-4 border-[3px] border-ink bg-white p-4 shadow-hard"
        >
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="ingest-text"
              className={smallMono}
            >
              Problem statement (paste verbatim)
            </label>
            <textarea
              id="ingest-text"
              value={text}
              onChange={handleTextChange}
              rows={8}
              placeholder="Copy the full original statement here — do not paraphrase it."
              aria-invalid={validationError ? true : undefined}
              aria-describedby={validationError ? 'ingest-text-error' : undefined}
              className="field w-full"
            />
          </div>
          <Input
            label="Source URL (optional — where the statement lives)"
            type="url"
            placeholder="https://example.org/problem-brief"
            value={sourceUrl}
            onChange={handleUrlChange}
          />
          {validationError ? (
            <p
              id="ingest-text-error"
              role="alert"
              className={cx(smallMono, 'text-red')}
            >
              {validationError}
            </p>
          ) : null}
          <button
            type="submit"
            disabled={ingest.isPending}
            className={cx(buttonClasses('primary'), 'self-start')}
          >
            {ingest.isPending
              ? 'Drafting — the AI can take a minute…'
              : 'Draft the card'}
          </button>
          {ingestError ? (
            <p role="alert" className={cx(smallMono, 'text-red')}>
              {ingestError}
            </p>
          ) : null}
        </form>

        {result ? (
          <div className="mt-6 flex flex-col gap-4">
            <DraftPreview draft={result.draft} evidence={result.evidence} />
            {me.data ? (
              publishedProblemId ? (
                <section className="border-[3px] border-ink bg-white p-4 shadow-hard">
                  <h2 className={panelHeading}>Published</h2>
                  <p className="mt-2 text-sm">
                    It is on the board now.
                  </p>
                  <Link
                    to={`/problems/${publishedProblemId}`}
                    className={cx(buttonClasses('primary'), 'mt-3 self-start')}
                  >
                    Open the card
                  </Link>
                </section>
              ) : (
                <button
                  type="button"
                  onClick={handlePublish}
                  disabled={publish.isPending}
                  className={cx(buttonClasses('primary'), 'self-start')}
                >
                  {publish.isPending
                    ? 'Publishing…'
                    : 'Publish to the board'}
                </button>
              )
            ) : (
              <section className="border-[3px] border-ink bg-white p-4 shadow-hard">
                <h2 className={panelHeading}>Publishing needs a login</h2>
                <p className="mt-2 text-sm leading-snug">
                  Log in with GitHub to publish this card to the public board.
                </p>
                <a
                  href="/api/auth/github/login"
                  className={cx(buttonClasses('primary'), 'mt-3 self-start')}
                >
                  Log in with GitHub
                </a>
              </section>
            )}
          </div>
        ) : null}
      </div>
    </main>
  );
}
