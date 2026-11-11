import { act, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { RetryCountdown } from './RetryCountdown';

describe('RetryCountdown', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('ticks down every second', () => {
    render(<RetryCountdown seconds={90} />);
    expect(screen.getByText(/Try again in/)).toHaveTextContent('Try again in 1:30');

    act(() => {
      vi.advanceTimersByTime(1_000);
    });
    expect(screen.getByText(/Try again in/)).toHaveTextContent('Try again in 1:29');

    act(() => {
      vi.advanceTimersByTime(89_000);
    });
    expect(screen.getByText('You can try again now.')).toBeInTheDocument();
  });

  it('formats waits over an hour as hours and minutes', () => {
    render(<RetryCountdown seconds={5_400} />);
    expect(screen.getByText(/Try again in/)).toHaveTextContent('Try again in 1h 30m');
  });
});
