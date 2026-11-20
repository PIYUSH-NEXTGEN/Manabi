import { useId, type ChangeEvent } from 'react';

export interface FilterOption {
  value: string;
  count?: number;
  hint?: string;
  disabled?: boolean;
}

interface FilterSelectProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: FilterOption[];
  /** Optional display-label resolver (e.g. the field catalog's labels). */
  labelFor?: (value: string) => string;
}

export function FilterSelect({
  label,
  value,
  onChange,
  options,
  labelFor,
}: FilterSelectProps) {
  const id = useId();

  function handleChange(event: ChangeEvent<HTMLSelectElement>) {
    onChange(event.target.value);
  }

  return (
    <div className="flex flex-col gap-1.5">
      <label
        htmlFor={id}
        className="text-sm font-medium text-muted"
      >
        {label}
      </label>
      <select
        id={id}
        value={value}
        onChange={handleChange}
        className="field w-full appearance-none text-[0.875rem] font-semibold"
      >
        <option value="">All</option>
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {labelFor ? labelFor(option.value) : option.value}
            {option.hint ? ` (${option.hint})` : ''}
          </option>
        ))}
      </select>
    </div>
  );
}
