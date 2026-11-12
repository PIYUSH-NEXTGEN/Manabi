import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cx } from '@/lib/cx';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'link';
export type ButtonSize = 'default' | 'small';

const BASE_CLASSES =
  'press inline-flex items-center justify-center gap-2 rounded-full border text-[0.875rem] font-semibold leading-none tracking-[-0.01em] disabled:pointer-events-none disabled:opacity-45';

const SIZE_CLASSES: Record<ButtonSize, string> = {
  default: 'px-5 py-3.5',
  small: 'px-4 py-2.5 text-[0.8125rem]',
};

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary:
    'border-transparent bg-accent text-paper shadow-soft hover:-translate-y-px hover:bg-ink',
  secondary:
    'border-line bg-sheet/80 text-ink hover:-translate-y-px hover:border-ink/25 hover:bg-sheet',
  danger:
    'border-transparent bg-danger text-paper shadow-soft hover:-translate-y-px hover:bg-ink',
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
