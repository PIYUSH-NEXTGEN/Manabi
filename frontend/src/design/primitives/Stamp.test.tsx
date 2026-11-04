import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Stamp } from './Stamp';

describe('Stamp', () => {
  it('renders the tone label uppercase with a space', () => {
    render(<Stamp tone="not-started" />);
    expect(screen.getByText('NOT STARTED')).toBeInTheDocument();
  });

  it('uses danger for closed and olive for AI-suggested', () => {
    const { rerender } = render(<Stamp tone="closed" />);
    expect(screen.getByText('CLOSED')).toHaveClass('bg-danger', 'text-paper');

    rerender(<Stamp tone="ai-suggested" />);
    expect(screen.getByText('AI-SUGGESTED')).toHaveClass('bg-olive', 'text-paper');
  });

  it('uses olive for active and accent for stale progress states', () => {
    const { rerender } = render(<Stamp tone="active" />);
    expect(screen.getByText('ACTIVE')).toHaveClass('bg-olive');

    rerender(<Stamp tone="stale" />);
    expect(screen.getByText('STALE')).toHaveClass('bg-accent');
  });

  it('accepts a custom label and rotation', () => {
    render(<Stamp tone="new" label="just landed" rotate={2} />);
    const stamp = screen.getByText('JUST LANDED');
    expect(stamp).toHaveStyle({ transform: 'rotate(2deg)' });
  });
});
