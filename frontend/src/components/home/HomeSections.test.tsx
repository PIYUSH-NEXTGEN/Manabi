import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { BuildInPublic } from './BuildInPublic';
import { renderWithProviders } from '@/test/renderWithProviders';

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