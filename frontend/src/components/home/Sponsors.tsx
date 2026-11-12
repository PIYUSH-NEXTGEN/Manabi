import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';

const SLOT_COUNT = 5;

export function Sponsors() {
  return (
    <section
      aria-labelledby="sponsors-heading"
      className="relative overflow-hidden border-b border-line bg-paper"
    >
      <div
        aria-hidden
        className="pointer-events-none absolute -right-28 top-6 size-[24rem] rounded-full bg-sky/20 blur-3xl dark:hidden"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -bottom-20 -left-32 size-[20rem] rounded-full bg-lime/15 blur-3xl dark:hidden"
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] py-16 md:py-20">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <div className="max-w-xl">
            <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
              <span className="text-ink">04</span> / Sponsors
            </p>
            <h2
              id="sponsors-heading"
              className="mt-3 font-display text-display leading-[1.03] tracking-[-0.03em] text-ink"
            >
              Sponsors.
            </h2>
            <p className="mt-4 text-body leading-relaxed text-ink-soft">
              MANABI is free to use, and it stays that way with help from the
              people and teams who back it. Sponsors get their project or logo
              shown right here.
            </p>
          </div>

          <Link
            to="/contact"
            className="press inline-flex w-fit items-center justify-center rounded-full border border-line bg-paper px-5 py-3 text-[0.875rem] font-semibold text-ink transition-colors hover:border-ink/25 hover:bg-tint"
          >
            Become a sponsor
          </Link>
        </div>

        <p className="mt-9 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          Five slots. All open right now.
        </p>

        <ul className="mt-4 grid max-w-2xl grid-cols-3 gap-3 sm:grid-cols-5">
          {Array.from({ length: SLOT_COUNT }, (_, index) => (
            <li key={index}>
              <Link
                to="/contact"
                aria-label={`Sponsor slot ${index + 1}, open`}
                className="group flex aspect-square items-center justify-center rounded-[1.4rem] border border-dashed border-line bg-tint/40 text-muted transition-colors hover:border-sky-strong hover:bg-sky/20 hover:text-ink dark:bg-sheet"
              >
                <Plus
                  aria-hidden
                  size={22}
                  strokeWidth={2}
                  className="transition-transform duration-200 group-hover:scale-110"
                />
              </Link>
            </li>
          ))}
        </ul>

        <p className="mt-6 text-body leading-relaxed text-ink-soft">
          Want your project here?{' '}
          <Link
            to="/contact"
            className="font-semibold text-ink underline decoration-ink/30 underline-offset-4 transition-colors hover:text-sky-strong"
          >
            Get in touch
          </Link>
          .
        </p>
      </div>
    </section>
  );
}
