import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders its label and fires onClick', async () => {
    const onClick = vi.fn();
    const user = userEvent.setup();
    render(<Button onClick={onClick}>Browse problems</Button>);

    await user.click(screen.getByRole('button', { name: 'Browse problems' }));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('applies neo-brutalist surface classes per variant', () => {
    const { rerender } = render(<Button variant="primary">Go</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-yellow', 'text-ink', 'shadow-hard');

    rerender(<Button variant="secondary">Go</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-white', 'text-ink');

    rerender(<Button variant="danger">Go</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-red', 'text-white');

    rerender(<Button variant="link">Go</Button>);
    expect(screen.getByRole('button')).toHaveClass('text-blue', 'underline');
  });

  it('defaults to type=button so it never submits forms by accident', () => {
    render(<Button>Ok</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('type', 'button');
  });

  it('disables itself when disabled', () => {
    render(<Button disabled>Wait</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
