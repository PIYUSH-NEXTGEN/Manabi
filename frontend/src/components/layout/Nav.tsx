import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import { Logo } from './Logo';
import { useMe } from '@/hooks/useMe';

const NAV_LINKS = [
  { to: '/problems', label: 'Projects' },
  { to: '/repo-analyzer', label: 'Repo Analyzer' },
  { to: '/how-it-works', label: 'How it works' },
];

export function Nav() {
  const me = useMe();
  const links = me.data?.is_admin
    ? [...NAV_LINKS, { to: '/admin/review', label: 'Review' }]
    : NAV_LINKS;

  return (
    <header className="sticky top-0 z-30 border-b-[3px] border-ink bg-paper">
      <nav
        aria-label="Main"
        className="mx-auto flex w-[min(1200px,96vw)] flex-wrap items-center justify-between gap-4 py-3"
      >
        <Link
          to="/"
          className="flex items-center gap-2"
        >
          <div className="flex items-center justify-center bg-ink p-1.5 rounded-[4px]">
            <Logo className="text-paper" />
          </div>
          <span className="font-display text-2xl uppercase leading-none tracking-tight">
            MANABI
          </span>
        </Link>

        <ul className="hidden items-center gap-5 md:flex">
          {links.map((link) => (
            <li key={link.to}>
              <Link
                to={link.to}
                className="font-mono text-[11px] font-bold uppercase tracking-widest underline-offset-4 hover:underline"
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-2">
          {me.data ? (
            <Link
              to="/me"
              className="flex items-center gap-2 border-[3px] border-ink bg-white px-4 py-2 shadow-hard-sm"
            >
              {me.data.avatar_url ? (
                <img
                  src={me.data.avatar_url}
                  alt=""
                  className="size-6 border-[2px] border-ink"
                />
              ) : null}
              <span className="font-mono text-sm font-bold uppercase tracking-widest">
                {me.data.username}
              </span>
            </Link>
          ) : (
            <Button
              variant="secondary"
              size="small"
              onClick={() => {
                window.location.assign('/api/auth/github/login');
              }}
              className="hover:-translate-y-0.5 active:translate-y-0 transition-transform duration-100"
            >
              GitHub
            </Button>
          )}
        </div>

        <ul className="order-last flex w-full items-center gap-4 overflow-x-auto pb-1 md:hidden">
          {links.map((link) => (
            <li key={link.to} className="shrink-0">
              <Link
                to={link.to}
                className="font-mono text-[11px] font-bold uppercase tracking-widest underline-offset-4 hover:underline"
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
