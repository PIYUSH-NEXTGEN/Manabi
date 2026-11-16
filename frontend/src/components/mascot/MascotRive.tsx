import { useEffect, useRef, useState } from 'react';
import {
  Alignment,
  Fit,
  Layout,
  useRive,
  useStateMachineInput,
} from '@rive-app/react-canvas';
import { useInView } from 'motion/react';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import { MASCOT_RIVE, MASCOT_RIVE_SRC } from './config';
import { MascotFallback } from './MascotFallback';
import type { MascotProps } from './types';

const LAYOUT = new Layout({ fit: Fit.Contain, alignment: Alignment.Center });

/**
 * Rive-backed mascot. Loaded lazily by `Mascot` only when a `.riv` URL is
 * configured, so the runtime stays out of the main bundle until then.
 *
 * Playback rules:
 * - nothing runs offscreen (IntersectionObserver via `useInView`);
 * - nothing runs for `prefers-reduced-motion: reduce`;
 * - no Rive listeners are attached because the mascot is decorative.
 */
export default function MascotRive({
  state = 'idle',
  className,
  label,
}: MascotProps) {
  const reduced = usePrefersReducedMotion();
  const containerRef = useRef<HTMLDivElement>(null);
  const inView = useInView(containerRef, { margin: '120px' });
  const [failed, setFailed] = useState(false);

  const { rive, RiveComponent } = useRive({
    src: MASCOT_RIVE_SRC,
    artboard: MASCOT_RIVE.artboard,
    stateMachine: MASCOT_RIVE.stateMachine,
    autoplay: false,
    layout: LAYOUT,
    shouldDisableRiveListeners: true,
    onLoadError: () => setFailed(true),
  });

  const stateInput = useStateMachineInput(
    rive,
    MASCOT_RIVE.stateMachine,
    MASCOT_RIVE.stateInput,
    MASCOT_RIVE.stateValues[state],
  );

  useEffect(() => {
    if (!stateInput) return;
    stateInput.value = MASCOT_RIVE.stateValues[state];
  }, [stateInput, state]);

  useEffect(() => {
    if (!rive) return;
    if (reduced || !inView) {
      rive.pause();
      return;
    }
    rive.play();
  }, [rive, reduced, inView]);

  if (failed) {
    return (
      <MascotFallback state={state} className={className} label={label} />
    );
  }

  return (
    <div
      ref={containerRef}
      className={cx(
        'aspect-[272/241] select-none',
        className,
      )}
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      data-mascot-state={state}
    >
      <RiveComponent className="block size-full" />
    </div>
  );
}
