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
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

const REPO_URL = 'github.com/you/your-repo';
const VERIFIED_SCORE = 0.82;

const GATES: { icon: LucideIcon; label: string; detail: string }[] = [
  { icon: ShieldCheck, label: 'Ownership', detail: 'you are the owner' },
  { icon: FileText, label: 'README', detail: 'found · explains it' },
  { icon: GitCommitHorizontal, label: 'Commits', detail: '14 · 5 needed' },
];

const STATUS = [
  'Paste a public repo',
  'Checking ownership',
  'Reading the README',
  'Counting commits',
  'AI relevance pass',
  'Verified · live on the board',
] as const;

const README_LINES = ['w-[94%]', 'w-[71%]', 'w-[86%]', 'w-[58%]'];

type GateState = 'idle' | 'active' | 'pass';

function GateRow({
  icon: Icon,
  label,
  detail,
  state,
  animated,
}: {
  icon: LucideIcon;
  label: string;
  detail: string;
  state: GateState;
  animated: boolean;
}) {
  return (
    <li
      className={cx(
        'flex items-center gap-2.5 border-b border-line py-2 pl-2 transition-colors duration-300',
        state === 'pass' && 'bg-tint/40',
        state === 'active' && 'shadow-[inset_2px_0_0_var(--accent)]',
      )}
    >
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
          'font-mono text-[10px] font-bold uppercase tracking-[0.14em] transition-colors duration-300',
          state === 'idle' ? 'text-muted' : 'text-ink',
        )}
      >
        {label}
      </span>
      <span
        className={cx(
          'ml-auto hidden font-mono text-[9px] uppercase tracking-[0.12em] transition-colors duration-300 sm:inline',
          state === 'pass' ? 'text-ink-soft' : 'text-muted/60',
        )}
      >
        {detail}
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
    </li>
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

  const running = step >= 1 && step < 5;
  const verified = step >= 5;
  const barWidth = verified ? 100 : Math.round(score * 100);

  return (
    <div
      ref={ref}
      className={cx(
        'border bg-paper text-ink shadow-[6px_6px_0_0_rgba(23,21,15,0.28)] transition-colors duration-500 sm:shadow-[14px_14px_0_0_rgba(23,21,15,0.28)]',
        verified ? 'border-accent' : 'border-paper/25',
      )}
    >
      <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
        <span className="flex items-center gap-2 font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
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
        <span className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
          Sample run
        </span>
      </div>

      <div className="p-4 sm:p-5">
        <p className="sr-only">
          A sample submission is checked for repository ownership, a README and
          at least five commits, then reviewed by AI for relevance before it is
          verified.
        </p>

        <div className="flex items-center gap-2 border border-ink bg-sheet px-2.5 py-2">
          <GithubMark size={13} className="shrink-0 text-ink" />
          <p className="min-w-0 truncate font-mono text-[10px] leading-none tracking-[0.02em]">
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
              'ml-auto shrink-0 border px-1.5 py-0.5 font-mono text-[8px] font-bold uppercase tracking-[0.14em] transition-colors duration-300',
              step === 0
                ? 'border-line text-muted'
                : 'border-ink bg-ink text-paper',
            )}
          >
            {step === 0 ? 'Paste' : 'Sent'}
          </span>
        </div>

        <div aria-hidden className="mt-3 flex gap-1">
          {[2, 3, 4, 5].map((threshold) => (
            <span
              key={threshold}
              className={cx(
                'h-1 flex-1 border transition-colors duration-500',
                step >= threshold
                  ? 'border-accent bg-accent'
                  : 'border-line bg-transparent',
              )}
            />
          ))}
        </div>

        <ul className="mt-3">
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
        </ul>

        <div className="relative mt-3 overflow-hidden border border-line bg-sheet p-3">
          <div className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-1.5 font-mono text-[9px] font-bold uppercase tracking-[0.14em]">
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
                'font-mono text-[9px] font-bold uppercase tabular-nums tracking-[0.14em] transition-colors duration-300',
                verified ? 'text-accent' : 'text-muted',
              )}
            >
              {step < 4
                ? 'queued'
                : step === 4
                  ? `${score.toFixed(2)}. Reading…`
                  : `${VERIFIED_SCORE.toFixed(2)} match`}
            </span>
          </div>

          <div aria-hidden className="relative mt-2.5 space-y-1.5">
            {README_LINES.map((width) => (
              <span
                key={width}
                className={cx(
                  'block h-1.5 transition-colors duration-700',
                  verified ? 'bg-ink/25' : 'bg-tint',
                  width,
                )}
              />
            ))}
            {step === 4 && !reduced ? (
              <motion.span
                aria-hidden
                className="pointer-events-none absolute inset-x-0 h-3 bg-gradient-to-b from-transparent via-accent/20 to-transparent"
                initial={{ top: '-10%' }}
                animate={{ top: ['-10%', '100%'] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
              >
                <span className="absolute inset-x-0 top-1/2 h-px bg-accent" />
              </motion.span>
            ) : null}
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
            'mt-3 flex items-center justify-between gap-3 border px-3 py-2 transition-colors duration-500',
            verified ? 'border-accent bg-accent/5' : 'border-ink',
          )}
        >
          <span className="font-mono text-[9px] font-bold uppercase tracking-[0.14em]">
            {STATUS[step]}
          </span>
          {verified ? (
            <motion.span
              initial={reduced ? false : { opacity: 0, scale: 0.6, rotate: -16 }}
              animate={{ opacity: 1, scale: 1, rotate: -3 }}
              transition={{ type: 'spring', stiffness: 320, damping: 18 }}
            >
              <Stamp tone="new" label="verified" />
            </motion.span>
          ) : (
            <motion.span
              key="pending"
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: reduced ? 0 : 0.3 }}
              className="flex items-center gap-1.5 font-mono text-[9px] font-bold uppercase tracking-[0.14em] text-muted"
            >
              <span aria-hidden className="block size-1.5 bg-tint" />
              Pending
            </motion.span>
          )}
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
        <span>Every submission runs these checks</span>
        <span className="flex items-center gap-1.5">
          <GithubMark size={11} />
          GitHub + AI
        </span>
      </div>
    </div>
  );
}
