import { buttonClasses } from '@/design/primitives';
import { openChatWidget } from '@/components/chat/ChatWidget';

export function AskManabi() {
  return (
    <section className="border-b border-ink">
      <div className="mx-auto w-[min(1240px,96vw)] py-14">
        <div className="flex flex-col gap-5 border-y border-ink py-6 md:flex-row md:items-center md:justify-between">
          <div className="flex gap-4">
            <span className="mt-1 font-mono text-[9px] font-bold tracking-[0.16em] text-accent">
              04
            </span>
            <div>
              <h2 className="font-display text-2xl uppercase leading-none tracking-tight md:text-3xl">
                Ask MANABI
              </h2>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-ink-soft">
                Tell it what you know and what you want to build. It finds
                problems that fit, scoped for a weekend, and never invents one.
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={openChatWidget}
            className={buttonClasses('secondary', 'shrink-0')}
          >
            Open the chat
          </button>
        </div>
      </div>
    </section>
  );
}
