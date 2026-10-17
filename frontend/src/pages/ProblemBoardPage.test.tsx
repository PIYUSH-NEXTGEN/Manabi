import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ProblemBoardPage } from './ProblemBoardPage';
import { renderWithProviders } from '@/test/renderWithProviders';

const extendedProblems = [
  ...Array.from({ length: 15 }, (_, index) => ({
    id: index + 1,
    title: `Problem ${index + 1}`,
    summary: `Summary ${index + 1}`,
    who_affected: 'someone',
    why_matters: 'because',
    field: 'ml',
    domain: 'healthcare',
    difficulty: 'beginner',
    est_hours: 10,
    tech_tags: ['python'],
    datasets: [],
    approaches: ['do a thing'],
    source_name: 'SIH 2026',
    source_id: `SRC${index + 1}`,
    source_url: null,
    source_note: null,
    project_count: 0,
    ai_fields: ['approaches'],
  })),
];

describe('ProblemBoardPage', () => {
  it('renders the problem cards and the index count', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    const cards = await screen.findAllByRole('heading', { level: 3 });
    expect(cards).toHaveLength(6);
    expect(
      await screen.findByText(/6 problems in the index/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Fraud pattern walkthrough for UPI micro-transactions'),
    ).toBeInTheDocument();
  });

  it('each card links to its problem detail page', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    const link = await screen.findByRole('link', {
      name: /crop disease triage for small farms/i,
    });
    expect(link).toHaveAttribute('href', '/problems/1');
  });

  it('typing in search filters the results', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    await user.type(screen.getByLabelText('Search'), 'fraud');

    expect(
      await screen.findByText('Fraud pattern walkthrough for UPI micro-transactions'),
    ).toBeInTheDocument();
    expect(
      screen.queryByText('Crop disease triage for small farms'),
    ).not.toBeInTheDocument();
    expect(await screen.findByText(/1 problems? in the index/i)).toBeInTheDocument();
  });

  it('the difficulty filter updates results', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    await user.selectOptions(screen.getByLabelText('Difficulty'), 'beginner');

    expect(
      await screen.findByText('Attendance pipeline that fails loudly'),
    ).toBeInTheDocument();
    expect(
      screen.queryByText('Streetlight outage tracker'),
    ).not.toBeInTheDocument();
    expect(await screen.findByText(/2 problems in the index/i)).toBeInTheDocument();
  });

  it('tech chips toggle on and off', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    const pythonChip = screen.getByRole('button', { name: /python \(5\)/i });

    await user.click(pythonChip);
    expect(await screen.findByText(/5 problems in the index/i)).toBeInTheDocument();

    await user.click(pythonChip);
    expect(await screen.findByText(/6 problems in the index/i)).toBeInTheDocument();
  });

  it('clear filters resets the board', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    await user.selectOptions(screen.getByLabelText('Difficulty'), 'beginner');

    const clearButton = await screen.findByRole('button', {
      name: 'Clear filters',
    });
    await user.click(clearButton);

    expect(await screen.findByText(/6 problems in the index/i)).toBeInTheDocument();
    expect(
      screen.queryByRole('button', { name: 'Clear filters' }),
    ).not.toBeInTheDocument();
  });

  it('load more fetches the next page and then disappears', async () => {
    server.use(
      http.get('*/api/problems', ({ request }) => {
        const url = new URL(request.url);
        const limit = Number(url.searchParams.get('limit') ?? '12');
        const offset = Number(url.searchParams.get('offset') ?? '0');
        return HttpResponse.json({
          items: extendedProblems.slice(offset, offset + limit),
          total: extendedProblems.length,
        });
      }),
    );

    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    const cards = await screen.findAllByRole('heading', { level: 3 });
    expect(cards).toHaveLength(12);
    expect(
      await screen.findByText(/15 problems in the index/i),
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Load more' }));

    const allCards = await screen.findAllByRole('heading', { level: 3 });
    expect(allCards).toHaveLength(15);
    expect(
      screen.queryByRole('button', { name: 'Load more' }),
    ).not.toBeInTheDocument();
  });

  it('shows an empty-state panel when filters match nothing', async () => {
    renderWithProviders(<ProblemBoardPage />, {
      route: '/problems?q=zzz-no-matches',
    });

    expect(
      await screen.findByText(/Nothing in the index matches those filters yet\./i),
    ).toBeInTheDocument();
  });

  it('shows a retry panel when the board fails to load', async () => {
    server.use(
      http.get('*/api/problems', () =>
        HttpResponse.json({ detail: 'nope' }, { status: 500 }),
      ),
    );

    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    expect(
      await screen.findByText(/The board could not be loaded\./i),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: 'Try again' }),
    ).toBeInTheDocument();
  });
});
