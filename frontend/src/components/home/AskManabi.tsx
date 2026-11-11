import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { EASE_SNAP, slideUpReveal } from '@/design/motion';
import { buttonClasses } from '@/design/primitives';
import { openChatWidget } from '@/components/chat/ChatWidget';
import {
  ArrowUpRight,
  FileText,
  Link2,
  MessageSquare,
  ShieldCheck,
  Timer,
} from 'lucide-react';

const POINTS = [
  {
    icon: Timer,
    copy: 'Say how much time you have. Weekend, week, or month.',
  },
  {
    icon: FileText,
    copy: 'It reads the index and answers from real briefs only.',
  },
  {
    icon: Link2,
    copy: 'Every suggestion links to the brief it came from.',
  },
];

const CHAT_REVEAL = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1, delayChildren: 0.1 } },
};

const BUBBLE_REVEAL = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3, ease: EASE_SNAP } },
};

function ChatPreview() {
  return (
    <div className="border border-ink bg-sheet shadow-[6px_6px_0_0_rgba(23,21,15,0.14)] sm:shadow-[10px_10px_0_0_rgba(23,21,15,0.14)]">
      <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-2.5">
        <span className="flex items-center gap-2 font-mono text-label font-bold uppercase tracking-[0.16em]">
          <MessageSquare aria-hidden size={13} strokeWidth={2.4} />
          Catalog assistant
        </span>
        <span className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          Example exchange
        </span>
      </div>

      <motion.div
        variants={CHAT_REVEAL}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.3 }}
        className="space-y-3 p-4 sm:p-5"
      >
        <motion.p
          variants={BUBBLE_REVEAL}
          className="ml-auto w-fit max-w-[85%] border border-ink bg-ink px-3.5 py-2.5 text-body leading-snug text-paper"
        >
          I know React and a little Python. What can I ship in a weekend?
        </motion.p>

        <motion.p
          variants={BUBBLE_REVEAL}
          className="w-fit max-w-[92%] border border-line bg-paper px-3.5 py-2.5 text-body leading-snug"
        >
          Three briefs fit that scope, all pulled from the index:
        </motion.p>

        <motion.ul variants={BUBBLE_REVEAL} className="space-y-2">
          {[
            { id: 'Brief 01', title: 'A civic reporting queue', scope: '2 days' },
            { id: 'Brief 02', title: 'A pipeline that fails loudly', scope: '3 days' },
            { id: 'Brief 03', title: 'A small vision demo', scope: '3 days' },
          ].map((item) => (
            <li
              key={item.id}
              className="flex items-center justify-between gap-3 border border-line bg-paper px-3 py-2"
            >
              <span className="flex min-w-0 items-center gap-2">
                <FileText aria-hidden size={13} strokeWidth={2.2} className="shrink-0 text-accent" />
                <span className="truncate text-body">{item.title}</span>
              </span>
              <span className="shrink-0 font-mono text-label font-bold uppercase tracking-[0.14em] text-muted">
                {item.scope}
              </span>
            </li>
          ))}
        </motion.ul>

        <motion.p
          variants={BUBBLE_REVEAL}
          className="w-fit max-w-[92%] border border-line bg-paper px-3.5 py-2.5 text-body leading-snug"
        >
          Start with the queue if you want a working demo by Sunday night.
        </motion.p>
      </motion.div>

      <p className="flex items-center gap-2 border-t border-line px-4 py-2.5 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
        <ShieldCheck aria-hidden size={12} strokeWidth={2.4} />
        Grounded in the index. It never invents a brief.
      </p>
    </div>
  );
}

export function AskManabi() {
  return (
    <section className="relative overflow-hidden border-b border-ink bg-paper">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(-45deg, rgba(23,21,15,0.035) 0 1px, transparent 1px 12px)',
        }}
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] py-16 md:py-20">
        <div className="grid items-center gap-12 lg:grid-cols-[0.95fr_1.05fr] lg:gap-16">
          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-ink pb-3">
              <p className="font-mono text-label font-bold uppercase tracking-[0.2em] text-muted">
                <span className="text-accent">03</span> / Ask the catalog
              </p>
              <span className="flex items-center gap-1.5 font-mono text-label font-bold uppercase tracking-[0.2em] text-muted">
                <MessageSquare aria-hidden size={12} strokeWidth={2.4} />
                Chat
              </span>
            </div>

            <h2 className="mt-7 font-display text-display uppercase leading-[0.9] tracking-tight">
              Ask <span className="text-accent">MANABI</span>
            </h2>
            <p className="mt-5 max-w-md text-body leading-relaxed text-ink-soft">
              Tell it what you know and what you want to build. It searches the
              index, matches the scope to the time you have, and points you at
              briefs that already exist.
            </p>

            <ul className="mt-7 space-y-3">
              {POINTS.map(({ icon: Icon, copy }) => (
                <li key={copy} className="flex items-start gap-3">
                  <Icon
                    aria-hidden
                    size={15}
                    strokeWidth={2.3}
                    className="mt-0.5 shrink-0 text-accent"
                  />
                  <span className="text-body leading-snug text-ink-soft">
                    {copy}
                  </span>
                </li>
              ))}
            </ul>

            <button
              type="button"
              onClick={openChatWidget}
              className={buttonClasses('primary', 'group mt-8')}
            >
              Open the chat
              <ArrowUpRight
                aria-hidden
                size={14}
                strokeWidth={2.6}
                className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
              />
            </button>
          </motion.div>

          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
          >
            <ChatPreview />
          </motion.div>
        </div>

        <p className="mt-10 border-t border-line pt-4 font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
          Prefer to browse?{' '}
          <Link
            to="/problems"
            className="text-accent underline underline-offset-4 hover:text-ink"
          >
            Skip the chat and open the index
          </Link>
        </p>
      </div>
    </section>
  );
}
