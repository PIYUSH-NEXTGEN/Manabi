import { Link } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  ArrowUpRight,
  ChevronRight,
  Info,
  Scale,
  Star,
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
    <footer className="inverted-surface relative overflow-hidden border-t border-ink bg-ink text-paper">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid gap-10 py-11 lg:grid-cols-[1.5fr_1fr] lg:gap-16">
          <div>
            <Link to="/" className="group inline-flex items-center gap-3">
              <Logo className="text-paper transition-colors group-hover:text-accent-soft" />
              <span className="font-display text-body uppercase leading-none tracking-tight">
                MANABI
              </span>
            </Link>

            <a
              href="https://github.com/PIYUSH-NEXTGEN/Manabi"
              target="_blank"
              rel="noreferrer"
              aria-label="Star MANABI on GitHub"
              className="github-star group mt-6 flex w-fit items-center gap-2 bg-ink px-3 py-2 font-mono text-label font-bold uppercase tracking-[0.16em] text-paper"
            >
              <Star
                aria-hidden
                size={12}
                strokeWidth={2.4}
                fill="currentColor"
                className="text-paper"
              />
              <GithubMark size={14} className="text-paper/80 transition-colors group-hover:text-paper" />
              Star on GitHub
            </a>

          </div>

          <nav
            aria-label="Footer"
            className="grid gap-x-8 gap-y-10 sm:grid-cols-2"
          >
            {FOOTER_COLUMNS.map((column) => {
              const Icon = column.icon;
              return (
                <div key={column.heading} className="flex flex-col">
                  <h2 className="flex items-center gap-2 border-b border-paper/20 pb-2.5 font-mono text-label font-bold uppercase tracking-[0.2em] text-paper/60">
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
                          className="group inline-flex items-start gap-1.5 text-body leading-snug text-paper/70 underline-offset-4 transition-colors hover:text-paper"
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

        <div className="flex flex-col gap-5 border-t border-paper/20 py-4 md:flex-row md:items-center md:justify-between">
          <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-paper/55">
            © 2026 MANABI
          </p>
          <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-paper/55">
            Built for builders · Night shift edition
          </p>
        </div>
      </div>

      <div className="relative aspect-[16/6.2] overflow-hidden bg-ink">
        <img
          src="/footer-scene.png"
          alt=""
          draggable={false}
          className="absolute inset-0 size-full object-cover object-top [image-rendering:pixelated]"
        />
        <div className="absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-ink via-ink/70 to-transparent pointer-events-none" />
        <div className="pointer-events-none absolute inset-x-0 bottom-0 h-6 bg-gradient-to-t from-ink/40 to-transparent" />
        <div className="absolute inset-x-0 top-0">
          <div className="mx-auto w-[min(1240px,96vw)] pt-7">
            <Link
              to="/problems"
              className="group inline-flex items-center gap-1.5 font-mono text-label font-bold uppercase tracking-[0.16em] text-paper/90 transition-colors hover:text-accent-soft"
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
        </div>
      </div>
    </footer>
  );
}
