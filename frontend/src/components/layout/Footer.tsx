import { Link } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  ArrowUpRight,
  ChevronRight,
  Compass,
  Hammer,
  Info,
  Scale,
} from 'lucide-react';
import { Logo } from './Logo';

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
    heading: 'Explore',
    icon: Compass,
    links: [
      { label: 'Projects', to: '/problems' },
      { label: 'Advanced projects', to: '/projects' },
      { label: 'How it works', to: '/how-it-works' },
    ],
  },
  {
    heading: 'Build',
    icon: Hammer,
    links: [
      { label: 'Repo analyzer', to: '/repo-analyzer' },
      { label: 'Submit a project', to: '/problems' },
      { label: 'Contribute', to: '/contribute' },
      { label: 'Your dashboard', to: '/me' },
    ],
  },
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
    <footer className="border-t border-ink bg-ink text-paper">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid gap-12 py-14 lg:grid-cols-[1.05fr_1.95fr] lg:gap-20">
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
              <span aria-hidden className="block size-1.5 bg-accent-soft" />
              Index open · 2026 edition
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
            className="grid gap-x-8 gap-y-10 sm:grid-cols-2 lg:grid-cols-4"
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
          <div className="space-y-1.5">
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/55">
              © 2026 MANABI
            </p>
            <p className="max-w-xl text-[11px] leading-relaxed text-paper/45">
              Problem briefs come from hackathons, companies, and public
              programs, and are reviewed before they appear on the board.
              Project progress is read from public GitHub repositories.
            </p>
          </div>

          <div className="flex items-end gap-4">
            <div className="text-right font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-paper/50">
              <p>Doc. no.</p>
              <p className="text-paper/85">EA.2026.001</p>
            </div>
            <span aria-hidden className="barcode block h-8 w-24 bg-paper/70" />
            <span aria-hidden className="block size-6 bg-accent" />
          </div>
        </div>
      </div>
    </footer>
  );
}
