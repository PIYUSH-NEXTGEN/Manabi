import { useEffect, useRef, useState } from 'react';
import { motion, useInView } from 'motion/react';
import type { LucideIcon } from 'lucide-react';
import {
  Check,
  FileText,
  GitCommitHorizontal,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { Stamp } from '@/design/primitives';
import { EASE_SNAP } from '@/design/motion';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

const REPO_URL = 'github.com/you/your-repo';
const VERIFIED_SCORE = 0.82;
const SAMPLE_BRIEF = 'Crop disease triage for small farms';

const README_EXCERPT: { text: string; match?: boolean }[][] = [
  [{ text: 'Offline-first ' }, { text: 'mobile app', match: true }],
  [
    { text: 'Reads ' },
    { text: 'leaf photos', match: true },
    { text: ' for crop blight' },
  ],
  [
    { text: 'Routes cases to ' },
    { text: 'extension officers', match: true },
  ],
  [{ text: 'Built for ' }, { text: 'small farms', match: true }],
];

type GateState = 'idle' | 'active' | 'pass';

const GATES: {
  icon: LucideIcon;
  label: string;
  detail: Record<GateState, string>;
}[] = [
  {
    icon: ShieldCheck,
    label: 'Ownership',
    detail: {
      idle: 'must be yours',
      active: 'checking owner…',
      pass: 'you are the owner',
    },
  },
  {
    icon: FileText,
    label: 'README',
    detail: {
      idle: 'must exist',
      active: 'opening readme…',
      pass: 'found · explains the brief',
    },
  },
  {
    icon: GitCommitHorizontal,
    label: 'Commits',
    detail: {
      idle: '5 needed',
      active: 'counting commits…',
      pass: '14 commits',
    },
  },
];

const STATUS = [
  {
    text: 'Paste a public repo',
    hint: 'We only accept repos you own.',
  },
  {
    text: 'Checking ownership',
    hint: 'Forks and other people’s repos are rejected.',
  },
  {
    text: 'Reading the README',
    hint: 'It has to explain what you built.',
  },
  {
    text: 'Counting commits',
    hint: 'At least five commits are required.',
  },
  {
    text: 'AI relevance pass',
    hint: 'The README is matched against the brief.',
  },
  {
    text: 'Verified · live on the board',
    hint: 'Commits, README and issues now update from GitHub.',
  },
] as const;

const GATES_REVEAL = {
  hidden: {},
  show: { transition: { staggerChildren: 0.07 } },
};

const GATE_ITEM_REVEAL = {
  hidden: { opacity: 0, x: -8 },
  show: { opacity: 1, x: 0, transition: { duration: 0.3, ease: EASE_SNAP } },
};

function pad(value: number) {
  return String(value).padStart(2, '0');
}

function FieldLabel({ label, meta }: { label: string; meta?: string }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <span className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
        {label}
      </span>
      {meta ? (
        <span className="font-mono text-label font-bold uppercase tabular-nums tracking-[0.14em] text-muted/80">
          {meta}
        </span>
      ) : null}
    </div>
  );
}

function GateRow({
  icon: Icon,
  label,
  detail,
  state,
  animated,
}: {
  icon: LucideIcon;
  label: string;
  detail: Record<GateState, string>;
  state: GateState;
  animated: boolean;
}) {
  return (
    <motion.li
      variants={GATE_ITEM_REVEAL}
      className={cx(
        'relative flex items-center gap-2.5 border-b border-line py-2.5 pl-3 pr-1 transition-colors duration-300',
        state === 'pass' && 'bg-tint/40',
      )}
    >
      <motion.span
        aria-hidden
        className="absolute inset-y-0 left-0 w-0.5 origin-top bg-accent"
        initial={false}
        animate={{ scaleY: state === 'idle' ? 0 : 1 }}
        transition={{ duration: animated ? 0.24 : 0, ease: EASE_SNAP }}
      />
      <Icon
        aria-hidden
        size={13}
        strokeWidth={2.2}
        className={cx(
          'shrink-0 transition-colors duration-300',
          state === 'idle' ? 'text-muted' : 'text-ink',
        )}
      />
      <span
        className={cx(
          'font-mono text-label font-bold uppercase tracking-[0.14em] transition-colors duration-300',
          state === 'idle' ? 'text-muted' : 'text-ink',
        )}
      >
        {label}
      </span>
      <span
        className={cx(
          'ml-auto hidden font-mono text-label uppercase tracking-[0.12em] transition-colors duration-300 sm:inline',
          state === 'pass' ? 'text-ink-soft' : 'text-muted/60',
        )}
      >
        <motion.span
          key={state}
          initial={animated ? { opacity: 0 } : false}
          animate={{ opacity: 1 }}
          transition={{ duration: animated ? 0.2 : 0 }}
          className="inline-block"
        >
          {detail[state]}
        </motion.span>
      </span>
      <span
        className={cx(
          'ml-auto flex size-4 shrink-0 items-center justify-center border transition-colors duration-300 sm:ml-3',
          state === 'pass'
            ? 'border-ink bg-ink text-paper'
            : 'border-line bg-transparent text-transparent',
        )}
      >
        {state === 'pass' ? (
          <motion.span
            initial={animated ? { scale: 0.4, opacity: 0 } : false}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 420, damping: 22 }}
            className="flex items-center justify-center"
          >
            <Check aria-hidden size={10} strokeWidth={3.2} />
          </motion.span>
        ) : state === 'active' && animated ? (
          <motion.span
            aria-hidden
            className="block size-1.5 bg-accent"
            animate={{ opacity: [0.25, 1, 0.25] }}
            transition={{ duration: 0.9, repeat: Infinity, ease: 'easeInOut' }}
          />
        ) : null}
      </span>
    </motion.li>
  );
}

/**
 * A scripted walkthrough of the submission pipeline: the same gates the backend
 * enforces (ownership, README, commit count, AI relevance) in order, ending on a
 * verified record. It starts when the section scrolls into view, loops while it
 * stays visible, and collapses to the finished state for reduced motion.
 */
export function VerificationConsole() {
  const reduced = usePrefersReducedMotion();
  const ref = useRef<HTMLDivElement | null>(null);
  const inView = useInView(ref, { amount: 0.3 });
  const [step, setStep] = useState(0);
  const [cycle, setCycle] = useState(0);
  const [typed, setTyped] = useState(0);
  const [score, setScore] = useState(0);

  useEffect(() => {
    if (reduced) {
      setStep(5);
      return;
    }
    if (!inView) {
      setStep(0);
      return;
    }
    const timers = [
      window.setTimeout(() => setStep(1), 1500),
      window.setTimeout(() => setStep(2), 2500),
      window.setTimeout(() => setStep(3), 3400),
      window.setTimeout(() => setStep(4), 4300),
      window.setTimeout(() => setStep(5), 6800),
      window.setTimeout(() => {
        setStep(0);
        setCycle((value) => value + 1);
      }, 11800),
    ];
    return () => timers.forEach((timer) => window.clearTimeout(timer));
  }, [reduced, inView, cycle]);

  useEffect(() => {
    if (reduced) {
      setTyped(REPO_URL.length);
      return;
    }
    if (!inView) {
      setTyped(0);
      return;
    }
    setTyped(0);
    const timer = window.setInterval(() => {
      setTyped((count) => {
        if (count >= REPO_URL.length) {
          window.clearInterval(timer);
          return count;
        }
        return count + 1;
      });
    }, 22);
    return () => window.clearInterval(timer);
  }, [reduced, inView, cycle]);

  useEffect(() => {
    if (reduced) {
      setScore(VERIFIED_SCORE);
      return;
    }
    if (step < 4) {
      setScore(0);
      return;
    }
    if (step >= 5) {
      setScore(VERIFIED_SCORE);
      return;
    }
    let frame = 0;
    const start = performance.now();
    const tick = (now: number) => {
      const progress = Math.min(1, (now - start) / 1500);
      const eased = 1 - (1 - progress) ** 3;
      setScore(VERIFIED_SCORE * eased);
      if (progress < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [step, reduced]);

  const gateState = (index: number): GateState => {
    if (step >= index + 2) return 'pass';
    if (step === index + 1) return 'active';
    return 'idle';
  };

  const passCount = GATES.filter((_, index) => gateState(index) === 'pass').length;
  const running = step >= 1 && step < 5;
  const reading = step === 4 && !reduced;
  const verified = step >= 5;
  const status = STATUS[step];
  const barWidth = verified ? 100 : Math.round(score * 100);

  return (
    <div
      ref={ref}
      className={cx(
        'relative overflow-hidden border bg-paper text-ink transition-colors duration-500 shadow-[6px_6px_0_0_rgba(23,21,15,0.28)] sm:shadow-[14px_14px_0_0_rgba(23,21,15,0.28)] dark:shadow-[10px_10px_0_0_rgba(0,0,0,0.45)]',
        verified ? 'border-accent' : 'border-paper/25',
      )}
    >
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.18em]">
          <motion.span
            aria-hidden
            className={cx(
              'block size-1.5',
              running ? 'bg-accent' : verified ? 'bg-ink' : 'bg-tint',
            )}
            animate={running && !reduced ? { opacity: [1, 0.25, 1] } : undefined}
            transition={{ duration: 1.1, repeat: Infinity, ease: 'easeInOut' }}
          />
          Verification console
        </span>
        <span className="flex items-center gap-1.5 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          <span>Sample run</span>
          <span aria-hidden className="text-muted/50">
            ·
          </span>
          <span aria-hidden className="tabular-nums">
            {pad(cycle + 1)}
          </span>
        </span>
      </div>

      <div className="p-4 sm:p-5">
        <p className="sr-only">
          A sample submission is checked for repository ownership, a README and
          at least five commits, then reviewed by AI for relevance before it is
          verified.
        </p>

        <div>
          <FieldLabel label="Repository" meta="public repo" />
        </div>

        <div className="mt-2 flex items-center gap-2 border border-ink bg-sheet px-2.5 py-2">
          <GithubMark size={13} className="shrink-0 text-ink" />
          <p className="min-w-0 truncate font-mono text-label leading-none tracking-[0.02em]">
            {REPO_URL.slice(0, typed)}
            {step === 0 && !reduced ? (
              <span
                aria-hidden
                className="ml-0.5 inline-block h-3 w-px translate-y-0.5 animate-pulse bg-ink"
              />
            ) : null}
          </p>
          <span
            className={cx(
              'ml-auto shrink-0 border px-1.5 py-0.5 font-mono text-label font-bold uppercase tracking-[0.14em] transition-colors duration-300',
              step === 0
                ? 'border-line text-muted'
                : 'border-ink bg-ink text-paper',
            )}
          >
            {step === 0 ? 'Paste' : 'Sent'}
          </span>
        </div>

        <div className="mt-4">
          <FieldLabel label="Checks" meta={`${passCount} / 3 passed`} />
        </div>

        <motion.ul
          variants={GATES_REVEAL}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          className="mt-1.5"
        >
          {GATES.map((gate, index) => (
            <GateRow
              key={gate.label}
              icon={gate.icon}
              label={gate.label}
              detail={gate.detail}
              state={gateState(index)}
              animated={!reduced}
            />
          ))}
        </motion.ul>

        <div
          className={cx(
            'relative mt-4 overflow-hidden border bg-sheet p-3 transition-colors duration-500',
            step >= 4 ? 'border-accent/50' : 'border-line',
          )}
        >
          <div className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-1.5 font-mono text-label font-bold uppercase tracking-[0.14em]">
              <Sparkles
                aria-hidden
                size={11}
                strokeWidth={2.4}
                className={cx(
                  'transition-colors duration-300',
                  step >= 4 ? 'text-accent' : 'text-muted',
                )}
              />
              AI relevance
            </span>
            <span
              className={cx(
                'font-mono text-label font-bold uppercase tabular-nums tracking-[0.14em] transition-colors duration-300',
                verified ? 'text-accent' : 'text-muted',
              )}
            >
              {step < 4
                ? 'queued'
                : step === 4
                  ? `${score.toFixed(2)} · reading…`
                  : `${VERIFIED_SCORE.toFixed(2)} · match`}
            </span>
          </div>

          <div className="mt-3 border-t border-line/80 pt-2.5">
            <div className="flex items-baseline gap-2">
              <span className="w-10 shrink-0 font-mono text-label font-bold uppercase tracking-[0.12em] text-muted">
                Brief
              </span>
              <span className="min-w-0 truncate font-mono text-label leading-snug text-ink-soft">
                {SAMPLE_BRIEF}
              </span>
            </div>

            <div className="mt-2 flex items-baseline gap-2">
              <span className="w-10 shrink-0 font-mono text-label font-bold uppercase tracking-[0.12em] text-muted">
                Readme
              </span>
              <div className="min-w-0 flex-1 space-y-0.5">
                {README_EXCERPT.map((line, lineIndex) => (
                  <p
                    key={lineIndex}
                    className={cx(
                      'font-mono text-label leading-[1.55] transition-opacity duration-500',
                      step >= 4 ? 'opacity-100' : 'opacity-50',
                    )}
                  >
                    {line.map((part, partIndex) =>
                      part.match ? (
                        <span key={partIndex} className="relative inline-block">
                          <motion.span
                            aria-hidden
                            className="absolute inset-x-0 bottom-px top-px bg-accent/25"
                            style={{ originX: 0 }}
                            initial={reading ? { scaleX: 0 } : false}
                            animate={{ scaleX: step >= 4 ? 1 : 0 }}
                            transition={{
                              duration: reduced ? 0 : 0.34,
                              delay: reading ? lineIndex * 0.18 + 0.12 : 0,
                              ease: EASE_SNAP,
                            }}
                          />
                          <motion.span
                            aria-hidden
                            className="absolute inset-x-0 bottom-0 h-px bg-accent"
                            style={{ originX: 0 }}
                            initial={reading ? { scaleX: 0 } : false}
                            animate={{ scaleX: step >= 4 ? 1 : 0 }}
                            transition={{
                              duration: reduced ? 0 : 0.34,
                              delay: reading ? lineIndex * 0.18 + 0.12 : 0,
                              ease: EASE_SNAP,
                            }}
                          />
                          <span
                            className={cx(
                              'relative transition-colors duration-300',
                              step >= 4 ? 'text-ink' : 'text-muted',
                            )}
                          >
                            {part.text}
                          </span>
                        </span>
                      ) : (
                        <span key={partIndex}>{part.text}</span>
                      ),
                    )}
                  </p>
                ))}
              </div>
            </div>
          </div>

          <div aria-hidden className="mt-2.5 h-1 bg-line">
            <div
              className="h-full bg-accent transition-[width] duration-300 ease-out"
              style={{ width: `${barWidth}%` }}
            />
          </div>
        </div>

        <div
          className={cx(
            'mt-3 flex items-start justify-between gap-3 border px-3 py-2.5 transition-colors duration-500',
            verified ? 'border-accent bg-accent/5' : 'border-ink',
          )}
        >
          <div className="min-w-0">
            <motion.p
              key={step}
              initial={reduced ? false : { opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: reduced ? 0 : 0.22 }}
              className="font-mono text-label font-bold uppercase tracking-[0.14em]"
            >
              {status.text}
            </motion.p>
            <p className="mt-1 text-label leading-snug text-muted">{status.hint}</p>
          </div>
          {verified ? (
            <motion.span
              initial={reduced ? false : { opacity: 0, scale: 0.6, rotate: -16 }}
              animate={{ opacity: 1, scale: 1, rotate: -3 }}
              transition={{ type: 'spring', stiffness: 320, damping: 18 }}
              className="shrink-0"
            >
              <Stamp tone="new" label="verified" />
            </motion.span>
          ) : (
            <motion.span
              key="pending"
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: reduced ? 0 : 0.3 }}
              className="flex shrink-0 items-center gap-1.5 pt-0.5 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted"
            >
              <span aria-hidden className="block size-1.5 bg-tint" />
              Pending
            </motion.span>
          )}
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-2.5 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
        <span>Every submission runs these checks</span>
        <span className="flex items-center gap-1.5">
          <GithubMark size={11} />
          GitHub + AI
        </span>
      </div>

      {verified && !reduced ? (
        <motion.span
          key={cycle}
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-transparent via-accent/10 to-transparent"
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{ duration: 0.9, ease: 'easeInOut' }}
        />
      ) : null}
    </div>
  );
}