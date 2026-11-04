import { Link } from 'react-router-dom';

export function FinalCta() {
  return (
    <section className="border-b border-ink bg-accent text-paper">
      <div className="mx-auto flex w-[min(1240px,96vw)] flex-col items-start gap-7 py-16">
        <div className="flex w-full flex-wrap items-center justify-between gap-3 border-b border-paper/30 pb-3 font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/70">
          <span>03 / Open call</span>
          <span>Doc. no. EA.2026.001</span>
        </div>
        <h2
          className="font-display uppercase leading-[0.88] tracking-[-0.02em]"
          style={{ fontSize: 'clamp(2.25rem, 6.5vw, 5rem)' }}
        >
          Find it. Build it.
          <br />
          Ship it in public.
        </h2>
        <Link
          to="/problems"
          className="inline-flex border border-paper bg-paper px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-ink transition-colors hover:bg-ink hover:text-paper"
        >
          Browse problems →
        </Link>
      </div>
    </section>
  );
}
