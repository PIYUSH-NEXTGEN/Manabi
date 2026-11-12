import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { cx } from '@/lib/cx';

export type ToastTone = 'info' | 'error';

interface ToastItem {
  id: number;
  message: string;
  tone: ToastTone;
}

type PushToast = (message: string, tone?: ToastTone) => void;

const ToastContext = createContext<PushToast | null>(null);

export function useToast(): PushToast {
  const push = useContext(ToastContext);
  if (!push) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return push;
}

const TOAST_DISMISS_MS = 4000;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const nextId = useRef(1);

  const push = useCallback<PushToast>((message, tone = 'info') => {
    const id = nextId.current;
    nextId.current += 1;
    setToasts((prev) => [...prev, { id, message, tone }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, TOAST_DISMISS_MS);
  }, []);

  const value = useMemo(() => push, [push]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div
        aria-live="polite"
        className="pointer-events-none fixed inset-x-0 bottom-5 z-50 flex flex-col items-center gap-2 px-4"
      >
        {toasts.map((toast) => (
          <div
            key={toast.id}
            role="status"
            className={cx(
              'pointer-events-auto max-w-[min(520px,92vw)] rounded-full px-5 py-3 text-left text-[0.875rem] font-semibold leading-snug text-paper shadow-lift',
              toast.tone === 'error' ? 'bg-danger' : 'bg-ink',
            )}
          >
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
