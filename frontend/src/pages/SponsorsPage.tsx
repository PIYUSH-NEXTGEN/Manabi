import type { ReactNode } from 'react';
import { ArrowUpRight, Check, Plus } from 'lucide-react';

const CONTACT_EMAIL = 'piyush.intech@gmail.com';
const SPONSOR_SUBJECT = 'Manabi sponsorship enquiry';
const MAILTO_URL = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(
  SPONSOR_SUBJECT,
)}`;

const AUDIENCE = [
  {
    title: 'Students',
    body: 'Looking for a real project for a resume, a portfolio or a final-year submission.',
  },
  {
    title: 'Developers',
    body: 'Early-career devs who want shipped work to show, not another tutorial to list.',
  },
  {
    title: 'Beginners',
    body: 'Starting their coding journey, with ideas sorted by difficulty so the next step is clear.',
  },
  {
    title: 'Resume and hackathon builders',
    body: 'Hunting for something they can defend in an interview or build inside a weekend.',
  },
];

const INCLUDES = [
  'Your icon and name in the home-page sponsor strip',
  'Clicking the block opens your website in a new tab',
  'Labelled “Sponsor”, never presented as a recommendation',
  'One of five slots, placed in the order sponsors are confirmed',
];

const FAQ = [
  {
    q: 'How long does a sponsorship last?',
    a: 'Placements run for one or three months. The period is agreed before we invoice.',
  },
  {
    q: 'Can we see the placement first?',
    a: 'Yes. We show you a preview of your icon, name and link before it goes live.',
  },
  {
    q: 'What if we want to stop?',
    a: 'Tell us before the next billing period and the placement is removed at the end of the current month. Unused full months are refunded; part months are not.',
  },
  {
    q: 'What can’t you promote?',
    a: 'Anything misleading, adult, gambling or harmful. We only accept sponsors whose products are useful to students, and we may decline or remove any placement that is not.',
  },
  {
    q: 'Do you collect or share student data with sponsors?',
    a: 'No. Sponsors only see aggregate placement statistics. No individual student, account or repository data is shared.',
  },
];

const linkClass =
  'text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink';

export function SponsorsPage() {
  return (
    <main className="border-b border-line bg-paper">
      <section className="relative overflow-hidden border-b border-line bg-tint/40">
        <div
          aria-hidden
          className="pointer-events-none absolute -right-32 top-0 size-[26rem] rounded-full bg-sky/25 blur-3xl dark:hidden"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute -bottom-32 -left-24 size-[22rem] rounded-full bg-lime/20 blur-3xl dark:hidden"
        />

        <div className="relative mx-auto w-[min(1120px,96vw)] py-14 md:py-20">
          <h1 className="max-w-3xl text-balance font-display text-display leading-[1.03] tracking-[-0.03em] text-ink">
            Partner with MANABI.
          </h1>
          <p className="mt-5 max-w-2xl text-lead leading-relaxed text-ink-soft">
            Put your product in front of students and developers who are actively
            choosing what to build.
          </p>

        </div>
      </section>

      <div className="mx-auto w-[min(1120px,96vw)]">
        <Section
          id="audience"
          index="01"
          label="Audience"
          title="Who uses MANABI"
          intro="MANABI helps students, developers and beginners pick real projects to build: for a resume, a hackathon or their first steps in code. Visitors browse 200+ problem ideas by domain and difficulty, build them, and prove their work with a verified GitHub repo."
        >
          <div className="grid gap-px overflow-hidden rounded-card border border-line bg-line sm:grid-cols-2">
            {AUDIENCE.map((group) => (
              <div key={group.title} className="bg-paper p-5">
                <h3 className="font-display text-[1.0625rem] leading-snug text-ink">
                  {group.title}
                </h3>
                <p className="mt-2 text-body leading-relaxed text-ink-soft">
                  {group.body}
                </p>
              </div>
            ))}
          </div>
        </Section>

        <Section
          id="options"
          index="02"
          label="The offer"
          title="One way to sponsor"
          intro="There is a single placement. Your icon and name on the landing page, linking to your website. Pricing is agreed before we invoice."
        >
          <div className="rounded-card border border-line-strong bg-ink p-6 text-paper shadow-lift md:p-8 dark:border-line dark:bg-sheet dark:text-ink dark:shadow-soft">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="max-w-sm">
                <h3 className="font-display text-[1.25rem] leading-snug text-paper dark:text-ink">
                  Home-page sponsor
                </h3>
                <p className="mt-1.5 text-body leading-relaxed text-paper/70 dark:text-ink-soft">
                  Your icon and name on the MANABI landing page, linked to your
                  website.
                </p>
              </div>
              <p className="flex items-baseline gap-1.5">
                <span className="font-display text-[1.5rem] leading-none text-paper dark:text-ink">
                  On request
                </span>
                <span className="font-mono text-label font-bold uppercase tracking-[0.12em] text-paper/60 dark:text-muted">
                  / month
                </span>
              </p>
            </div>

            <ul className="mt-6 flex flex-col gap-2.5">
              {INCLUDES.map((item) => (
                <li key={item} className="flex gap-2.5 text-body leading-snug">
                  <Check
                    aria-hidden
                    size={13}
                    strokeWidth={2.6}
                    className="mt-0.5 shrink-0 text-paper dark:text-ink"
                  />
                  <span className="text-paper/80 dark:text-ink-soft">{item}</span>
                </li>
              ))}
            </ul>

            <a
              href={MAILTO_URL}
              className="press mt-7 inline-flex items-center justify-center gap-2 rounded-full border border-transparent bg-paper px-5 py-3 text-[0.875rem] font-semibold leading-none text-ink transition-colors hover:bg-tint dark:bg-ink dark:text-paper dark:hover:bg-ink/90"
            >
              Email us about sponsorship
              <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
            </a>
          </div>

          <p className="mt-4 text-label leading-relaxed text-muted">
            Slots are limited to five on the home page and are sold in the order
            they are confirmed.
          </p>
        </Section>

        <section
          id="faq"
          className="scroll-mt-24 border-t border-line py-12 md:py-16"
        >
          <div className="grid gap-8 lg:grid-cols-[minmax(0,260px)_minmax(0,1fr)] lg:gap-14">
            <div>
              <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
                FAQ
              </p>
              <h2 className="mt-3 font-display text-[1.75rem] leading-[1.15] tracking-[-0.02em] text-ink">
                Questions sponsors ask
              </h2>
              <p className="mt-3 text-body leading-relaxed text-ink-soft">
                Anything else, email{' '}
                <a href={MAILTO_URL} className={linkClass}>
                  {CONTACT_EMAIL}
                </a>
                .
              </p>
            </div>

            <div className="flex flex-col">
              {FAQ.map((entry) => (
                <details
                  key={entry.q}
                  className="group border-t border-line py-4 first:border-t-0 first:pt-0"
                >
                  <summary className="flex cursor-pointer list-none items-start justify-between gap-4 [&::-webkit-details-marker]:hidden">
                    <span className="font-medium text-ink">{entry.q}</span>
                    <Plus
                      aria-hidden
                      size={14}
                      strokeWidth={2}
                      className="mt-1 shrink-0 text-muted transition-transform duration-200 group-open:rotate-45"
                    />
                  </summary>
                  <p className="mt-2 max-w-2xl pr-6 text-body leading-relaxed text-ink-soft">
                    {entry.a}
                  </p>
                </details>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function Section({
  id,
  index,
  label,
  title,
  intro,
  children,
}: {
  id: string;
  index: string;
  label: string;
  title: string;
  intro?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-24 border-t border-line py-12 md:py-16">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,260px)_minmax(0,1fr)] lg:gap-14">
        <div>
          <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
            <span className="text-accent">{index}</span> / {label}
          </p>
          <h2 className="mt-3 text-balance font-display text-[1.75rem] leading-[1.15] tracking-[-0.02em] text-ink">
            {title}
          </h2>
          {intro ? (
            <p className="mt-3 text-body leading-relaxed text-ink-soft">{intro}</p>
          ) : null}
        </div>
        <div className="min-w-0">{children}</div>
      </div>
    </section>
  );
}
