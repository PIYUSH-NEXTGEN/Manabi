import { screen, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { BuildInPublic } from './BuildInPublic';
import { MarqueeTape } from './MarqueeTape';
import { MlTeaser } from './MlTeaser';
import { useFacets } from '@/hooks/useFacets';
import { renderWithProviders } from '@/test/renderWithProviders';

function TapeHarness() {
  const query = useFacets();
  return <MarqueeTape query={query} />;
}

describe('MlTeaser', () => {
  it('shows a real scenario excerpt and topic from the ML API', async () => {
    renderWithProviders(<MlTeaser />);

    expect(
      await screen.findByText(/0\.93 AUC on the holdout set/),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Metrics lie after the launch · bad-eval-split'),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'Start practicing' }),
    ).toHaveAttribute('href', '/ml');
  });
});

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
});

describe('MarqueeTape', () => {
  it('lists source names from facets', async () => {
    renderWithProviders(<TapeHarness />);

    const tape = await screen.findByLabelText('Sources');
    expect(tape).toHaveTextContent('SIH 2026');
    expect(tape).toHaveTextContent('TCOE');
  });

  it('renders no tape when facets error', async () => {
    server.use(
      http.get('*/api/problems/facets', () =>
        HttpResponse.json({ detail: 'facets down' }, { status: 500 }),
      ),
    );

    renderWithProviders(<TapeHarness />);

    await waitFor(() => {
      expect(screen.queryByLabelText('Sources')).not.toBeInTheDocument();
      expect(document.querySelector('[aria-busy="true"]')).toBeNull();
    });
  });
});
