import { useEffect, useState } from 'react';
import { cx } from '@/lib/cx';
import { SpaceShooter } from './SpaceShooter';

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
      <SpaceShooter />
      <div>
        <h2 className="font-mono text-label font-bold uppercase tracking-widest">
          Submission in progress
        </h2>
        <p className="mt-1 text-body text-ink-soft" role="status" aria-live="polite">
          {stage.label}
          <span className="sr-only">
            {' '}
            Step {stageIndex + 1} of {STAGES.length}
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
                className={cx('text-label font-mono font-bold', state === 'done' ? 'text-accent' : 'text-muted')}
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
