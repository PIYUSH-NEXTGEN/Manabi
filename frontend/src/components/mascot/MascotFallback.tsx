import {
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { animate } from 'animejs';
import { useInView } from 'motion/react';
import baseSrc from '@/assets/mascot/base.png';
import eyeLeftSrc from '@/assets/mascot/eye-left.png';
import eyeRightSrc from '@/assets/mascot/eye-right.png';
import handSrc from '@/assets/mascot/hand.png';
import { cx } from '@/lib/cx';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';
import type { MascotProps } from './types';

// Eye centres inside the 272x241 canvas, used as per-layer transform origins
// so blinks squash in place instead of sliding with the canvas centre.
const LEFT_EYE_ORIGIN = '57.5% 40.9%';
const RIGHT_EYE_ORIGIN = '66.7% 42.7%';

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

/**
 * Static-artwork fallback used until the Rive file is available (and whenever
 * that file fails to load). The artwork is transparent, so it picks up the
 * page background in both themes.
 *
 * The character is split into base, eye and hand layers. The body stays
 * completely still. anime.js keeps the eyes and hand busy on their own:
 * glances, blinks, squints, double-blinks, wide-eyed looks and the occasional
 * hand stretch. When the cursor comes close the eyes track it and open up; on
 * hover they open wider and the hand lifts, and tapping makes the character
 * flinch and the hand bounce.
 */
export function MascotFallback({
  state = 'idle',
  className,
  label,
}: MascotProps) {
  const reduced = usePrefersReducedMotion();
  const containerRef = useRef<HTMLDivElement>(null);
  const eyeGroupRef = useRef<HTMLDivElement>(null);
  const leftEyeRef = useRef<HTMLImageElement>(null);
  const rightEyeRef = useRef<HTMLImageElement>(null);
  const handRef = useRef<HTMLImageElement>(null);
  const pointerRef = useRef<{ x: number; y: number } | null>(null);
  const inView = useInView(containerRef, { margin: '120px' });
  const [hovered, setHovered] = useState(false);
  const [near, setNear] = useState(false);
  const [pressing, setPressing] = useState(false);

  const active = inView && !reduced;

  const applyGaze = (clientX: number, clientY: number) => {
    const container = containerRef.current;
    const group = eyeGroupRef.current;
    if (!container || !group) return;

    const rect = container.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;

    const dx = (clientX - rect.left) / rect.width - 0.5;
    const dy = (clientY - rect.top) / rect.height - 0.5;

    // Mirror the X axis: the mascot itself is flipped with `-scale-x-100`.
    group.style.transition = 'transform 120ms ease-out';
    group.style.transform = `translate(${clamp(-dx * 6, -2.5, 2.5)}px, ${clamp(dy * 4, -2, 2)}px)`;
  };

  useEffect(() => {
    if (!active) return;

    const track = (event: PointerEvent) => {
      if (event.pointerType !== 'mouse') return;

      const container = containerRef.current;
      if (!container) return;

      const rect = container.getBoundingClientRect();
      const pad = Math.max(96, rect.width);
      const isNear =
        event.clientX >= rect.left - pad &&
        event.clientX <= rect.right + pad &&
        event.clientY >= rect.top - pad &&
        event.clientY <= rect.bottom + pad;

      pointerRef.current = { x: event.clientX, y: event.clientY };
      setNear((previous) => (previous === isNear ? previous : isNear));
      if (isNear) applyGaze(event.clientX, event.clientY);
    };

    const leave = () => setNear(false);

    window.addEventListener('pointermove', track, { passive: true });
    window.addEventListener('pointerleave', leave);
    window.addEventListener('blur', leave);

    return () => {
      window.removeEventListener('pointermove', track);
      window.removeEventListener('pointerleave', leave);
      window.removeEventListener('blur', leave);
    };
  }, [active]);

  useEffect(() => {
    if (!active) return;

    const eyeGroup = eyeGroupRef.current;
    const leftEye = leftEyeRef.current;
    const rightEye = rightEyeRef.current;
    const hand = handRef.current;
    if (!eyeGroup || !leftEye || !rightEye || !hand) return;

    const eyes = [leftEye, rightEye];

    if (pressing) {
      const poke = animate(eyes, {
        keyframes: [
          { scaleY: 1, duration: 0 },
          { scaleY: 0.28, duration: 90 },
          { scaleY: 0.55, duration: 70 },
          { scaleY: 0.18, duration: 80 },
          { scaleY: 1.12, duration: 140 },
          { scaleY: 1, duration: 160 },
        ],
        ease: 'inOutQuad',
        onComplete: () => setPressing(false),
      });
      const handPoke = animate(hand, {
        keyframes: [
          { translateY: 0, duration: 0 },
          { translateY: -4, duration: 100 },
          { translateY: 0, duration: 120 },
          { translateY: -3, duration: 90 },
          { translateY: 0, duration: 130 },
        ],
        ease: 'inOutQuad',
      });

      return () => {
        poke.revert();
        handPoke.revert();
      };
    }

    const pointer = pointerRef.current;

    if (hovered || near) {
      const open = animate(eyes, {
        scaleY: hovered ? 1.14 : 1.08,
        duration: 220,
        ease: 'outQuad',
      });
      const handLift = animate(hand, {
        translateY: hovered ? -2.5 : -1.2,
        duration: 220,
        ease: 'outQuad',
      });
      if (pointer) applyGaze(pointer.x, pointer.y);

      return () => {
        open.revert();
        handLift.revert();
        eyeGroup.style.transition = '';
        eyeGroup.style.transform = '';
      };
    }

    const look = animate(eyeGroup, {
      keyframes: [
        { translateX: 0, translateY: 0, duration: 0 },
        { translateX: -1, translateY: 0.5, duration: 700 },
        { translateX: 0, translateY: 0, duration: 800 },
        { translateX: 1, translateY: 0.2, duration: 750 },
        { translateX: 0.2, translateY: -0.8, duration: 600 },
        { translateX: 0, translateY: 0, duration: 800 },
      ],
      loop: true,
      loopDelay: 2200,
      ease: 'inOutQuad',
    });

    // One eyelid animation carries a varied cycle: blink, squint, double blink,
    // then a wide-eyed look, so the face never repeats the same beat.
    const blink = animate(eyes, {
      keyframes: [
        { scaleY: 1, duration: 0 },
        { scaleY: 0.08, duration: 80 },
        { scaleY: 1, duration: 120 },
        { scaleY: 1, duration: 1700 },
        { scaleY: 0.45, duration: 170 },
        { scaleY: 0.45, duration: 180 },
        { scaleY: 1, duration: 200 },
        { scaleY: 1, duration: 1600 },
        { scaleY: 0.1, duration: 80 },
        { scaleY: 1, duration: 110 },
        { scaleY: 0.12, duration: 70 },
        { scaleY: 1, duration: 130 },
        { scaleY: 1, duration: 2100 },
        { scaleY: 1.14, duration: 240 },
        { scaleY: 1.14, duration: 260 },
        { scaleY: 1, duration: 260 },
        { scaleY: 1, duration: 1900 },
      ],
      loop: true,
      loopDelay: 1000,
      delay: 1600,
      ease: 'inOutQuad',
    });

    const typing =
      state === 'working'
        ? animate(hand, {
            keyframes: [
              { translateY: 0, duration: 0 },
              { translateY: -3, duration: 110 },
              { translateY: 0, duration: 130 },
              { translateY: -2, duration: 90 },
              { translateY: 0, duration: 150 },
              { translateY: 0, duration: 1400 },
              { translateY: -7, duration: 320 },
              { translateY: -7, duration: 220 },
              { translateY: 0, duration: 300 },
              { translateY: 0, duration: 1600 },
            ],
            loop: true,
            loopDelay: 400,
            ease: 'inOutQuad',
          })
        : animate(hand, {
            keyframes: [
              { translateY: 0, duration: 0 },
              { translateY: 0, duration: 2600 },
              { translateY: -5, duration: 340 },
              { translateY: -5, duration: 260 },
              { translateY: -3, duration: 200 },
              { translateY: -5, duration: 200 },
              { translateY: 0, duration: 360 },
              { translateY: 0, duration: 2400 },
            ],
            loop: true,
            loopDelay: 800,
            ease: 'inOutQuad',
          });

    return () => {
      look.revert();
      blink.revert();
      typing.revert();
    };
  }, [active, hovered, near, pressing, state]);

  const handlePointerEnter = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (!active || event.pointerType !== 'mouse') return;

    pointerRef.current = { x: event.clientX, y: event.clientY };
    setHovered(true);
  };

  const handlePointerLeave = () => {
    if (!hovered) return;
    setHovered(false);
  };

  const handlePointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (!active) return;

    if (event.pointerType !== 'mouse') {
      pointerRef.current = null;
      setHovered(false);
      setNear(false);
    }
    setPressing(true);
  };

  return (
    <div
      ref={containerRef}
      className={cx('cursor-pointer select-none', className)}
      data-mascot-state={state}
      onPointerEnter={handlePointerEnter}
      onPointerLeave={handlePointerLeave}
      onPointerDown={handlePointerDown}
    >
      <div className="relative">
        <img
          src={baseSrc}
          alt={label ?? ''}
          loading="lazy"
          decoding="async"
          draggable={false}
          className="block h-auto w-full"
        />
        <div
          ref={eyeGroupRef}
          aria-hidden
          className="pointer-events-none absolute inset-0 will-change-transform"
        >
          <img
            ref={leftEyeRef}
            src={eyeLeftSrc}
            alt=""
            loading="lazy"
            decoding="async"
            draggable={false}
            style={{ transformOrigin: LEFT_EYE_ORIGIN }}
            className="absolute inset-0 block size-full"
          />
          <img
            ref={rightEyeRef}
            src={eyeRightSrc}
            alt=""
            loading="lazy"
            decoding="async"
            draggable={false}
            style={{ transformOrigin: RIGHT_EYE_ORIGIN }}
            className="absolute inset-0 block size-full"
          />
        </div>
        <img
          ref={handRef}
          src={handSrc}
          alt=""
          loading="lazy"
          decoding="async"
          draggable={false}
          className="pointer-events-none absolute inset-0 block size-full will-change-transform"
        />
      </div>
    </div>
  );
}
