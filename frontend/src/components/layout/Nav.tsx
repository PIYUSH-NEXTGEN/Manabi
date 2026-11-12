import { NavLink, Link } from 'react-router-dom';
import { Moon, Sun } from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { Button } from '@/design/primitives';
import { Logo } from './Logo';
import { useMe } from '@/hooks/useMe';
import { useTheme } from '@/lib/useTheme';
import { cx } from '@/lib/cx';

const NAV_LINKS = [
  { to: '/problems', label: 'Projects' },
  { to: '/repo-analyzer', label: 'Repo Analyzer' },
  { to: '/me', label: 'Dashboard' },
];

const ADMIN_LINK = { to: '/admin/review', label: 'Review' };

const navLinkClasses = ({ isActive }: { isActive: boolean }) =>
  cx(
    'press inline-flex items-center whitespace-nowrap rounded-full px-3.5 py-2 text-[0.875rem] font-semibold tracking-[-0.01em] transition-colors',
    isActive ? 'bg-tint text-ink' : 'text-ink-soft hover:bg-tint/70 hover:text-ink',
  );

export function Nav({ overlay = false }: { overlay?: boolean }) {
  const me = useMe();
  const { theme, toggleTheme } = useTheme();
  const links = me.data?.is_admin ? [...NAV_LINKS, ADMIN_LINK] : NAV_LINKS;
  const themeLabel = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';

  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    overlay
      ? cx(
          'press inline-flex items-center whitespace-nowrap rounded-full px-2 py-2 text-[0.9375rem] font-medium tracking-[-0.01em] transition-colors',
          isActive ? 'text-white' : 'text-white/70 hover:text-white',
        )
      : navLinkClasses({ isActive });

  return (
    <header
      className={cx(
        'z-30',
        overlay
          ? 'absolute inset-x-0 top-0 px-5 pt-5 md:px-10 md:pt-7'
          : 'sticky top-0 px-3 pt-3 md:px-5 md:pt-4',
      )}
    >
      <nav
        aria-label="Main"
        className={cx(
          'mx-auto flex flex-wrap items-center justify-between gap-x-6 gap-y-3',
          overlay
            ? 'w-full max-w-[1400px] text-white md:grid md:grid-cols-[1fr_auto_1fr]'
            : 'w-[min(1240px,100%)] gap-x-5 rounded-pill border border-line bg-sheet/85 px-3 py-2.5 shadow-soft backdrop-blur-md md:px-4',
        )}
      >
        <Link
          to="/"
          className={cx(
            'group flex items-center gap-2.5 py-1 transition-opacity',
            overlay
              ? 'hover:opacity-80'
              : 'rounded-pill pl-2 pr-3 hover:bg-tint/60',
          )}
        >
          <Logo
            className={cx(
              'transition-colors',
              overlay ? 'text-white' : 'text-ink group-hover:text-accent',
            )}
          />
          <span
            className={cx(
              'font-brand text-[0.9375rem] uppercase leading-none tracking-[-0.01em]',
              overlay && 'text-white',
            )}
          >
            MANABI
          </span>
        </Link>

        <ul className={cx('hidden md:flex', overlay ? 'items-center gap-5' : 'items-center gap-1')}>
          {links.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} className={linkClasses}>
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className={cx('flex items-center gap-2', overlay && 'md:justify-self-end')}>
          {me.data ? (
            <Link
              to="/me"
              className={cx(
                'press flex items-center gap-2 rounded-pill border px-2 py-1.5 pr-3',
                overlay
                  ? 'border-white/35 hover:bg-white/10'
                  : 'border-line bg-sheet hover:border-ink/20',
              )}
            >
              {me.data.avatar_url ? (
                <img
                  src={me.data.avatar_url}
                  alt=""
                  className="size-6 rounded-full object-cover"
                />
              ) : (
                <span aria-hidden className="block size-6 rounded-full bg-tint" />
              )}
              <span className="text-[0.8125rem] font-semibold leading-none">
                {me.data.username}
              </span>
            </Link>
          ) : overlay ? (
            <button
              type="button"
              onClick={() => {
                window.location.assign('/api/auth/github/login');
              }}
              className="inline-flex items-center gap-2 rounded-full border border-white/40 px-4 py-2 text-[0.8125rem] font-semibold text-white transition-colors hover:border-white/70 hover:bg-white/10"
            >
              <GithubMark size={14} />
              GitHub
            </button>
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
            className={cx(
              'press flex size-9 shrink-0 items-center justify-center rounded-full border',
              overlay
                ? 'border-transparent text-white/80 hover:bg-white/10 hover:text-white'
                : 'border-line bg-sheet text-ink hover:bg-tint',
            )}
          >
            {theme === 'dark' ? (
              <Sun aria-hidden size={15} strokeWidth={2.2} />
            ) : (
              <Moon aria-hidden size={15} strokeWidth={2.2} />
            )}
          </button>
        </div>

        <ul
          className={cx(
            'order-last flex w-full flex-wrap items-center md:hidden',
            overlay
              ? 'justify-center gap-x-4 gap-y-1'
              : 'gap-1 rounded-pill bg-tint/50 p-1',
          )}
        >
          {links.map((link) => (
            <li key={link.to} className="shrink-0">
              <NavLink to={link.to} className={linkClasses}>
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
