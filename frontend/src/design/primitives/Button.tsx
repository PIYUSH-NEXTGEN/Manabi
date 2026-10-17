import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cx } from '@/lib/cx';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'link';

const BASE_CLASSES =
  'inline-flex items-center justify-center gap-2 border-[3px] border-ink px-5 py-2.5 font-mono text-xs font-bold uppercase tracking-widest disabled:pointer-events-none disabled:opacity-50';

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary: 'bg-yellow text-ink shadow-hard press',
  secondary: 'bg-white text-ink shadow-hard press',
  danger: 'bg-red text-white shadow-hard press',
  link: 'bg-transparent text-blue border-transparent underline underline-offset-4',
};

export function buttonClasses(variant: ButtonVariant, className?: string): string {
  return cx(BASE_CLASSES, VARIANT_CLASSES[variant], className);
}

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { variant = 'primary', className, type = 'button', ...rest },
  ref,
) {
  return (
    <button
      ref={ref}
      type={type}
      className={buttonClasses(variant, className)}
      {...rest}
    />
  );
});
