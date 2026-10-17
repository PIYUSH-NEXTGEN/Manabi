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
      className="flex shrink-0 items-center gap-8 pr-8"
      aria-hidden={hidden || undefined}
    >
      {items.map((item, index) => (
        <li
          key={`${item}-${index}`}
          className="whitespace-nowrap font-mono text-xs font-bold uppercase tracking-widest"
        >
          {item}
        </li>
      ))}
    </ul>
  );
}

export function Marquee({
  items,
  durationSec = 30,
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
        'marquee overflow-hidden border-y-[3px] border-ink bg-yellow py-2',
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
