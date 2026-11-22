import { useRef } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { AnimatePresence, motion } from 'motion/react';
import { Moon, Sun } from 'lucide-react';
import { GithubMark } from '@/components/icons/GithubMark';
import { EASE_SNAP } from '@/design/motion';
import { loginUrl } from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { playRainWipe } from '@/lib/rainThemeWipe';
import { useTheme } from '@/lib/useTheme';
import { cx } from '@/lib/cx';

const NAV_LINKS = [
  { to: '/problems', label: 'Projects' },
  { to: '/me', label: 'Dashboard' },
];

const navLinkClasses = ({ isActive }: { isActive: boolean }) =>
  cx(
    'press inline-flex items-center whitespace-nowrap rounded-full px-4 py-2 text-[0.875rem] font-semibold tracking-[-0.01em] transition-colors',
    isActive
      ? 'bg-sky text-[#0a0b0d]'
      : 'text-ink-soft hover:bg-tint hover:text-ink',
  );

function ThemeIcon({ dark }: { dark: boolean }) {
  return dark ? (
    <Sun aria-hidden size={16} strokeWidth={2.2} />
  ) : (
    <Moon aria-hidden size={16} strokeWidth={2.2} />
  );
}

export function Nav({ overlay = false }: { overlay?: boolean }) {
  const me = useMe();
  const { theme, setTheme } = useTheme();
  const themeButtonRef = useRef<HTMLButtonElement>(null);
  const wiping = useRef(false);
  const themeLabel =
    theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';

  const switchTheme = () => {
    if (wiping.current) return;
    const next = theme === 'dark' ? 'light' : 'dark';
    const rect = themeButtonRef.current?.getBoundingClientRect();
    wiping.current = true;
    playRainWipe({
      to: next,
      origin: rect
        ? { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 }
        : undefined,
      onCommit: () => setTheme(next),
      onDone: () => {
        wiping.current = false;
      },
    });
  };

  return (
    <header
      className={cx(
        'z-30',
        overlay
          ? 'absolute inset-x-0 top-0 px-3 pt-[max(1rem,env(safe-area-inset-top))] sm:px-4 md:px-8 md:pt-6'
          : 'sticky top-0 px-3 pt-[max(0.75rem,env(safe-area-inset-top))] md:px-5 md:pt-4',
      )}
    >
      <nav
        aria-label="Main"
        className="relative mx-auto flex w-full max-w-[680px] items-center justify-between gap-2 rounded-full border border-ink/15 bg-paper/85 px-3 py-2 shadow-[0_18px_50px_-28px_rgba(10,11,13,0.35)] backdrop-blur-xl md:gap-3 md:px-4"
      >
        <div className="flex items-center gap-2 md:gap-4">
          <Link
            to="/"
            className="press flex w-fit items-center rounded-full py-1.5 pl-1 pr-2 transition-opacity hover:opacity-80"
          >
            <span className="font-brand text-[0.9375rem] uppercase leading-none tracking-[-0.01em] text-ink">
              MANABI
            </span>
          </Link>

          <ul className="hidden items-center gap-1 min-[500px]:flex">
            {NAV_LINKS.map((link) => (
              <li key={link.to}>
                <NavLink to={link.to} className={navLinkClasses}>
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>

        <div className="flex shrink-0 items-center justify-end gap-2">
          {me.data ? (
            <Link
              to="/me"
              className="press flex items-center gap-2 rounded-full border border-line bg-paper px-2 py-1.5 pr-3 transition-colors hover:border-ink/20"
            >
              {me.data.avatar_url ? (
                <img
                  src={me.data.avatar_url}
                  alt=""
                  className="size-6 rounded-full object-cover"
                />
              ) : (
                <span aria-hidden className="block size-6 rounded-full bg-sky" />
              )}
              <span className="max-w-[7.5rem] truncate text-[0.8125rem] font-semibold leading-none text-ink md:max-w-[10rem]">
                {me.data.username}
              </span>
            </Link>
          ) : (
            <button
              type="button"
              onClick={() => {
                window.location.assign(loginUrl());
              }}
              className="press inline-flex items-center gap-2 whitespace-nowrap rounded-full bg-ink px-3 py-2.5 text-[0.8125rem] font-semibold leading-none text-paper transition-colors hover:bg-ink/90 min-[360px]:px-4"
            >
              <GithubMark size={14} />
              GitHub login
            </button>
          )}

          <button
            ref={themeButtonRef}
            type="button"
            onClick={switchTheme}
            aria-label={themeLabel}
            title={themeLabel}
            className="press group relative grid size-10 shrink-0 place-items-center overflow-hidden rounded-full border border-line bg-paper text-ink transition-colors hover:bg-tint"
          >
            <AnimatePresence mode="wait" initial={false}>
              <motion.span
                key={theme}
                initial={{ rotate: -90, scale: 0.6, opacity: 0 }}
                animate={{ rotate: 0, scale: 1, opacity: 1 }}
                exit={{ rotate: 90, scale: 0.6, opacity: 0 }}
                transition={{ duration: 0.24, ease: EASE_SNAP }}
                className="grid place-items-center"
              >
                <ThemeIcon dark={theme === 'dark'} />
              </motion.span>
            </AnimatePresence>
          </button>
        </div>
      </nav>

      <nav
        aria-label="Mobile"
        className="mx-auto mt-2 w-fit rounded-full border border-ink/15 bg-paper/85 p-1 shadow-soft backdrop-blur-xl min-[500px]:hidden"
      >
        <ul className="flex items-center gap-1">
          {NAV_LINKS.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} className={navLinkClasses}>
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
