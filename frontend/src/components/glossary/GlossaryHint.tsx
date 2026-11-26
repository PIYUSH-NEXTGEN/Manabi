import { motion, useReducedMotion } from "motion/react";
import { cx } from "@/lib/cx";

/**
 * Quiet nudge on brief pages: glossary words are underlined with dots, and
 * clicking one opens its definition. Sits in the page's empty right column so
 * it reads as a suggestion, not a banner. The only motion is a slow blink on
 * the sample underline, and it stops entirely under reduced motion.
 */
export function GlossaryHint({ className }: { className?: string }) {
  const reducedMotion = useReducedMotion();

  return (
    <div
      className={cx(
        "rounded-card border border-dashed border-line bg-sheet/70 px-4 py-3",
        className,
      )}
    >
      <p className="font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-muted">
        Reading tip
      </p>
      <p className="mt-1.5 text-[0.82rem] leading-relaxed text-ink-soft">
        Words with{" "}
        <motion.span
          className="text-accent underline decoration-accent/50 decoration-dotted decoration-[1.5px] underline-offset-[3px]"
          animate={reducedMotion ? { opacity: 1 } : { opacity: [0.55, 1, 0.55] }}
          transition={
            reducedMotion
              ? { duration: 0 }
              : { duration: 3.2, repeat: Infinity, ease: "easeInOut" }
          }
        >
          a dotted underline
        </motion.span>{" "}
        are clickable. Tap one to see what it means.
      </p>
    </div>
  );
}
