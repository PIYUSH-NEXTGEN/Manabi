import { useSyncExternalStore } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  getConsent,
  isPostHogConfigured,
  setConsent,
  subscribeConsent,
} from '@/lib/analytics';

/**
 * Non-modal consent bar. It only appears when PostHog is configured and the
 * visitor has not decided yet; "No thanks" is as easy as allowing.
 */
export function ConsentBanner() {
  const consent = useSyncExternalStore(
    subscribeConsent,
    getConsent,
    () => null,
  );

  if (!isPostHogConfigured || consent !== null) return null;

  return (
    <section
      aria-label="Analytics choice"
      className="fixed bottom-[5.5rem] left-4 right-4 z-30 rounded-[1.25rem] border border-line bg-paper/95 p-4 shadow-lift backdrop-blur-xl md:bottom-5 md:right-auto md:max-w-[27rem]"
    >
      <p className="font-mono text-[0.5625rem] font-bold uppercase tracking-[0.18em] text-accent">
        Analytics
      </p>
      <p className="mt-2 text-body leading-relaxed text-ink">
        Can we measure which pages help and record short, text-masked sessions
        so we can fix what breaks? Nothing is sent unless you allow it.
      </p>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <Button size="small" onClick={() => setConsent('granted')}>
          Allow analytics
        </Button>
        <Button
          size="small"
          variant="secondary"
          onClick={() => setConsent('denied')}
        >
          No thanks
        </Button>
        <Link
          to="/privacy"
          className="press text-[0.8125rem] font-semibold text-accent underline underline-offset-4 hover:text-ink"
        >
          Details
        </Link>
      </div>
    </section>
  );
}
