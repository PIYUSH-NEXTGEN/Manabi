import { cx } from '@/lib/cx';
import type { Facet } from '@/api/client';

interface TechChipsProps {
  options: Facet[];
  selected: string[];
  onToggle: (value: string) => void;
}

export function TechChips({ options, selected, onToggle }: TechChipsProps) {
  return (
    <div
      role="group"
      aria-label="Filter by tech"
      className="flex flex-wrap gap-1.5"
    >
      {options.map((option) => {
        const active = selected.includes(option.value);
        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={active}
            onClick={() => onToggle(option.value)}
            className={cx(
              'border-[3px] border-ink px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-widest transition-colors',
              active
                ? 'bg-yellow text-ink'
                : 'bg-white text-ink hover:bg-paper',
            )}
          >
            {option.value}
            {option.count != null ? ` (${option.count})` : ''}
          </button>
        );
      })}
    </div>
  );
}
