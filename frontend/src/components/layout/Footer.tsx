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
      { label: 'ML Practice', to: '/ml' },
      { label: 'Ingest', to: '/ingest' },
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
    <footer className="border-t-[3px] border-ink bg-ink text-paper">
      <div className="mx-auto w-[min(1200px,96vw)] py-10">
        <nav aria-label="Footer" className="grid gap-8 md:grid-cols-4">
          {FOOTER_COLUMNS.map((column) => (
            <div key={column.heading} className="flex flex-col gap-3">
              <h2 className="border-b-[3px] border-paper pb-1 font-mono text-xs font-bold uppercase tracking-widest">
                {column.heading}
              </h2>
              <ul className="flex flex-col gap-2">
                {column.links.map((link) => (
                  <li key={`${column.heading}-${link.label}`}>
                    <Link
                      to={link.to}
                      className="text-sm underline-offset-4 hover:underline"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>

        <div className="mt-10 flex flex-col gap-2 border-t-[3px] border-paper pt-4 font-mono text-[11px] font-bold uppercase tracking-widest">
          <p>© 2026 MANABI · Prototype built at a hackathon</p>
          <p>
            Problem text belongs to the publishing organisations. MANABI shows
            the original statement and credits the source on every card.
          </p>
        </div>
      </div>
    </footer>
  );
}
