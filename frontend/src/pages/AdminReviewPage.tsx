import { useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { Button, Skeleton, Tag, useToast } from '@/design/primitives';
import {
  useAdminReview,
  useEditProblem,
  useModerateProblem,
} from '@/hooks/useAdmin';
import { useMe } from '@/hooks/useMe';
import { ApiError } from '@/api/client';
import { safeExternalUrl } from '@/lib/url';

const sectionHeading =
  'font-mono text-[11px] font-bold uppercase tracking-widest';

export function AdminReviewPage() {
  const me = useMe();
  const review = useAdminReview();
  const moderate = useModerateProblem();
  const edit = useEditProblem();
  const toast = useToast();
  const [editingId, setEditingId] = useState<number | null>(null);
  const [draftTitle, setDraftTitle] = useState('');
  const [draftSummary, setDraftSummary] = useState('');

  if (me.isPending) {
    return (
      <main className="mx-auto w-[min(1100px,96vw)] space-y-3 py-16">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-40" />
      </main>
    );
  }

  if (!me.data?.is_admin) {
    return (
      <main className="mx-auto w-[min(760px,96vw)] py-16">
        <h1 className="font-display text-4xl uppercase">Review queue</h1>
        <p className="mt-4 border border-ink bg-sheet p-4">
          Admin access required. Add your GitHub username to
          {' '}
          <code>ADMIN_GITHUB_USERNAMES</code> to use this page.
        </p>
      </main>
    );
  }

  function startEdit(id: number, title: string, summary: string) {
    setEditingId(id);
    setDraftTitle(title);
    setDraftSummary(summary);
  }

  function saveEdit(event: FormEvent) {
    event.preventDefault();
    if (editingId == null) return;
    edit.mutate(
      { id: editingId, body: { title: draftTitle, summary: draftSummary } },
      {
        onSuccess: () => {
          setEditingId(null);
          toast('Problem edited and flagged for review.');
        },
        onError: (error) =>
          toast(error instanceof ApiError ? error.detail : error.message, 'error'),
      },
    );
  }

  function runAction(
    id: number,
    action: 'approve' | 'reject' | 'unpublish',
  ) {
    moderate.mutate(
      { id, action },
      {
        onSuccess: () => toast(`Problem ${action}d.`),
        onError: (error) =>
          toast(error instanceof ApiError ? error.detail : error.message, 'error'),
      },
    );
  }

  return (
    <main className="mx-auto w-[min(1200px,96vw)] py-12">
      <p className="font-mono text-xs font-bold uppercase tracking-widest text-accent">
        Admin
      </p>
      <h1 className="mt-2 font-display text-4xl uppercase">Review queue</h1>
      <p className="mt-2 text-sm">
        Only published problems appear on the public board. Approve, edit, or
        reject problems before they go live.
      </p>

      {review.isError ? (
        <p role="alert" className="mt-6 border border-ink bg-sheet p-4">
          Could not load the queue — {review.error.detail}
        </p>
      ) : review.isPending ? (
        <Skeleton className="mt-6 h-48" />
      ) : review.data.items.length === 0 ? (
        <p className="mt-6 border border-ink bg-sheet p-4">
          Nothing waiting for review.
        </p>
      ) : (
        <ul className="mt-6 flex list-none flex-col gap-4">
          {review.data.items.map((problem) => {
            const sourceUrl = safeExternalUrl(problem.source_url);
            return (
              <li
                key={problem.id}
                className="border border-ink bg-sheet p-4"
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h2 className="font-display text-xl uppercase leading-tight">
                      {problem.title}
                    </h2>
                    <p className="mt-1 text-sm">{problem.summary}</p>
                  </div>
                  <div className="flex shrink-0 flex-col items-end gap-1">
                    <Tag>{problem.source_id ?? 'no id'}</Tag>
                  </div>
                </div>

                <p className={`${sectionHeading} mt-3`}>
                  {problem.source_name}
                  {problem.source_year ? ` · ${problem.source_year}` : ''}
                  {problem.organisation ? ` · ${problem.organisation}` : ''}
                </p>
                {sourceUrl ? (
                  <a
                    href={sourceUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm text-accent underline underline-offset-4"
                  >
                    View original ↗
                  </a>
                ) : null}

                <div className="mt-4 flex flex-wrap gap-2">
                  <Button onClick={() => runAction(problem.id, 'approve')}>
                    Approve
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => runAction(problem.id, 'reject')}
                  >
                    Reject
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => runAction(problem.id, 'unpublish')}
                  >
                    Unpublish
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() =>
                      startEdit(problem.id, problem.title, problem.summary)
                    }
                  >
                    Edit
                  </Button>
                </div>

                {editingId === problem.id ? (
                  <form
                    onSubmit={saveEdit}
                    className="mt-4 flex flex-col gap-2 border-t border-ink pt-4"
                  >
                    <label className={`${sectionHeading}`} htmlFor={`title-${problem.id}`}>
                      Title
                    </label>
                    <input
                      id={`title-${problem.id}`}
                      value={draftTitle}
                      onChange={(event) => setDraftTitle(event.target.value)}
                      className="border border-ink bg-paper px-3 py-2"
                    />
                    <label className={`${sectionHeading}`} htmlFor={`summary-${problem.id}`}>
                      Summary
                    </label>
                    <textarea
                      id={`summary-${problem.id}`}
                      value={draftSummary}
                      onChange={(event) => setDraftSummary(event.target.value)}
                      rows={4}
                      className="border border-ink bg-paper px-3 py-2"
                    />
                    <div className="flex gap-2">
                      <Button type="submit">Save edit</Button>
                      <Button
                        variant="secondary"
                        onClick={() => setEditingId(null)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </form>
                ) : null}
              </li>
            );
          })}
        </ul>
      )}

      <p className="mt-8">
        <Link to="/problems" className="font-mono text-xs underline">
          Back to the board
        </Link>
      </p>
    </main>
  );
}
