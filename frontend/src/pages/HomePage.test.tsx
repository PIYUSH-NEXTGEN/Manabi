import { screen, waitFor, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { HomePage } from './HomePage';
import { renderWithProviders } from '@/test/renderWithProviders';

describe('HomePage', () => {
  it('renders the hero with the real problem count from the API', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      screen.getByRole('heading', {
        name: 'Pick a project. Ship it. Prove it.',
        level: 1,
      }),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/briefs curated/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole('button', { name: 'Browse projects' }),
    ).toBeInTheDocument();
  });

  it(
    'cycles the hero brief showcase every three seconds',
    async () => {
      renderWithProviders(<HomePage />, { route: '/' });

      const showcase = await screen.findByRole('figure');
      expect(
        await within(showcase).findByRole('heading', {
          name: 'Crop disease triage for small farms',
        }),
      ).toBeInTheDocument();

      await waitFor(
        () => {
          expect(
            within(showcase).getByRole('heading', {
              name: 'Streetlight outage tracker',
            }),
          ).toBeInTheDocument();
        },
        { timeout: 5000 },
      );
    },
    10000,
  );

  it('shows the sample project progress panel with an ACTIVE stamp', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(
      await screen.findByText('demo-farmer / crop-triage'),
    ).toBeInTheDocument();
    expect(screen.getAllByText('ACTIVE').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByLabelText('14 commits').length).toBeGreaterThanOrEqual(1);
  });
});
