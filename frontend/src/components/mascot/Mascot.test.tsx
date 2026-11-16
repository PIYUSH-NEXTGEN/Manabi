import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Mascot } from './Mascot';
import type { MascotState } from './types';

const STATES: MascotState[] = ['idle', 'working', 'thinking', 'celebrating'];

describe('Mascot', () => {
  it('defaults to idle and treats the artwork as decorative', () => {
    const { container } = render(<Mascot className="w-32" />);

    expect(
      container.querySelector('[data-mascot-state="idle"]'),
    ).not.toBeNull();
    expect(container.querySelector('img')).toHaveAttribute('alt', '');
  });

  it('exposes every supported state', () => {
    for (const state of STATES) {
      const { container, unmount } = render(<Mascot state={state} />);
      expect(
        container.querySelector(`[data-mascot-state="${state}"]`),
      ).not.toBeNull();
      unmount();
    }
  });

  it('is announced when given a label', () => {
    render(<Mascot label="MANABI mascot" />);

    expect(
      screen.getByRole('img', { name: 'MANABI mascot' }),
    ).toBeInTheDocument();
  });
});
