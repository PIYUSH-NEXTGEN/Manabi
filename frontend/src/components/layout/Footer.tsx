import { Link } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  ArrowUpRight,
  ChevronRight,
  Info,
  Scale,
} from 'lucide-react';
import { Logo } from './Logo';
import { GithubMark } from '@/components/icons/GithubMark';

export interface FooterLink {
  label: string;
  to: string;
}

export interface FooterColumn {
  heading: string;
  icon: LucideIcon;
  links: FooterLink[];
}

export const FOOTER_COLUMNS: FooterColumn[] = [
  {
    heading: 'MANABI',
    icon: Info,
    links: [
      { label: 'About', to: '/about' },
      { label: 'FAQ', to: '/faq' },
      { label: 'Contact', to: '/contact' },
    ],
  },
  {
    heading: 'Legal',
    icon: Scale,
    links: [
      { label: 'Privacy', to: '/privacy' },
      { label: 'Terms', to: '/terms' },
    ],
  },
];

export function Footer() {
  return (
    <footer className="relative overflow-hidden border-t border-ink bg-ink text-paper">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid gap-12 py-14 lg:grid-cols-[1.5fr_1fr] lg:gap-16">
          <div>
            <Link to="/" className="group inline-flex items-center gap-3">
              <Logo className="text-paper transition-colors group-hover:text-accent-soft" />
              <span className="font-display text-2xl uppercase leading-none tracking-tight">
                MANABI
              </span>
            </Link>

            <p className="mt-5 max-w-xs text-sm leading-relaxed text-paper/70">
              Real problems worth building. Claim a brief, link your GitHub
              repo, and MANABI tracks commits, README status, and open issues
              while you ship it.
            </p>

            <span className="mt-6 inline-flex items-center gap-2 border border-paper/25 px-3 py-2 font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/65">
              <a
                href="https://github.com/PIYUSH-NEXTGEN/Manabi"
                target="_blank"
                rel="noreferrer"
                aria-label="MANABI on GitHub"
                className="group inline-flex items-center gap-2 transition-colors hover:text-paper"
              >
                <span aria-hidden className="block size-1.5 bg-accent-soft" />
                <GithubMark size={14} className="text-paper/65 transition-colors group-hover:text-accent-soft" />
                Source on GitHub
              </a>
            </span>

            <Link
              to="/problems"
              className="group mt-6 flex w-fit items-center gap-1.5 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent-soft transition-colors hover:text-paper"
            >
              Start with a brief
              <ArrowUpRight
                aria-hidden
                size={13}
                strokeWidth={2.6}
                className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
              />
            </Link>
          </div>

          <nav
            aria-label="Footer"
            className="grid gap-x-8 gap-y-10 sm:grid-cols-2"
          >
            {FOOTER_COLUMNS.map((column) => {
              const Icon = column.icon;
              return (
                <div key={column.heading} className="flex flex-col">
                  <h2 className="flex items-center gap-2 border-b border-paper/20 pb-2.5 font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-paper/60">
                    <Icon
                      aria-hidden
                      size={12}
                      strokeWidth={2.4}
                      className="text-accent-soft"
                    />
                    {column.heading}
                  </h2>
                  <ul className="mt-3.5 flex flex-col gap-2.5">
                    {column.links.map((link) => (
                      <li key={`${column.heading}-${link.label}`}>
                        <Link
                          to={link.to}
                          className="group inline-flex items-start gap-1.5 text-sm leading-snug text-paper/70 underline-offset-4 transition-colors hover:text-paper"
                        >
                          <ChevronRight
                            aria-hidden
                            size={13}
                            strokeWidth={2.6}
                            className="mt-0.5 shrink-0 text-paper/30 transition-colors group-hover:text-accent-soft"
                          />
                          {link.label}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </nav>
        </div>

        <div className="flex flex-col gap-5 border-t border-paper/20 py-5 md:flex-row md:items-center md:justify-between">
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/55">
            © 2026 MANABI
          </p>
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/55">
            Built for builders · Night shift edition
          </p>
        </div>
      </div>

      <div aria-hidden className="relative">
        <img
          src="/footer-scene.png"
          alt=""
          loading="lazy"
          draggable={false}
          className="block h-[300px] w-full object-cover object-bottom md:h-[380px]"
        />
        <div className="absolute inset-x-0 top-0 h-28 bg-gradient-to-b from-ink via-ink/60 to-transparent" />
      </div>
    </footer>
  );
}
