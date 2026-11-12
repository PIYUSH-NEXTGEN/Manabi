import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Skeleton } from './Skeleton';

describe('Skeleton', () => {
  it('renders the soft skeleton hidden from assistive tech', () => {
    const { container } = render(<Skeleton className="h-16" />);

    const block = container.firstElementChild;
    expect(block).toHaveClass('skeleton', 'h-16');
    expect(block).toHaveAttribute('aria-hidden');
  });
});
