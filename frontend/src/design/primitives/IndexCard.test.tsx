import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { IndexCard } from './IndexCard';

describe('IndexCard', () => {
  it('renders the mono header with source ID and field', () => {
    render(
      <IndexCard
        sourceId="SIH26017"
        field="aiml"
        title="Crop disease triage"
        difficulty="beginner"
      />,
    );

    expect(screen.getByText('SIH26017')).toBeInTheDocument();
    expect(screen.getByText('aiml')).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Crop disease triage' }),
    ).toBeInTheDocument();
  });

  it('shows difficulty as filled bars with a screen-reader label', () => {
    render(
      <IndexCard field="data-science" title="Drift detector" difficulty="intermediate" />,
    );

    const label = screen.getByText('intermediate');
    const bars = label.previousElementSibling?.children;
    expect(bars).toHaveLength(3);
    expect(bars?.[0]).toHaveClass('bg-accent');
    expect(bars?.[1]).toHaveClass('bg-accent');
    expect(bars?.[2]).toHaveClass('bg-tint');
  });

  it('falls back to NO-ID when the source has no ID', () => {
    render(<IndexCard field="data-science" title="Untitled draft" difficulty="advanced" />);
    expect(screen.getByText('NO-ID')).toBeInTheDocument();
    expect(screen.getByText('advanced')).toBeInTheDocument();
  });

  it('renders summary, domain and est hours when present', () => {
    render(
      <IndexCard
        field="web-dev"
        title="Permit tracker"
        summary="Track applications end to end."
        difficulty="beginner"
        domain="governance"
        estHours={16}
      />,
    );

    expect(screen.getByText('Track applications end to end.')).toBeInTheDocument();
    expect(screen.getByText('governance · 16 h')).toBeInTheDocument();
  });
});
