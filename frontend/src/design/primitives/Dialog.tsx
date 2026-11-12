import type { ReactNode } from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { cx } from '@/lib/cx';
import { Button } from './Button';

interface DialogProps {
  title: string;
  triggerLabel: string;
  children: ReactNode;
  className?: string;
  /** Optional controlled state; omit both for the uncontrolled default. */
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function Dialog({
  title,
  triggerLabel,
  children,
  className,
  open,
  onOpenChange,
}: DialogProps) {
  return (
    <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
      <DialogPrimitive.Trigger asChild>
        <Button variant="secondary">{triggerLabel}</Button>
      </DialogPrimitive.Trigger>
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-40 bg-ink/35" />
        <DialogPrimitive.Content
          aria-describedby={undefined}
          className={cx(
            'fixed left-1/2 top-1/2 z-50 w-[min(560px,92vw)] -translate-x-1/2 -translate-y-1/2 rounded-xl border border-line bg-sheet p-6 shadow-lift',
            className,
          )}
        >
          <div className="mb-4 flex items-start justify-between gap-4 border-b border-line pb-3.5">
            <DialogPrimitive.Title className="font-display text-[1.0625rem] leading-snug text-ink">
              {title}
            </DialogPrimitive.Title>
            <DialogPrimitive.Close asChild>
              <button
                type="button"
                aria-label="Close dialog"
                className="press -mr-1 -mt-1 flex size-8 shrink-0 items-center justify-center rounded-full text-body text-muted hover:bg-tint hover:text-ink"
              >
                ×
              </button>
            </DialogPrimitive.Close>
          </div>
          <div className="text-body leading-relaxed">{children}</div>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}
