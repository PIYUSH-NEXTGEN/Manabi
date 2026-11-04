import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { slideUpReveal } from '@/design/motion';
import { useStats } from '@/hooks/useStats';
import { CountUp } from './CountUp';
import {
  ArrowRight,
  ArrowUpRight,
  FileText,
  GitBranch,
  Layers,
  ScanSearch,
} from 'lucide-react';

const SLIP_ROWS = [
  { key: 'problems', label: 'Briefs', icon: FileText },
  { key: 'fields', label: 'Fields', icon: Layers },
  { key: 'projects', label: 'Projects', icon: GitBranch },
] as const;

export function FinalCta() {
  const stats = useStats();

  return (
    <section className="relative overflow-hidden border-b border-ink bg-accent text-paper">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(-45deg, rgba(234,229,219,0.09) 0 1px, transparent 1px 14px)',
        }}
      />

      <div className="relative mx-auto w-[min(1240px,96vw)] py-16 md:py-20">
        <div className="grid items-end gap-12 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16">
          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-paper/35 pb-3 font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-paper/90">
              <span>
                <span className="text-paper">04</span> / Open call
              </span>
              <span>Doc. no. EA.2026.001</span>
            </div>

            <h2
              className="mt-7 font-display uppercase leading-[0.86] tracking-[-0.02em]"
              style={{ fontSize: 'clamp(2.5rem, 7vw, 5.5rem)' }}
            >
              Find it. Build it.
              <br />
              <span className="text-paper/85">Ship it in public.</span>
            </h2>

            <p className="mt-6 max-w-lg text-sm leading-relaxed text-paper/90 sm:text-base">
              The index is open. Pick a brief, link your repository, and let the
              commits say the rest. Browsing needs no account.
            </p>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link
                to="/problems"
                className="group inline-flex items-center gap-2 border border-paper bg-paper px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-ink transition-colors hover:bg-ink hover:text-paper"
              >
                Browse problems
                <ArrowRight
                  aria-hidden
                  size={14}
                  strokeWidth={2.6}
                  className="transition-transform group-hover:translate-x-0.5"
                />
              </Link>
              <Link
                to="/repo-analyzer"
                className="group inline-flex items-center gap-2 border border-paper/70 px-5 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-paper transition-colors hover:border-paper hover:bg-paper hover:text-ink"
              >
                <ScanSearch aria-hidden size={14} strokeWidth={2.4} />
                Repo analyzer
                <ArrowUpRight
                  aria-hidden
                  size={13}
                  strokeWidth={2.6}
                  className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
                />
              </Link>
            </div>
          </motion.div>

          <motion.div
            variants={slideUpReveal}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            transition={{ delay: 0.1 }}
            className="border border-paper bg-paper text-ink shadow-[6px_6px_0_0_rgba(23,21,15,0.3)] sm:shadow-[14px_14px_0_0_rgba(23,21,15,0.3)]"
          >
            <div className="flex items-center justify-between gap-3 border-b border-ink px-4 py-2.5">
              <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]">
                Catalog at a glance
              </span>
              <span className="flex items-center gap-1.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-muted">
                <span aria-hidden className="block size-1.5 bg-accent" />
                Live
              </span>
            </div>

            <ul className="divide-y divide-line">
              {SLIP_ROWS.map(({ key, label, icon: Icon }) => (
                <li
                  key={key}
                  className="flex items-center justify-between gap-3 px-4 py-3.5"
                >
                  <span className="flex items-center gap-2 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
                    <Icon aria-hidden size={14} strokeWidth={2.2} />
                    {label}
                  </span>
                  <span className="font-display text-2xl leading-none">
                    {stats.data ? <CountUp value={stats.data[key]} /> : '0'}
                  </span>
                </li>
              ))}
            </ul>

            <Link
              to="/problems"
              className="group flex items-center justify-between gap-3 border-t border-line px-4 py-2.5 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-accent transition-colors hover:bg-tint/40 hover:text-ink"
            >
              Open the index
              <ArrowRight
                aria-hidden
                size={13}
                strokeWidth={2.6}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
