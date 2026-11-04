import type { ReactNode } from 'react';

interface StaticShellProps {
  kicker: string;
  title: string;
  children: ReactNode;
  wide?: boolean;
}

export function StaticShell({ kicker, title, children, wide }: StaticShellProps) {
  const width = wide ? 'w-[min(1080px,96vw)]' : 'w-[min(820px,96vw)]';

  return (
    <main className="border-b border-ink bg-paper">
      <div className={`mx-auto ${width} py-12`}>
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-muted">
          <span className="flex items-center gap-2 text-accent">
            <span aria-hidden className="block size-2 bg-accent" />
            {kicker}
          </span>
          <span>MANABI / Reference</span>
        </div>
        <h1
          className="mt-6 font-display uppercase leading-[0.9] tracking-[-0.03em]"
          style={{ fontSize: 'clamp(2.5rem, 6vw, 4.5rem)' }}
        >
          {title}
        </h1>
        <div className="mt-8 flex flex-col gap-5 text-sm leading-relaxed text-ink-soft">
          {children}
        </div>
      </div>
    </main>
  );
}
