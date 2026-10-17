import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Skeleton } from './Skeleton';

describe('Skeleton', () => {
  it('renders the diagonal-stripe skeleton hidden from assistive tech', () => {
    const { container } = render(<Skeleton className="h-16" />);

    const stripe = container.firstElementChild;
    expect(stripe).toHaveClass('skeleton', 'h-16', 'border-ink');
    expect(stripe).toHaveAttribute('aria-hidden');
  });
});
