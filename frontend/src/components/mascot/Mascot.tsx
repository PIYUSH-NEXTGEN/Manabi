import { Suspense, lazy } from 'react';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { MASCOT_RIVE_SRC } from './config';
import { MascotFallback } from './MascotFallback';
import type { MascotProps } from './types';

const MascotRive = lazy(() => import('./MascotRive'));

/**
 * Public mascot entry point.
 *
 * `<Mascot state="working" />` renders the Rive animation when a `.riv` asset
 * is configured, and otherwise renders the PNG fallback with the same state
 * animation. Sizing comes from `className`; the default state is `idle`.
 */
export function Mascot(props: MascotProps) {
  const reduced = usePrefersReducedMotion();

  if (!MASCOT_RIVE_SRC || reduced) {
    return <MascotFallback {...props} />;
  }

  return (
    <Suspense fallback={<MascotFallback {...props} />}>
      <MascotRive {...props} />
    </Suspense>
  );
}
