import { act, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { SubmittingCard } from './SubmittingCard';

describe('SubmittingCard', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  function renderCard() {
    return render(<SubmittingCard />);
  }

  it('announces the running check for screen readers', () => {
    renderCard();
    const status = screen.getByRole('status');
    expect(status.textContent).toContain('Reading the repository from GitHub');
    expect(status.textContent).toContain('step 1 of 4');
  });

  it('renders the full check ledger', () => {
    renderCard();
    expect(screen.getByText('Submission in progress')).toBeInTheDocument();
    expect(screen.getByText('Confirming you own the repository')).toBeInTheDocument();
    expect(screen.getByText('Scoring relevance with the AI check')).toBeInTheDocument();
    expect(screen.getByText('Recording your submission')).toBeInTheDocument();
  });

  it('advances to the AI check stage after a few seconds', () => {
    renderCard();
    act(() => {
      vi.advanceTimersByTime(6_000);
    });
    expect(screen.getByRole('status').textContent).toContain(
      'Scoring relevance with the AI check',
    );
  });
});
