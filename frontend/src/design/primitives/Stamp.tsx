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
  open: 'bg-white text-ink',
  closed: 'bg-red text-white',
  'ai-suggested': 'bg-blue text-white',
  new: 'bg-yellow text-ink',
  active: 'bg-blue text-white',
  stale: 'bg-yellow text-ink',
  'not-started': 'bg-white text-ink',
};

const DEFAULT_ROTATION: Record<StampTone, number> = {
  open: -2,
  closed: 2,
  'ai-suggested': -3,
  new: 3,
  active: -2,
  stale: 2,
  'not-started': -1,
};

interface StampProps {
  tone: StampTone;
  label?: string;
  rotate?: number;
  className?: string;
}

export function Stamp({ tone, label, rotate, className }: StampProps) {
  const rotation = rotate ?? DEFAULT_ROTATION[tone];
  const raw = label ?? (tone === 'not-started' ? 'not started' : tone);
  const text = raw.toUpperCase();
  const style: CSSProperties = { transform: `rotate(${rotation}deg)` };

  return (
    <span
      style={style}
      className={cx(
        'inline-block border-[3px] border-ink px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-widest',
        TONE_CLASSES[tone],
        className,
      )}
    >
      {text}
    </span>
  );
}
