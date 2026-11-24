import type { ReactNode } from "react";
import {
  useCallback,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import { createPortal } from "react-dom";
import { cx } from "@/lib/cx";
import type { GlossaryEntry } from "@/lib/glossary";

interface GlossaryTermProps {
  entry: GlossaryEntry;
  children: ReactNode;
}

interface Position {
  top: number;
  left: number;
  width: number;
}

const POPOVER_WIDTH = 300;
const POPOVER_ESTIMATED_HEIGHT = 132;
const EDGE = 12;

export function GlossaryTerm({ entry, children }: GlossaryTermProps) {
  const [open, setOpen] = useState(false);
  const [position, setPosition] = useState<Position | null>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const popoverRef = useRef<HTMLDivElement>(null);
  const closeTimerRef = useRef<number | null>(null);
  const pinnedRef = useRef(false);
  const popoverId = useId();

  const clearClose = useCallback(() => {
    if (closeTimerRef.current !== null) {
      window.clearTimeout(closeTimerRef.current);
      closeTimerRef.current = null;
    }
  }, []);

  const place = useCallback(() => {
    const trigger = triggerRef.current;
    if (!trigger) return;

    const rect = trigger.getBoundingClientRect();
    const popover = popoverRef.current;
    const width = Math.min(
      popover?.offsetWidth || POPOVER_WIDTH,
      window.innerWidth - EDGE * 2,
    );
    const height = popover?.offsetHeight || POPOVER_ESTIMATED_HEIGHT;
    const left = Math.min(
      Math.max(EDGE, rect.left + rect.width / 2 - width / 2),
      window.innerWidth - width - EDGE,
    );
    const below = rect.bottom + 10;
    const above = rect.top - height - 10;
    const fitsBelow = below + height <= window.innerHeight - EDGE;
    const fitsAbove = above >= EDGE;
    const top = !fitsBelow && fitsAbove ? above : below;

    setPosition({ top, left, width });
  }, []);

  const close = useCallback(() => {
    clearClose();
    pinnedRef.current = false;
    setOpen(false);
  }, [clearClose]);

  const scheduleClose = useCallback(() => {
    if (pinnedRef.current) return;
    clearClose();
    closeTimerRef.current = window.setTimeout(() => {
      closeTimerRef.current = null;
      setOpen(false);
    }, 140);
  }, [clearClose]);

  const openNow = useCallback(() => {
    clearClose();
    if (!open) {
      place();
      setOpen(true);
    }
  }, [clearClose, open, place]);

  const togglePinned = useCallback(() => {
    clearClose();
    if (pinnedRef.current) {
      close();
      return;
    }
    pinnedRef.current = true;
    place();
    setOpen(true);
  }, [clearClose, close, place]);

  useEffect(() => {
    if (!open) return;

    const onPointerDown = (event: PointerEvent) => {
      const target = event.target as Node | null;
      if (
        triggerRef.current?.contains(target) ||
        popoverRef.current?.contains(target)
      ) {
        return;
      }
      close();
    };

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      close();
      triggerRef.current?.focus();
    };

    const onScroll = () => close();
    const onResize = () => place();

    document.addEventListener("pointerdown", onPointerDown, true);
    document.addEventListener("keydown", onKeyDown);
    window.addEventListener("scroll", onScroll, true);
    window.addEventListener("resize", onResize);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown, true);
      document.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("scroll", onScroll, true);
      window.removeEventListener("resize", onResize);
    };
  }, [close, open, place]);

  useLayoutEffect(() => {
    if (!open) return;
    place();
    const frame = window.requestAnimationFrame(place);
    return () => window.cancelAnimationFrame(frame);
  }, [open, place]);

  useEffect(() => clearClose, [clearClose]);

  return (
    <>
      <button
        ref={triggerRef}
        type="button"
        aria-describedby={open ? popoverId : undefined}
        aria-expanded={open}
        onClick={togglePinned}
        onMouseEnter={openNow}
        onMouseLeave={scheduleClose}
        onFocus={openNow}
        onBlur={scheduleClose}
        className={cx(
          "inline cursor-help rounded-[2px] border-0 bg-transparent p-0 align-baseline text-inherit [font:inherit] leading-[inherit] underline decoration-accent/40 decoration-dotted decoration-[1.5px] underline-offset-[3px] transition-colors hover:text-accent hover:decoration-accent focus-visible:text-accent",
          open && "text-accent decoration-accent",
        )}
      >
        {children}
      </button>
      {open
        ? createPortal(
            <div
              ref={popoverRef}
              id={popoverId}
              role="tooltip"
              onMouseEnter={clearClose}
              onMouseLeave={scheduleClose}
              style={
                position
                  ? {
                      top: position.top,
                      left: position.left,
                      width: position.width,
                    }
                  : { top: -9999, left: -9999, width: POPOVER_WIDTH }
              }
              className="fixed z-[70] rounded-panel border border-line bg-sheet px-4 py-3 shadow-lift"
            >
              <p className="font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-accent">
                {entry.category}
              </p>
              <p className="mt-1 font-display text-[0.95rem] leading-snug text-ink">
                {entry.term}
              </p>
              <p className="mt-1.5 text-[0.82rem] leading-relaxed text-ink-soft">
                {entry.definition}
              </p>
            </div>,
            document.body,
          )
        : null}
    </>
  );
}
