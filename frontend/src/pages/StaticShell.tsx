import type { ReactNode } from 'react';
import { cx } from '@/lib/cx';

interface StaticShellProps {
  kicker: string;
  title: string;
  intro?: ReactNode;
  code?: string;
  aside?: ReactNode;
  children: ReactNode;
  wide?: boolean;
}

export function StaticShell({
  kicker,
  title,
  intro,
  code,
  aside,
  children,
  wide,
}: StaticShellProps) {
  const width =
    aside || wide ? 'w-[min(1120px,96vw)]' : 'w-[min(820px,96vw)]';

  return (
    <main className="border-b border-line bg-paper">
      <div className={cx('mx-auto py-12 md:py-16', width)}>
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-3 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          <span className="flex items-center gap-2 text-accent">
            <span aria-hidden className="block size-1.5 rounded-full bg-accent" />
            {kicker}
          </span>
          <span className="flex items-center gap-2.5">
            {code ? <span className="text-muted/70">{code}</span> : null}
            <span aria-hidden className="block h-2.5 w-px bg-line" />
            <span>MANABI / Reference</span>
          </span>
        </div>

        <div
          className={cx(
            'mt-8 grid gap-10 lg:gap-x-12',
            Boolean(aside) && 'lg:grid-cols-[minmax(0,1fr)_288px]',
          )}
        >
          <div className="min-w-0 lg:col-start-1 lg:row-start-1">
            <h1 className="text-balance font-display text-display leading-[1.03] tracking-[-0.03em] text-ink">
              {title}
            </h1>
            {intro ? (
              <div className="mt-5 max-w-2xl text-lead leading-relaxed text-muted">
                {intro}
              </div>
            ) : null}
          </div>

          {aside ? (
            <aside className="flex flex-col gap-4 lg:col-start-2 lg:row-span-2 lg:row-start-1 lg:sticky lg:top-24 lg:self-start">
              {aside}
            </aside>
          ) : null}

          <div className="flex min-w-0 flex-col gap-8 text-body leading-relaxed text-ink-soft lg:col-start-1 lg:row-start-2">
            {children}
          </div>
        </div>
      </div>
    </main>
  );
}