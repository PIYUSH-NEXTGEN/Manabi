import type { ReactNode } from 'react';

interface StaticShellProps {
  kicker: string;
  title: string;
  children: ReactNode;
  wide?: boolean;
}

export function StaticShell({ kicker, title, children, wide }: StaticShellProps) {
  const width = wide ? 'w-[min(1000px,96vw)]' : 'w-[min(760px,96vw)]';

  return (
    <main className="border-b-[3px] border-ink">
      <div className={`mx-auto ${width} py-12`}>
        <p className="font-mono text-xs font-bold uppercase tracking-widest text-blue">
          {kicker}
        </p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-none md:text-6xl">
          {title}
        </h1>
        <div className="mt-8 flex flex-col gap-5 text-sm leading-relaxed">
          {children}
        </div>
      </div>
    </main>
  );
}
