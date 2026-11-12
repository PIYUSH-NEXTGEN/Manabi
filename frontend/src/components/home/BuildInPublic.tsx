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
    <section className="border-b border-line bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-14 md:py-20">
        <div className="relative overflow-hidden rounded-xl bg-accent-soft px-6 py-10 text-ink shadow-lift sm:px-10 md:py-14">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0"
            style={{
              backgroundImage:
                'radial-gradient(60% 80% at 92% -10%, rgba(255,255,255,0.75) 0%, transparent 60%), radial-gradient(55% 70% at 0% 110%, rgba(191,227,255,0.55) 0%, transparent 65%)',
            }}
          />

          <div className="relative">
            <motion.div
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.4 }}
              className="flex flex-wrap items-center justify-between gap-3 border-b border-ink/10 pb-3"
            >
              <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-ink/65">
                <span className="text-ink">02</span> / Submission
              </p>
              <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-ink/45">
                Checked, not claimed
              </p>
            </motion.div>

            <div className="mt-10 grid items-start gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] lg:gap-16 xl:gap-20">
              <motion.div
                variants={LEFT_REVEAL}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true, amount: 0.25 }}
              >
                <motion.h2
                  variants={ITEM_REVEAL}
                  className="text-balance font-display text-display leading-[1.05] tracking-[-0.03em]"
                >
                  Submit a repo.
                  <br />
                  <span className="text-ink/55">We check the work.</span>
                </motion.h2>

                <motion.p
                  variants={ITEM_REVEAL}
                  className="mt-5 max-w-lg text-body leading-relaxed text-ink/70"
                >
                  Every project is checked before it goes public: your own repo, a
                  README, real commits, then an AI relevance check. Only what passes
                  gets tracked.
                </motion.p>

                <motion.p
                  variants={ITEM_REVEAL}
                  className="mt-6 rounded-panel border border-ink/10 bg-paper/55 px-4 py-3 text-label leading-relaxed text-ink/65"
                >
                  If the AI can’t judge, a keyword check takes over. It can send work
                  to human review, but never mark it verified.
                </motion.p>

                <motion.div variants={ITEM_REVEAL} className="mt-9">
                  <Link
                    to="/problems"
                    className="press group inline-flex items-center gap-2 rounded-full bg-ink px-5 py-3.5 text-[0.875rem] font-semibold text-paper transition-colors hover:bg-ink/90"
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

              <motion.ul
                variants={LIST_REVEAL}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true, amount: 0.25 }}
                transition={{ delay: 0.1 }}
                className="flex flex-col gap-2"
              >
                {STEPS.map(({ step, icon: Icon, title, copy }) => (
                  <motion.li
                    key={step}
                    variants={ITEM_REVEAL}
                    className="flex items-start gap-4 rounded-panel border border-ink/10 bg-paper/55 px-4 py-3.5"
                  >
                    <span className="mt-1.5 w-5 shrink-0 font-mono text-label font-bold tracking-[0.14em] text-ink/35">
                      {step}
                    </span>
                    <Icon
                      aria-hidden
                      size={17}
                      strokeWidth={2.1}
                      className="mt-1 shrink-0 text-ink"
                    />
                    <div className="min-w-0">
                      <h3 className="text-[0.9375rem] font-semibold leading-snug">
                        {title}
                      </h3>
                      <p className="mt-1 text-body leading-relaxed text-ink/65">
                        {copy}
                      </p>
                    </div>
                  </motion.li>
                ))}
              </motion.ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
