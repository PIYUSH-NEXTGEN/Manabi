import { useEffect } from 'react';

const LINE_HEIGHT = 16;
const PAGE_FRACTION = 0.9;
const SMOOTHING_MS = 110;

function scrollableAncestor(target: EventTarget | null, deltaY: number): boolean {
  let element = target instanceof Element ? target : null;

  while (
    element &&
    element !== document.body &&
    element !== document.documentElement
  ) {
    const { overflowY } = window.getComputedStyle(element);
    if (
      overflowY === 'auto' ||
      overflowY === 'scroll' ||
      overflowY === 'overlay'
    ) {
      const max = element.scrollHeight - element.clientHeight;
      if (max > 1) {
        if (deltaY < 0 && element.scrollTop > 0) return true;
        if (deltaY > 0 && element.scrollTop < max - 1) return true;
      }
    }
    element = element.parentElement;
  }

  return false;
}

/**
 * Eases mouse-wheel scrolling without taking over nested panes, touch input,
 * keyboard scrolling, or scrollbar dragging. Disabled for reduced motion.
 */
export function useSmoothScroll(): void {
  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (typeof window.matchMedia !== 'function') return;

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    if (reduced.matches || !finePointer.matches) return;

    let target = window.scrollY;
    let current = target;
    let lastApplied = target;
    let frame = 0;
    let lastTime = 0;

    const maxScroll = () =>
      Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

    const halt = () => {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      lastTime = 0;
    };

    const tick = (now: number) => {
      frame = 0;
      if (!lastTime) lastTime = now;
      const dt = Math.min(64, now - lastTime);
      lastTime = now;

      target = Math.max(0, Math.min(target, maxScroll()));
      const distance = target - current;

      if (Math.abs(distance) < 0.5) {
        current = target;
        if (Math.abs(window.scrollY - current) > 0.5) {
          lastApplied = current;
          window.scrollTo({ top: current, behavior: 'instant' });
        }
        lastTime = 0;
        return;
      }

      current += distance * (1 - Math.exp(-dt / SMOOTHING_MS));
      lastApplied = Math.round(current);
      window.scrollTo({ top: lastApplied, behavior: 'instant' });
      frame = requestAnimationFrame(tick);
    };

    const start = () => {
      if (frame) return;
      lastTime = 0;
      frame = requestAnimationFrame(tick);
    };

    const onWheel = (event: WheelEvent) => {
      if (event.defaultPrevented || event.ctrlKey) return;
      if (Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
      if (scrollableAncestor(event.target, event.deltaY)) {
        halt();
        return;
      }

      let delta = event.deltaY;
      if (event.deltaMode === WheelEvent.DOM_DELTA_LINE) delta *= LINE_HEIGHT;
      else if (event.deltaMode === WheelEvent.DOM_DELTA_PAGE) {
        delta *= window.innerHeight * PAGE_FRACTION;
      }

      const max = maxScroll();
      if (!delta || max <= 0) return;

      if (Math.abs(window.scrollY - lastApplied) > 1.5) {
        current = window.scrollY;
        target = window.scrollY;
      }

      target = Math.max(0, Math.min(target + delta, max));
      event.preventDefault();
      start();
    };

    const onScroll = () => {
      if (Math.abs(window.scrollY - lastApplied) <= 1.5) return;
      halt();
      target = window.scrollY;
      current = window.scrollY;
      lastApplied = window.scrollY;
    };

    const onResize = () => {
      const max = maxScroll();
      target = Math.min(target, max);
      current = Math.min(current, max);
      lastApplied = window.scrollY;
    };

    window.addEventListener('wheel', onWheel, { passive: false });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);

    return () => {
      halt();
      window.removeEventListener('wheel', onWheel);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
    };
  }, []);
}
