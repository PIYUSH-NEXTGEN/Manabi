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

  it('explains the pipeline when the board has no project records', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ items: [], total: 0 }),
      ),
    );
    renderWithProviders(<BuildInPublic />);

    expect(await screen.findByText('Verification console')).toBeInTheDocument();
    expect(screen.getByText('Sample run')).toBeInTheDocument();
    expect(
      screen.queryByText('demo-farmer / crop-triage'),
    ).not.toBeInTheDocument();
  });

  it('keeps the console and says so when the projects API errors', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ detail: 'Internal server error' }, { status: 500 }),
      ),
    );
    renderWithProviders(<BuildInPublic />);

    expect(await screen.findByText('Verification console')).toBeInTheDocument();
    expect(
      await screen.findByText(
        'Live example unavailable — the projects API is down.',
      ),
    ).toBeInTheDocument();
  });
});