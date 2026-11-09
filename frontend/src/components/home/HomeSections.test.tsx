import { http, HttpResponse } from 'msw';
import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { BuildInPublic } from './BuildInPublic';
import { renderWithProviders } from '@/test/renderWithProviders';
import { server } from '@/api/mocks/server';

describe('BuildInPublic', () => {
  it('renders the sample project progress panel from the API', async () => {
    renderWithProviders(<BuildInPublic />);

    expect(
      await screen.findByText('demo-farmer / crop-triage'),
    ).toBeInTheDocument();
    expect(screen.getByText('ACTIVE')).toBeInTheDocument();
    expect(screen.getByLabelText('14 commits')).toBeInTheDocument();
    expect(screen.getByText('README ✓')).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'Claim a problem' }),
    ).toHaveAttribute('href', '/problems');
  });

  it('shows the honest empty state when the board has no project records', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ items: [], total: 0 }),
      ),
    );
    renderWithProviders(<BuildInPublic />);

    expect(
      await screen.findByText('No project records on the board yet. Be the first.'),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'Browse the index' }),
    ).toHaveAttribute('href', '/problems');
    expect(
      screen.queryByText(/the projects API is up/),
    ).not.toBeInTheDocument();
  });

  it('keeps the API-down fallback when the projects API errors', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ detail: 'Internal server error' }, { status: 500 }),
      ),
    );
    renderWithProviders(<BuildInPublic />);

    expect(
      await screen.findByText('Progress panel loads when the projects API is up.'),
    ).toBeInTheDocument();
  });
});