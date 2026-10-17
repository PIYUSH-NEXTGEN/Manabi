import { useState, type ReactNode } from 'react';
import {
  Button,
  Dialog,
  IndexCard,
  Input,
  Marquee,
  Skeleton,
  Stamp,
  Tabs,
  Tag,
  useToast,
  type StampTone,
} from '@/design/primitives';

const STAMP_TONES: StampTone[] = [
  'open',
  'closed',
  'ai-suggested',
  'new',
  'active',
  'stale',
  'not-started',
];

const MARQUEE_ITEMS = ['Source one', 'Source two', 'Source three', 'Source four'];

function Section({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="flex flex-col gap-3">
      <h2 className="border-b-[3px] border-ink pb-1 font-mono text-sm font-bold uppercase tracking-widest">
        {title}
      </h2>
      {children}
    </section>
  );
}

export function KitPage() {
  const pushToast = useToast();
  const [name, setName] = useState('');

  return (
    <main className="mx-auto flex w-[min(960px,92vw)] flex-col gap-10 py-10">
      <header className="flex flex-col gap-2">
        <p className="font-mono text-xs font-bold uppercase tracking-widest">
          Design system / neo-brutalism
        </p>
        <h1 className="font-display text-5xl uppercase leading-none">MANABI /_kit</h1>
      </header>

      <Section title="Button">
        <div className="flex flex-wrap items-center gap-4">
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="danger">Danger</Button>
          <Button variant="link">Link</Button>
          <Button disabled>Disabled</Button>
        </div>
      </Section>

      <Section title="Stamp">
        <div className="flex flex-wrap items-center gap-4">
          {STAMP_TONES.map((tone) => (
            <Stamp key={tone} tone={tone} />
          ))}
        </div>
      </Section>

      <Section title="Tag">
        <div className="flex flex-wrap items-center gap-3">
          <Tag>python</Tag>
          <Tag>ml</Tag>
          <Tag>governance</Tag>
        </div>
      </Section>

      <Section title="Input">
        <div className="max-w-md">
          <Input
            label="Search problems"
            placeholder="e.g. crop disease"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </div>
        <div className="max-w-md">
          <Input label="Repo URL" defaultValue="not-a-url" error="Enter a valid repo URL" />
        </div>
      </Section>

      <Section title="IndexCard">
        <div className="grid gap-6 md:grid-cols-2">
          <IndexCard
            sourceId="SIH26017"
            field="computer-vision"
            title="Crop disease triage"
            summary="Sample card for the design kit. Real cards come from the API."
            difficulty="beginner"
            domain="agriculture"
            estHours={20}
          />
          <IndexCard
            sourceId="TCOE PS12"
            field="data-engineering"
            title="Streetlight outage tracker"
            difficulty="intermediate"
            domain="governance"
            estHours={40}
          />
        </div>
      </Section>

      <Section title="Difficulty squares">
        <div className="flex flex-wrap items-center gap-4 font-mono text-sm font-bold uppercase tracking-widest">
          <span>
            <span aria-hidden>■□□</span> beginner
          </span>
          <span>
            <span aria-hidden>■■□</span> intermediate
          </span>
          <span>
            <span aria-hidden>■■■</span> advanced
          </span>
        </div>
      </Section>

      <Section title="Tabs">
        <div className="max-w-xl">
          <Tabs
            tabs={[
              { value: 'url', label: 'From URL', content: 'Paste a source URL. The backend fetches and drafts a problem.' },
              { value: 'text', label: 'Paste text', content: 'Paste the raw problem statement text instead.' },
            ]}
          />
        </div>
      </Section>

      <Section title="Skeleton">
        <div className="flex flex-col gap-3">
          <Skeleton className="h-16" />
          <Skeleton className="h-16 w-2/3" />
        </div>
      </Section>

      <Section title="Marquee">
        <Marquee items={MARQUEE_ITEMS} label="Sample sources" />
      </Section>

      <Section title="Dialog">
        <Dialog title="Sample dialog" triggerLabel="Open dialog">
          Hard-edged modal on a paper slab. Esc or the × closes it.
        </Dialog>
      </Section>

      <Section title="Toast">
        <div className="flex flex-wrap gap-4">
          <Button onClick={() => pushToast('Saved to the board')}>Fire info toast</Button>
          <Button variant="danger" onClick={() => pushToast('Something broke', 'error')}>
            Fire error toast
          </Button>
        </div>
      </Section>

      <Section title="Divider stripes">
        <div className="bg-stripes h-8 border-[3px] border-ink" />
      </Section>
    </main>
  );
}
