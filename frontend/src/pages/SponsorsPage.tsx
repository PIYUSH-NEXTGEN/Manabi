import { useState, type MouseEvent, type ReactNode } from 'react';
import { ArrowDown, ArrowUpRight, Check, Plus } from 'lucide-react';
import { buttonClasses } from '@/design/primitives';
import { useStats } from '@/hooks/useStats';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import {
  AUDIENCE,
  FAQ,
  HERO,
  HOW_IT_WORKS,
  MAILTO_URL,
  OFFER,
  PROMISE,
  SPONSOR_EMAIL,
  SPONSOR_PRICE,
  SPONSOR_PRICE_NOTE,
  SPONSOR_SLOTS,
} from './sponsors/sponsorContent';

export function SponsorsPage() {
  const reduced = usePrefersReducedMotion();
  const [openFaq, setOpenFaq] = useState<string | null>(null);

  const jumpToOffer = (event: MouseEvent<HTMLAnchorElement>) => {
    const target = document.getElementById('offer');
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({
      behavior: reduced ? 'auto' : 'smooth',
      block: 'start',
    });
  };

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
            {HERO.title}
          </h1>
          <p className="mt-5 max-w-2xl text-lead leading-relaxed text-ink-soft">
            {HERO.subline}
          </p>

          <div className="mt-8">
            <a
              href="#offer"
              onClick={jumpToOffer}
              className={buttonClasses('primary')}
            >
              {HERO.cta}
              <ArrowDown aria-hidden size={13} strokeWidth={2.6} />
            </a>
          </div>

          <p className="mt-4 max-w-md text-label leading-relaxed text-muted">
            {HERO.note}
          </p>
        </div>
      </section>

      <div className="mx-auto w-[min(1120px,96vw)]">
        <Section
          id="audience"
          index={AUDIENCE.index}
          label={AUDIENCE.label}
          title={AUDIENCE.title}
          intro={AUDIENCE.intro}
        >
          <ul className="grid gap-px overflow-hidden rounded-card border border-line bg-line md:grid-cols-3">
            {AUDIENCE.cards.map((card) => (
              <li key={card.title} className="bg-paper p-5">
                <h3 className="font-display text-[1.0625rem] leading-snug text-ink">
                  {card.title}
                </h3>
                <p className="mt-2 text-body leading-relaxed text-ink-soft">
                  {card.body}
                </p>
              </li>
            ))}
          </ul>

          <TodayOnManabi />
        </Section>

        <Section
          id="offer"
          index={OFFER.index}
          label={OFFER.label}
          title={OFFER.title}
          intro={OFFER.intro}
        >
          <div className="rounded-card border border-line-strong bg-ink p-6 text-paper shadow-lift md:p-8 dark:border-line dark:bg-sheet dark:text-ink dark:shadow-soft">
            <div className="flex flex-wrap items-start justify-between gap-5">
              <div className="max-w-sm">
                <h3 className="font-display text-[1.25rem] leading-snug text-paper dark:text-ink">
                  {OFFER.cardTitle}
                </h3>
                <p className="mt-1.5 text-body leading-relaxed text-paper/70 dark:text-ink-soft">
                  {OFFER.description}
                </p>
              </div>

              <div className="text-left sm:text-right">
                <p className="flex items-baseline gap-1.5 sm:justify-end">
                  <span className="font-display text-[1.5rem] leading-none text-paper dark:text-ink">
                    {SPONSOR_PRICE}
                  </span>
                  <span className="font-mono text-label font-bold uppercase tracking-[0.12em] text-paper/60 dark:text-muted">
                    / month
                  </span>
                </p>
                <p className="mt-2 flex sm:justify-end">
                  <span className="rounded-full border border-paper/25 px-2.5 py-1 font-mono text-[0.625rem] font-bold uppercase tracking-[0.12em] text-paper/75 dark:border-line dark:text-ink-soft">
                    {SPONSOR_PRICE_NOTE}
                  </span>
                </p>
              </div>
            </div>

            <ul className="mt-6 flex flex-col gap-2.5">
              {OFFER.bullets.map((item) => (
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
              {OFFER.cta}
              <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
            </a>
          </div>

          <p className="mt-4 text-label leading-relaxed text-muted">
            {OFFER.footnote}
          </p>

          <div className="mt-8">
            <p className="font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
              {OFFER.previewCaption}
            </p>
            <ul className="mt-3 grid max-w-md grid-cols-5 gap-2 sm:gap-3">
              {Array.from({ length: SPONSOR_SLOTS }, (_, index) => (
                <li
                  key={index}
                  className={cx(
                    'flex aspect-square items-center justify-center rounded-[1.2rem] border border-dashed border-line px-1 text-center font-mono text-[0.5625rem] font-bold uppercase leading-tight tracking-[0.05em] dark:bg-sheet',
                    index === 0
                      ? 'bg-tint/40 text-ink-soft'
                      : 'bg-paper text-muted',
                  )}
                >
                  {index === 0
                    ? OFFER.previewFirstSlot
                    : OFFER.previewOtherSlot}
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-8 rounded-card border border-line bg-tint/50 p-6">
            <h3 className="font-display text-[1.0625rem] leading-snug text-ink">
              {PROMISE.title}
            </h3>
            <p className="mt-2 text-body leading-relaxed text-ink-soft">
              {PROMISE.text}
            </p>
          </div>
        </Section>

        <Section
          id="how-it-works"
          index={HOW_IT_WORKS.index}
          label={HOW_IT_WORKS.label}
          title={HOW_IT_WORKS.title}
        >
          <ol className="grid gap-px overflow-hidden rounded-card border border-line bg-line sm:grid-cols-2">
            {HOW_IT_WORKS.steps.map((step, position) => (
              <li key={step.title} className="bg-paper p-5">
                <span
                  aria-hidden
                  className="font-mono text-label font-bold tabular-nums tracking-[0.16em] text-accent"
                >
                  {String(position + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-2 font-display text-[1.0625rem] leading-snug text-ink">
                  {step.title}
                </h3>
                <p className="mt-1.5 text-body leading-relaxed text-ink-soft">
                  {step.body}
                </p>
              </li>
            ))}
          </ol>
        </Section>

        <Section
          id="faq"
          index={FAQ.index}
          label={FAQ.label}
          title={FAQ.title}
          intro={
            <>
              {FAQ.introPrefix}{' '}
              <a
                href={MAILTO_URL}
                className="break-words text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink"
              >
                {SPONSOR_EMAIL}
              </a>
              .
            </>
          }
        >
          <div className="flex flex-col">
            {FAQ.items.map((entry) => {
              const open = openFaq === entry.id;
              const panelId = `sponsor-faq-panel-${entry.id}`;
              const buttonId = `sponsor-faq-toggle-${entry.id}`;

              return (
                <div
                  key={entry.id}
                  className="border-t border-line first:border-t-0"
                >
                  <h3>
                    <button
                      type="button"
                      id={buttonId}
                      aria-expanded={open}
                      aria-controls={panelId}
                      onClick={() => setOpenFaq(open ? null : entry.id)}
                      className="flex w-full cursor-pointer list-none items-start justify-between gap-4 py-4 text-left font-medium text-ink focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink"
                    >
                      <span>{entry.question}</span>
                      <Plus
                        aria-hidden
                        size={14}
                        strokeWidth={2}
                        className={cx(
                          'mt-1 shrink-0 text-muted transition-transform duration-200',
                          open && 'rotate-45',
                        )}
                      />
                    </button>
                  </h3>
                  <div
                    id={panelId}
                    role="region"
                    aria-labelledby={buttonId}
                    hidden={!open}
                    className="max-w-2xl pr-6 pb-4"
                  >
                    <p className="text-body leading-relaxed text-ink-soft">
                      {entry.answer}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </Section>
      </div>
    </main>
  );
}

/**
 * Live counts only. Nothing renders while the stats are loading, withholding
 * numbers, or missing, so the page never shows a figure we cannot back up.
 */
function TodayOnManabi() {
  const stats = useStats();
  const problems = stats.data?.problems;
  const fields = stats.data?.fields;

  if (!problems || !fields) return null;

  return (
    <p className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
      <span>{AUDIENCE.statsLabel}</span>
      <span aria-hidden>·</span>
      <span className="text-ink-soft">{problems} project ideas</span>
      <span aria-hidden>·</span>
      <span className="text-ink-soft">{fields} fields</span>
    </p>
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
