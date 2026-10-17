import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { IndexCard } from './IndexCard';

describe('IndexCard', () => {
  it('renders the mono header with source ID and field', () => {
    render(
      <IndexCard
        sourceId="SIH26017"
        field="computer-vision"
        title="Crop disease triage"
        difficulty="beginner"
      />,
    );

    expect(screen.getByText('SIH26017')).toBeInTheDocument();
    expect(screen.getByText('computer-vision')).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Crop disease triage' }),
    ).toBeInTheDocument();
  });

  it('shows difficulty as filled squares with a screen-reader label', () => {
    const { container } = render(
      <IndexCard field="ml" title="Drift detector" difficulty="intermediate" />,
    );

    expect(container.querySelector('[aria-hidden]')).toHaveTextContent('■■□');
    expect(screen.getByText('intermediate')).toBeInTheDocument();
  });

  it('falls back to NO-ID when the source has no ID', () => {
    render(<IndexCard field="ml" title="Untitled draft" difficulty="advanced" />);
    expect(screen.getByText('NO-ID')).toBeInTheDocument();
    expect(screen.getByText('advanced')).toBeInTheDocument();
  });

  it('renders summary, domain and est hours when present', () => {
    render(
      <IndexCard
        field="web-fullstack"
        title="Permit tracker"
        summary="Track applications end to end."
        difficulty="beginner"
        domain="governance"
        estHours={16}
      />,
    );

    expect(screen.getByText('Track applications end to end.')).toBeInTheDocument();
    expect(screen.getByText('governance · 16h')).toBeInTheDocument();
  });
});
