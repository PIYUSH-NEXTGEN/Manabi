import { screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { HomePage } from './HomePage';
import { renderWithProviders } from '@/test/renderWithProviders';

describe('HomePage', () => {
  it('renders the hero with the real problem count from the API', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      screen.getByRole('heading', { name: 'MANABI', level: 1 }),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/briefs indexed/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole('button', { name: 'Browse projects' }),
    ).toBeInTheDocument();
  });

  it('shows real problem cards in the featured grid', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    const cropHeadings = await screen.findAllByRole('heading', {
      name: 'Crop disease triage for small farms',
    });
    expect(cropHeadings.length).toBeGreaterThanOrEqual(1);

    expect(
      screen.getAllByRole('heading', { name: 'Streetlight outage tracker' }).length,
    ).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('SIH26017').length).toBeGreaterThanOrEqual(1);
  });

  it('marquees only the sources returned by /api/problems/facets', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    const tape = await screen.findByLabelText('Sources');
    expect(within(tape).getAllByText('SIH 2026').length).toBeGreaterThan(0);
    expect(within(tape).getAllByText('TCOE').length).toBeGreaterThan(0);
    expect(
      within(tape).getAllByText('OpenGov Data Challenge').length,
    ).toBeGreaterThan(0);
  });

  it('shows the sample project progress panel with an ACTIVE stamp', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      await screen.findByText('demo-farmer / crop-triage'),
    ).toBeInTheDocument();
    expect(screen.getAllByText('ACTIVE').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByLabelText('14 commits').length).toBeGreaterThanOrEqual(1);
    expect(
      screen.getByRole('heading', { name: /Find it\. Build it\./ }),
    ).toBeInTheDocument();
  });
});
