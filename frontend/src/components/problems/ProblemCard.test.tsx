import { screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { ProblemCard } from './ProblemCard';
import type { ProblemOut } from '@/api/client';
import { renderWithProviders } from '@/test/renderWithProviders';

const baseProblem: ProblemOut = {
  id: 42,
  title: 'Civic issue tracker for a ward office',
  summary: 'Residents report local problems with a photo and location.',
  who_affected: 'Residents and ward staff',
  why_matters: 'Untracked complaints disappear.',
  field: 'web-dev',
  domain: 'governance',
  difficulty: 'intermediate',
  est_hours: 40,
  tech_tags: ['typescript', 'postgres'],
  datasets: [],
  approaches: ['Bucket reports by location'],
  source_name: 'MANABI Curated',
  source_id: 'manabi-web-hackathon-002',
  source_url: null,
  source_note: null,
  project_count: 0,
  completed_count: 0,
  ai_fields: [],
  origin: 'manual',
  star_count: 0,
  starred_by_me: false,
  goal: 'hackathon',
  learning_concepts: [],
};

function renderCard(overrides: Partial<ProblemOut> = {}) {
  return renderWithProviders(
    <ProblemCard problem={{ ...baseProblem, ...overrides }} />,
    { route: '/problems' },
  );
}

describe('ProblemCard', () => {
  it('shows the hackathon track without a difficulty badge', () => {
    renderCard();

    const card = screen.getByRole('link', {
      name: /civic issue tracker for a ward office/i,
    });
    expect(within(card).getByText('Hackathon')).toBeInTheDocument();
    expect(within(card).getByText('Web Dev')).toBeInTheDocument();
    expect(within(card).queryByText('intermediate')).not.toBeInTheDocument();
  });

  it('shows the resume track without a difficulty badge', () => {
    renderCard({ goal: 'resume' });

    const card = screen.getByRole('link', {
      name: /civic issue tracker for a ward office/i,
    });
    expect(within(card).getByText('Resume')).toBeInTheDocument();
    expect(within(card).queryByText('intermediate')).not.toBeInTheDocument();
  });

  it('shows the learning track with its difficulty badge', () => {
    renderCard({ goal: 'learning' });

    const card = screen.getByRole('link', {
      name: /civic issue tracker for a ward office/i,
    });
    expect(within(card).getByText('Learning')).toBeInTheDocument();
    expect(within(card).getByText('intermediate')).toBeInTheDocument();
  });
});
