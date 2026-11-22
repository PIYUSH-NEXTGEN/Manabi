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
    expect(await screen.findByText(/5 real projects/i)).toBeInTheDocument();
    expect(await screen.findByText(/1 online now/i)).toBeInTheDocument();
    expect(
      await screen.findByText(/12 visitors all-time/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole('link', { name: 'Browse all projects' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'How the platform works' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', {
        name: 'Find a project worth proving.',
        level: 2,
      }),
    ).toBeInTheDocument();
  }, 10000);

  it(
    'cycles three random briefs every three seconds',
    async () => {
      renderWithProviders(<HomePage />, { route: '/' });

      const showcase = await screen.findByRole('figure');
      expect(
        await within(showcase).findByText('01 / 03'),
      ).toBeInTheDocument();
      expect(
        within(showcase).getAllByRole('button', { name: /Show brief/ }),
      ).toHaveLength(3);

      await waitFor(
        () => {
          expect(within(showcase).getByText('02 / 03')).toBeInTheDocument();
        },
        { timeout: 5000 },
      );
    },
    10000,
  );

  it(
    'pauses the brief carousel while keyboard focus is inside it',
    async () => {
      renderWithProviders(<HomePage />, { route: '/' });

      const showcase = await screen.findByRole('figure');
      const counter = await within(showcase).findByText(/\d\d \/ 03/);
      const before = counter.textContent;
      const indicator = within(showcase).getAllByRole('button', {
        name: /Show brief/,
      })[0];
      indicator.focus();
      expect(indicator).toHaveFocus();

      await new Promise((resolve) => window.setTimeout(resolve, 3400));

      expect(within(showcase).getByText(/\d\d \/ 03/).textContent).toBe(before);
    },
    10000,
  );

  it('shows the submission rules without the animated console', async () => {
    renderWithProviders(<HomePage />, { route: '/' });

    expect(await screen.findByText('Your own repo')).toBeInTheDocument();
    expect(screen.queryByText('Verification console')).not.toBeInTheDocument();
    expect(screen.queryByText('Live sample')).not.toBeInTheDocument();
  });
});
