import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';

export function FinalCta() {
  return (
    <section className="border-b-[3px] border-ink bg-yellow">
      <div className="mx-auto flex w-[min(1200px,96vw)] flex-col items-start gap-6 py-14">
        <h2
          className="font-display uppercase leading-[0.9] tracking-tight"
          style={{ fontSize: 'clamp(2rem, 6vw, 4.5rem)' }}
        >
          Find it. Build it.
          <br />
          Ship it in public.
        </h2>
        <Link to="/problems" className={buttonClasses('secondary')}>
          Browse problems →
        </Link>
      </div>
    </section>
  );
}
