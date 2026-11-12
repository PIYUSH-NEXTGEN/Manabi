import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { ArrowRight } from 'lucide-react';
import { EASE_SNAP } from '@/design/motion';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

const HEADLINE_LINES = ['Pick a project.', 'Ship it. Prove it.'];
const HEADLINE_STEP_MS = 700;

/** Two-line centered headline, revealed without layout shift. */
function HeroHeadline() {
  const reduced = usePrefersReducedMotion();

  return (
    <h1 className="text-balance font-hero text-hero leading-[0.98] tracking-[-0.035em] text-ink">
      {HEADLINE_LINES.map((line, index) => (
        <motion.span
          key={line}
          className="block"
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

function HeroScene() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 -z-10 overflow-hidden"
    >
      <div className="hero-sky absolute inset-0" />

      {/* A soft sun and a handful of drifting clouds keep the scene alive
          without pulling attention away from the copy. */}
      <div className="absolute right-[9%] top-[9%] size-48 rounded-full bg-sky/40 blur-3xl dark:bg-sky/10" />
      <div className="absolute left-[2%] top-[42%] size-56 rounded-full bg-sky/20 blur-3xl dark:bg-sky/10" />

      <div
        className="cloud-drift absolute left-[8%] top-[24%] h-14 w-56 rounded-full bg-white/80 blur-xl dark:bg-sky/10"
        style={{ animationDuration: '34s' }}
      />
      <div
        className="cloud-drift absolute left-[22%] top-[17%] h-10 w-40 rounded-full bg-white/70 blur-lg dark:bg-sky/10"
        style={{ animationDuration: '28s', animationDelay: '-6s' }}
      />
      <div
        className="cloud-drift absolute right-[14%] top-[30%] h-12 w-48 rounded-full bg-white/75 blur-xl dark:bg-sky/10"
        style={{ animationDuration: '40s', animationDelay: '-14s' }}
      />
      <div
        className="cloud-drift absolute right-[30%] top-[12%] h-8 w-32 rounded-full bg-white/60 blur-lg dark:bg-sky/10"
        style={{ animationDuration: '30s', animationDelay: '-3s' }}
      />
      <div
        className="cloud-drift absolute left-[42%] top-[8%] h-7 w-28 rounded-full bg-white/55 blur-lg dark:bg-sky/10"
        style={{ animationDuration: '38s', animationDelay: '-20s' }}
      />

      <div className="absolute inset-0 hidden md:block">
        <svg
          className="twinkle absolute left-[12%] top-[34%] text-ink/15"
          width="26"
          height="26"
          viewBox="0 0 24 24"
          fill="currentColor"
          style={{ animationDelay: '-1.5s' }}
        >
          <path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12C7 11 11 7 12 0Z" />
        </svg>
        <svg
          className="twinkle absolute right-[13%] top-[25%] text-sky-strong"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="currentColor"
          style={{ animationDelay: '-3.4s' }}
        >
          <path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12C7 11 11 7 12 0Z" />
        </svg>
        <svg
          className="twinkle absolute left-[17%] top-[56%] text-ink/10"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="currentColor"
          style={{ animationDelay: '-5s' }}
        >
          <path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12C7 11 11 7 12 0Z" />
        </svg>
      </div>

      <div
        className="cloud-drift absolute right-[20%] top-[22%] hidden sm:block"
        style={{ animationDuration: '46s', animationDelay: '-11s' }}
      >
        <svg width="58" height="78" viewBox="0 0 64 86" fill="none" aria-hidden>
          <path
            d="M32 2c17 0 28 13 28 28 0 17-18 31-28 39C22 61 4 47 4 30 4 15 15 2 32 2Z"
            fill="var(--sky)"
            stroke="var(--ink)"
            strokeOpacity="0.12"
            strokeWidth="1.5"
          />
          <path
            d="M32 2c-8 8-12 20-12 34 0 13 5 24 12 32"
            stroke="var(--scene-snow)"
            strokeOpacity="0.7"
            strokeWidth="2"
          />
          <path
            d="M32 2c8 8 12 20 12 34 0 13-5 24-12 32"
            stroke="var(--scene-snow)"
            strokeOpacity="0.45"
            strokeWidth="2"
          />
          <path
            d="M27 62l-4 10M37 62l4 10"
            stroke="var(--ink)"
            strokeOpacity="0.35"
            strokeWidth="1.5"
          />
          <rect x="22" y="72" width="20" height="12" rx="3" fill="var(--ink)" opacity="0.85" />
        </svg>
      </div>

      <svg
        className="absolute inset-x-0 bottom-0 h-[68%] w-full"
        viewBox="0 0 1440 760"
        preserveAspectRatio="none"
        fill="none"
        aria-hidden
      >
        <defs>
          <g id="hero-tree">
            <rect x="-3" y="-40" width="6" height="40" rx="3" fill="var(--scene-tree)" />
            <circle cx="0" cy="-54" r="27" fill="var(--scene-tree)" />
            <circle cx="-21" cy="-38" r="18" fill="var(--scene-tree)" />
            <circle cx="21" cy="-38" r="18" fill="var(--scene-tree)" />
          </g>
          <g id="hero-bush">
            <circle cx="-14" cy="0" r="13" fill="var(--scene-tree)" />
            <circle cx="0" cy="-9" r="18" fill="var(--scene-tree)" />
            <circle cx="16" cy="0" r="12" fill="var(--scene-tree)" />
          </g>
        </defs>

        {/* Distant peaks give the horizon some architecture. */}
        <path
          d="M0 448L118 328L214 412L332 296L454 424L572 346L692 440L822 310L962 438L1082 362L1202 430L1322 330L1440 418V760H0V448Z"
          fill="var(--scene-far)"
        />
        <g fill="var(--scene-snow)" opacity="0.32">
          <path d="M332 296L364 332L344 344L328 330L310 340L302 328Z" />
          <path d="M822 310L850 342L832 352L818 340L802 348L796 336Z" />
          <path d="M1322 330L1348 360L1330 370L1318 358L1304 366L1298 354Z" />
        </g>
        <path
          d="M0 512L152 400L282 490L412 380L562 510L702 424L842 518L982 410L1122 518L1262 440L1382 510L1440 468V760H0V512Z"
          fill="var(--scene-mid)"
          opacity="0.85"
        />

        {/* Rolling hills, back to front. */}
        <path
          d="M0 526C220 476 360 546 560 516C780 481 920 546 1120 511C1260 488 1360 526 1440 506V760H0V526Z"
          fill="var(--scene-far)"
          opacity="0.92"
        />
        <path
          d="M0 596C180 526 360 586 560 556C760 526 930 606 1120 571C1280 542 1370 581 1440 566V760H0V596Z"
          fill="var(--scene-mid)"
        />
        <path
          d="M0 666C220 616 380 666 580 646C800 624 980 686 1180 656C1300 638 1380 666 1440 654V760H0V666Z"
          fill="var(--scene-near)"
        />

        {/* A quiet river winding toward the viewer. */}
        <path
          d="M704 506C766 566 626 626 726 696C826 756 686 736 746 766L866 766C806 726 926 706 826 646C736 592 866 550 806 506Z"
          fill="var(--scene-water)"
          opacity="0.7"
        />
        <path
          d="M720 546C766 592 664 638 734 700"
          stroke="var(--scene-snow)"
          strokeOpacity="0.85"
          strokeWidth="2"
        />
        <path
          d="M0 706C220 666 380 706 580 686C800 664 980 716 1180 694C1300 681 1380 706 1440 696V760H0V706Z"
          fill="var(--scene-front)"
        />
        <path
          d="M0 698C220 658 380 698 580 678C800 656 980 708 1180 686C1300 673 1380 698 1440 688"
          stroke="var(--scene-snow)"
          strokeOpacity="0.42"
          strokeWidth="2"
        />

        {/* A windmill on the left hill keeps the horizon quietly moving. */}
        <g
          transform="translate(552 694) scale(1.15)"
          opacity="0.55"
          style={{ color: 'var(--ink)' }}
        >
          <path d="M-9 0h18l-5-50h-8Z" fill="currentColor" />
          <rect x="-4" y="-34" width="8" height="9" rx="1" fill="var(--scene-snow)" opacity="0.7" />
          <path d="M-3 0v-11h6V0Z" fill="var(--scene-snow)" opacity="0.35" />
          <g transform="translate(0 -52)">
            <g className="windmill-blades">
              <path
                d="M0 0V-34M0 0V34M0 0H34M0 0H-34"
                stroke="currentColor"
                strokeWidth="3.4"
                strokeLinecap="round"
              />
              <circle r="4.5" fill="currentColor" />
            </g>
          </g>
        </g>

        {/* A tiny cabin on the right hill, with a chimney that keeps smoking. */}
        <g
          transform="translate(1012 706) scale(1.4)"
          opacity="0.55"
          style={{ color: 'var(--ink)' }}
        >
          <rect x="10" y="-42" width="5" height="14" fill="currentColor" />
          <path d="M-20 0v-24h40V0Z" fill="currentColor" />
          <path d="M-26-22L0-42L26-22Z" fill="currentColor" />
          <rect x="-4" y="-14" width="9" height="14" rx="1" fill="var(--scene-snow)" opacity="0.65" />
          <rect x="-16" y="-17" width="6" height="7" rx="1" fill="var(--scene-snow)" opacity="0.75" />
          <rect x="9" y="-17" width="6" height="7" rx="1" fill="var(--scene-snow)" opacity="0.75" />
          <g transform="translate(12 -50)">
            <g className="smoke-rise" fill="var(--scene-snow)">
              <circle cx="0" cy="0" r="3" opacity="0.8" />
              <circle cx="3" cy="-7" r="4" opacity="0.6" />
              <circle cx="-1" cy="-14" r="5" opacity="0.42" />
              <circle cx="-5" cy="-22" r="6" opacity="0.25" />
            </g>
          </g>
          <g stroke="currentColor" strokeWidth="1.8" strokeOpacity="0.7">
            <path d="M-34-2v-10M-40-2v-10M-46-2v-10" />
            <path d="M-48-8h16" />
          </g>
        </g>
        <path
          d="M1048 706c10 8 20 14 28 22"
          stroke="var(--scene-snow)"
          strokeOpacity="0.45"
          strokeWidth="3"
          strokeLinecap="round"
        />

        {/* Trees, bushes and stones, sized by depth. */}
        <g opacity="0.6">
          <use href="#hero-tree" transform="translate(84 620) scale(0.42)" />
          <use href="#hero-tree" transform="translate(164 628) scale(0.34)" />
          <use href="#hero-tree" transform="translate(1300 616) scale(0.4)" />
          <use href="#hero-tree" transform="translate(1372 628) scale(0.32)" />
        </g>
        <use href="#hero-tree" transform="translate(334 664) scale(0.72)" opacity="0.85" />
        <use href="#hero-tree" transform="translate(380 670) scale(0.58)" opacity="0.8" />
        <use href="#hero-tree" transform="translate(1068 662) scale(0.7)" opacity="0.85" />
        <use href="#hero-tree" transform="translate(1128 672) scale(0.55)" opacity="0.8" />
        <use href="#hero-bush" transform="translate(468 712) scale(0.9)" opacity="0.8" />
        <use href="#hero-bush" transform="translate(1020 716) scale(0.8)" opacity="0.75" />
        <use href="#hero-bush" transform="translate(1236 690) scale(0.7)" opacity="0.7" />
        <use href="#hero-tree" transform="translate(118 760) scale(1.42)" />
        <use href="#hero-tree" transform="translate(252 744) scale(0.9)" />
        <use href="#hero-tree" transform="translate(1336 760) scale(1.5)" />
        <use href="#hero-tree" transform="translate(1228 748) scale(0.82)" />

        <g fill="var(--scene-tree)" opacity="0.35">
          <ellipse cx="414" cy="744" rx="44" ry="14" />
          <ellipse cx="446" cy="740" rx="22" ry="9" />
          <ellipse cx="800" cy="748" rx="50" ry="15" />
          <ellipse cx="762" cy="744" rx="22" ry="9" />
        </g>

        <g fill="var(--scene-snow)" opacity="0.8">
          <circle cx="188" cy="722" r="2.4" />
          <circle cx="216" cy="730" r="1.8" />
          <circle cx="300" cy="736" r="2.2" />
          <circle cx="352" cy="726" r="1.6" />
          <circle cx="916" cy="736" r="2" />
          <circle cx="984" cy="728" r="1.7" />
          <circle cx="1092" cy="742" r="2.3" />
          <circle cx="1280" cy="724" r="1.8" />
        </g>

        <g
          className="bird-fly"
          style={{ animationDuration: '18s' }}
          stroke="var(--ink)"
          strokeOpacity="0.2"
          strokeWidth="2"
          strokeLinecap="round"
        >
          <path d="M240 186c5-5 10-5 15 0 5-5 10-5 15 0" />
          <path d="M300 158c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M356 182c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M412 152c3-3 6-3 9 0 3-3 6-3 9 0" />
        </g>
        <g
          className="bird-fly"
          style={{ animationDuration: '24s', animationDelay: '-7s' }}
          stroke="var(--ink)"
          strokeOpacity="0.26"
          strokeWidth="2"
          strokeLinecap="round"
        >
          <path d="M1000 214c6-6 12-6 18 0 6-6 12-6 18 0" />
          <path d="M1080 182c5-5 10-5 15 0 5-5 10-5 15 0" />
          <path d="M930 168c5-5 10-5 15 0 5-5 10-5 15 0" />
          <path d="M1044 148c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M1140 150c4-4 8-4 12 0 4-4 8-4 12 0" />
        </g>
      </svg>
    </div>
  );
}

export function Hero() {
  const reduced = usePrefersReducedMotion();

  return (
    <section className="relative isolate flex min-h-[100svh] flex-col overflow-hidden">
        <HeroScene />

        <div className="relative mx-auto flex w-[min(1180px,94vw)] flex-1 flex-col justify-center pb-28 pt-40 text-center sm:pb-32">
          <div className="mx-auto max-w-5xl">
            <HeroHeadline />

            <motion.p
              initial={reduced ? false : { opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={
                reduced
                  ? { duration: 0 }
                  : { duration: 0.6, delay: 0.45, ease: EASE_SNAP }
              }
              className="mx-auto mt-7 max-w-2xl text-balance text-lead leading-relaxed text-ink-soft"
            >
              Stop Googling project ideas. Browse 260+ real problems for
              learning, resumes and hackathons, from beginner to final-year.
              Build one, link your GitHub repo and live demo, and show your work
              to everyone.
            </motion.p>

            <motion.div
              initial={reduced ? false : { opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={
                reduced
                  ? { duration: 0 }
                  : { duration: 0.6, delay: 0.6, ease: EASE_SNAP }
              }
              className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4"
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
              <Link
                to="/about"
                className="press inline-flex items-center justify-center rounded-full bg-sky px-7 py-4 text-[0.9375rem] font-semibold text-[#0a0b0d] transition-colors hover:bg-sky-strong"
              >
                Learn More
              </Link>
            </motion.div>
          </div>
        </div>
    </section>
  );
}
