import { useMutation } from '@tanstack/react-query';
import { useEffect, useRef, useState, type FormEvent } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  ArrowUp,
  ArrowUpRight,
  LoaderCircle,
  LockKeyhole,
  MessageSquare,
  Sparkles,
  X,
} from 'lucide-react';
import { cx } from '@/lib/cx';
import { fieldLabel } from '@/lib/fields';
import { buttonClasses } from '@/design/primitives';
import { EASE_SNAP } from '@/design/motion';
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

const SUGGESTIONS = [
  'I know Python and pandas. Find me a weekend data project.',
  'I build with React and want a portfolio project.',
  'I want an ML project for my resume.',
  'Show me something with APIs and auth.',
];

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
    <div className="mt-2.5 flex flex-col gap-2">
      {problems.map((problem) => (
        <Link
          key={problem.id}
          to={`/problems/${problem.id}`}
          className="group relative block rounded-xl border border-line bg-paper py-2.5 pl-3 pr-9 text-[0.875rem] font-semibold leading-snug text-ink transition-colors hover:border-ink/20 hover:bg-tint/60"
        >
          {problem.title}
          <span className="mt-0.5 block font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-muted">
            {fieldLabel(problem.field)} · {problem.difficulty}
          </span>
          <ArrowUpRight
            aria-hidden
            size={13}
            className="absolute right-3 top-2.5 text-muted transition-colors group-hover:text-ink"
          />
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
  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    function handleOpen() {
      setOpen(true);
    }
    window.addEventListener(OPEN_CHAT_EVENT, handleOpen);
    return () => window.removeEventListener(OPEN_CHAT_EVENT, handleOpen);
  }, []);

  useEffect(() => {
    const node = textareaRef.current;
    if (!node) return;
    node.style.height = 'auto';
    node.style.height = `${Math.min(node.scrollHeight, 112)}px`;
  }, [draft]);

  const chat = useMutation<ChatOut, Error, ChatMessage[]>({
    mutationFn: (history) =>
      postChat({
        messages: history.slice(-MAX_HISTORY),
        page_context: pageContext(location.pathname),
      }),
    onSuccess: (reply) => {
      setEntries((current) => [
        ...current,
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

  useEffect(() => {
    const node = scrollRef.current;
    if (!node) return;
    node.scrollTop = node.scrollHeight;
  }, [entries, chat.isPending]);

  function send() {
    if (chat.isPending) return;
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

  function applySuggestion(prompt: string) {
    setDraft(prompt);
    textareaRef.current?.focus();
  }

  if (!open) {
    return (
      <motion.button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Open the MANABI chat"
        whileHover={{ y: -2 }}
        whileTap={{ scale: 0.98 }}
        transition={{ duration: 0.18, ease: EASE_SNAP }}
        className="press group fixed bottom-4 right-4 z-40 inline-flex items-center gap-2.5 rounded-full border border-line bg-ink p-1.5 pr-4 text-paper shadow-lift lg:bottom-5 lg:right-5"
      >
        <span className="relative flex size-10 items-center justify-center rounded-full bg-accent text-paper">
          <MessageSquare aria-hidden size={16} strokeWidth={2.2} />
        </span>
        <span className="pr-1 text-[0.875rem] font-semibold tracking-[-0.01em]">
          Ask Ai
        </span>
      </motion.button>
    );
  }

  const userInitial = (me.data?.name ?? me.data?.username ?? 'You')
    .trim()
    .charAt(0)
    .toUpperCase();

  return (
    <motion.section
      aria-label="MANABI chat"
      aria-busy={chat.isPending}
      initial={{ opacity: 0, y: 18, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.24, ease: EASE_SNAP }}
      className="fixed bottom-4 right-4 z-40 flex h-[min(620px,calc(100dvh-2rem))] w-[min(410px,calc(100vw-2rem))] flex-col overflow-hidden rounded-[1.75rem] border border-line bg-sheet/95 shadow-lift backdrop-blur-xl lg:bottom-5 lg:right-5"
    >
      <header className="relative border-b border-line bg-sheet px-4 pb-3 pt-4">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h2 className="truncate text-[0.9375rem] font-semibold tracking-[-0.01em] text-ink">
                Ask Manabi
              </h2>
              <span className="rounded-full bg-lime/15 px-2 py-0.5 font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-olive dark:text-lime">
                online
              </span>
            </div>
            <p className="mt-0.5 truncate text-[0.6875rem] leading-relaxed text-ink-soft">
              Finds real project briefs for your skills.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close the chat"
            className="press -mr-1 -mt-1 flex size-8 shrink-0 items-center justify-center rounded-full text-ink-soft transition-colors hover:bg-tint hover:text-ink"
          >
            <X aria-hidden size={16} strokeWidth={2.2} />
          </button>
        </div>

        <div className="mt-3 flex items-center justify-between gap-2 rounded-xl border border-line bg-tint/35 px-2.5 py-1.5">
          <span className="flex items-center gap-1.5 font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-muted">
            <LockKeyhole aria-hidden size={10} strokeWidth={2.4} />
            Catalog only
          </span>
          <span className="font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-muted">
            No outside links
          </span>
        </div>
      </header>

      {me.isPending ? (
        <div className="flex flex-1 flex-col gap-3 p-4">
          <div className="skeleton h-20 w-3/4 rounded-2xl" />
          <div className="skeleton ml-auto h-10 w-1/2 rounded-full" />
          <div className="skeleton h-16 w-5/6 rounded-2xl" />
        </div>
      ) : !me.data ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-4 px-6 text-center">
          <span className="flex size-12 items-center justify-center rounded-2xl border border-line bg-tint text-ink">
            <LockKeyhole aria-hidden size={20} strokeWidth={2} />
          </span>
          <div>
            <p className="text-[0.9375rem] font-semibold text-ink">Members only</p>
            <p className="mt-1 text-body leading-relaxed text-ink-soft">
              Log in with GitHub to ask Manabi what to build next.
            </p>
          </div>
          <a
            href="/api/auth/github/login"
            className={cx(buttonClasses('primary'), 'w-full max-w-[15rem]')}
          >
            Log in with GitHub
          </a>
        </div>
      ) : (
        <>
          <div
            ref={scrollRef}
            className="chat-scroll flex-1 overflow-y-auto overscroll-contain bg-paper/45 px-4 py-4"
            role="log"
            aria-live="polite"
            aria-relevant="additions text"
          >
            {entries.length === 0 && !chat.isPending ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.28, ease: EASE_SNAP }}
                className="flex h-full flex-col justify-center"
              >
                <div className="rounded-2xl border border-line bg-sheet p-4 shadow-soft">
                  <span className="flex size-9 items-center justify-center rounded-xl bg-accent-soft text-ink">
                    <Sparkles aria-hidden size={16} strokeWidth={2.1} />
                  </span>
                  <p className="mt-3 text-[0.9375rem] font-semibold text-ink">
                    Start with your strongest side.
                  </p>
                  <p className="mt-1.5 text-body leading-relaxed text-ink-soft">
                    Tell it what you know and what you want to build. It finds
                    problems that fit, scoped for a weekend, and it only ever
                    points at real problems already in the index.
                  </p>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {SUGGESTIONS.map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => applySuggestion(prompt)}
                      className="press rounded-full border border-line bg-sheet px-2.5 py-1.5 text-left text-[0.6875rem] font-semibold leading-snug text-ink-soft transition-colors hover:border-ink/20 hover:bg-tint hover:text-ink"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </motion.div>
            ) : (
              <ul className="space-y-4">
                {entries.map((entry, index) => {
                  const isUser = entry.message.role === 'user';
                  const isLast = index === entries.length - 1;
                  const sending = isUser && isLast && chat.isPending;

                  return (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, y: 10, filter: 'blur(3px)' }}
                      animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
                      transition={{ duration: 0.26, ease: EASE_SNAP }}
                      className={cx('flex items-start gap-2.5', isUser && 'flex-row-reverse')}
                    >
                      <span
                        className={cx(
                          'mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-xl text-[0.625rem] font-bold',
                          isUser
                            ? 'border border-line bg-accent-soft text-ink'
                            : 'bg-ink text-paper',
                        )}
                      >
                        {isUser ? userInitial : <Sparkles aria-hidden size={13} />}
                      </span>

                      <div
                        className={cx(
                          'flex max-w-[82%] flex-col gap-1',
                          isUser ? 'items-end' : 'items-start',
                        )}
                      >
                        <div
                          className={cx(
                            'rounded-2xl px-3.5 py-2.5 text-body leading-relaxed',
                            isUser
                              ? 'rounded-tr-md border border-sky/25 bg-accent-soft text-ink'
                              : 'rounded-tl-md border border-line bg-sheet text-ink shadow-soft',
                          )}
                        >
                          {isUser ? (
                            <p className="whitespace-pre-wrap">{entry.message.content}</p>
                          ) : (
                            <Markdown problemsAsLinks>{entry.message.content}</Markdown>
                          )}
                          {entry.problems && entry.problems.length > 0 ? (
                            <ReplyProblems problems={entry.problems} />
                          ) : null}
                        </div>

                        {sending ? (
                          <span className="flex items-center gap-1.5 pr-1 font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-muted">
                            <span aria-hidden className="flex items-center gap-0.5">
                              <span className="thinking-dot size-1 rounded-full bg-current" />
                              <span className="thinking-dot size-1 rounded-full bg-current" />
                              <span className="thinking-dot size-1 rounded-full bg-current" />
                            </span>
                            Sending
                          </span>
                        ) : null}
                      </div>
                    </motion.li>
                  );
                })}
                {chat.isPending ? <ThinkingIndicator /> : null}
              </ul>
            )}
          </div>

          {error ? (
            <div
              role="alert"
              className="border-t border-line bg-danger-soft/45 px-4 py-2.5 text-[0.8125rem] font-semibold leading-snug text-danger"
            >
              <p>{error}</p>
              {retryAfter != null ? <RetryCountdown seconds={retryAfter} /> : null}
            </div>
          ) : null}

          <form
            noValidate
            onSubmit={handleSubmit}
            className="border-t border-line bg-sheet p-3"
          >
            <div className="rounded-[1.35rem] border border-line bg-paper p-1.5 shadow-soft transition-[border-color,box-shadow] duration-200 focus-within:border-ink/25 focus-within:ring-4 focus-within:ring-sky/20 dark:focus-within:ring-sky/10">
              <label htmlFor="chat-message" className="sr-only">
                Message Manabi
              </label>
              <textarea
                ref={textareaRef}
                id="chat-message"
                rows={1}
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    send();
                  }
                }}
                placeholder="What do you want to build?"
                maxLength={MAX_MESSAGE_LENGTH}
                autoComplete="off"
                autoFocus
                className="chat-composer max-h-28 min-h-10 w-full resize-none overflow-y-auto border-0 bg-transparent px-2 py-1.5 text-body leading-relaxed text-ink outline-none placeholder:text-muted"
              />

              <div className="mt-1 flex items-center justify-between gap-3 px-1.5 pb-0.5">
                <span
                  className={cx(
                    'font-mono text-[0.5625rem] font-bold tabular-nums tracking-[0.1em]',
                    draft.length > MAX_MESSAGE_LENGTH - 50
                      ? 'text-danger'
                      : 'text-muted',
                  )}
                >
                  {draft.length}/{MAX_MESSAGE_LENGTH}
                </span>

                <motion.button
                  type="submit"
                  disabled={chat.isPending || draft.trim().length === 0}
                  whileTap={{ scale: 0.96 }}
                  transition={{ duration: 0.14, ease: EASE_SNAP }}
                  className="press inline-flex h-9 items-center justify-center gap-1.5 rounded-full bg-accent px-3.5 text-[0.8125rem] font-semibold text-paper shadow-soft transition-colors hover:bg-ink disabled:pointer-events-none disabled:bg-tint disabled:text-muted disabled:shadow-none"
                >
                  {chat.isPending ? (
                    <LoaderCircle aria-hidden size={14} className="animate-spin" />
                  ) : (
                    <ArrowUp aria-hidden size={14} strokeWidth={2.6} />
                  )}
                  {chat.isPending ? 'Sending' : 'Send'}
                </motion.button>
              </div>
            </div>
          </form>
        </>
      )}
    </motion.section>
  );
}
