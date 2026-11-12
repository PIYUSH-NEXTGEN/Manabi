import type { CSSProperties } from 'react';
import { cx } from '@/lib/cx';

export type StampTone =
  | 'open'
  | 'closed'
  | 'ai-suggested'
  | 'new'
  | 'active'
  | 'stale'
  | 'not-started';

const TONE_CLASSES: Record<StampTone, string> = {
  open: 'bg-tint text-ink-soft',
  closed: 'bg-danger text-white',
  'ai-suggested': 'bg-olive text-paper',
  new: 'bg-accent text-white',
  active: 'bg-olive/10 text-olive ring-1 ring-olive/25 dark:bg-dawn-sage dark:text-ink',
  stale: 'bg-accent-soft text-accent',
  'not-started': 'bg-tint/60 text-muted',
};

interface StampProps {
  tone: StampTone;
  label?: string;
  rotate?: number;
  className?: string;
}

export function Stamp({ tone, label, rotate = 0, className }: StampProps) {
  const raw = label ?? (tone === 'not-started' ? 'not started' : tone);
  const text = raw.toUpperCase();
  const style: CSSProperties = rotate ? { transform: `rotate(${rotate}deg)` } : {};

  return (
    <span
      style={style}
      className={cx(
        'inline-block rounded-full px-2.5 py-1 font-mono text-label font-bold uppercase leading-none tracking-[0.1em]',
        TONE_CLASSES[tone],
        className,
      )}
    >
      {text}
    </span>
  );
}
