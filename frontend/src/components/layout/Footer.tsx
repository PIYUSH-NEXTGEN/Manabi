import type { FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { ArrowUpRight, Star } from 'lucide-react';
import { Logo } from './Logo';
import { GithubMark } from '@/components/icons/GithubMark';
import { XMark } from '@/components/icons/XMark';
import { EASE_SNAP } from '@/design/motion';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';
const X_URL = 'https://x.com/Piyush_NextGen';
const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL;

const FOOTER_COLUMNS = [
  {
    heading: 'MANABI',
    links: [
      { label: 'About', to: '/about' },
      { label: 'FAQ', to: '/faq' },
      { label: 'Contact', to: '/contact' },
    ],
  },
  {
    heading: 'Platform',
    links: [
      { label: 'Projects', to: '/problems' },
      { label: 'Dashboard', to: '/me' },
      { label: 'Contribute', to: '/contribute' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { label: 'Privacy', to: '/privacy' },
      { label: 'Terms', to: '/terms' },
    ],
  },
];

const reveal = {
  hidden: {},
  show: { transition: { staggerChildren: 0.06, delayChildren: 0.05 } },
};

const item = {
  hidden: { opacity: 0, y: 14 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: EASE_SNAP } },
};

function handleSubscribe(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const email = String(new FormData(event.currentTarget).get('email') ?? '').trim();
  if (!CONTACT_EMAIL || email.length === 0) return;
  const subject = encodeURIComponent('MANABI updates');
  const body = encodeURIComponent(`Please add ${email} to MANABI updates.`);
  window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
}

export function Footer() {
  return (
    <footer className="relative overflow-hidden border-t border-line bg-tint/40">
      <div
        aria-hidden
        className="pointer-events-none absolute -left-32 top-0 size-[26rem] rounded-full bg-sky/25 blur-3xl dark:bg-sky/10"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -right-24 bottom-0 size-[22rem] rounded-full bg-lime/20 blur-3xl dark:bg-lime/5"
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] px-2 pb-6 pt-10 sm:px-4 sm:pt-14">
        <motion.div
          variants={reveal}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.15 }}
          className="overflow-hidden rounded-[2rem] border border-line bg-paper shadow-lift"
        >
          <div className="grid gap-10 p-6 sm:p-10 lg:grid-cols-[1.5fr_2fr] lg:gap-14 lg:p-12">
            <motion.div variants={item}>
              <Link to="/" className="group inline-flex items-center gap-3">
                <Logo className="text-ink transition-colors group-hover:text-accent" />
                <span className="font-brand text-[0.9375rem] uppercase leading-none tracking-[-0.01em]">
                  MANABI
                </span>
              </Link>

              <p className="mt-5 max-w-xs text-body leading-relaxed text-ink-soft">
                Pick a real problem, build it in public, and show the work in a
                public repo. Made for devs who ship.
              </p>

              <div className="mt-6 flex flex-col gap-2.5 text-body text-ink-soft">
                <a
                  href={X_URL}
                  target="_blank"
                  rel="noreferrer"
                  className="group inline-flex w-fit items-center gap-2.5 transition-colors hover:text-ink"
                >
                  <span className="flex size-7 items-center justify-center rounded-full border border-line bg-tint text-ink">
                    <XMark size={13} />
                  </span>
                  @Piyush_NextGen
                </a>
              </div>
            </motion.div>

            <div className="grid gap-8 sm:grid-cols-3">
              {FOOTER_COLUMNS.map((column) => (
                <motion.div key={column.heading} variants={item}>
                  <h2 className="font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
                    {column.heading}
                  </h2>
                  <ul className="mt-4 flex flex-col gap-2.5">
                    {column.links.map((link) => (
                      <li key={`${column.heading}-${link.label}`}>
                        <Link
                          to={link.to}
                          className="group inline-flex items-center gap-1 text-body leading-snug text-ink-soft transition-colors hover:text-ink"
                        >
                          <span className="relative">
                            {link.label}
                            <span className="absolute inset-x-0 -bottom-0.5 h-px origin-left scale-x-0 bg-ink transition-transform duration-300 group-hover:scale-x-100" />
                          </span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </div>

          <motion.div
            variants={item}
            className="grid gap-6 border-t border-line px-6 py-6 sm:px-10 lg:grid-cols-[1fr_auto] lg:items-center lg:px-12"
          >
            <div>
              <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-ink">
                Get new briefs first
              </p>
              <p className="mt-1.5 max-w-md text-body leading-relaxed text-ink-soft">
                New briefs, fixes and features land on GitHub first. Follow the
                build and watch it ship.
              </p>
            </div>

            {CONTACT_EMAIL ? (
              <form
                className="flex w-full max-w-md gap-2"
                onSubmit={handleSubscribe}
              >
                <label htmlFor="footer-email" className="sr-only">
                  Email address
                </label>
                <input
                  id="footer-email"
                  name="email"
                  type="email"
                  required
                  placeholder="Enter your email"
                  className="field min-w-0 flex-1 rounded-full text-body"
                />
                <button
                  type="submit"
                  className="press inline-flex shrink-0 items-center gap-1.5 rounded-full bg-ink px-4 py-2.5 text-[0.8125rem] font-semibold text-paper transition-colors hover:bg-ink/90"
                >
                  Subscribe
                  <ArrowUpRight aria-hidden size={13} strokeWidth={2.6} />
                </button>
              </form>
            ) : (
              <a
                href={REPO_URL}
                target="_blank"
                rel="noreferrer"
                aria-label="Star MANABI on GitHub"
                className="press group inline-flex w-fit items-center gap-2 rounded-full bg-ink px-5 py-3 text-[0.875rem] font-semibold text-paper transition-colors hover:bg-ink/90"
              >
                <Star
                  aria-hidden
                  size={12}
                  strokeWidth={2.4}
                  fill="currentColor"
                  className="text-paper"
                />
                <GithubMark
                  size={14}
                  className="text-paper/80 transition-colors group-hover:text-paper"
                />
                Star on GitHub
              </a>
            )}
          </motion.div>

          <div className="relative border-t border-line px-6 py-6 sm:px-10 lg:px-12">
            <div
              aria-hidden
              className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-sky/20 to-transparent dark:bg-none"
            />

            <div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
              <p className="font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
                Real problems · public builds · open source
              </p>

              <div className="flex flex-wrap items-center gap-x-5 gap-y-2 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
                <Link to="/privacy" className="transition-colors hover:text-ink">
                  Privacy
                </Link>
                <Link to="/terms" className="transition-colors hover:text-ink">
                  Terms
                </Link>
                <span>© 2026 MANABI</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </footer>
  );
}
