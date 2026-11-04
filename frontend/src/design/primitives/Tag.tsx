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
        'inline-block border border-line bg-sheet px-2 py-1 font-mono text-[10px] font-bold uppercase leading-none tracking-[0.14em] text-ink-soft',
        className,
      )}
    >
      {children}
    </span>
  );
}
