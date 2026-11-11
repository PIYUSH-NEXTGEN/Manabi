import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { BuildInPublic } from './BuildInPublic';
import { renderWithProviders } from '@/test/renderWithProviders';

describe('BuildInPublic', () => {
  it('renders the verification console as the only sample panel', () => {
    renderWithProviders(<BuildInPublic />);

    expect(screen.getByText('Verification console')).toBeInTheDocument();
    expect(screen.getByText('Sample run')).toBeInTheDocument();
    expect(screen.getByText('Ownership')).toBeInTheDocument();
    expect(screen.getByText('README')).toBeInTheDocument();
    expect(screen.getAllByText('Commits').length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText('Project record')).not.toBeInTheDocument();
  });

  it('links to the board to claim a problem', () => {
    renderWithProviders(<BuildInPublic />);

    expect(
      screen.getByRole('link', { name: 'Claim a problem' }),
    ).toHaveAttribute('href', '/problems');
  });
});