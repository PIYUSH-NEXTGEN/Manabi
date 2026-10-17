import { useId, type ChangeEvent } from 'react';

export interface FilterOption {
  value: string;
  count?: number;
}

interface FilterSelectProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: FilterOption[];
}

export function FilterSelect({
  label,
  value,
  onChange,
  options,
}: FilterSelectProps) {
  const id = useId();

  function handleChange(event: ChangeEvent<HTMLSelectElement>) {
    onChange(event.target.value);
  }

  return (
    <div className="flex flex-col gap-1.5">
      <label
        htmlFor={id}
        className="font-mono text-[11px] font-bold uppercase tracking-widest"
      >
        {label}
      </label>
      <select
        id={id}
        value={value}
        onChange={handleChange}
        className="field w-full appearance-none font-mono text-xs font-bold uppercase tracking-widest"
      >
        <option value="">All</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.value}
            {option.count != null ? ` (${option.count})` : ''}
          </option>
        ))}
      </select>
    </div>
  );
}
