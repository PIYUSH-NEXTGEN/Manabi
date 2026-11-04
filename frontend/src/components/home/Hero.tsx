import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { buttonClasses } from '@/design';
import { useStats } from '@/hooks/useStats';
import { CountUp } from './CountUp';

const FEATURES = [
  {
    title: 'Sourced briefs',
    copy: 'Every problem links back to the organisation that published it.',
  },
  {
    title: 'Progress tracked',
    copy: 'Commits and README update themselves from the repo you link.',
  },
  {
    title: 'Built in public',
    copy: 'One page per project, so the work speaks before the pitch does.',
  },
];

function HeroArtwork() {
  return (
    <svg
      viewBox="0 0 560 420"
      role="img"
      aria-labelledby="hero-artwork-title"
      className="h-auto w-full"
    >
      <title id="hero-artwork-title">
        Layered problem brief cards, a repo progress panel and a phone mockup
      </title>

      {/* back brief card */}
      <g transform="rotate(6 200 130)">
        <rect
          x="84"
          y="46"
          width="240"
          height="150"
          transform="translate(8 8)"
          fill="var(--ink)"
        />
        <rect
          x="84"
          y="46"
          width="240"
          height="150"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect x="102" y="66" width="92" height="10" fill="var(--ink)" />
        <rect
          x="102"
          y="90"
          width="196"
          height="7"
          fill="var(--ink)"
          opacity="0.28"
        />
        <rect
          x="102"
          y="106"
          width="168"
          height="7"
          fill="var(--ink)"
          opacity="0.28"
        />
        <rect
          x="102"
          y="134"
          width="62"
          height="20"
          fill="var(--yellow)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect
          x="174"
          y="134"
          width="52"
          height="20"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
      </g>

      {/* phone mockup */}
      <g transform="rotate(-8 450 200)">
        <rect
          x="398"
          y="56"
          width="128"
          height="268"
          rx="24"
          transform="translate(8 8)"
          fill="var(--ink)"
        />
        <rect
          x="398"
          y="56"
          width="128"
          height="268"
          rx="24"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect x="442" y="72" width="40" height="8" rx="4" fill="var(--ink)" />
        <rect
          x="416"
          y="102"
          width="92"
          height="54"
          fill="var(--yellow)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect x="428" y="118" width="58" height="7" fill="var(--ink)" />
        <rect
          x="428"
          y="132"
          width="40"
          height="7"
          fill="var(--ink)"
          opacity="0.4"
        />
        {[176, 200, 224, 248].map((y) => (
          <g key={y}>
            <rect
              x="416"
              y={y}
              width="14"
              height="14"
              fill="var(--white)"
              stroke="var(--ink)"
              strokeWidth="3"
            />
            <rect
              x="440"
              y={y + 4}
              width={y === 224 ? 48 : 66}
              height="7"
              fill="var(--ink)"
              opacity="0.3"
            />
          </g>
        ))}
        <rect
          x="416"
          y="282"
          width="92"
          height="18"
          fill="var(--ink)"
          opacity="0.85"
        />
      </g>

      {/* front brief card */}
      <g transform="rotate(-5 300 250)">
        <rect
          x="148"
          y="148"
          width="300"
          height="196"
          transform="translate(9 9)"
          fill="var(--ink)"
        />
        <rect
          x="148"
          y="148"
          width="300"
          height="196"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect
          x="148"
          y="148"
          width="300"
          height="36"
          fill="var(--yellow)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        {[166, 180, 194].map((cx) => (
          <circle key={cx} cx={cx} cy="166" r="4.5" fill="var(--ink)" />
        ))}
        <rect
          x="170"
          y="204"
          width="86"
          height="18"
          fill="var(--ink)"
        />
        <rect x="266" y="209" width="52" height="8" fill="var(--ink)" opacity="0.35" />
        <rect x="170" y="240" width="240" height="10" fill="var(--ink)" opacity="0.8" />
        <rect x="170" y="260" width="196" height="8" fill="var(--ink)" opacity="0.3" />
        <rect x="170" y="278" width="216" height="8" fill="var(--ink)" opacity="0.3" />
        <rect
          x="170"
          y="304"
          width="74"
          height="22"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect
          x="252"
          y="304"
          width="58"
          height="22"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect x="322" y="300" width="88" height="26" fill="var(--red)" />
      </g>

      {/* repo progress card */}
      <g transform="rotate(-3 190 356)">
        <rect
          x="70"
          y="300"
          width="240"
          height="96"
          transform="translate(7 7)"
          fill="var(--ink)"
        />
        <rect
          x="70"
          y="300"
          width="240"
          height="96"
          fill="var(--white)"
          stroke="var(--ink)"
          strokeWidth="3"
        />
        <rect x="86" y="316" width="58" height="8" fill="var(--ink)" />
        <rect x="86" y="332" width="96" height="7" fill="var(--ink)" opacity="0.3" />
        <g>
          {Array.from({ length: 10 }, (_, index) => (
            <rect
              key={index}
              x={86 + index * 18}
              y="352"
              width="13"
              height="13"
              fill={index < 7 ? 'var(--ink)' : 'var(--white)'}
              stroke="var(--ink)"
              strokeWidth="2.5"
            />
          ))}
        </g>
        <rect
          x="86"
          y="374"
          width="44"
          height="6"
          fill="var(--ink)"
          opacity="0.4"
        />
        <rect
          x="140"
          y="374"
          width="30"
          height="6"
          fill="var(--ink)"
          opacity="0.4"
        />
      </g>

      {/* accents */}
      <path
        d="M36 200 L96 140"
        stroke="var(--ink)"
        strokeWidth="3"
        strokeDasharray="8 7"
      />
      <path
        d="M52 300 L88 264"
        stroke="var(--ink)"
        strokeWidth="3"
        strokeDasharray="8 7"
      />
      <circle cx="474" cy="34" r="12" fill="var(--yellow)" stroke="var(--ink)" strokeWidth="3" />
      <path
        d="M112 28 L124 52 L100 52 Z"
        fill="var(--red)"
        stroke="var(--ink)"
        strokeWidth="3"
      />
    </svg>
  );
}

export function Hero() {
  const stats = useStats();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = query.trim();
    navigate(trimmed ? `/problems?q=${encodeURIComponent(trimmed)}` : '/problems');
  }

  return (
    <section className="overflow-hidden border-b-[3px] border-ink">
      <div className="mx-auto grid w-[min(1200px,96vw)] items-center gap-12 py-12 md:grid-cols-2 md:gap-10 md:py-16">
        <div className="flex flex-col items-start gap-7">
          <h1
            className="relative inline-block font-display uppercase leading-[0.85] tracking-tight"
            style={{ fontSize: 'clamp(3.25rem, 9vw, 7rem)' }}
          >
            <span className="relative z-10">MANABI</span>
            <span
              aria-hidden
              className="absolute inset-x-0 bottom-[0.12em] z-0 h-[0.16em] bg-yellow"
            />
          </h1>

          <p className="max-w-xl text-lg leading-snug md:text-xl">
            Real problem briefs with real sources. Claim one, link your repo,
            and build in public.
          </p>

          <form
            role="search"
            noValidate
            onSubmit={handleSubmit}
            className="flex w-full max-w-xl flex-col gap-3 sm:flex-row"
          >
            <label htmlFor="hero-search" className="sr-only">
              Search problem briefs
            </label>
            <input
              id="hero-search"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search problems — leaf blight, SLAs…"
              className="field min-w-0 flex-1"
            />
            <button type="submit" className={buttonClasses('primary')}>
              Browse projects
            </button>
          </form>

          <dl className="flex w-full max-w-xl items-stretch gap-6 border-t-[3px] border-ink pt-6 sm:gap-8">
            <div className="flex flex-col-reverse gap-1 border-r-[3px] border-ink pr-6 sm:pr-8">
              <dt className="font-mono text-[11px] font-bold uppercase tracking-widest">
                Problem briefs indexed
              </dt>
              <dd className="font-display text-4xl leading-none md:text-5xl">
                {stats.data ? (
                  <CountUp value={stats.data.problems} />
                ) : (
                  <span aria-hidden>—</span>
                )}
              </dd>
            </div>
            <div className="flex flex-col-reverse gap-1">
              <dt className="font-mono text-[11px] font-bold uppercase tracking-widest">
                Official sources credited
              </dt>
              <dd className="font-display text-4xl leading-none md:text-5xl">
                {stats.data ? (
                  <CountUp value={stats.data.sources} />
                ) : (
                  <span aria-hidden>—</span>
                )}
              </dd>
            </div>
          </dl>
          <p className="sr-only" role="status">
            {stats.data
              ? `${stats.data.problems} problem briefs indexed from ${stats.data.sources} sources`
              : stats.isError
                ? 'Problem count unavailable'
                : 'Counting problems…'}
          </p>

          <p className="flex flex-wrap items-center gap-3 font-mono text-[11px] font-bold uppercase tracking-widest">
            <span className="bg-ink px-2 py-1 text-yellow">Sources</span>
            <span className="text-ink/70">
              Official portals · public briefings · open data — each one credited
            </span>
          </p>
        </div>

        <div className="flex flex-col gap-6">
          <div className="border-[3px] border-ink bg-white p-4 shadow-hard-lg sm:p-6">
            <HeroArtwork />
          </div>

          <ul className="grid gap-4 sm:grid-cols-3">
            {FEATURES.map((feature) => (
              <li key={feature.title} className="border-t-[3px] border-ink pt-3">
                <h2 className="font-mono text-[11px] font-bold uppercase tracking-widest">
                  {feature.title}
                </h2>
                <p className="mt-1.5 text-sm leading-snug">{feature.copy}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
