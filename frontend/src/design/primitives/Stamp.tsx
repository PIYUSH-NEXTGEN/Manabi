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
  open: 'border-ink bg-sheet text-ink',
  closed: 'border-danger bg-danger text-paper',
  'ai-suggested': 'border-olive bg-olive text-paper',
  new: 'border-accent bg-accent text-paper',
  active: 'border-olive bg-olive text-paper',
  stale: 'border-accent bg-accent text-paper',
  'not-started': 'border-line bg-sheet text-ink-soft',
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
        'inline-block border px-2 py-1 font-mono text-[10px] font-bold uppercase leading-none tracking-[0.14em]',
        TONE_CLASSES[tone],
        className,
      )}
    >
      {text}
    </span>
  );
}
