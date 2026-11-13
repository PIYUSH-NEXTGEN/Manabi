import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';

const SLOT_COUNT = 5;

// Sponsors appear in slot order. Add one here and its tile shows the sponsor's
// icon and name; clicking it opens the sponsor's website.
type Sponsor = {
  name: string;
  href: string;
  /** Path or URL to the sponsor's icon. Falls back to their initial. */
  icon?: string;
  /** One or two lines about the sponsor's product, shown under the block. */
  blurb?: string;
};

const SPONSORS: Sponsor[] = [
  // {
  //   name: 'Acme',
  //   href: 'https://acme.com',
  //   icon: '/sponsors/acme.svg',
  //   blurb: 'One or two lines about what Acme makes.',
  // },
];

export function Sponsors() {
  const remaining = SLOT_COUNT - SPONSORS.length;

  const status =
    remaining === 0
      ? 'All five slots are taken.'
      : remaining === SLOT_COUNT
        ? 'Five slots. All open right now.'
        : `${remaining} of five slots open.`;

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
            people and teams who back it. Their icon and name sit right here,
            and clicking one opens their website.
          </p>
        </div>

        <p className="mt-9 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          {status}
        </p>

        <ul className="mt-6 grid max-w-4xl grid-cols-2 gap-6 sm:grid-cols-3 sm:gap-7 lg:grid-cols-5 lg:gap-8">
          {Array.from({ length: SLOT_COUNT }, (_, index) => {
            const sponsor = SPONSORS[index];

            return (
              <li key={sponsor?.name ?? `open-${index}`}>
                {sponsor ? (
                  <a
                    href={sponsor.href}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="group flex flex-col"
                  >
                    <span className="flex aspect-square items-center justify-center rounded-[1.2rem] border border-line bg-paper p-3 shadow-soft transition-colors group-hover:border-ink/25 group-hover:bg-tint">
                      {sponsor.icon ? (
                        <img
                          src={sponsor.icon}
                          alt=""
                          loading="lazy"
                          className="size-9 rounded-[0.6rem] object-contain"
                        />
                      ) : (
                        <span
                          aria-hidden
                          className="flex size-9 items-center justify-center rounded-[0.6rem] bg-tint font-display text-[1rem] leading-none text-ink"
                        >
                          {sponsor.name.slice(0, 1)}
                        </span>
                      )}
                    </span>
                    <span className="mt-3 block text-balance text-center font-display text-[0.875rem] font-medium leading-snug text-ink">
                      {sponsor.name}
                    </span>
                    {sponsor.blurb ? (
                      <span className="mt-1 block text-balance text-center text-[0.75rem] leading-snug text-muted">
                        {sponsor.blurb}
                      </span>
                    ) : null}
                  </a>
                ) : (
                  <Link
                    to="/sponsors"
                    aria-label={`Sponsor slot ${index + 1}, open`}
                    className="group flex aspect-square items-center justify-center rounded-[1.2rem] border border-dashed border-line bg-tint/40 text-muted transition-colors hover:border-sky-strong hover:bg-sky/20 hover:text-ink dark:bg-sheet"
                  >
                    <Plus
                      aria-hidden
                      size={22}
                      strokeWidth={2}
                      className="transition-transform duration-200 group-hover:scale-110"
                    />
                  </Link>
                )}
              </li>
            );
          })}
        </ul>

        <p className="mt-6 text-body leading-relaxed text-ink-soft">
          Want your project here?{' '}
          <Link
            to="/sponsors"
            className="font-semibold text-ink underline decoration-ink/30 underline-offset-4 transition-colors hover:text-sky-strong"
          >
            See how sponsorship works
          </Link>
          .
        </p>
      </div>
    </section>
  );
}
