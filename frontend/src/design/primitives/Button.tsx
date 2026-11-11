import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cx } from '@/lib/cx';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'link';
export type ButtonSize = 'default' | 'small';

const BASE_CLASSES =
  'inline-flex items-center justify-center gap-2 border border-ink font-mono text-label font-bold uppercase tracking-[0.16em] disabled:pointer-events-none disabled:opacity-45 press';

const SIZE_CLASSES: Record<ButtonSize, string> = {
  default: 'px-5 py-3',
  small: 'px-3 py-2',
};

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary:
    'border-accent bg-accent text-paper hover:border-ink hover:bg-ink hover:text-paper',
  secondary:
    'border-ink bg-transparent text-ink hover:bg-ink hover:text-paper',
  danger:
    'border-danger bg-danger text-paper hover:border-ink hover:bg-ink hover:text-paper',
  link: 'border-transparent bg-transparent px-0 py-0 text-accent underline underline-offset-4 hover:text-ink',
};

export function buttonClasses(variant: ButtonVariant, className?: string): string {
  return cx(BASE_CLASSES, SIZE_CLASSES.default, VARIANT_CLASSES[variant], className);
}

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { variant = 'primary', size = 'default', className, type = 'button', ...rest },
  ref,
) {
  return (
    <button
      ref={ref}
      type={type}
      className={cx(
        BASE_CLASSES,
        SIZE_CLASSES[size],
        VARIANT_CLASSES[variant],
        className,
      )}
      {...rest}
    />
  );
});
