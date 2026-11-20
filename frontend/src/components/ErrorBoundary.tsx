import { Component, type ErrorInfo, type ReactNode } from 'react';
import { reportClientError } from '@/lib/errorReporting';

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

/**
 * Last-resort UI boundary. A render error must not leave a blank page, and the
 * fallback must not expose the stack trace or component internals to users.
 */
export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // Browser logs stay available for support; users only see the fallback.
    // In production the same error is sent to the backend so it is visible
    // after the tab is closed.
    console.error('Unhandled UI error', error, info.componentStack);
    reportClientError('react_error_boundary', error, {
      component_stack: info.componentStack ?? undefined,
    });
  }

  render(): ReactNode {
    if (!this.state.hasError) return this.props.children;

    return (
      <main className="flex min-h-screen items-center justify-center bg-paper px-5 py-16 text-ink">
        <div className="w-full max-w-[560px] border-y border-line py-10">
          <p className="font-mono text-label font-bold uppercase tracking-widest text-muted">
            Unexpected error
          </p>
          <h1 className="mt-3 font-display text-display leading-tight">
            Something went wrong.
          </h1>
          <p className="mt-4 text-body leading-relaxed text-ink-soft">
            The page could not finish loading. Reload to try again. If it keeps
            happening, tell us what you were doing so we can fix it.
          </p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-6 inline-flex rounded-full bg-ink px-4 py-2.5 text-[0.875rem] font-semibold text-paper transition-colors hover:bg-ink/90"
          >
            Reload the page
          </button>
        </div>
      </main>
    );
  }
}
