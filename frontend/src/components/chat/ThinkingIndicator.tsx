import { motion } from 'motion/react';
import { Sparkles } from 'lucide-react';
import { EASE_SNAP } from '@/design/motion';

/** Assistant-side "typing" bubble shown while the reply is being generated. */
export function ThinkingIndicator() {
  return (
    <motion.li
      role="status"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24, ease: EASE_SNAP }}
      className="flex items-start gap-2.5"
    >
      <span className="mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-xl bg-ink text-paper">
        <Sparkles aria-hidden size={13} strokeWidth={2.1} />
      </span>
      <div className="rounded-2xl rounded-tl-md border border-line bg-sheet px-3.5 py-2.5 shadow-soft">
        <p className="sr-only">Manabi is typing a reply</p>
        <div aria-hidden="true" className="flex items-center gap-2">
          <span className="flex items-center gap-1">
            <span className="thinking-dot size-1.5 rounded-full bg-ink" />
            <span className="thinking-dot size-1.5 rounded-full bg-ink" />
            <span className="thinking-dot size-1.5 rounded-full bg-ink" />
          </span>
          <span className="font-mono text-[0.5625rem] font-bold uppercase tracking-[0.12em] text-muted">
            Manabi is thinking
          </span>
        </div>
      </div>
    </motion.li>
  );
}
