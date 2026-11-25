import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { Logo } from './Logo';
import { GithubMark } from '@/components/icons/GithubMark';
import { XMark } from '@/components/icons/XMark';
import { X_URL } from '@/lib/socials';
import { CONTACT_EMAIL } from '@/lib/contact';

const REPO_URL = 'https://github.com/PIYUSH-NEXTGEN/Manabi';

type FooterLink = {
  label: string;
  to?: string;
  href?: string;
  icon?: 'x' | 'github';
};

type FooterColumn = {
  heading: string;
  links: FooterLink[];
};

const FOOTER_COLUMNS: FooterColumn[] = [
  {
    heading: 'Explore',
    links: [
      { label: 'Projects', to: '/problems' },
      { label: 'Contribute', to: '/contribute' },
      { label: 'Dashboard', to: '/me' },
    ],
  },
  {
    heading: 'MANABI',
    links: [
      { label: 'About', to: '/about' },
      { label: 'FAQ', to: '/faq' },
      { label: 'Sponsors', to: '/sponsors' },
      { label: 'Contact', to: '/contact' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { label: 'Privacy', to: '/privacy' },
      { label: 'Terms', to: '/terms' },
    ],
  },
  {
    heading: 'Support',
    links: [
      { label: 'Email us', href: `mailto:${CONTACT_EMAIL}` },
      { label: 'Report a bug', href: `${REPO_URL}/issues` },
      { label: 'Discussions', href: `${REPO_URL}/discussions` },
    ],
  },
  {
    heading: 'Social Media',
    links: [
      { label: '@Piyush_NextGen', href: X_URL, icon: 'x' },
      { label: 'manabi', href: REPO_URL, icon: 'github' },
    ],
  },
];

const LINK_CLASS =
  'rounded-[3px] text-[0.9375rem] leading-none text-[#22242a] transition-[color,transform] duration-200 hover:translate-x-0.5 hover:text-[#0a0b0d] hover:underline hover:underline-offset-4 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#15161a] focus-visible:ring-offset-2 focus-visible:ring-offset-white';

function FooterLinkItem({ link }: { link: FooterLink }) {
  const className = link.icon
    ? `group inline-flex items-center gap-2.5 ${LINK_CLASS}`
    : `inline-block ${LINK_CLASS}`;

  const content = (
    <>
      {link.icon === 'x' ? (
        <XMark
          size={14}
          className="shrink-0 text-[#15161a] transition-transform duration-200 group-hover:scale-110"
        />
      ) : null}
      {link.icon === 'github' ? (
        <GithubMark
          size={16}
          className="shrink-0 text-[#15161a] transition-transform duration-200 group-hover:scale-110"
        />
      ) : null}
      {link.label}
    </>
  );

  if (link.to) {
    return (
      <Link to={link.to} className={className}>
        {content}
      </Link>
    );
  }

  return (
    <a href={link.href} target="_blank" rel="noreferrer" className={className}>
      {content}
    </a>
  );
}

export function Footer() {
  return (
    <footer className="relative overflow-hidden border-t border-[#eceae3] bg-white [--paper:#ffffff] [--danger:#b42318]">
      <div className="mx-auto w-full max-w-[1360px] px-6 pt-12 sm:px-10 sm:pt-14 lg:px-16 lg:pt-16">
        <div className="flex flex-col gap-3">
          <Link
            to="/"
            className="group inline-flex w-fit items-center gap-3 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#15161a] focus-visible:ring-offset-4 focus-visible:ring-offset-white"
          >
            <Logo
              size={38}
              className="text-[#15161a] transition-colors group-hover:text-[#4a7fb5]"
            />
            <span className="font-brand text-[1.25rem] uppercase leading-none tracking-[-0.01em] text-[#15161a]">
              MANABI
            </span>
          </Link>
          <p className="text-[0.8125rem] leading-relaxed text-[#8b897f]">
            Real problems, built in public.
          </p>
        </div>

        <nav
          aria-label="Footer"
          className="mt-10 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:mt-12 lg:grid-cols-5 lg:gap-x-8"
        >
          {FOOTER_COLUMNS.map((column) => (
            <div key={column.heading}>
              <h2 className="text-[0.8125rem] font-normal text-[#a6a49b]">
                {column.heading}
              </h2>

              <ul className="mt-5 flex flex-col gap-3.5">
                {column.links.map((link) => (
                  <li key={`${column.heading}-${link.label}`}>
                    <FooterLinkItem link={link} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>

        <div className="mt-10 flex flex-col gap-4 border-t border-[#eceae3] pt-6 pb-2 sm:mt-12 sm:flex-row sm:items-center sm:justify-between sm:pt-8">
          <p className="text-[0.8125rem] text-[#78766d]">
            © 2026 MANABI. All rights reserved.
          </p>
          <p className="inline-flex items-center gap-1.5 text-[0.8125rem] text-[#78766d]">
            <Heart
              aria-hidden
              size={14}
              fill="currentColor"
              strokeWidth={0}
              className="text-[#e5484d]"
            />
            Made with love, in public
          </p>
        </div>
      </div>

      {/* Full-bleed pencil sketch. Only the empty sky is clipped away; the drawing
          keeps its aspect ratio, resolution and detail, with no filters. */}
      <div className="overflow-hidden">
        <img
          src="/footer.webp"
          alt=""
          aria-hidden
          loading="lazy"
          decoding="async"
          draggable={false}
          className="block h-auto w-full select-none -mt-[4%] sm:-mt-[7%]"
        />
      </div>
    </footer>
  );
}
