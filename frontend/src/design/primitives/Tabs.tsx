import type { ReactNode } from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';

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
  '-ml-px first:ml-0 border border-ink bg-sheet px-4 py-2 font-mono text-label font-bold uppercase tracking-[0.16em] text-ink data-[state=active]:bg-ink data-[state=active]:text-paper';

const CONTENT_CLASSES = 'border border-t-0 border-ink bg-sheet p-5 text-body';

export function Tabs({ tabs, defaultValue, className }: TabsProps) {
  const initial = defaultValue ?? tabs[0]?.value;
  if (!initial) {
    return null;
  }

  return (
    <TabsPrimitive.Root defaultValue={initial} className={className}>
      <TabsPrimitive.List className="flex flex-wrap">
        {tabs.map((tab) => (
          <TabsPrimitive.Trigger key={tab.value} value={tab.value} className={TRIGGER_CLASSES}>
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
