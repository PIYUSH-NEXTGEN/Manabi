import { forwardRef, useId, type InputHTMLAttributes } from 'react';
import { cx } from '@/lib/cx';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, error, id, className, ...rest },
  ref,
) {
  const autoId = useId();
  const inputId = id ?? autoId;
  const errorId = `${inputId}-error`;

  return (
    <div className="flex flex-col gap-1.5">
      <label
        htmlFor={inputId}
        className="font-mono text-[11px] font-bold uppercase tracking-widest"
      >
        {label}
      </label>
      <input
        ref={ref}
        id={inputId}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : undefined}
        className={cx('field w-full', className)}
        {...rest}
      />
      {error ? (
        <p
          id={errorId}
          role="alert"
          className="font-mono text-[11px] font-bold uppercase tracking-widest text-red"
        >
          {error}
        </p>
      ) : null}
    </div>
  );
});
