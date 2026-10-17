import { useMutation } from '@tanstack/react-query';
import { useEffect, useState, type FormEvent } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { buttonClasses, Stamp } from '@/design/primitives';
import {
  ApiError,
  postChat,
  type ChatMessage,
  type ChatOut,
  type ChatProblemItem,
} from '@/api/client';
import { Markdown } from '@/components/markdown/Markdown';

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
          className="border-[3px] border-ink bg-paper px-3 py-2 font-mono text-[11px] font-bold uppercase tracking-widest underline-offset-4 hover:underline"
        >
          {problem.title}
          <span className="ml-2 text-ink/60">
            {problem.field} · {problem.difficulty}
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
    },
    onError: (mutationError) => {
      setError(
        mutationError instanceof ApiError
          ? mutationError.detail
          : 'The chatbot is unreachable right now. Try again later.',
      );
    },
  });

  function send() {
    setError(null);

    const content = draft.trim();
    if (content.length === 0) return;
    if (content.length > MAX_MESSAGE_LENGTH) {
      setError('Keep each message under 1000 characters.');
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
        className="fixed bottom-4 right-4 z-40 border-[3px] border-ink bg-yellow px-4 py-3 font-mono text-xs font-bold uppercase tracking-widest text-ink shadow-lg press"
      >
        Ask Manabi
      </button>
    );
  }

  return (
    <section
      aria-label="MANABI chat"
      className="fixed bottom-4 right-4 z-40 flex h-[min(560px,80vh)] w-[min(380px,94vw)] flex-col border-[3px] border-ink bg-white shadow-lg"
    >
      <header className="flex items-center justify-between border-b-[3px] border-ink bg-ink px-3 py-2">
        <h2 className="font-mono text-xs font-bold uppercase tracking-widest text-paper">
          Ask Manabi
        </h2>
        <div className="flex items-center gap-2">
          <Stamp tone="new" label="catalog only" rotate={-3} />
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close the chat"
            className="border-[2px] border-paper px-2 font-mono text-xs font-bold uppercase tracking-widest text-paper hover:bg-black/20"
          >
            ×
          </button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-3" role="log" aria-live="polite">
        {entries.length === 0 ? (
          <p className="text-sm leading-snug">
            Tell it what you know and what you want to build. It finds problems
            that fit, scoped for a weekend — and it only ever points at real
            problems already in the index.
          </p>
        ) : (
          <ul className="space-y-3">
            {entries.map((entry, index) => (
              <li
                key={index}
                className={cx(
                  'max-w-[92%] border-[3px] border-ink p-2 text-sm leading-snug',
                  entry.message.role === 'user'
                    ? 'ml-auto bg-yellow/60'
                    : 'bg-white',
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
          </ul>
        )}
      </div>

      {error ? (
        <p
          role="alert"
          className="border-t-[3px] border-ink px-3 py-2 font-mono text-[11px] font-bold uppercase tracking-widest text-red"
        >
          {error}
        </p>
      ) : null}

      <form
        noValidate
        onSubmit={handleSubmit}
        className="flex gap-2 border-t-[3px] border-ink p-3"
      >
        <textarea
          rows={2}
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="What do you want to build? Which side is your strongest?"
          maxLength={MAX_MESSAGE_LENGTH}
          className="field flex-1 text-sm"
        />
        <button
          type="submit"
          disabled={chat.isPending}
          className={cx(buttonClasses('primary'), 'self-stretch')}
        >
          {chat.isPending ? 'Thinking…' : 'Send'}
        </button>
      </form>
    </section>
  );
}
