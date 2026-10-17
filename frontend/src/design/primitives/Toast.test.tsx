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
    expect(status).toHaveClass('bg-yellow');
  });

  it('renders error toasts on a red slab', async () => {
    const user = userEvent.setup();
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>,
    );

    await user.click(screen.getByRole('button', { name: 'Break' }));

    expect(screen.getByRole('status')).toHaveClass('bg-red', 'text-white');
  });

  it('throws if useToast is used outside the provider', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => render(<ToastTrigger />)).toThrow(
      'useToast must be used within ToastProvider',
    );
    spy.mockRestore();
  });
});
