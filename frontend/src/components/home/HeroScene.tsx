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
      <ellipse
        cx={8}
        cy={2}
        rx={30}
        ry={6}
        fill="var(--scene-shadow)"
        opacity="0.24"
        stroke="none"
      />
      <g
        className="tree-sway"
        style={{ animationDuration: `${duration}s`, animationDelay: `${delay}s` }}
      >
        <use href={href} />
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
  return (
    <div
      aria-hidden
      className="hero-scene pointer-events-none absolute inset-0 -z-10 overflow-hidden"
    >
      <div className="hero-sky absolute inset-0" />

      <div className="absolute left-[13%] top-[6%] size-52 rounded-full bg-white/80 blur-3xl dark:hidden" />
      <div className="absolute right-[7%] top-[24%] size-64 rounded-full bg-white/35 blur-3xl dark:hidden" />

      <div className="absolute inset-0 hidden dark:block">
        {STARS.map((star, index) => (
          <span
            key={index}
            className="twinkle absolute rounded-full bg-white"
            style={{
              left: star.left,
              top: star.top,
              width: star.size,
              height: star.size,
              animationDelay: star.delay,
              boxShadow: '0 0 6px rgba(255, 255, 255, 0.55)',
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
      >
        <svg className="balloon-bob" viewBox="0 0 72 96" fill="none" aria-hidden>
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
          <clipPath id="river-clip">
            <path d="M828 448C822 464 812 476 806 494C798 518 806 542 798 566C790 592 770 612 750 638C730 664 692 694 640 742L830 742C818 714 826 690 828 668C830 644 826 618 824 594C822 570 830 550 836 528C842 506 844 480 842 462C841 452 836 448 828 448Z" />
          </clipPath>
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

          <g id="tree-round" stroke="var(--sketch-ink-soft)" strokeWidth="1.15" strokeOpacity="0.62" strokeLinejoin="round">
            <path
              d="M-4 0C-4.2-10-3.8-22-3.2-34L-2.4-52H2.4L3.2-34C3.8-22 4.2-10 4 0Z"
              fill="var(--scene-trunk)"
            />
            <path
              d="M-2.2-46C-6-56-9-64-12-74M2.2-46C6-56 9-64 13-72"
              stroke="var(--scene-trunk)"
              strokeWidth="2"
              strokeLinecap="round"
              fill="none"
            />
            <path
              d="M0-112C18-112 30-102 31-88C42-84 47-72 41-62C46-51 38-41 26-42L-26-42C-38-41-46-51-41-62C-47-72-42-84-31-88C-30-102-18-112 0-112Z"
              fill="var(--scene-tree-deep)"
            />
            <path
              d="M0-104C14-104 23-96 24-85C31-79 33-68 27-61C25-55 17-50 8-51L-8-51C-19-51-27-58-28-66C-33-74-29-85-21-89C-17-99-9-104 0-104Z"
              fill="var(--scene-tree)"
              stroke="none"
            />
            <ellipse cx="-10" cy="-84" rx="12" ry="9" fill="var(--scene-tree-alt)" opacity="0.45" stroke="none" />
            <ellipse cx="14" cy="-59" rx="13" ry="8" fill="url(#sketch-hatch)" opacity="0.38" stroke="none" />
            <path
              d="M-20-96C-10-101 2-102 12-99"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="0.9"
              strokeOpacity="0.35"
              strokeLinecap="round"
              fill="none"
            />
          </g>

          <g id="tree-birch" stroke="var(--sketch-ink-soft)" strokeWidth="1.05" strokeOpacity="0.6" strokeLinejoin="round">
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

          <g id="tree-pine" stroke="var(--sketch-ink-soft)" strokeWidth="1.05" strokeOpacity="0.6" strokeLinejoin="round">
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

          <g id="tree-cypress" stroke="var(--sketch-ink-soft)" strokeWidth="1.05" strokeOpacity="0.6" strokeLinejoin="round">
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

          <g id="bush" stroke="var(--sketch-ink-soft)" strokeWidth="1.05" strokeOpacity="0.6" strokeLinejoin="round">
            <circle cx="-18" cy="-10" r="16" fill="var(--scene-tree-deep)" />
            <circle cx="0" cy="-20" r="22" fill="var(--scene-tree)" />
            <circle cx="20" cy="-9" r="15" fill="var(--scene-tree-deep)" />
            <circle cx="-6" cy="-26" r="12" fill="var(--scene-tree-alt)" opacity="0.7" />
            <circle cx="12" cy="-18" r="9" fill="var(--scene-tree-alt)" opacity="0.45" />
            <circle cx="10" cy="-16" r="13" fill="url(#sketch-hatch)" opacity="0.45" stroke="none" />
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
          <g
            stroke="var(--sketch-ink-faint)"
            strokeOpacity="0.45"
            strokeWidth="1.1"
            strokeLinecap="round"
          >
            <path d="M128 380C156 360 184 350 210 358M306 410C332 402 358 404 382 414M528 376C556 380 584 392 610 408M780 400C806 392 832 390 858 396M898 396C924 404 950 412 976 414M1022 418C1048 414 1074 406 1098 398M1246 424C1272 428 1298 428 1322 422M1474 392C1500 398 1526 406 1550 414" />
            <path d="M64 420C108 402 152 382 196 374M352 416C394 408 436 404 478 408M622 418C664 414 706 406 746 398M946 414C988 410 1030 404 1070 398M1320 420C1360 414 1400 406 1438 396M1560 416C1592 418 1622 416 1650 410" />
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
        </g>

        <g className="hero-parallax hero-parallax--near">
          <Tree href="#tree-round" x={580} y={615} scale={1.15} opacity={0.95} duration={8.5} delay={-3} />
        </g>

        <g className="hero-parallax hero-parallax--near">
          <path
            d="M828 448C822 464 812 476 806 494C798 518 806 542 798 566C790 592 770 612 750 638C730 664 692 694 640 742L830 742C818 714 826 690 828 668C830 644 826 618 824 594C822 570 830 550 836 528C842 506 844 480 842 462C841 452 836 448 828 448Z"
            fill="url(#river)"
            stroke="var(--sketch-ink-soft)"
            strokeWidth="1.5"
            strokeOpacity="0.65"
          />
          <g stroke="var(--scene-foam)" strokeLinecap="round" fill="none" clipPath="url(#river-clip)">
            <path
              d="M826 470C818 500 822 540 812 574C802 608 782 636 762 668C748 690 740 714 736 742"
              strokeWidth="2.4"
              strokeOpacity="0.55"
              className="river-flow river-flow-strong"
            />
            <path
              d="M834 486C828 514 832 548 822 580C812 612 798 640 786 672C778 694 772 718 768 742"
              strokeWidth="2.2"
              strokeOpacity="0.5"
              className="river-flow river-flow-soft"
              style={{ animationDelay: '-2.4s' }}
            />
            <path
              d="M812 500C806 530 810 562 800 594C790 626 772 654 758 684C750 706 744 724 740 742"
              strokeWidth="1.8"
              strokeOpacity="0.3"
              className="river-flow river-flow-soft"
              style={{ animationDelay: '-1.6s' }}
            />
            <path
              d="M828 512C824 540 830 570 820 600C810 630 798 658 788 688C780 708 774 726 770 742"
              strokeWidth="2"
              strokeOpacity="0.28"
              className="river-flow"
              style={{ animationDelay: '-3.6s', animationDuration: '9.5s' }}
            />
          </g>
          <g>
            <path
              d="M724 596C730 520 762 458 828 444C894 458 926 520 932 596C896 604 862 606 828 606C794 606 760 604 724 596Z"
              fill="url(#meadow-mid)"
            />
            <path
              d="M860 456C902 478 924 530 929 590C917 594 903 597 890 598C895 542 884 494 854 462Z"
              fill="url(#sketch-hatch)"
              opacity="0.32"
              stroke="none"
            />
            <path
              d="M724 596C730 520 762 458 828 444C894 458 926 520 932 596"
              stroke="var(--sketch-ink-soft)"
              strokeWidth="1.5"
              strokeOpacity="0.55"
              strokeLinecap="round"
              fill="none"
            />
            <Tree href="#tree-pine" x={786} y={464} scale={0.6} opacity={0.92} duration={9} delay={-2} />
            <use href="#bush" transform="translate(884 476) scale(0.6)" />
          </g>
          <g
            fill="var(--sketch-paper)"
            stroke="var(--sketch-ink-soft)"
            strokeWidth="1.1"
          >
            <ellipse cx="788" cy="648" rx="16" ry="5.5" />
            <path d="M788 648l10-3" stroke="var(--sketch-ink-soft)" strokeWidth="1" />
            <ellipse cx="800" cy="704" rx="14" ry="5" />
            <path d="M800 704l10-3" stroke="var(--sketch-ink-soft)" strokeWidth="1" />
            <ellipse cx="736" cy="700" rx="14" ry="5" />
            <path d="M736 700l9-2.5" stroke="var(--sketch-ink-soft)" strokeWidth="1" />
            <ellipse cx="770" cy="728" rx="16" ry="5.5" />
            <path d="M770 728l10-3" stroke="var(--sketch-ink-soft)" strokeWidth="1" />
          </g>
          <g
            fill="var(--scene-stone)"
            stroke="var(--sketch-ink-soft)"
            strokeWidth="1"
            strokeOpacity="0.5"
          >
            <ellipse cx="820" cy="616" rx="8" ry="3" />
            <ellipse cx="810" cy="676" rx="10" ry="4" />
            <ellipse cx="700" cy="732" rx="12" ry="4.5" />
          </g>
          <g
            stroke="var(--sketch-ink-faint)"
            strokeOpacity="0.25"
            strokeWidth="1"
            strokeLinecap="round"
            fill="none"
            clipPath="url(#river-clip)"
          >
            <path d="M812 528c8-2 16-2 24 0M800 566c8-2 16-2 24 0M786 604c9-2 18-2 27 0M782 644c9-2 18-2 27 0M772 684c10-3 20-3 30 0M756 716c10-3 20-3 30 0" />
          </g>
        </g>

        <g className="hero-parallax hero-parallax--near">
          <ellipse cx="300" cy="660" rx="40" ry="7" fill="var(--scene-shadow)" opacity="0.12" stroke="none" />
          <g transform="translate(300 656) scale(1.36)">
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
          </g>
        </g>

        <g className="hero-parallax hero-parallax--near">
          <g transform="translate(1336 654) scale(1.34)">
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

        <g fill="var(--sketch-ink-faint)" opacity="0.5">
          <circle cx="520" cy="690" r="1.3" />
          <circle cx="1114" cy="678" r="1.5" />
          <circle cx="1540" cy="700" r="1.4" />
        </g>
      </svg>

      <div className="hero-light-shimmer absolute inset-0" />
      <div className="hero-grain absolute inset-0" />
    </div>
  );
}
