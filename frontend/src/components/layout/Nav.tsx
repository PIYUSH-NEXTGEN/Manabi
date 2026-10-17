import { Link, useNavigate } from 'react-router-dom';
import { Button, useToast } from '@/design/primitives';
import { useLogout } from '@/hooks/useLogout';
import { useMe } from '@/hooks/useMe';

const NAV_LINKS = [
  { to: '/problems', label: 'Problems' },
  { to: '/ml', label: 'ML Practice' },
  { to: '/ingest', label: 'Ingest' },
  { to: '/how-it-works', label: 'How it works' },
];

export function Nav() {
  const me = useMe();
  const logoutMutation = useLogout();
  const navigate = useNavigate();
  const toast = useToast();

  function handleLogout() {
    logoutMutation.mutate(undefined, {
      onSuccess: () => {
        toast('Logged out. The board will still be here.');
        navigate('/');
      },
      onError: () => {
        toast('Log out failed — try again.', 'error');
      },
    });
  }

  return (
    <header className="sticky top-0 z-30 border-b-[3px] border-ink bg-paper">
      <nav
        aria-label="Main"
        className="mx-auto flex w-[min(1200px,96vw)] flex-wrap items-center justify-between gap-4 py-3"
      >
        <Link
          to="/"
          className="font-display text-2xl uppercase leading-none tracking-tight"
        >
          MANABI
        </Link>

        <ul className="hidden items-center gap-5 md:flex">
          {NAV_LINKS.map((link) => (
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
            <>
              <Link
                to="/me"
                className="flex items-center gap-2 border-[3px] border-ink bg-white px-3 py-1.5 shadow-hard-sm"
              >
                {me.data.avatar_url ? (
                  <img
                    src={me.data.avatar_url}
                    alt=""
                    className="size-5 border-[2px] border-ink"
                  />
                ) : null}
                <span className="font-mono text-[11px] font-bold uppercase tracking-widest">
                  {me.data.username}
                </span>
              </Link>
              <Button
                variant="secondary"
                onClick={handleLogout}
                disabled={logoutMutation.isPending}
              >
                {logoutMutation.isPending ? 'Logging out…' : 'Log out'}
              </Button>
            </>
          ) : (
            <Button
              variant="secondary"
              onClick={() => {
                window.location.assign('/api/auth/github/login');
              }}
            >
              Log in with GitHub
            </Button>
          )}
        </div>

        <ul className="order-last flex w-full items-center gap-4 overflow-x-auto pb-1 md:hidden">
          {NAV_LINKS.map((link) => (
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
