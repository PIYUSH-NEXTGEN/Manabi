import { Link } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import { ChevronRight, Info, Scale, Star } from 'lucide-react';
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
    <footer className="dawn-field relative overflow-hidden border-t border-line">
      <div className="mx-auto w-[min(1240px,96vw)]">
        <div className="grid gap-10 py-14 lg:grid-cols-[1.4fr_1fr] lg:gap-16">
          <div>
            <Link to="/" className="group inline-flex items-center gap-3">
              <Logo className="text-ink transition-colors group-hover:text-accent" />
              <span className="font-brand text-[0.9375rem] uppercase leading-none tracking-[-0.01em]">
                MANABI
              </span>
            </Link>

            <p className="mt-4 max-w-sm text-body leading-relaxed text-ink-soft">
              Real problems, picked from the index and proven by a public
              repository.
            </p>

            <a
              href="https://github.com/PIYUSH-NEXTGEN/Manabi"
              target="_blank"
              rel="noreferrer"
              aria-label="Star MANABI on GitHub"
              className="github-star group mt-6 flex w-fit items-center gap-2 rounded-full bg-ink px-4 py-2.5 text-[0.8125rem] font-semibold text-paper"
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

          <nav aria-label="Footer" className="grid gap-x-8 gap-y-10 sm:grid-cols-2">
            {FOOTER_COLUMNS.map((column) => {
              const Icon = column.icon;
              return (
                <div key={column.heading} className="flex flex-col">
                  <h2 className="flex items-center gap-2 border-b border-line pb-2.5 font-mono text-label font-bold uppercase tracking-[0.18em] text-muted">
                    <Icon aria-hidden size={12} strokeWidth={2.4} className="text-accent" />
                    {column.heading}
                  </h2>
                  <ul className="mt-3.5 flex flex-col gap-2">
                    {column.links.map((link) => (
                      <li key={`${column.heading}-${link.label}`}>
                        <Link
                          to={link.to}
                          className="group inline-flex items-start gap-1.5 text-body leading-snug text-ink-soft underline-offset-4 transition-colors hover:text-accent hover:underline"
                        >
                          <ChevronRight
                            aria-hidden
                            size={13}
                            strokeWidth={2.6}
                            className="mt-1 shrink-0 text-ink/25 transition-colors group-hover:text-accent"
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

        <div className="flex flex-col gap-3 border-t border-line py-5 md:flex-row md:items-center md:justify-between">
          <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
            © 2026 MANABI
          </p>
          <p className="font-mono text-label font-bold uppercase tracking-[0.16em] text-muted">
            Built for builders · Night shift edition
          </p>
        </div>
      </div>
    </footer>
  );
}
