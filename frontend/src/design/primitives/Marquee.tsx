import type { CSSProperties } from 'react';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

interface MarqueeProps {
  items: string[];
  durationSec?: number;
  className?: string;
  label?: string;
}

function MarqueeRow({ items, hidden }: { items: string[]; hidden: boolean }) {
  return (
    <ul
      className="flex shrink-0 items-center gap-7 pr-7"
      aria-hidden={hidden || undefined}
    >
      {items.map((item, index) => (
        <li
          key={`${item}-${index}`}
          className="flex items-center gap-3 whitespace-nowrap font-mono text-label font-bold uppercase tracking-[0.18em] text-ink-soft"
        >
          <span aria-hidden className="block size-1.5 rounded-full bg-accent" />
          {item}
        </li>
      ))}
    </ul>
  );
}

export function Marquee({
  items,
  durationSec = 38,
  className,
  label = 'Sources',
}: MarqueeProps) {
  const reduced = usePrefersReducedMotion();

  if (items.length === 0) {
    return null;
  }

  const style = {
    '--marquee-duration': `${durationSec}s`,
    animation: reduced ? 'none' : undefined,
  } as CSSProperties;

  return (
    <div
      aria-label={label}
      className={cx(
        'marquee overflow-hidden border-y border-line bg-sheet/60 py-3',
        className,
      )}
    >
      <div className="marquee-track" style={style}>
        <MarqueeRow items={items} hidden={false} />
        <MarqueeRow items={items} hidden />
      </div>
    </div>
  );
}
