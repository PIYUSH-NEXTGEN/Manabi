import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cx } from '@/lib/cx';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'link';
export type ButtonSize = 'default' | 'small';

const BASE_CLASSES =
  'inline-flex items-center justify-center gap-2 border-[3px] border-ink font-mono font-bold uppercase tracking-widest disabled:pointer-events-none disabled:opacity-50 shadow-hard press';

const SIZE_CLASSES: Record<ButtonSize, string> = {
  default: 'px-5 py-2.5 text-xs',
  small: 'px-3 py-1.5 text-[11px]',
};

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary: 'bg-yellow text-ink',
  secondary: 'bg-white text-ink',
  danger: 'bg-red text-white',
  link: 'bg-transparent text-blue border-transparent underline underline-offset-4',
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
