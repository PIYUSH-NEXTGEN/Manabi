import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import {
  ArrowUpRight,
  BrainCircuit,
  FileText,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';
import { VerificationConsole } from './VerificationConsole';

const STEPS = [
  {
    step: '01',
    icon: ShieldCheck,
    title: 'Your own repo',
    copy: 'A public GitHub repo you own. Forks and other people’s repos don’t count.',
  },
  {
    step: '02',
    icon: FileText,
    title: 'README + 5 commits',
    copy: 'Your repo needs a README and at least 5 commits.',
  },
  {
    step: '03',
    icon: BrainCircuit,
    title: 'AI checks relevance',
    copy: 'AI reads your README and checks it matches the brief.',
  },
  {
    step: '04',
    icon: RefreshCw,
    title: 'Tracked after approval',
    copy: 'Commits, README and open issues update from GitHub.',
  },
];

const LEFT_REVEAL = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08, delayChildren: 0.05 } },
};

const LIST_REVEAL = {
  hidden: {},
  show: { transition: { staggerChildren: 0.06 } },
};

const ITEM_REVEAL = {
  hidden: { opacity: 0, y: 14 },
  show: { opacity: 1, y: 0, transition: { duration: 0.34, ease: EASE_SNAP } },
};

export function BuildInPublic() {
  return (
    <section className="relative overflow-hidden border-b border-ink bg-olive text-paper dark:bg-[#2f3025] dark:text-ink">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(90deg, rgba(234,229,219,0.07) 0 1px, transparent 1px 96px)',
        }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -right-32 top-1/2 hidden size-[520px] -translate-y-1/2 border border-paper/10 lg:block dark:border-ink/10"
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] py-14 md:py-20">
        <motion.div
          variants={slideUpReveal}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.4 }}
          className="flex flex-wrap items-center justify-between gap-3 border-b border-paper/25 pb-3 dark:border-ink/25"
        >
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/60 dark:text-ink/60">
            <span className="text-accent-soft dark:text-ink">02</span> / Submission
          </p>
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/45 dark:text-ink/45">
            Checked, not claimed
          </p>
        </motion.div>

        <div className="mt-10 grid items-center gap-12 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)] lg:gap-16 xl:gap-20">
          <motion.div
            variants={LEFT_REVEAL}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
          >
            <motion.h2
              variants={ITEM_REVEAL}
              className="font-display text-4xl uppercase leading-[0.9] tracking-tight sm:text-5xl xl:text-[3.65rem]"
            >
              Submit a repo.
              <br />
              <span className="text-accent-soft dark:text-ink">
                We check the work.
              </span>
            </motion.h2>

            <motion.p
              variants={ITEM_REVEAL}
              className="mt-5 max-w-md text-sm leading-relaxed text-paper/75 dark:text-ink/75"
            >
              Every project is checked before it goes public: your own repo, a
              README, real commits, then an AI relevance check. Only what passes
              gets tracked.
            </motion.p>

            <motion.ul
              variants={LIST_REVEAL}
              className="mt-8 border-t border-paper/20 dark:border-ink/20"
            >
              {STEPS.map(({ step, icon: Icon, title, copy }) => (
                <motion.li
                  key={step}
                  variants={ITEM_REVEAL}
                  className="flex items-start gap-4 border-b border-paper/20 py-4 dark:border-ink/20"
                >
                  <span className="mt-0.5 font-mono text-[9px] font-bold tracking-[0.16em] text-paper/35 dark:text-ink/35">
                    {step}
                  </span>
                  <Icon
                    aria-hidden
                    size={17}
                    strokeWidth={2.1}
                    className="mt-0.5 shrink-0 text-accent-soft dark:text-ink"
                  />
                  <div className="min-w-0">
                    <h3 className="font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
                      {title}
                    </h3>
                    <p className="mt-1 text-[13px] leading-snug text-paper/65 dark:text-ink/65">
                      {copy}
                    </p>
                  </div>
                </motion.li>
              ))}
            </motion.ul>

            <motion.p
              variants={ITEM_REVEAL}
              className="mt-5 border-l-2 border-accent-soft/60 pl-3 text-[12px] leading-relaxed text-paper/60 dark:border-ink/40 dark:text-ink/60"
            >
              If the AI can’t judge, a keyword check takes over. It can send work
              to human review, but never mark it verified.
            </motion.p>

            <motion.div variants={ITEM_REVEAL} className="mt-8">
              <Link
                to="/problems"
                className="group inline-flex items-center gap-2 border border-paper bg-paper px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-ink transition-colors hover:border-accent hover:bg-accent hover:text-paper dark:border-ink dark:bg-transparent dark:text-ink dark:hover:border-accent dark:hover:bg-accent dark:hover:text-[#f4f0e7]"
              >
                Claim a problem
                <ArrowUpRight
                  aria-hidden
                  size={14}
                  strokeWidth={2.6}
                  className="transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
                />
              </Link>
            </motion.div>
          </motion.div>

          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            transition={{ delay: 0.1 }}
          >
            <div className="mb-3 flex flex-wrap items-center justify-between gap-2 font-mono text-[9px] font-bold uppercase tracking-[0.18em] text-paper/45 dark:text-ink/45">
              <span className="flex items-center gap-2">
                <span
                  aria-hidden
                  className="block size-1.5 bg-accent-soft motion-safe:animate-pulse dark:bg-accent"
                />
                Live sample
              </span>
              <span>Auto-loops while in view</span>
            </div>

            <VerificationConsole />

            <p className="mt-3 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/40 dark:text-ink/40">
              Sample run only — no repo is submitted.
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}