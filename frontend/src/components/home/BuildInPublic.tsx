import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import {
  ArrowUpRight,
  FileText,
  GitCommitHorizontal,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';

const REQUIREMENTS = [
  {
    icon: ShieldCheck,
    title: 'Your own repo',
    copy: 'A public GitHub repo that belongs to you. Forks and other people’s repos don’t count.',
  },
  {
    icon: FileText,
    title: 'README + 5 commits',
    copy: 'Your README explains what you built. At least five real commits show the work.',
  },
  {
    icon: GitCommitHorizontal,
    title: 'It matches the brief',
    copy: 'Build the project you claimed, not something different with a borrowed name.',
  },
  {
    icon: RefreshCw,
    title: 'Easy to open and check',
    copy: 'Share a working demo link and a repo anyone can read. Private or empty repos can’t pass.',
  },
];

const REVIEW = [
  {
    step: '01',
    title: 'Submit the repo',
    copy: 'Add your public repo and demo link to the problem you claimed.',
  },
  {
    step: '02',
    title: 'Automated checks',
    copy: 'We quickly check that the repo is yours, the README is real, and there are at least five commits.',
  },
  {
    step: '03',
    title: 'AI checks relevance',
    copy: 'We compare your README with the brief. If it’s a weak match, we flag it.',
  },
  {
    step: '04',
    title: 'Accept or reject',
    copy: 'You get a clear answer. Passes go live; unclear cases go to a person.',
  },
];

const REVEAL = {
  hidden: {},
  show: { transition: { staggerChildren: 0.07, delayChildren: 0.04 } },
};

const ITEM = {
  hidden: { opacity: 0, y: 14 },
  show: { opacity: 1, y: 0, transition: { duration: 0.36, ease: EASE_SNAP } },
};

export function BuildInPublic() {
  return (
    <section className="border-b border-line bg-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-14 md:py-20">
        <div className="relative overflow-hidden rounded-[2rem] border border-ink/10 bg-accent-soft text-ink shadow-lift dark:bg-sheet">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 dark:hidden"
            style={{
              backgroundImage:
                'radial-gradient(58% 80% at 94% -10%, rgba(255,255,255,0.7) 0%, transparent 60%), radial-gradient(55% 70% at 0% 112%, rgba(201,242,109,0.28) 0%, transparent 62%)',
            }}
          />

          <div className="relative p-6 sm:p-10 md:p-12">
            <motion.div
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.4 }}
              className="border-b border-ink/10 pb-3"
            >
              <p className="font-mono text-label font-bold uppercase tracking-[0.18em] text-ink/65">
                <span className="text-ink">02</span> / Submission &amp; review
              </p>
            </motion.div>

            <motion.div
              variants={REVEAL}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.2 }}
              className="mt-8"
            >
              <motion.div variants={ITEM}>
                <h2 className="text-balance font-display text-display leading-[1.05] tracking-[-0.03em]">
                  Submit your project.
                  <br />
                  <span className="text-ink/55">Here’s how we check it.</span>
                </h2>
                <p className="mt-5 max-w-xl text-body leading-relaxed text-ink/70">
                  We run the same checks on every project before it goes on the
                  board. Here’s what you need and what happens after you submit.
                </p>
              </motion.div>
            </motion.div>

            <div className="mt-8 grid gap-4 lg:grid-cols-2">
              <motion.div
                variants={REVEAL}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true, amount: 0.2 }}
                className="rounded-panel border border-ink/10 bg-paper/55 p-5 sm:p-6"
              >
                <div className="flex items-center justify-between gap-3">
                  <h3 className="font-mono text-label font-bold uppercase tracking-[0.16em] text-ink/70">
                    What you need to submit
                  </h3>
                  <span className="font-mono text-label font-bold uppercase tracking-[0.14em] text-ink/40">
                    4 requirements
                  </span>
                </div>
                <ul className="mt-4 divide-y divide-ink/10">
                  {REQUIREMENTS.map(({ icon: Icon, title, copy }) => (
                    <motion.li
                      key={title}
                      variants={ITEM}
                      className="flex items-start gap-3 py-3 first:pt-0 last:pb-0"
                    >
                      <span className="mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-full border border-ink/15 bg-paper/70">
                        <Icon aria-hidden size={14} strokeWidth={2.2} className="text-ink" />
                      </span>
                      <div className="min-w-0">
                        <h4 className="text-[0.9375rem] font-semibold leading-snug">
                          {title}
                        </h4>
                        <p className="mt-1 text-body leading-relaxed text-ink/65">
                          {copy}
                        </p>
                      </div>
                    </motion.li>
                  ))}
                </ul>
              </motion.div>

              <motion.div
                variants={REVEAL}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true, amount: 0.2 }}
                className="rounded-panel border border-ink/10 bg-paper/55 p-5 sm:p-6"
              >
                <div className="flex items-center justify-between gap-3">
                  <h3 className="font-mono text-label font-bold uppercase tracking-[0.16em] text-ink/70">
                    What happens next
                  </h3>
                  <span className="font-mono text-label font-bold uppercase tracking-[0.14em] text-ink/40">
                    Same for everyone
                  </span>
                </div>
                <ol className="mt-4 space-y-3">
                  {REVIEW.map(({ step, title, copy }, index) => (
                    <motion.li
                      key={step}
                      variants={ITEM}
                      className="relative flex gap-3 pb-3 last:pb-0"
                    >
                      <span className="relative flex shrink-0 flex-col items-center">
                        <span className="flex size-7 items-center justify-center rounded-full bg-ink font-mono text-label font-bold text-paper">
                          {index + 1}
                        </span>
                        {index < REVIEW.length - 1 ? (
                          <span className="mt-1 h-full w-px flex-1 bg-ink/15" />
                        ) : null}
                      </span>
                      <div className="min-w-0 pb-1">
                        <h4 className="text-[0.9375rem] font-semibold leading-snug">
                          {title}
                        </h4>
                        <p className="mt-1 text-body leading-relaxed text-ink/65">
                          {copy}
                        </p>
                      </div>
                    </motion.li>
                  ))}
                </ol>
              </motion.div>
            </div>

            <motion.div
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.4 }}
              className="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-ink/10 pt-6"
            >
              <p className="max-w-md text-label leading-relaxed text-ink/60">
                If something is unclear, a person takes a look. Nothing goes live
                until every check passes.
              </p>
              <div className="flex flex-wrap items-center gap-3">
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
                <Link
                  to="/about"
                  className="press inline-flex items-center gap-2 rounded-full border border-ink/15 bg-paper/60 px-5 py-3.5 text-[0.875rem] font-semibold text-ink transition-colors hover:bg-paper/85"
                >
                  Read the review guide
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
