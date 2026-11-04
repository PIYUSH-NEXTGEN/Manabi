import { Link } from 'react-router-dom';

export interface FooterLink {
  label: string;
  to: string;
}

export const FOOTER_COLUMNS: { heading: string; links: FooterLink[] }[] = [
  {
    heading: 'Explore',
    links: [
      { label: 'Problems', to: '/problems' },
      { label: 'Sources', to: '/sources' },
    ],
  },
  {
    heading: 'Build',
    links: [
      { label: 'How it works', to: '/how-it-works' },
      { label: 'Submit a project →', to: '/problems' },
      { label: 'Contribute', to: '/contribute' },
    ],
  },
  {
    heading: 'MANABI',
    links: [
      { label: 'About', to: '/about' },
      { label: 'FAQ', to: '/faq' },
      { label: 'Contact', to: '/contact' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { label: 'Privacy', to: '/privacy' },
      { label: 'Terms', to: '/terms' },
      { label: 'Data & credits', to: '/sources#credits' },
    ],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-ink bg-ink text-paper">
      <div className="mx-auto w-[min(1240px,96vw)] py-12">
        <div className="mb-10 flex flex-wrap items-end justify-between gap-6 border-b border-paper/25 pb-6">
          <p className="font-display text-3xl uppercase leading-none tracking-tight">
            MANABI
          </p>
          <p className="max-w-sm font-mono text-[10px] font-bold uppercase leading-relaxed tracking-[0.16em] text-paper/70">
            Real briefs, credited sources, public progress.
          </p>
          <span aria-hidden className="block size-10 bg-accent" />
        </div>

        <nav aria-label="Footer" className="grid gap-8 md:grid-cols-4">
          {FOOTER_COLUMNS.map((column) => (
            <div key={column.heading} className="flex flex-col gap-3">
              <h2 className="border-b border-paper/25 pb-2 font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-paper/60">
                {column.heading}
              </h2>
              <ul className="flex flex-col gap-2">
                {column.links.map((link) => (
                  <li key={`${column.heading}-${link.label}`}>
                    <Link
                      to={link.to}
                      className="text-sm text-paper/90 underline-offset-4 transition-colors hover:text-accent"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>

        <div className="mt-12 flex flex-col gap-4 border-t border-paper/25 pt-5 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-paper/60 md:flex-row md:items-end md:justify-between">
          <div className="space-y-1.5">
            <p>© 2026 MANABI · Prototype built at a hackathon</p>
            <p className="max-w-2xl normal-case tracking-normal text-paper/50">
              Problem text belongs to the publishing organisations. MANABI shows
              the original statement and credits the source on every card.
            </p>
          </div>
          <div className="flex items-end gap-4">
            <div className="text-right">
              <p>Doc. no.</p>
              <p className="text-paper">EA.2026.001</p>
            </div>
            <span aria-hidden className="barcode block h-8 w-28 bg-paper/80" />
            <span aria-hidden className="block size-6 bg-accent" />
          </div>
        </div>
      </div>
    </footer>
  );
}
