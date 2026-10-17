import { buttonClasses } from '@/design/primitives';
import { openChatWidget } from '@/components/chat/ChatWidget';

export function AskManabi() {
  return (
    <section className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1200px,96vw)] py-12">
        <div className="flex flex-col gap-4 border-[3px] border-ink bg-white p-6 shadow-hard md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="font-display text-2xl uppercase leading-none md:text-3xl">
              Ask MANABI
            </h2>
            <p className="mt-2 max-w-xl text-sm leading-snug">
              Tell it what you know and what you want to build. It finds
              problems that fit, scoped for a weekend, and never invents one.
            </p>
          </div>
          <button
            type="button"
            onClick={openChatWidget}
            className={buttonClasses('primary')}
          >
            Open the chat
          </button>
        </div>
      </div>
    </section>
  );
}
