import type { ReactNode } from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import { cx } from '@/lib/cx';

export interface TabItem {
  value: string;
  label: string;
  content: ReactNode;
}

interface TabsProps {
  tabs: TabItem[];
  defaultValue?: string;
  className?: string;
}

const TRIGGER_CLASSES =
  'rounded-full px-4 py-2 text-[0.875rem] font-semibold text-ink-soft transition-colors hover:text-ink data-[state=active]:bg-sheet data-[state=active]:text-ink data-[state=active]:shadow-soft';

const CONTENT_CLASSES =
  'mt-4 rounded-panel border border-line bg-sheet p-5 text-body leading-relaxed text-ink-soft';

export function Tabs({ tabs, defaultValue, className }: TabsProps) {
  const initial = defaultValue ?? tabs[0]?.value;
  if (!initial) {
    return null;
  }

  return (
    <TabsPrimitive.Root defaultValue={initial} className={className}>
      <TabsPrimitive.List className="inline-flex flex-wrap gap-1 rounded-pill border border-line bg-tint/60 p-1">
        {tabs.map((tab) => (
          <TabsPrimitive.Trigger key={tab.value} value={tab.value} className={cx(TRIGGER_CLASSES)}>
            {tab.label}
          </TabsPrimitive.Trigger>
        ))}
      </TabsPrimitive.List>
      {tabs.map((tab) => (
        <TabsPrimitive.Content key={tab.value} value={tab.value} className={CONTENT_CLASSES}>
          {tab.content}
        </TabsPrimitive.Content>
      ))}
    </TabsPrimitive.Root>
  );
}
