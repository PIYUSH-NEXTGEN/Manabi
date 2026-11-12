import type { ReactNode } from 'react';
import { cx } from '@/lib/cx';

interface TagProps {
  children: ReactNode;
  className?: string;
}

export function Tag({ children, className }: TagProps) {
  return (
    <span
      className={cx(
        'inline-block rounded-full border border-line bg-tint/70 px-2.5 py-1 font-mono text-label font-bold uppercase leading-none tracking-[0.1em] text-ink-soft',
        className,
      )}
    >
      {children}
    </span>
  );
}
