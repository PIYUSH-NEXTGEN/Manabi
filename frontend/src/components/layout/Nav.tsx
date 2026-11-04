import { NavLink, Link } from 'react-router-dom';
import {
  FolderKanban,
  ListOrdered,
  Moon,
  ScanSearch,
  ShieldCheck,
  Sun,
} from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { Button } from '@/design/primitives';
import { Logo } from './Logo';
import { useMe } from '@/hooks/useMe';
import { useTheme } from '@/lib/useTheme';
import { cx } from '@/lib/cx';

const NAV_LINKS = [
  { to: '/problems', label: 'Projects', icon: FolderKanban },
  { to: '/repo-analyzer', label: 'Repo Analyzer', icon: ScanSearch },
  { to: '/how-it-works', label: 'How it works', icon: ListOrdered },
];

const ADMIN_LINK = {
  to: '/admin/review',
  label: 'Review',
  icon: ShieldCheck,
};

const navLinkClasses = ({ isActive }: { isActive: boolean }) =>
  cx(
    'label relative inline-flex items-center gap-1.5 py-1 transition-colors',
    isActive
      ? 'text-accent after:absolute after:inset-x-0 after:-bottom-0.5 after:h-px after:bg-accent'
      : 'text-ink hover:text-accent',
  );

export function Nav() {
  const me = useMe();
  const { theme, toggleTheme } = useTheme();
  const links = me.data?.is_admin ? [...NAV_LINKS, ADMIN_LINK] : NAV_LINKS;
  const themeLabel = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';

  return (
    <header className="sticky top-0 z-30 border-b border-ink bg-paper">
      <nav
        aria-label="Main"
        className="mx-auto flex w-[min(1240px,96vw)] flex-wrap items-center justify-between gap-x-6 gap-y-3 py-3"
      >
        <Link to="/" className="group flex items-center gap-2.5">
          <Logo className="text-ink transition-colors group-hover:text-accent" />
          <span className="font-display text-xl uppercase leading-none tracking-tight">
            MANABI
          </span>
        </Link>

        <ul className="hidden items-center gap-7 md:flex">
          {links.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} className={navLinkClasses}>
                <link.icon aria-hidden size={13} strokeWidth={2.4} />
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-3">
          {me.data ? (
            <Link
              to="/me"
              className="press flex items-center gap-2 border border-line bg-sheet px-3 py-1.5 hover:border-ink"
            >
              {me.data.avatar_url ? (
                <img
                  src={me.data.avatar_url}
                  alt=""
                  className="size-5 border border-ink object-cover"
                />
              ) : (
                <span aria-hidden className="block size-5 bg-tint" />
              )}
              <span className="font-mono text-[10px] font-bold uppercase tracking-[0.14em]">
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
            >
              <GithubMark size={14} />
              GitHub login
            </Button>
          )}

          <button
            type="button"
            onClick={toggleTheme}
            aria-label={themeLabel}
            title={themeLabel}
            className="press flex size-8 shrink-0 items-center justify-center border border-ink bg-sheet text-ink hover:bg-ink hover:text-paper"
          >
            {theme === 'dark' ? (
              <Sun aria-hidden size={15} strokeWidth={2.2} />
            ) : (
              <Moon aria-hidden size={15} strokeWidth={2.2} />
            )}
          </button>
        </div>

        <ul className="order-last flex w-full items-center gap-5 overflow-x-auto border-t border-line pt-2 md:hidden">
          {links.map((link) => (
            <li key={link.to} className="shrink-0">
              <NavLink to={link.to} className={navLinkClasses}>
                <link.icon aria-hidden size={13} strokeWidth={2.4} />
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
