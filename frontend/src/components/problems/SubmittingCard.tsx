import { useEffect, useState } from 'react';
import { animate, createTimeline } from 'animejs';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

/**
 * The mascot: a line-art cat (provided image, rendered with a transparent
 * background so it sits on the paper surfaces) that bobs gently while the
 * checks run. Inverted in dark mode so the ink lines stay visible.
 * Animated by anime.js.
 */
function MascotCat({ className }: { className?: string }) {
  const reduced = usePrefersReducedMotion();

  useEffect(() => {
    if (reduced) {
      return;
    }
    const entrance = animate('.cat-figure', {
      scale: [0.85, 1],
      opacity: [0, 1],
      duration: 400,
      ease: 'outBack',
    });
    const idle = createTimeline({ loop: true, defaults: { ease: 'inOutSine' } });
    idle
      .add('.cat-cat', { translateY: [0, -3], duration: 1400 }, 0)
      .add('.cat-cat', { translateY: [-3, 0], duration: 1400 }, 1400)
      .add('.cat-cat', { rotate: [0, 1.4], duration: 2800 }, 0);
    return () => {
      entrance.pause();
      idle.pause();
    };
  }, [reduced]);

  return (
    <span aria-hidden="true" className={cx('cat-figure block shrink-0', className)}>
      <img
        src="/cat.png"
        alt=""
        className="cat-cat h-[5.5rem] w-auto select-none object-contain dark:invert"
        draggable={false}
      />
    </span>
  );
}

interface Stage {
  at: number;
  label: string;
}

const STAGES: Stage[] = [
  { at: 0, label: 'Reading the repository from GitHub' },
  { at: 2, label: 'Confirming you own the repository' },
  { at: 5, label: 'Scoring relevance with the AI check' },
  { at: 26, label: 'Recording your submission' },
];

export function SubmittingCard() {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => window.clearInterval(timer);
  }, []);

  const stageIndex = STAGES.reduce(
    (last, stage, index) => (elapsed >= stage.at ? index : last),
    0,
  );
  const stage = STAGES[stageIndex]!;

  return (
    <aside className="submit-card-enter flex flex-col gap-4 border border-ink bg-sheet p-4">
      <MascotCat />
      <div>
        <h2 className="font-mono text-xs font-bold uppercase tracking-widest">
          Submission in progress
        </h2>
        <p className="mt-1 text-sm text-ink-soft" role="status" aria-live="polite">
          {stage.label}
          <span className="sr-only">
            {' '}
            — step {stageIndex + 1} of {STAGES.length}
          </span>
        </p>
      </div>
      <ul className="flex flex-col">
        {STAGES.map((entry, index) => {
          const state = index < stageIndex ? 'done' : index === stageIndex ? 'active' : 'wait';
          return (
            <li
              key={entry.label}
              className="flex items-center justify-between gap-4 border-t border-line py-2"
            >
              <span
                className={cx(
                  'label',
                  state === 'active' && 'text-ink',
                  state === 'wait' && 'text-muted',
                  state === 'done' && 'text-muted',
                )}
              >
                {entry.label}
              </span>
              <span
                aria-hidden="true"
                className={cx('text-xs font-mono font-bold', state === 'done' ? 'text-accent' : 'text-muted')}
              >
                {state === 'done' ? '✓' : (
                  <span
                    className={cx(
                      'inline-block size-[7px]',
                      state === 'active' ? 'stage-dot bg-accent' : 'border border-line bg-tint',
                    )}
                  />
                )}
              </span>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
