import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { Input } from './Input';

describe('Input', () => {
  it('associates the label with the field', () => {
    render(<Input label="Search problems" />);
    expect(screen.getByLabelText('Search problems')).toBeInTheDocument();
  });

  it('fires onChange while typing', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();
    render(<Input label="Search" onChange={onChange} />);

    await user.type(screen.getByLabelText('Search'), 'crop');

    expect(onChange).toHaveBeenCalled();
    expect(screen.getByLabelText('Search')).toHaveValue('crop');
  });

  it('shows an error message and marks the field invalid', () => {
    render(<Input label="Repo URL" error="Enter a valid repo URL" />);

    const field = screen.getByLabelText('Repo URL');
    expect(field).toHaveAttribute('aria-invalid', 'true');
    expect(screen.getByRole('alert')).toHaveTextContent('Enter a valid repo URL');
    expect(field).toHaveAttribute('aria-describedby', screen.getByRole('alert').id);
  });
});
