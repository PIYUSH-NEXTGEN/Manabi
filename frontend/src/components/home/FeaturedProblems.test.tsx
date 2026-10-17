import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { useProblems } from '@/hooks/useProblems';
import { FeaturedProblems } from './FeaturedProblems';
import { renderWithProviders } from '@/test/renderWithProviders';

function FeaturedHarness() {
  const query = useProblems({ sort: 'newest', limit: 6 });
  return <FeaturedProblems query={query} />;
}

describe('FeaturedProblems', () => {
  it('renders six index cards from the API', async () => {
    renderWithProviders(<FeaturedHarness />);

    expect(
      await screen.findByRole('heading', { name: 'Featured problems' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Fraud pattern walkthrough for UPI micro-transactions' }),
    ).toBeInTheDocument();
    expect(
      screen.getAllByRole('heading', { level: 3 }),
    ).toHaveLength(6);
  });

  it('shows the API error detail with a working retry', async () => {
    server.use(
      http.get(
        '*/api/problems',
        () => HttpResponse.json({ detail: 'Database exploded' }, { status: 500 }),
        { once: true },
      ),
    );
    const user = userEvent.setup();
    renderWithProviders(<FeaturedHarness />);

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Database exploded');

    await user.click(screen.getByRole('button', { name: 'Retry' }));

    expect(
      await screen.findByRole('heading', { name: 'Crop disease triage for small farms' }),
    ).toBeInTheDocument();
  });

  it('shows a helpful empty state when the board has no problems', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ items: [], total: 0 }),
      ),
    );

    renderWithProviders(<FeaturedHarness />);

    expect(
      await screen.findByText(/Import one from a real source on the Ingest page/),
    ).toBeInTheDocument();
  });
});
