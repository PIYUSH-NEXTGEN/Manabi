import { useEffect, useRef, useState } from 'react';
import { useInView } from 'motion/react';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

const COUNT_DURATION_MS = 700;

export function CountUp({ value }: { value: number }) {
  const reduced = usePrefersReducedMotion();
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, amount: 0.5 });
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!inView) {
      return;
    }
    if (reduced) {
      setDisplay(value);
      return;
    }

    let frame = 0;
    const start = performance.now();

    const tick = (now: number) => {
      const progress = Math.min(1, (now - start) / COUNT_DURATION_MS);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(value * eased));
      if (progress < 1) {
        frame = requestAnimationFrame(tick);
      }
    };

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [inView, reduced, value]);

  return <span ref={ref}>{display}</span>;
}
