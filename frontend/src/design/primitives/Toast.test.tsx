import { Component, type ReactNode } from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { ToastProvider, useToast } from './Toast';

function ToastTrigger() {
  const push = useToast();
  return (
    <>
      <button type="button" onClick={() => push('Saved to the board')}>
        Save
      </button>
      <button type="button" onClick={() => push('Something broke', 'error')}>
        Break
      </button>
    </>
  );
}

describe('Toast', () => {
  it('renders an info toast in the bottom slab', async () => {
    const user = userEvent.setup();
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>,
    );

    await user.click(screen.getByRole('button', { name: 'Save' }));

    const status = screen.getByRole('status');
    expect(status).toHaveTextContent('Saved to the board');
    expect(status).toHaveClass('bg-accent', 'text-paper');
  });

  it('renders error toasts on a red slab', async () => {
    const user = userEvent.setup();
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>,
    );

    await user.click(screen.getByRole('button', { name: 'Break' }));

    expect(screen.getByRole('status')).toHaveClass('bg-danger', 'text-paper');
  });

  it('throws if useToast is used outside the provider', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    // The hook throws during render. Catching it with an error boundary
    // keeps the throw inside React — a bare expect(() => render(...))
    // rethrows through React's guarded callback, and jsdom then reports it
    // as an uncaught error that fails whichever test is running when it
    // surfaces (a cross-file flake in full-suite runs).
    // A holder object instead of a plain `let`: TypeScript's control flow
    // cannot see the assignment inside getDerivedStateFromError and would
    // otherwise narrow the variable to `null`.
    const captured = { error: null as Error | null };
    class CaptureBoundary extends Component<
      { children: ReactNode },
      { error: Error | null }
    > {
      state = { error: null };
      static getDerivedStateFromError(error: Error) {
        captured.error = error;
        return { error };
      }
      render() {
        return this.state.error ? null : this.props.children;
      }
    }
    render(
      <CaptureBoundary>
        <ToastTrigger />
      </CaptureBoundary>,
    );
    spy.mockRestore();
    expect(captured.error?.message).toBe(
      'useToast must be used within ToastProvider',
    );
  });
});
