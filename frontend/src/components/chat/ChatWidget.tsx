import { useMutation } from '@tanstack/react-query';
import { useEffect, useState, type FormEvent } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MessageSquare } from 'lucide-react';
import { cx } from '@/lib/cx';
import { fieldLabel } from '@/lib/fields';
import { buttonClasses, Stamp } from '@/design/primitives';
import { useMe } from '@/hooks/useMe';
import {
  ApiError,
  postChat,
  type ChatMessage,
  type ChatOut,
  type ChatProblemItem,
} from '@/api/client';
import { Markdown } from '@/components/markdown/Markdown';
import { RetryCountdown } from '@/components/common/RetryCountdown';
import { ThinkingIndicator } from './ThinkingIndicator';

const OPEN_CHAT_EVENT = 'manabi:open-chat';
const MAX_HISTORY = 6;
const MAX_MESSAGE_LENGTH = 500;

export function openChatWidget() {
  window.dispatchEvent(new CustomEvent(OPEN_CHAT_EVENT));
}

interface ChatEntry {
  message: ChatMessage;
  problems?: ChatProblemItem[];
}

export function pageContext(pathname: string) {
  const problemMatch = /^\/problems\/(\d+)$/.exec(pathname);
  return problemMatch ? { problem_id: Number(problemMatch[1]) } : undefined;
}

function ReplyProblems({ problems }: { problems: ChatProblemItem[] }) {
  if (problems.length === 0) return null;

  return (
    <div className="mt-2 flex flex-col gap-2">
      {problems.map((problem) => (
        <Link
          key={problem.id}
          to={`/problems/${problem.id}`}
          className="rounded-panel border border-line bg-paper px-3 py-2 text-[0.875rem] font-semibold text-ink underline-offset-4 hover:underline"
        >
          {problem.title}
          <span className="ml-2 text-ink/60">
            {fieldLabel(problem.field)} · {problem.difficulty}
          </span>
        </Link>
      ))}
    </div>
  );
}

export function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [entries, setEntries] = useState<ChatEntry[]>([]);
  const [draft, setDraft] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [retryAfter, setRetryAfter] = useState<number | null>(null);
  const me = useMe();
  const location = useLocation();

  useEffect(() => {
    function handleOpen() {
      setOpen(true);
    }
    window.addEventListener(OPEN_CHAT_EVENT, handleOpen);
    return () => window.removeEventListener(OPEN_CHAT_EVENT, handleOpen);
  }, []);

  const chat = useMutation<ChatOut, Error, ChatMessage[]>({
    mutationFn: (history) =>
      postChat({
        messages: history.slice(-MAX_HISTORY),
        page_context: pageContext(location.pathname),
      }),
    onSuccess: (reply, history) => {
      setEntries([
        ...history.map((message) => ({ message })),
        {
          message: { role: 'assistant', content: reply.reply },
          problems: reply.problems,
        },
      ]);
      setError(null);
      setRetryAfter(null);
    },
    onError: (mutationError) => {
      setError(
        mutationError instanceof ApiError
          ? mutationError.detail
          : 'The chatbot is unreachable right now. Try again later.',
      );
      setRetryAfter(
        mutationError instanceof ApiError
          ? mutationError.retryAfterSeconds
          : null,
      );
    },
  });

  function send() {
    setError(null);
    setRetryAfter(null);

    const content = draft.trim();
    if (content.length === 0) return;
    if (content.length > MAX_MESSAGE_LENGTH) {
      setError('Keep each message under 500 characters.');
      return;
    }

    const history: ChatMessage[] = [
      ...entries.map((entry) => entry.message),
      { role: 'user', content },
    ];
    setEntries([...entries, { message: { role: 'user', content } }]);
    setDraft('');
    chat.mutate(history);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    send();
  }

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Open the MANABI chat"
        className="press fixed bottom-4 right-4 z-40 inline-flex items-center gap-2 rounded-full bg-accent p-3.5 text-[0.875rem] font-semibold text-paper shadow-lift lg:bottom-5 lg:right-5 lg:px-5"
      >
        <MessageSquare aria-hidden size={16} strokeWidth={2.2} />
        <span className="hidden lg:inline">Ask Manabi</span>
      </button>
    );
  }

  return (
    <section
      aria-label="MANABI chat"
      className="fixed bottom-5 right-5 z-40 flex h-[min(560px,80vh)] w-[min(380px,94vw)] flex-col overflow-hidden rounded-card border border-line bg-sheet shadow-lift"
    >
      <header className="flex items-center justify-between bg-ink px-4 py-3">          <h2 className="text-[0.9375rem] font-semibold text-paper">
          Ask Manabi
        </h2>
        <div className="flex items-center gap-2">
          <Stamp tone="new" label="catalog only" rotate={-3} />
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close the chat"
            className="flex size-8 items-center justify-center rounded-full text-paper/80 hover:bg-white/10 hover:text-paper"
          >
            ×
          </button>
        </div>
      </header>

      {me.isPending ? (
        <div className="flex-1 p-3">
          <p className="text-body leading-snug">Checking whether you are logged in…</p>
        </div>
      ) : !me.data ? (
        <div className="flex flex-col gap-3 p-3">
          <p className="text-body leading-snug">
            The MANABI chat is for logged-in members. Log in with GitHub to
            continue.
          </p>
          <a
            href="/api/auth/github/login"
            className={cx(buttonClasses('primary'), 'self-start')}
          >
            Log in with GitHub
          </a>
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-y-auto p-3" role="log" aria-live="polite">
            {entries.length === 0 && !chat.isPending ? (
            <p className="text-body leading-snug">
              Tell it what you know and what you want to build. It finds problems
              that fit, scoped for a weekend, and it only ever points at real
              problems already in the index.
            </p>
            ) : (
              <ul className="space-y-3">
                {entries.map((entry, index) => (
                  <li
                    key={index}
                    className={cx(
                      'max-w-[92%] rounded-panel p-3 text-body leading-relaxed',
                      entry.message.role === 'user'
                        ? 'ml-auto rounded-br-sm bg-accent-soft text-ink'
                        : 'rounded-bl-sm border border-line bg-paper text-ink',
                    )}
                  >
                    {entry.message.role === 'assistant' ? (
                      <Markdown problemsAsLinks>
                        {entry.message.content}
                      </Markdown>
                    ) : (
                      <p>{entry.message.content}</p>
                    )}
                    {entry.problems && entry.problems.length > 0 ? (
                      <ReplyProblems problems={entry.problems} />
                    ) : null}
                  </li>
                ))}
                {chat.isPending ? <ThinkingIndicator /> : null}
              </ul>
            )}
          </div>

          {error ? (
            <div
              role="alert"
              className="border-t border-line bg-danger-soft/50 px-4 py-2.5 text-label font-semibold text-danger"
            >
              <p>{error}</p>
              {retryAfter != null ? (
                <RetryCountdown seconds={retryAfter} />
              ) : null}
            </div>
          ) : null}

          <form
            noValidate
            onSubmit={handleSubmit}
            className="flex gap-2 border-t border-line p-3"
          >
            <textarea
              rows={2}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                // Enter sends, Shift+Enter inserts a newline.
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault();
                  send();
                }
              }}
              placeholder="What do you want to build? Which side is your strongest? (Shift+Enter for a new line)"
              maxLength={MAX_MESSAGE_LENGTH}
              className="field flex-1 text-body"
            />
            <button
              type="submit"
              disabled={chat.isPending}
              className={cx(buttonClasses('primary'), 'self-stretch')}
            >
              {chat.isPending ? 'Thinking…' : 'Send'}
            </button>
          </form>
        </>
      )}
    </section>
  );
}
