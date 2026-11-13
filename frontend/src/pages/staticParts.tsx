import type { ReactNode } from 'react';

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
