import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ErrorBoundary } from './ErrorBoundary';

function Broken(): never {
  throw new Error('render exploded with internal detail');
}

describe('ErrorBoundary', () => {
  it('shows a safe fallback without leaking the error', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {});

    try {
      render(
        <ErrorBoundary>
          <Broken />
        </ErrorBoundary>,
      );
    } finally {
      consoleError.mockRestore();
    }

    expect(
      screen.getByRole('heading', { name: 'Something went wrong.' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: 'Reload the page' }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/internal detail/i)).not.toBeInTheDocument();
  });
});
