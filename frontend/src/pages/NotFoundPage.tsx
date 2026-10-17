import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';

export function NotFoundPage() {
  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto flex w-[min(760px,96vw)] flex-col gap-6 py-16">
        <h1
          aria-label="404 — page not found"
          className="font-display uppercase leading-none text-red"
          style={{ fontSize: 'clamp(5rem, 18vw, 12rem)' }}
        >
          <span aria-hidden>4</span>
          <span aria-hidden className="inline-block align-top text-ink">
            0
          </span>
          <span aria-hidden>4</span>
        </h1>
        <p className="text-lg">
          This page does not exist. The board, though, is very real.
        </p>
        <div className="flex flex-wrap gap-4">
          <Link to="/problems" className={buttonClasses('primary')}>
            Browse problems
          </Link>
          <Link to="/" className={buttonClasses('secondary')}>
            Back home
          </Link>
        </div>
      </div>
    </main>
  );
}
