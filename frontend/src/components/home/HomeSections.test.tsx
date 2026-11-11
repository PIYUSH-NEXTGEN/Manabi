import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { BuildInPublic } from './BuildInPublic';
import { renderWithProviders } from '@/test/renderWithProviders';

describe('BuildInPublic', () => {
  it('renders the submission rules without the animated console', () => {
    renderWithProviders(<BuildInPublic />);

    expect(screen.getByText('Your own repo')).toBeInTheDocument();
    expect(screen.getByText('README + 5 commits')).toBeInTheDocument();
    expect(screen.getByText('AI checks relevance')).toBeInTheDocument();
    expect(screen.queryByText('Verification console')).not.toBeInTheDocument();
    expect(screen.queryByText('Live sample')).not.toBeInTheDocument();
  });

  it('links to the board to claim a problem', () => {
    renderWithProviders(<BuildInPublic />);

    expect(
      screen.getByRole('link', { name: 'Claim a problem' }),
    ).toHaveAttribute('href', '/problems');
  });
});