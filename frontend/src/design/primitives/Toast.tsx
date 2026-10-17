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
      <div aria-live="polite" className="fixed inset-x-0 bottom-0 z-50 flex flex-col">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            role="status"
            className={cx(
              'border-t-[3px] border-ink px-4 py-3 font-mono text-xs font-bold uppercase tracking-widest',
              toast.tone === 'error' ? 'bg-red text-white' : 'bg-yellow text-ink',
            )}
          >
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
