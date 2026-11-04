import type { ReactNode } from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { cx } from '@/lib/cx';
import { Button } from './Button';

interface DialogProps {
  title: string;
  triggerLabel: string;
  children: ReactNode;
  className?: string;
}

export function Dialog({ title, triggerLabel, children, className }: DialogProps) {
  return (
    <DialogPrimitive.Root>
      <DialogPrimitive.Trigger asChild>
        <Button variant="secondary">{triggerLabel}</Button>
      </DialogPrimitive.Trigger>
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-40 bg-ink/70" />
        <DialogPrimitive.Content
          aria-describedby={undefined}
          className={cx(
            'fixed left-1/2 top-1/2 z-50 w-[min(560px,92vw)] -translate-x-1/2 -translate-y-1/2 border border-ink bg-paper p-6',
            className,
          )}
        >
          <div className="mb-4 flex items-start justify-between gap-4 border-b border-line pb-3">
            <DialogPrimitive.Title className="font-display text-xl uppercase leading-tight tracking-tight">
              {title}
            </DialogPrimitive.Title>
            <DialogPrimitive.Close asChild>
              <button
                type="button"
                aria-label="Close dialog"
                className="press border border-ink bg-sheet px-2 py-0.5 font-mono text-sm font-bold hover:bg-ink hover:text-paper"
              >
                ×
              </button>
            </DialogPrimitive.Close>
          </div>
          <div className="text-sm leading-relaxed">{children}</div>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}
