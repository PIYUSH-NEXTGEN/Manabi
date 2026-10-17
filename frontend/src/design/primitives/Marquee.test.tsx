import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Marquee } from './Marquee';

function stubMatchMedia(reduced: boolean) {
  window.matchMedia = (query: string): MediaQueryList =>
    ({
      matches: query.includes('prefers-reduced-motion') ? reduced : false,
      media: query,
      onchange: null,
      addEventListener: () => {},
      removeEventListener: () => {},
      addListener: () => {},
      removeListener: () => {},
      dispatchEvent: () => false,
    }) as MediaQueryList;
}

describe('Marquee', () => {
  it('renders items once visibly and once aria-hidden for the loop', () => {
    stubMatchMedia(false);
    render(<Marquee items={['Source one', 'Source two']} label="Sources" />);

    expect(screen.getByLabelText('Sources')).toBeInTheDocument();
    const matches = screen.getAllByText('Source one');
    expect(matches).toHaveLength(2);
    expect(matches[0].closest('ul')).not.toHaveAttribute('aria-hidden');
    expect(matches[1].closest('ul')).toHaveAttribute('aria-hidden');
  });

  it('renders nothing when there are no items', () => {
    stubMatchMedia(false);
    const { container } = render(<Marquee items={[]} />);
    expect(container.firstElementChild).toBeNull();
  });

  it('disables the animation under prefers-reduced-motion', () => {
    stubMatchMedia(true);
    render(<Marquee items={['Source one']} />);

    const track = document.querySelector('.marquee-track');
    expect(track).not.toBeNull();
    expect(track).toHaveStyle({ animation: 'none' });
  });
});
