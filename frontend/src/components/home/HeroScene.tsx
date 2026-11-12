import { useEffect, useRef } from 'react';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

const STARS = [
  { left: '7%', top: '10%', size: 2, delay: '0s' },
  { left: '13%', top: '22%', size: 1.5, delay: '-1.4s' },
  { left: '21%', top: '8%', size: 2.5, delay: '-2.8s' },
  { left: '29%', top: '18%', size: 1.5, delay: '-0.7s' },
  { left: '38%', top: '6%', size: 2, delay: '-3.6s' },
  { left: '47%', top: '15%', size: 1.5, delay: '-2.1s' },
  { left: '56%', top: '7%', size: 2.5, delay: '-4.4s' },
  { left: '64%', top: '20%', size: 1.5, delay: '-1.8s' },
  { left: '73%', top: '10%', size: 2, delay: '-3.1s' },
  { left: '81%', top: '24%', size: 1.5, delay: '-0.4s' },
  { left: '89%', top: '12%', size: 2.5, delay: '-5.2s' },
  { left: '95%', top: '28%', size: 2, delay: '-2.5s' },
  { left: '34%', top: '30%', size: 1.5, delay: '-4.8s' },
  { left: '68%', top: '33%', size: 2, delay: '-1.2s' },
  { left: '17%', top: '36%', size: 1.5, delay: '-3.9s' },
  { left: '86%', top: '38%', size: 1.5, delay: '-0.9s' },
  { left: '53%', top: '27%', size: 2, delay: '-2.3s' },
  { left: '42%', top: '40%', size: 1.5, delay: '-5.5s' },
];

type TreeProps = {
  href: string;
  x: number;
  y: number;
  scale?: number;
  opacity?: number;
  duration?: number;
  delay?: number;
};

function Tree({
  href,
  x,
  y,
  scale = 1,
  opacity = 1,
  duration = 8,
  delay = 0,
}: TreeProps) {
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity}>
      <g
        className="tree-sway"
        style={{ animationDuration: `${duration}s`, animationDelay: `${delay}s` }}
      >
        <use href={href} />
      </g>
    </g>
  );
}

type TuftProps = {
  x: number;
  y: number;
  scale?: number;
  opacity?: number;
  color?: string;
  duration?: number;
  delay?: number;
};

function Tuft({
  x,
  y,
  scale = 1,
  opacity = 1,
  color = 'var(--scene-grass-shadow)',
  duration = 5,
  delay = 0,
}: TuftProps) {
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity}>
      <g
        className="grass-sway"
        style={{ animationDuration: `${duration}s`, animationDelay: `${delay}s` }}
      >
        <use href="#grass-tuft" style={{ color }} />
      </g>
    </g>
  );
}

const POLLEN = [
  { left: '7%', top: '57%', size: 3, duration: 17, delay: -2 },
  { left: '13%', top: '72%', size: 2, duration: 21, delay: -9 },
  { left: '22%', top: '63%', size: 2.5, duration: 19, delay: -5 },
  { left: '31%', top: '79%', size: 2, duration: 23, delay: -13 },
  { left: '63%', top: '68%', size: 2.5, duration: 20, delay: -7 },
  { left: '71%', top: '81%', size: 2, duration: 24, delay: -16 },
  { left: '82%', top: '61%', size: 3, duration: 18, delay: -4 },
  { left: '89%', top: '76%', size: 2, duration: 22, delay: -11 },
  { left: '94%', top: '66%', size: 2.5, duration: 20, delay: -15 },
];

function Pollen() {
  return (
    <div className="absolute inset-0 hidden sm:block">
      {POLLEN.map((p, index) => (
        <span
          key={index}
          className="pollen absolute rounded-full"
          style={{
            left: p.left,
            top: p.top,
            width: p.size,
            height: p.size,
            animationDuration: `${p.duration}s`,
            animationDelay: `${p.delay}s`,
          }}
        />
      ))}
    </div>
  );
}

function Cloud({
  className,
  duration,
  delay,
}: {
  className: string;
  duration: number;
  delay?: number;
}) {
  return (
    <div
      className={className}
      style={{
        animationDuration: `${duration}s`,
        animationDelay: delay ? `${delay}s` : undefined,
      }}
    >
      <svg className="hero-cloud" viewBox="0 0 220 72" fill="none" aria-hidden>
        <path
          d="M20 58c-12 0-18-7-15-16 2-8 10-12 18-11 3-13 14-21 27-20 10 1 18 6 22 15 5-5 12-7 19-5 10 2 16 10 15 19 9 0 16 6 17 14 1 9-6 15-17 15H20Z"
          fill="var(--scene-cloud)"
          opacity="0.9"
        />
        <path
          d="M34 50c9-3 19-2 27 2M78 34c5-4 11-5 17-3"
          stroke="var(--scene-cloud-light)"
          strokeWidth="2"
          strokeLinecap="round"
          opacity="0.55"
        />
      </svg>
    </div>
  );
}

export function HeroScene() {
  const ref = useRef<HTMLDivElement>(null);
  const reduced = usePrefersReducedMotion();

  useEffect(() => {
    const node = ref.current;
    if (!node || reduced) return;

    let frame = 0;
    let mouseX = 0;
    let mouseY = 0;
    let scroll = 0;

    const apply = () => {
      frame = 0;
      node.style.setProperty('--mx', mouseX.toFixed(3));
      node.style.setProperty('--my', mouseY.toFixed(3));
      node.style.setProperty('--scroll', scroll.toFixed(3));
    };

    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(apply);
    };

    const onPointerMove = (event: PointerEvent) => {
      mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
      mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
      schedule();
    };

    const onScroll = () => {
      const rect = node.getBoundingClientRect();
      scroll = Math.min(Math.max(-rect.top / window.innerHeight, 0), 1);
      schedule();
    };

    window.addEventListener('pointermove', onPointerMove, { passive: true });
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('scroll', onScroll);
    };
  }, [reduced]);

  return (
    <div
      ref={ref}
      aria-hidden
      className="hero-scene pointer-events-none absolute inset-0 -z-10 overflow-hidden"
    >
      <div className="hero-sky absolute inset-0" />

      <div className="absolute left-[13%] top-[6%] size-52 rounded-full bg-[#fffdf8]/80 blur-3xl dark:bg-[#a9c4ff]/10" />
      <div className="absolute left-[15%] top-[8%] hidden size-16 rounded-full dark:block dark:bg-[#eef4ff] dark:shadow-[0_0_50px_16px_rgba(180,205,255,0.24)]" />
      <div className="absolute right-[7%] top-[24%] size-64 rounded-full bg-[#e9e5dc]/35 blur-3xl dark:bg-[#3f4f76]/12" />

      <div className="absolute inset-0 hidden dark:block">
        {STARS.map((star, index) => (
          <span
            key={index}
            className="twinkle absolute rounded-full bg-[#eaf2ff]"
            style={{
              left: star.left,
              top: star.top,
              width: star.size,
              height: star.size,
              animationDelay: star.delay,
              boxShadow: '0 0 6px rgba(190, 215, 255, 0.55)',
            }}
          />
        ))}
      </div>

      <Cloud
        className="cloud-drift absolute left-[7%] top-[20%] w-52 opacity-95 dark:opacity-55"
        duration={38}
      />

      <svg
        className="bird-drift absolute right-[29%] top-[19%] w-40 text-ink/45 dark:text-paper/40"
        viewBox="0 0 180 80"
        fill="none"
        aria-hidden
        style={{ animationDuration: '39s' }}
      >
        <g stroke="currentColor" strokeWidth="1.6" strokeLinecap="round">
          <path d="M8 34c5-5 10-5 15 0 5-5 10-5 15 0" />
          <path d="M48 18c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M82 46c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M116 24c3-3 6-3 9 0 3-3 6-3 9 0" />
          <path d="M142 54c3-3 6-3 9 0 3-3 6-3 9 0" />
        </g>
      </svg>
      <svg
        className="bird-drift absolute left-[17%] top-[24%] w-24 text-ink/30 dark:text-paper/25"
        viewBox="0 0 120 44"
        fill="none"
        aria-hidden
        style={{ animationDuration: '47s', animationDelay: '-18s' }}
      >
        <g stroke="currentColor" strokeWidth="1.4" strokeLinecap="round">
          <path d="M6 24c4-4 8-4 12 0 4-4 8-4 12 0" />
          <path d="M38 12c3-3 6-3 9 0 3-3 6-3 9 0" />
          <path d="M70 30c3-3 6-3 9 0 3-3 6-3 9 0" />
        </g>
      </svg>

      <div
        className="hero-balloon balloon-drift absolute right-[17%] top-[27%] hidden w-20 opacity-80 dark:opacity-65 sm:block"
        style={{ animationDuration: '32s' }}
      >
        <svg viewBox="0 0 72 96" fill="none" aria-hidden>
          <defs>
            <linearGradient
              id="hero-balloon-body"
              x1="14"
              y1="6"
              x2="58"
              y2="68"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset="0" stopColor="var(--sky)" />
              <stop offset="0.58" stopColor="var(--sky)" />
              <stop offset="1" stopColor="var(--sky-strong)" />
            </linearGradient>
            <linearGradient
              id="hero-balloon-sheen"
              x1="24"
              y1="10"
              x2="34"
              y2="62"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset="0" stopColor="var(--paper)" stopOpacity="0.7" />
              <stop offset="1" stopColor="var(--paper)" stopOpacity="0" />
            </linearGradient>
          </defs>

          <path
            d="M36 3C52 3 64 15 64 32C64 49 49 63 40 73H32C23 63 8 49 8 32C8 15 20 3 36 3Z"
            fill="url(#hero-balloon-body)"
          />

          <path
            d="M36 3C27 3 19 9 15 19C19 16 23 14 27 13C30 12 33 10 36 8Z"
            fill="var(--sky-strong)"
            opacity="0.2"
          />
          <path
            d="M36 3C45 3 53 9 57 19C53 16 49 14 45 13C42 12 39 10 36 8Z"
            fill="var(--sky-strong)"
            opacity="0.35"
          />

          <path
            d="M27 5C23 12 20 21 20 32C20 44 25 56 32 67"
            stroke="var(--sky-strong)"
            strokeWidth="0.8"
            strokeLinecap="round"
            opacity="0.32"
          />
          <path
            d="M45 5C49 12 52 21 52 32C52 44 47 56 40 67"
            stroke="var(--sky-strong)"
            strokeWidth="0.8"
            strokeLinecap="round"
            opacity="0.32"
          />

          <path
            d="M30 8C27 15 25 23 25 32C25 42 28 52 33 61C29 51 27 42 27 32C27 23 28 15 30 8Z"
            fill="url(#hero-balloon-sheen)"
          />
          <ellipse
            cx="25.5"
            cy="18"
            rx="4"
            ry="8"
            transform="rotate(-30 25.5 18)"
            fill="var(--paper)"
            opacity="0.45"
          />

          <path d="M34 71h4l3 9h-10Z" fill="var(--sky-strong)" />
          <path
            d="M31 72 29 81M41 72l2 9"
            stroke="var(--sky-strong)"
            strokeWidth="0.8"
            strokeLinecap="round"
            opacity="0.7"
          />
          <rect x="27" y="79.4" width="18" height="2.8" rx="1.4" fill="var(--sky-strong)" />
          <path
            d="M29 82h14l-1.3 10.4a2 2 0 0 1-2 1.6H32.3a2 2 0 0 1-2-1.6L29 82Z"
            fill="var(--sky-strong)"
          />
          <path
            d="M31 85h10M31.6 88h8.8M32.2 91h7.6"
            stroke="var(--paper)"
            strokeWidth="0.7"
            strokeLinecap="round"
            opacity="0.45"
          />
        </svg>
      </div>

      <Pollen />

      <svg
        className="hero-sketch absolute inset-x-0 bottom-0 h-[78%] w-full"
        viewBox="0 0 1680 720"
        preserveAspectRatio="none"
        fill="none"
        aria-hidden
      >
        <defs>
          <linearGradient id="mountain-far" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="var(--sketch-highlight)" />
            <stop offset="0.55" stopColor="var(--sketch-wash)" />
            <stop offset="1" stopColor="var(--sketch-shade)" />
          </linearGradient>
          <linearGradient id="mountain-mid" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="var(--sketch-wash)" />
            <stop offset="0.52" stopColor="var(--sketch-shade)" />
            <stop offset="1" stopColor="var(--sketch-deep)" />
          </linearGradient>
          <linearGradient id="meadow-far" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="var(--sketch-wash)" />
            <stop offset="1" stopColor="var(--sketch-shade)" />
          </linearGradient>
          <linearGradient id="meadow-mid" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="var(--sketch-shade)" />
            <stop offset="1" stopColor="var(--sketch-deep)" />
          </linearGradient>
          <linearGradient id="meadow-near" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="var(--sketch-deep)" />
            <stop offset="1" stopColor="var(--scene-front)" />
          </linearGradient>
          <linearGradient id="river" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="var(--sketch-highlight)" />
            <stop offset="0.42" stopColor="var(--sketch-wash)" />
            <stop offset="1" stopColor="var(--sketch-shade)" />
          </linearGradient>
          <filter id="hero-blur" x="-20%" y="-60%" width="140%" height="220%">
            <feGaussianBlur stdDeviation="18" />
          </filter>
          <filter id="hero-soft" x="-20%" y="-40%" width="140%" height="180%">
            <feGaussianBlur stdDeviation="5" />
          </filter>
          <filter id="hero-glow" x="-80%" y="-80%" width="260%" height="260%">
            <feGaussianBlur stdDeviation="8" />
          </filter>

          <pattern
            id="sketch-hatch-soft"
            width="9"
            height="9"
            patternUnits="userSpaceOnUse"
            patternTransform="rotate(-16)"
          >
            <path
              d="M-2 9L9-2M5 11L11 5"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.7"
              strokeOpacity="0.42"
              strokeLinecap="round"
            />
          </pattern>
          <pattern
            id="sketch-hatch"
            width="5.5"
            height="5.5"
            patternUnits="userSpaceOnUse"
            patternTransform="rotate(-14)"
          >
            <path
              d="M-1 5.5L5.5-1M4 7L7 4"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.62"
              strokeOpacity="0.6"
              strokeLinecap="round"
            />
          </pattern>
          <pattern
            id="sketch-hatch-dense"
            width="3.4"
            height="3.4"
            patternUnits="userSpaceOnUse"
            patternTransform="rotate(-12)"
          >
            <path
              d="M-1 3.4L3.4-1M2.6 4.2L4.2 2.6"
              stroke="var(--sketch-ink)"
              strokeWidth="0.52"
              strokeOpacity="0.5"
              strokeLinecap="round"
            />
          </pattern>
          <pattern
            id="sketch-cross"
            width="7"
            height="7"
            patternUnits="userSpaceOnUse"
            patternTransform="rotate(-8)"
          >
            <path
              d="M-1 7L7-1M-1 0L7 8"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.55"
              strokeOpacity="0.45"
              strokeLinecap="round"
            />
          </pattern>

          <g id="tree-round">
            <rect x="-3.2" y="-50" width="6.4" height="50" rx="3.2" fill="var(--scene-trunk)" />
            <path
              d="M-1-50l-8-14M1-50l8-14"
              stroke="var(--scene-trunk)"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
            <path
              d="M-1.4-44v7M1.4-34v6M0-25v5"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.9"
              strokeOpacity="0.5"
              strokeLinecap="round"
            />
            <circle cx="-18" cy="-56" r="20" fill="var(--scene-tree-deep)" />
            <circle cx="18" cy="-54" r="21" fill="var(--scene-tree-deep)" />
            <circle cx="0" cy="-70" r="25" fill="var(--scene-tree)" />
            <circle cx="-22" cy="-62" r="17" fill="var(--scene-tree)" />
            <circle cx="20" cy="-64" r="18" fill="var(--scene-tree)" />
            <circle cx="-8" cy="-78" r="16" fill="var(--scene-tree-alt)" opacity="0.85" />
            <circle cx="12" cy="-72" r="12" fill="var(--scene-tree-alt)" opacity="0.7" />
            <circle cx="-24" cy="-60" r="8" fill="var(--scene-tree-alt)" opacity="0.35" />
            <circle cx="14" cy="-62" r="15" fill="url(#sketch-hatch)" opacity="0.5" stroke="none" />
            <circle cx="-18" cy="-58" r="12" fill="url(#sketch-hatch-soft)" opacity="0.4" stroke="none" />
            <path
              d="M-26-50C-18-42-10-39-2-41M2-58C10-50 17-46 22-38M-14-72c5-4 11-4 16 0"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.9"
              strokeOpacity="0.45"
              strokeLinecap="round"
              fill="none"
            />
            <circle cx="-4" cy="-81" r="5" fill="var(--scene-grass-light)" opacity="0.55" />
          </g>

          <g id="tree-birch">
            <path d="M-3 0L-1-62H3L4 0Z" fill="var(--scene-birch)" />
            <path
              d="M-2-12h4M-2-25h4M-1-38h4M-1-50h3"
              stroke="var(--scene-birch-mark)"
              strokeWidth="1.6"
              opacity="0.55"
            />
            <path
              d="M0-60l-8-12M0-60l9-10"
              stroke="var(--scene-birch)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <circle cx="-12" cy="-70" r="16" fill="var(--scene-tree-deep)" />
            <circle cx="12" cy="-72" r="17" fill="var(--scene-tree-deep)" />
            <circle cx="0" cy="-84" r="20" fill="var(--scene-tree)" />
            <circle cx="-4" cy="-92" r="13" fill="var(--scene-tree-alt)" opacity="0.85" />
            <circle cx="10" cy="-82" r="10" fill="var(--scene-tree-alt)" opacity="0.55" />
            <circle cx="12" cy="-74" r="13" fill="url(#sketch-hatch)" opacity="0.45" stroke="none" />
            <path
              d="M-18-78c6-4 13-4 19 1M-10-64c7-3 14-2 19 2"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.9"
              strokeOpacity="0.4"
              strokeLinecap="round"
              fill="none"
            />
          </g>

          <g id="tree-pine">
            <rect x="-2.4" y="-34" width="4.8" height="34" rx="2.4" fill="var(--scene-trunk)" />
            <path d="M0-100L22-62H-22Z" fill="var(--scene-tree-deep)" />
            <path d="M0-86L26-48H-26Z" fill="var(--scene-tree)" />
            <path d="M0-72L30-34H-30Z" fill="var(--scene-tree)" />
            <path d="M0-92L12-72H-12Z" fill="var(--scene-tree-alt)" opacity="0.55" />
            <path d="M0-78L16-58H-16Z" fill="var(--scene-tree-alt)" opacity="0.45" />
            <path d="M0-64L18-44H-18Z" fill="var(--scene-tree-alt)" opacity="0.3" />
            <path d="M0-100L22-62H0Z" fill="url(#sketch-hatch)" opacity="0.5" stroke="none" />
            <path d="M0-86L26-48H0Z" fill="url(#sketch-hatch)" opacity="0.45" stroke="none" />
            <path d="M0-72L30-34H0Z" fill="url(#sketch-hatch-soft)" opacity="0.5" stroke="none" />
          </g>

          <g id="tree-cypress">
            <rect x="-2" y="-26" width="4" height="26" rx="2" fill="var(--scene-trunk)" />
            <path d="M0-96C12-74 16-50 10-26H-10C-16-50-12-74 0-96Z" fill="var(--scene-tree-deep)" />
            <path d="M0-88C7-70 9-50 5-30H-5C-9-50-7-70 0-88Z" fill="var(--scene-tree)" />
            <path
              d="M-2-76C2-62 3-48 1-34"
              stroke="var(--scene-tree-alt)"
              strokeWidth="2.5"
              strokeLinecap="round"
              opacity="0.5"
            />
            <path d="M0-88C7-70 9-50 5-30H0Z" fill="url(#sketch-hatch)" opacity="0.5" stroke="none" />
          </g>

          <g id="bush">
            <circle cx="-18" cy="-10" r="16" fill="var(--scene-tree-deep)" />
            <circle cx="0" cy="-20" r="22" fill="var(--scene-tree)" />
            <circle cx="20" cy="-9" r="15" fill="var(--scene-tree-deep)" />
            <circle cx="-6" cy="-26" r="12" fill="var(--scene-tree-alt)" opacity="0.7" />
            <circle cx="12" cy="-18" r="9" fill="var(--scene-tree-alt)" opacity="0.45" />
            <circle cx="10" cy="-16" r="13" fill="url(#sketch-hatch)" opacity="0.45" stroke="none" />
          </g>

          <g id="grass-tuft">
            <path
              d="M0 0C-4-12-10-18-16-22M0 0C-2-14-4-24-8-32M0 0C0-14 0-26 0-34M0 0C2-14 5-24 9-30M0 0C4-12 10-18 16-22M0 0C-6-8-12-10-18-12M0 0C6-8 12-10 18-12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </g>

          <g id="flower">
            <circle cx="0" cy="-3" r="1.5" fill="var(--scene-bloom)" />
            <circle cx="-3" cy="0" r="1.4" fill="var(--scene-bloom)" />
            <circle cx="3" cy="0" r="1.4" fill="var(--scene-bloom)" />
            <circle cx="-1.7" cy="2.6" r="1.3" fill="var(--scene-blossom)" />
            <circle cx="1.7" cy="2.6" r="1.3" fill="var(--scene-blossom)" />
            <circle cx="0" cy="0" r="1.1" fill="var(--scene-snow)" />
          </g>
        </defs>

        <g className="hero-parallax hero-parallax--far">
          <path
            d="M0 432C52 418 92 390 128 380C158 342 190 326 222 354C250 378 274 402 306 410C344 420 378 410 412 398C454 384 488 366 528 376C568 386 604 410 650 418C700 426 740 416 780 400C820 384 858 382 898 396C940 410 978 424 1022 418C1064 412 1098 396 1136 396C1176 396 1210 412 1246 424C1284 436 1324 430 1362 410C1400 390 1436 380 1474 392C1516 406 1550 422 1590 422C1628 422 1656 414 1680 404V720H0V432Z"
            fill="url(#mountain-far)"
            stroke="var(--sketch-ink-soft)"
            strokeWidth="1.6"
            strokeOpacity="0.55"
          />
          <g fill="var(--sketch-highlight)" opacity="0.42">
            <path d="M222 354C198 368 176 390 150 400C184 410 214 408 246 398C236 382 228 368 222 354Z" />
            <path d="M1136 396C1110 402 1086 408 1064 412C1088 418 1112 416 1140 410C1138 404 1136 400 1136 396Z" />
            <path d="M1474 392C1450 400 1428 404 1408 406C1430 414 1454 416 1482 410C1478 404 1476 398 1474 392Z" />
          </g>
          <g fill="url(#sketch-hatch-soft)" opacity="0.9">
            <path d="M222 354C234 372 246 390 262 404C238 412 218 408 200 400C210 386 218 370 222 354Z" />
            <path d="M1246 424C1260 430 1274 430 1288 426C1276 420 1264 414 1254 408Z" />
            <path d="M1362 410C1376 416 1390 416 1404 410C1394 404 1384 398 1376 392Z" />
          </g>
          <g fill="var(--sketch-highlight)" opacity="0.55">
            <path d="M216 350C222 356 228 362 232 370C224 368 218 360 212 354Z" />
            <path d="M1468 388C1474 394 1480 400 1484 408C1476 406 1470 398 1464 392Z" />
          </g>
          <g
            stroke="var(--sketch-ink-faint)"
            strokeOpacity="0.55"
            strokeWidth="1.6"
            strokeLinecap="round"
          >
            <path d="M222 354C198 368 176 390 150 400M1362 410C1378 400 1394 390 1410 386" />
          </g>
          <g
            stroke="var(--sketch-ink-soft)"
            strokeOpacity="0.35"
            strokeWidth="1.2"
            strokeLinecap="round"
          >
            <path d="M232 368C240 384 248 396 260 406M304 410C322 416 340 420 360 418M1026 418C1040 420 1054 420 1068 416M1136 396C1148 404 1162 410 1178 414" />
            <path d="M56 414C104 394 152 366 196 360M430 402C474 384 508 376 552 382M704 420C748 408 786 398 826 404M934 414C972 406 1008 400 1044 404M1210 424C1248 420 1286 416 1320 420M1518 412C1554 414 1590 414 1622 408" />
          </g>
          <ellipse
            cx="826"
            cy="404"
            rx="660"
            ry="46"
            fill="var(--scene-haze)"
            opacity="0.6"
            filter="url(#hero-blur)"
          />
        </g>

        <g className="hero-parallax hero-parallax--mid">
          <path
            d="M0 482C52 474 92 458 136 440C186 420 242 402 300 400C358 398 408 418 462 432C526 448 588 448 650 440C712 432 764 420 826 422C888 424 944 438 1004 442C1064 446 1122 440 1174 430C1226 420 1272 404 1324 400C1376 396 1428 414 1482 430C1534 446 1592 450 1680 440V720H0V482Z"
            fill="url(#mountain-mid)"
            stroke="var(--sketch-ink)"
            strokeWidth="1.5"
            strokeOpacity="0.6"
          />
          <g fill="var(--sketch-highlight)" opacity="0.3">
            <path d="M136 440C186 420 242 402 300 400C250 412 204 426 164 442C154 446 144 446 136 440Z" />
            <path d="M1174 430C1226 420 1272 404 1324 400C1280 410 1240 422 1204 434C1192 438 1182 438 1174 430Z" />
          </g>
          <g fill="url(#sketch-hatch)" opacity="0.9">
            <path d="M300 400C358 398 408 418 462 432C406 434 354 424 314 412C306 408 302 404 300 400Z" />
            <path d="M1324 400C1376 396 1428 414 1482 430C1430 432 1382 424 1342 412C1334 408 1328 404 1324 400Z" />
          </g>
          <g
            stroke="var(--sketch-ink-faint)"
            strokeOpacity="0.55"
            strokeWidth="1.5"
            strokeLinecap="round"
          >
            <path d="M136 440C186 420 242 402 300 400M1174 430C1226 420 1272 404 1324 400" />
          </g>
          <g
            stroke="var(--sketch-ink-soft)"
            strokeOpacity="0.38"
            strokeWidth="1.2"
            strokeLinecap="round"
          >
            <path d="M182 424C236 412 286 412 328 422M1204 426C1258 416 1306 414 1352 420" />
            <path d="M360 408C410 408 452 418 492 430M616 442C656 436 696 426 732 420M862 426C906 430 948 438 988 440M1100 438C1140 436 1180 430 1216 424M1390 406C1436 416 1480 428 1524 434" />
          </g>
        </g>

        <g
          className="hero-parallax hero-parallax--mid"
          stroke="var(--sketch-ink-faint)"
          strokeOpacity="0.28"
          strokeWidth="1.1"
          strokeLinecap="round"
          opacity="0.8"
        >
          <path d="M140 446C220 438 302 442 384 448M462 452C536 446 612 448 688 454M760 444C836 438 912 440 988 446M1060 458C1138 450 1218 452 1298 458M1370 446C1444 440 1520 442 1596 448" />
          <path d="M250 462C322 456 396 458 470 462M700 466C772 460 846 462 918 466M1150 468C1222 462 1296 464 1368 468" />
        </g>

        <g className="hero-parallax hero-parallax--mid">
          <path
            d="M0 506C220 456 380 522 580 494C780 466 932 526 1120 490C1320 452 1500 506 1680 472V720H0V506Z"
            fill="url(#meadow-far)"
            stroke="none"
          />
          <path
            d="M0 566C200 508 420 572 620 542C820 512 1000 582 1200 546C1400 512 1540 560 1680 536V720H0V566Z"
            fill="url(#meadow-mid)"
            stroke="none"
          />
        </g>

        <g className="hero-parallax hero-parallax--near">
          <path
            d="M0 620C220 574 400 638 620 606C840 574 1040 650 1260 612C1440 582 1580 630 1680 602V720H0V620Z"
            fill="url(#meadow-near)"
            stroke="none"
          />
          <path
            d="M0 672C220 640 420 690 640 666C860 642 1060 700 1280 672C1460 650 1600 690 1680 668V720H0V672Z"
            fill="var(--scene-front)"
            stroke="none"
          />
          <path
            d="M312 626C406 654 486 682 560 720"
            stroke="var(--scene-path)"
            strokeOpacity="0.28"
            strokeWidth="26"
            strokeLinecap="round"
          />
          <path
            d="M312 626C406 654 486 682 560 720"
            stroke="var(--scene-grass-light)"
            strokeOpacity="0.16"
            strokeWidth="9"
            strokeLinecap="round"
          />
          <path
            d="M1370 636C1296 664 1226 690 1160 720"
            stroke="var(--scene-path)"
            strokeOpacity="0.3"
            strokeWidth="24"
            strokeLinecap="round"
          />
          <path
            d="M1370 636C1296 664 1226 690 1160 720"
            stroke="var(--scene-grass-light)"
            strokeOpacity="0.18"
            strokeWidth="8"
            strokeLinecap="round"
          />
        </g>

        <g className="hero-parallax hero-parallax--near">
          <Tree href="#tree-round" x={92} y={596} scale={0.58} opacity={0.62} duration={9} delay={-2} />
          <Tree href="#tree-cypress" x={1520} y={592} scale={0.6} opacity={0.6} duration={9.5} delay={-4} />
        </g>

        <g className="hero-parallax hero-parallax--near">
          <path
            d="M824 410C902 470 716 522 820 582C930 648 704 680 788 742L1018 742C926 680 1084 642 982 582C878 522 1012 472 920 410Z"
            stroke="var(--scene-grass-shadow)"
            strokeWidth="22"
            strokeOpacity="0.22"
            fill="none"
            filter="url(#hero-soft)"
          />
          <path
            d="M824 410C902 470 716 522 820 582C930 648 704 680 788 742L1018 742C926 680 1084 642 982 582C878 522 1012 472 920 410Z"
            fill="url(#river)"
            stroke="var(--sketch-ink-soft)"
            strokeWidth="1.5"
            strokeOpacity="0.65"
          />
          <g
            stroke="var(--sketch-ink-faint)"
            strokeOpacity="0.38"
            strokeWidth="1.1"
            strokeLinecap="round"
            fill="none"
          >
            <path d="M832 424C844 470 730 516 818 574C846 592 850 610 840 628" />
            <path d="M946 430C938 474 1024 520 944 568C916 588 912 608 924 626" />
            <path d="M830 470C842 500 790 520 822 548C854 576 854 600 844 620" />
            <path d="M946 504C936 532 978 552 950 580C922 608 926 630 938 650" />
            <path d="M806 650C830 672 798 696 812 720" />
          </g>
          <g stroke="var(--scene-foam)" strokeLinecap="round">
            <path
              d="M850 462C878 496 806 522 850 556"
              strokeWidth="2.4"
              strokeOpacity="0.7"
              className="river-flow"
            />
            <path
              d="M876 548C916 584 844 612 886 646"
              strokeWidth="2.8"
              strokeOpacity="0.62"
              className="river-flow"
              style={{ animationDelay: '-2.5s', animationDuration: '7.5s' }}
            />
            <path
              d="M840 636C866 664 824 684 850 712"
              strokeWidth="3"
              strokeOpacity="0.55"
              className="river-flow"
              style={{ animationDelay: '-4s', animationDuration: '8.5s' }}
            />
            <path
              d="M934 500C958 526 912 548 942 576"
              strokeWidth="1.8"
              strokeOpacity="0.45"
              className="river-flow"
              style={{ animationDelay: '-1.2s', animationDuration: '9s' }}
            />
            <path
              d="M950 604C972 626 936 648 958 672"
              strokeWidth="2"
              strokeOpacity="0.42"
              className="river-flow"
              style={{ animationDelay: '-3.2s', animationDuration: '10s' }}
            />
          </g>
          <g fill="var(--scene-sky-tint)" opacity="0.32">
            <ellipse cx="860" cy="470" rx="22" ry="3.5" />
            <ellipse cx="900" cy="538" rx="30" ry="4" />
            <ellipse cx="842" cy="612" rx="36" ry="5" />
            <ellipse cx="892" cy="690" rx="44" ry="6" />
          </g>
          <g fill="var(--scene-stone)">
            <ellipse cx="842" cy="660" rx="14" ry="5" />
            <ellipse cx="902" cy="682" rx="17" ry="6" />
            <ellipse cx="966" cy="704" rx="20" ry="7" />
          </g>
          <g fill="var(--scene-stone-light)" opacity="0.65">
            <ellipse cx="838" cy="658" rx="8" ry="2.4" />
            <ellipse cx="897" cy="680" rx="10" ry="2.8" />
            <ellipse cx="960" cy="702" rx="12" ry="3.2" />
          </g>
          <g stroke="var(--scene-water-deep)" strokeOpacity="0.4" strokeWidth="1.5">
            <path d="M830 654c8-3 16-3 24 0M890 676c9-3 18-3 27 0M952 698c10-3 20-3 30 0" />
          </g>
        </g>

        <g className="hero-parallax hero-parallax--near">
          <Tree href="#tree-round" x={452} y={652} scale={0.98} opacity={0.95} duration={8} delay={-3} />
          <Tree href="#tree-round" x={1200} y={642} scale={0.86} opacity={0.9} duration={8.5} delay={-4} />
        </g>

        <g className="hero-parallax hero-parallax--near">
          <ellipse cx="344" cy="660" rx="88" ry="15" fill="var(--scene-grass-shadow)" opacity="0.18" />
          <g transform="translate(300 656) scale(1.36)">
            <path d="M48 4c54-2 86 2 114 12-38 4-78 3-114-12Z" fill="var(--scene-grass-shadow)" opacity="0.28" />
            <path d="M-18 0h36l-4-10h-28Z" fill="var(--scene-stone)" />
            <path d="M-14-10h28l-3-8h-22Z" fill="var(--scene-stone-light)" opacity="0.5" />
            <path d="M-12-18h24l-4-46h-16Z" fill="var(--scene-wood)" />
            <path d="M-12-18l4-46h6l-2 46Z" fill="var(--scene-wood-light)" opacity="0.55" />
            <path d="M4-64h8l-2 46h-6Z" fill="var(--scene-wood-dark)" opacity="0.5" />
            <g stroke="var(--scene-wood-dark)" strokeOpacity="0.35" strokeWidth="0.8">
              <path d="M-10-24h20M-9-32h19M-8-40h18M-7-48h17M-6-56h16" />
            </g>
            <path d="M-4-18v-13h8v13Z" fill="var(--scene-wood-dark)" />
            <path d="M-4-29h8" stroke="var(--scene-wood-light)" strokeWidth="1.2" />
            <rect x="-4" y="-46" width="8" height="8" rx="1" fill="var(--scene-window)" opacity="0.9" />
            <path d="M0-46v8M-4-42h8" stroke="var(--scene-wood-dark)" strokeWidth="0.8" />
            <path d="M-18-64h36" stroke="var(--scene-wood-dark)" strokeWidth="2.5" strokeLinecap="round" />
            <path
              d="M-16-64v-6M-10-64v-6M-4-64v-6M4-64v-6M10-64v-6M16-64v-6"
              stroke="var(--scene-wood-dark)"
              strokeWidth="1"
            />
            <path d="M-16-64h32l-6-12h-20Z" fill="var(--scene-roof)" />
            <path d="M-13-64h26l-3-7h-20Z" fill="var(--scene-roof-light)" opacity="0.5" />
            <path d="M0-76v-5" stroke="var(--scene-wood-dark)" strokeWidth="1.5" strokeLinecap="round" />
            <circle cx="0" cy="-83" r="2.5" fill="var(--scene-wood-dark)" />
            <g
              transform="translate(15 -26)"
              stroke="var(--scene-wood-dark)"
              strokeWidth="1.1"
              fill="none"
              opacity="0.7"
            >
              <circle r="4.5" />
              <circle r="2.5" />
            </g>
            <g transform="translate(0 -70)">
              <g className="windmill-blades">
                {[0, 90, 180, 270].map((rotation) => (
                  <g key={rotation} transform={`rotate(${rotation})`}>
                    <rect
                      x="-2.2"
                      y="-58"
                      width="4.4"
                      height="54"
                      rx="2.2"
                      fill="var(--scene-wood-dark)"
                    />
                    <rect
                      x="-10"
                      y="-52"
                      width="20"
                      height="32"
                      rx="1.5"
                      fill="var(--scene-wood)"
                      opacity="0.95"
                    />
                    <g stroke="var(--scene-wood-light)" strokeWidth="1" opacity="0.6">
                      <path d="M-10-44h20M-10-36h20M-10-28h20" />
                    </g>
                    <path d="M0-52v32" stroke="var(--scene-wood-dark)" strokeWidth="1.2" />
                    <path
                      d="M-10-52l20 32M10-52l-20 32"
                      stroke="var(--scene-wood-dark)"
                      strokeWidth="0.7"
                      opacity="0.5"
                    />
                  </g>
                ))}
                <circle r="6" fill="var(--scene-wood-dark)" />
                <circle r="2.5" fill="var(--scene-wood-light)" />
              </g>
            </g>
            <g transform="translate(46 4) scale(1 -0.22) skewX(-28)" opacity="0.13">
              <g className="windmill-shadow-spin">
                {[0, 90, 180, 270].map((rotation) => (
                  <rect
                    key={rotation}
                    x="-2"
                    y="-58"
                    width="4"
                    height="54"
                    fill="var(--scene-wood-dark)"
                    transform={`rotate(${rotation})`}
                  />
                ))}
              </g>
            </g>
          </g>
        </g>

        <g className="hero-parallax hero-parallax--near">
          <ellipse cx="1356" cy="660" rx="100" ry="17" fill="var(--scene-grass-shadow)" opacity="0.2" />
          <g transform="translate(1336 654) scale(1.34)">
            <path d="M-34 2h68l38 12H-50Z" fill="var(--scene-grass-shadow)" opacity="0.24" />
            <g stroke="var(--scene-wood-dark)" strokeWidth="2" strokeLinecap="round" opacity="0.8">
              <path d="M-66 0v-23M-56 0v-23M-46 0v-23M-36 0v-23M-26 0v-23" />
              <path d="M-70-14h48M-66-6h40" strokeWidth="1.4" />
            </g>
            <path d="M-34-2h68v-42h-68Z" fill="var(--scene-stone)" />
            <path d="M-34-44h68v-8h-68Z" fill="var(--scene-wood)" />
            <path d="M-34-2h20v-42h-20Z" fill="var(--scene-stone-light)" opacity="0.35" />
            <path d="M-44-44L0-74L44-44Z" fill="var(--scene-roof)" />
            <path d="M-44-44L0-74V-68L-36-44Z" fill="var(--scene-roof-light)" opacity="0.55" />
            <g stroke="var(--scene-roof-light)" strokeOpacity="0.35" strokeWidth="1">
              <path d="M-36-40h72M-30-34h60M-24-48h48M-18-42h36" />
            </g>
            <path d="M22-68h10v18h-10Z" fill="var(--scene-stone)" />
            <path d="M20-70h14v4H20Z" fill="var(--scene-roof-light)" />
            <ellipse cx="-15" cy="-27" rx="20" ry="16" fill="var(--scene-window-glow)" opacity="0.24" filter="url(#hero-glow)" />
            <ellipse cx="16" cy="-27" rx="18" ry="15" fill="var(--scene-window-glow)" opacity="0.2" filter="url(#hero-glow)" />
            <rect x="-22" y="-34" width="14" height="14" rx="2" fill="var(--scene-window)" />
            <rect x="10" y="-34" width="12" height="14" rx="2" fill="var(--scene-window)" />
            <path
              d="M-15-34v14M-22-27h14M16-34v14M10-27h12"
              stroke="var(--scene-wood-dark)"
              strokeWidth="1.2"
            />
            <path d="M-5-2v-20h10v20Z" fill="var(--scene-wood-dark)" />
            <circle cx="2" cy="-12" r="1" fill="var(--scene-window)" />
            <g transform="translate(27 -70)">
              <g className="smoke-rise" fill="var(--scene-snow)" opacity="0.55">
                <circle cx="0" cy="0" r="3" />
                <circle cx="3" cy="-7" r="4" opacity="0.7" />
                <circle cx="-1" cy="-14" r="5" opacity="0.45" />
                <circle cx="-5" cy="-22" r="6" opacity="0.24" />
              </g>
              <g
                className="smoke-rise"
                fill="var(--scene-snow)"
                opacity="0.35"
                style={{ animationDelay: '-2.2s' }}
              >
                <circle cx="1" cy="-4" r="2.5" />
                <circle cx="4" cy="-11" r="3.5" opacity="0.7" />
                <circle cx="0" cy="-18" r="4.5" opacity="0.4" />
              </g>
            </g>
            <g transform="translate(-48 -15)">
              <path d="M0-14v10" stroke="var(--scene-wood-dark)" strokeWidth="1.2" />
              <rect x="-3" y="-4" width="6" height="8" rx="1" fill="var(--scene-lantern)" />
              <circle cx="0" cy="0" r="7" fill="var(--scene-lantern)" opacity="0.18" filter="url(#hero-glow)" />
            </g>
            <g stroke="var(--scene-wood-dark)" strokeWidth="2" strokeLinecap="round" opacity="0.75">
              <path d="M-64-2v-23M-54-2v-23M-44-2v-23M-34-2v-23" />
              <path d="M-68-14h38M-64-6h30" strokeWidth="1.4" />
            </g>
          </g>
        </g>

        <g className="hero-parallax hero-parallax--front">
          <Tree href="#tree-pine" x={44} y={742} scale={1.42} opacity={0.92} duration={7} delay={-2} />
          <Tree href="#tree-pine" x={1660} y={742} scale={1.2} opacity={0.9} duration={9} delay={-4} />
        </g>

        <g fill="var(--scene-bloom)" opacity="0.8">
          <circle cx="214" cy="682" r="2.6" />
          <circle cx="556" cy="710" r="2.4" />
          <circle cx="1266" cy="688" r="2.4" />
        </g>
        <g fill="var(--scene-blossom)" opacity="0.76">
          <circle cx="324" cy="692" r="1.7" />
          <circle cx="1196" cy="692" r="2.1" />
        </g>
        <g fill="var(--scene-lavender)" opacity="0.62">
          <circle cx="606" cy="692" r="1.5" />
          <circle cx="1372" cy="720" r="1.8" />
        </g>
        <use href="#flower" transform="translate(342 718) scale(1.1)" />
        <use href="#flower" transform="translate(1452 708) scale(1)" />

        <g style={{ color: 'var(--sketch-ink-soft)' }} opacity="0.42">
          <use href="#grass-tuft" transform="translate(168 664) scale(0.42)" />
          <use href="#grass-tuft" transform="translate(248 682) scale(0.34)" />
          <use href="#grass-tuft" transform="translate(386 676) scale(0.4)" />
          <use href="#grass-tuft" transform="translate(566 696) scale(0.38)" />
          <use href="#grass-tuft" transform="translate(676 684) scale(0.32)" />
          <use href="#grass-tuft" transform="translate(1044 672) scale(0.42)" />
          <use href="#grass-tuft" transform="translate(1148 690) scale(0.34)" />
          <use href="#grass-tuft" transform="translate(1244 660) scale(0.4)" />
          <use href="#grass-tuft" transform="translate(1330 684) scale(0.3)" />
          <use href="#grass-tuft" transform="translate(1484 684) scale(0.4)" />
          <use href="#grass-tuft" transform="translate(1572 668) scale(0.34)" />
          <use href="#grass-tuft" transform="translate(744 706) scale(0.3)" />
          <use href="#grass-tuft" transform="translate(966 704) scale(0.32)" />
        </g>

        <g fill="var(--sketch-ink-faint)" opacity="0.5">
          <circle cx="298" cy="674" r="1.5" />
          <circle cx="520" cy="690" r="1.3" />
          <circle cx="636" cy="674" r="1.4" />
          <circle cx="1114" cy="678" r="1.5" />
          <circle cx="1310" cy="672" r="1.3" />
          <circle cx="1540" cy="700" r="1.4" />
        </g>

        <g className="hero-parallax hero-parallax--front">
          <Tuft x={16} y={720} scale={2.1} opacity={0.85} duration={6} delay={-2} />
          <Tuft x={204} y={720} scale={1.5} opacity={0.7} duration={8} delay={-1} />
          <Tuft x={486} y={720} scale={1.3} opacity={0.65} duration={7.5} delay={-3} />
          <Tuft x={606} y={720} scale={1.2} opacity={0.6} duration={7} delay={-2.4} />
          <Tuft x={940} y={720} scale={1.15} opacity={0.55} duration={8.2} delay={-4.2} />
          <Tuft x={1138} y={720} scale={1.35} opacity={0.65} duration={8.5} delay={-5} color="var(--scene-grass-light)" />
          <Tuft x={1420} y={720} scale={1.5} opacity={0.72} duration={6} delay={-4} color="var(--scene-grass-light)" />
          <Tuft x={1556} y={720} scale={1.25} opacity={0.6} duration={7.6} delay={-1.6} />
          <Tuft x={1664} y={720} scale={2} opacity={0.85} duration={6.5} delay={-5} />
        </g>
      </svg>

      <div className="hero-light-shimmer absolute inset-0" />
      <div className="hero-grain absolute inset-0" />
    </div>
  );
}
