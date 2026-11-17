import { screen, within } from '@testing-library/react';
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
    field: 'data-science',
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
    expect(cards).toHaveLength(5);
    expect(
      await screen.findByText(/5 projects in the index/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Fraud pattern walkthrough for UPI micro-transactions'),
    ).toBeInTheDocument();
  });

  it('shows problems with submitted projects first', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    const cards = await screen.findAllByRole('heading', { level: 3 });
    expect(cards[0]).toHaveTextContent(
      'Crop disease triage for small farms',
    );
  });

  it('keeps the same discover seed when the board remounts', async () => {
    const seeds: string[] = [];
    server.use(
      http.get('*/api/problems', ({ request }) => {
        const url = new URL(request.url);
        seeds.push(url.searchParams.get('seed') ?? '');
        return HttpResponse.json({
          items: extendedProblems.slice(0, 5),
          total: 5,
        });
      }),
    );

    const first = renderWithProviders(<ProblemBoardPage />, {
      route: '/problems',
    });
    await screen.findAllByRole('heading', { level: 3 });
    first.unmount();

    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });
    await screen.findAllByRole('heading', { level: 3 });

    expect(seeds.length).toBeGreaterThanOrEqual(2);
    expect(seeds[0]).toBe(seeds[1]);
  });

  it('each card links to its problem detail page', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    const link = await screen.findByRole('link', {
      name: /crop disease triage for small farms/i,
    });
    expect(link).toHaveAttribute('href', '/problems/1');
  });

  it('shows the star chip only on cards that have been starred', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });

    // The attendance pipeline carries star_count: 2 in the fixtures...
    const starredCard = screen.getByRole('link', {
      name: /attendance pipeline that fails loudly/i,
    });
    expect(within(starredCard).getByTitle('2 stars')).toBeInTheDocument();

    // ...crop triage has zero stars, so no chip and no "0".
    const unstarredCard = screen.getByRole('link', {
      name: /crop disease triage for small farms/i,
    });
    expect(within(unstarredCard).queryByTitle(/stars?/)).not.toBeInTheDocument();
    expect(within(unstarredCard).queryByText(/^0$/)).not.toBeInTheDocument();
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
    expect(await screen.findByText(/1 projects? in the index/i)).toBeInTheDocument();
  });

  it('shows the difficulty filter only on the learning track', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems?goal=resume' });

    await screen.findAllByRole('heading', { level: 3 });
    expect(screen.queryByLabelText('Difficulty')).not.toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /Learning/i }));
    expect(await screen.findByLabelText('Difficulty')).toBeInTheDocument();
  });

  it('shows difficulty on learning cards only', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, {
      route: '/problems?goal=learning',
    });

    await screen.findAllByRole('heading', { level: 3 });
    const learningCard = screen.getByRole('link', {
      name: /Fraud pattern walkthrough/i,
    });
    expect(within(learningCard).getByText('advanced')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /Resume/i }));
    const resumeCard = await screen.findByRole('link', {
      name: /Pharmacy stock-out early warning/i,
    });
    expect(within(resumeCard).queryByText('intermediate')).not.toBeInTheDocument();
  });

  it('the difficulty filter updates learning results', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, {
      route: '/problems?goal=learning',
    });

    await screen.findAllByRole('heading', { level: 3 });
    await user.selectOptions(screen.getByLabelText('Difficulty'), 'advanced');

    expect(
      await screen.findByText('Fraud pattern walkthrough for UPI micro-transactions'),
    ).toBeInTheDocument();
    expect(await screen.findByText(/1 projects? in the index/i)).toBeInTheDocument();
  });

  it('scopes difficulty counts to the selected field and learning track', async () => {
    renderWithProviders(<ProblemBoardPage />, {
      route: '/problems?field=aiml&goal=learning',
    });

    await screen.findAllByRole('heading', { level: 3 });

    expect(
      await screen.findByRole('option', { name: 'advanced (1)' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('option', { name: 'beginner (0)' }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole('option', { name: 'beginner (2)' }),
    ).not.toBeInTheDocument();
  });

  it('clear filters resets the board', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    await user.type(screen.getByLabelText('Search'), 'crop');

    const clearButton = await screen.findByRole('button', {
      name: 'Clear filters',
    });
    await user.click(clearButton);

    expect(await screen.findByText(/5 projects in the index/i)).toBeInTheDocument();
    expect(
      screen.queryByRole('button', { name: 'Clear filters' }),
    ).not.toBeInTheDocument();
  });

  it('shows curated track counts on the browse-by-track chips', async () => {
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });

    expect(
      screen.getByRole('button', { name: /Resume/i }),
    ).toHaveTextContent('1 project');
    expect(
      screen.getByRole('button', { name: /Hackathon/i }),
    ).toHaveTextContent('0 projects');
    expect(
      screen.getByRole('button', { name: /Learning/i }),
    ).toHaveTextContent('1 project');
  });

  it('clicking a track chip filters the board to that goal', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ProblemBoardPage />, { route: '/problems' });

    await screen.findAllByRole('heading', { level: 3 });
    await user.click(screen.getByRole('button', { name: /Learning/i }));

    const chip = screen.getByRole('button', { name: /Learning/i });
    expect(chip).toHaveAttribute('aria-pressed', 'true');
    expect(
      await screen.findByText(/1 projects in the index/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Fraud pattern walkthrough for UPI micro-transactions'),
    ).toBeInTheDocument();
    expect(
      screen.queryByText('Crop disease triage for small farms'),
    ).not.toBeInTheDocument();

    await user.click(chip);
    expect(
      await screen.findByText(/5 projects in the index/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByText('Crop disease triage for small farms'),
    ).toBeInTheDocument();
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
      await screen.findByText(/15 projects in the index/i),
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
