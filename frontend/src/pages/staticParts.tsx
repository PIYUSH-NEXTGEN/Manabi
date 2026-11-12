import type { ReactNode } from 'react';
import { cx } from '@/lib/cx';

interface ProsePageProps {
  kicker?: string;
  title: string;
  intro?: ReactNode;
  children: ReactNode;
}

export function ProsePage({ kicker, title, intro, children }: ProsePageProps) {
  return (
    <main className="border-b border-line bg-paper">
      <div className="mx-auto w-[min(720px,92vw)] py-16 md:py-24">
        {kicker ? (
          <p className="text-sm font-medium text-muted">{kicker}</p>
        ) : null}
        <h1 className="mt-2 text-balance font-display text-display leading-[1.05] text-ink">
          {title}
        </h1>
        {intro ? (
          <p className="mt-5 max-w-2xl text-lead leading-relaxed text-ink-soft">
            {intro}
          </p>
        ) : null}
        <div className="mt-12 flex flex-col gap-10">{children}</div>
      </div>
    </main>
  );
}

interface ProseSectionProps {
  id?: string;
  title: string;
  children: ReactNode;
}

export function ProseSection({ id, title, children }: ProseSectionProps) {
  return (
    <section id={id} className="scroll-mt-24 border-t border-line pt-8">
      <h2 className="font-display text-[1.375rem] leading-snug text-ink">
        {title}
      </h2>
      <div className="mt-3 flex flex-col gap-3 text-body leading-relaxed text-ink-soft">
        {children}
      </div>
    </section>
  );
}

interface RefSectionProps {
  id?: string;
  index?: string;
  title: string;
  children: ReactNode;
  className?: string;
}

export function RefSection({
  id,
  index,
  title,
  children,
  className,
}: RefSectionProps) {
  return (
    <section
      id={id}
      className={cx(
        'scroll-mt-24 border-t border-line pt-6 first:border-t-0 first:pt-0',
        className,
      )}
    >
      <div className="flex items-baseline gap-3">
        {index ? (
          <span
            aria-hidden
            className="font-mono text-label font-bold tabular-nums tracking-[0.16em] text-accent"
          >
            {index}
          </span>
        ) : null}
        <h2 className="font-mono text-label font-bold uppercase tracking-[0.18em] text-ink">
          {title}
        </h2>
      </div>
      <div className="mt-3 flex flex-col gap-3">{children}</div>
    </section>
  );
}

interface RefAsideProps {
  title: string;
  children: ReactNode;
  className?: string;
}

export function RefAside({ title, children, className }: RefAsideProps) {
  return (
    <section className={cx('overflow-hidden rounded-card border border-line bg-sheet shadow-soft', className)}>
      <h2 className="border-b border-line px-4 py-3 font-mono text-label font-bold uppercase tracking-[0.14em] text-ink-soft">
        {title}
      </h2>
      <div className="flex flex-col gap-3 p-4 text-body leading-relaxed text-ink-soft">
        {children}
      </div>
    </section>
  );
}

interface RefFactsProps {
  items: { label: string; value: ReactNode }[];
}

export function RefFacts({ items }: RefFactsProps) {
  return (
    <dl className="flex flex-col">
      {items.map((item) => (
        <div
          key={item.label}
          className="flex items-baseline justify-between gap-3 border-t border-line py-1.5 first:border-t-0 first:pt-0"
        >
          <dt className="shrink-0 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
            {item.label}
          </dt>
          <dd className="text-right text-label leading-snug text-ink">
            {item.value}
          </dd>
        </div>
      ))}
    </dl>
  );
}

interface RefIndexProps {
  items: { href: string; label: string }[];
}

export function RefIndex({ items }: RefIndexProps) {
  return (
    <nav aria-label="On this page">
      <ol className="flex flex-col">
        {items.map((item, position) => (
          <li key={item.href} className="border-t border-line first:border-t-0">
            <a
              href={item.href}
              className="group flex items-baseline gap-3 rounded-full py-2 font-mono text-label font-bold uppercase tracking-[0.1em] text-ink-soft transition-colors hover:text-accent"
            >
              <span aria-hidden className="tabular-nums text-label text-muted">
                {String(position + 1).padStart(2, '0')}
              </span>
              <span>{item.label}</span>
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

interface RefNoteProps {
  children: ReactNode;
  tone?: 'ink' | 'accent';
}

export function RefNote({ children, tone = 'ink' }: RefNoteProps) {
  return (
    <p
      className={cx(
        'rounded-r-panel border-l-2 py-2.5 pl-4 text-body leading-relaxed',
        tone === 'accent'
          ? 'border-accent bg-accent-soft/40 text-ink'
          : 'border-ink/30 bg-tint/40 text-ink-soft',
      )}
    >
      {children}
    </p>
  );
}

export function RefList({ children }: { children: ReactNode }) {
  return <ul className="flex list-none flex-col gap-2.5">{children}</ul>;
}

export function RefItem({ children }: { children: ReactNode }) {
  return (
    <li className="relative pl-4 text-body leading-relaxed before:absolute before:left-0 before:top-[0.6em] before:block before:size-1.5 before:rounded-full before:bg-accent">
      {children}
    </li>
  );
}

export function RefLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <a
      href={href}
      className="inline-flex items-center gap-1.5 font-mono text-label font-bold uppercase tracking-[0.14em] text-accent underline-offset-4 transition-colors hover:text-ink hover:underline"
    >
      {children}
    </a>
  );
}