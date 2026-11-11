import { useEffect, useState } from 'react';

function format(seconds: number): string {
  if (seconds >= 3600) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${String(m).padStart(2, '0')}m`;
  }
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

/** Live "try again in MM:SS" clock, driven by a 429's Retry-After seconds. */
export function RetryCountdown({ seconds }: { seconds: number }) {
  const [left, setLeft] = useState(seconds);

  useEffect(() => {
    setLeft(seconds);
  }, [seconds]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setLeft((current) => Math.max(0, current - 1));
    }, 1000);
    return () => window.clearInterval(timer);
  }, []);

  if (left <= 0) {
    return <p className="text-sm font-bold">You can try again now.</p>;
  }

  return (
    <p className="text-sm leading-snug">
      Try again in{' '}
      <span className="font-bold tabular-nums">{format(left)}</span>
    </p>
  );
}
