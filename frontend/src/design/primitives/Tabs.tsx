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
  '-ml-[3px] first:ml-0 border-[3px] border-ink bg-white px-4 py-2 font-mono text-xs font-bold uppercase tracking-widest data-[state=active]:bg-yellow';

const CONTENT_CLASSES = 'border-[3px] border-ink bg-white p-4 text-sm';

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
