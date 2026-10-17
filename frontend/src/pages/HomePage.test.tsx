import { screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { HomePage } from './HomePage';
import { renderWithProviders } from '@/test/renderWithProviders';

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

describe('HomePage', () => {
  it('renders the hero with the real problem count from the API', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      screen.getByRole('heading', { name: 'MANABI', level: 1 }),
    ).toBeInTheDocument();
    expect(
      await screen.findByText('6 problems on the board'),
    ).toBeInTheDocument();

    const ctas = screen.getAllByRole('link');
    expect(ctas.some((link) => link.textContent === 'Browse problems')).toBe(true);
    expect(ctas.some((link) => link.textContent === 'Practice ML')).toBe(true);
  });

  it('shows real problem cards in the hero stack and featured grid', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    const cropHeadings = await screen.findAllByRole('heading', {
      name: 'Crop disease triage for small farms',
    });
    expect(cropHeadings.length).toBeGreaterThanOrEqual(2);

    expect(
      screen.getByRole('heading', { name: 'Pharmacy stock-out early warning' }),
    ).toBeInTheDocument();
    expect(screen.getAllByText('SIH26017').length).toBeGreaterThanOrEqual(2);
  });

  it('counts up the stats strip to the values from /api/stats', async () => {
    stubMatchMedia(true);
    renderWithProviders(<HomePage />, { route: '/' });

    const strip = await screen.findByRole('region', { name: 'Platform stats' });
    expect(await within(strip).findByText('6')).toBeInTheDocument();
    expect(within(strip).getByText('3')).toBeInTheDocument();
    expect(within(strip).getByText('5')).toBeInTheDocument();
    expect(within(strip).getAllByText('2')).toHaveLength(2);
    expect(within(strip).getByText('ML questions')).toBeInTheDocument();
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

  it('renders the how-it-works numerals and the ML teaser excerpt', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(screen.getByText('01')).toBeInTheDocument();
    expect(screen.getByText('04')).toBeInTheDocument();
    expect(await screen.findByText(/0\.93 AUC/)).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Production bugs, not puzzles' }),
    ).toBeInTheDocument();
  });

  it('shows the sample project progress panel with an ACTIVE stamp', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      await screen.findByText('demo-farmer / crop-triage'),
    ).toBeInTheDocument();
    expect(screen.getByText('ACTIVE')).toBeInTheDocument();
    expect(screen.getByLabelText('14 commits')).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: /Find it\. Build it\./ }),
    ).toBeInTheDocument();
  });
});
