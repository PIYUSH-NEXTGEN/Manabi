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
        'inline-block border-[3px] border-ink bg-white px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-widest',
        className,
      )}
    >
      {children}
    </span>
  );
}
