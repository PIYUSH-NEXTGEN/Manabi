import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { ArrowRight } from 'lucide-react';
import { EASE_SNAP } from '@/design/motion';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { HeroScene } from '@/components/home/HeroScene';

const HEADLINE_LINES = ['Stop Searching.', 'Start Building.'];
const HEADLINE_STEP_MS = 700;

/** Two-line centered headline, revealed without layout shift. */
function HeroHeadline() {
  const reduced = usePrefersReducedMotion();

  return (
    <h1 className="hero-headline text-balance font-hero text-hero leading-[0.98] tracking-[-0.035em] text-ink">
      {HEADLINE_LINES.map((line, index) => (
        <motion.span
          key={line}
          className={
            index === 1
              ? 'block font-serif font-normal italic tracking-[-0.02em]'
              : 'block'
          }
          initial={reduced ? false : { opacity: 0, y: 22 }}
          animate={{ opacity: 1, y: 0 }}
          transition={
            reduced
              ? { duration: 0 }
              : {
                  duration: 0.8,
                  delay: 0.12 + (index * HEADLINE_STEP_MS) / 1000,
                  ease: EASE_SNAP,
                }
          }
        >
          {line}{' '}
        </motion.span>
      ))}
    </h1>
  );
}

export function Hero() {
  const reduced = usePrefersReducedMotion();

  return (
    <section className="relative isolate flex min-h-[100svh] flex-col overflow-hidden">
      <HeroScene />

      <div className="hero-copy relative mx-auto flex w-full max-w-[1220px] flex-1 flex-col justify-center px-5 pb-20 pt-32 text-center sm:px-6 sm:pb-28 sm:pt-40">
        <div className="relative mx-auto max-w-5xl">
          <div
            aria-hidden
            className="pointer-events-none absolute -inset-x-6 -inset-y-5 -z-10 rounded-[50%] bg-[radial-gradient(ellipse_at_center,var(--paper)_0%,var(--paper)_46%,transparent_76%)] opacity-90 sm:hidden"
          />
          <HeroHeadline />

          <motion.div
            initial={reduced ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={
              reduced
                ? { duration: 0 }
                : { duration: 0.6, delay: 0.45, ease: EASE_SNAP }
            }
            className="hero-sub mx-auto mt-7 max-w-2xl text-balance text-lead leading-relaxed font-medium text-ink/85"
          >
            <p>
              Tired of searching for the project to build? MANABI gives you
              quality projects worth building. Pick a problem, build your
              solution, connect your GitHub repo. Whether you're learning,
              building resume, preparing for hackathons, find something worth
              building with MANABI.
            </p>
          </motion.div>

          <motion.div
            initial={reduced ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={
              reduced
                ? { duration: 0 }
                : { duration: 0.6, delay: 0.6, ease: EASE_SNAP }
            }
            className="hero-cta mt-9 flex justify-center"
          >
            <Link
              to="/problems"
              className="press group inline-flex items-center justify-center gap-2 rounded-full bg-ink px-7 py-4 text-[0.9375rem] font-semibold text-paper transition-colors hover:bg-ink/90"
            >
              Explore Projects
              <ArrowRight
                aria-hidden
                size={16}
                strokeWidth={2.4}
                className="transition-transform duration-200 group-hover:translate-x-0.5"
              />
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
