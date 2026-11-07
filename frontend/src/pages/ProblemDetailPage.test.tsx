import { Routes, Route } from 'react-router-dom';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { ProblemDetailPage } from './ProblemDetailPage';
import { ProblemGuidePage } from './ProblemGuidePage';
import { renderWithProviders } from '@/test/renderWithProviders';

function renderDetail(route: string) {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path="/problems/:id" element={<ProblemDetailPage />} />
        <Route path="/problems/:id/guide" element={<ProblemGuidePage />} />
      </Routes>
    </ToastProvider>,
    { route },
  );
}

describe('ProblemDetailPage', () => {
  it('renders the problem title, fuller description and why it matters in one card', async () => {
    renderDetail('/problems/1');

    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 1,
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Farmers photograph leaf blight;/),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/This project is for smallholder farmers/),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Late detection destroys a season of income.'),
    ).toBeInTheDocument();
  });

  it('shows the tech stack as options, not a single rule', async () => {
    renderDetail('/problems/1');

    await screen.findByRole('heading', { level: 1 });

    expect(screen.getByText('python')).toBeInTheDocument();
    expect(
      screen.getByText(
        /The stack below is a starting point, not a rule/i,
      ),
    ).toBeInTheDocument();
    expect(screen.getByText(/Python or Go/i)).toBeInTheDocument();
  });

  it('shows what you can add later with a fallback when none is listed', async () => {
    renderDetail('/problems/1');

    await screen.findByRole('heading', { level: 1 });

    expect(
      await screen.findByText(
        /Ship the MVP first, then add whatever matters to you/i,
      ),
    ).toBeInTheDocument();
  });

  it('links to a separate build guide page', async () => {
    renderDetail('/problems/1');

    await screen.findByRole('heading', { level: 1 });
    const link = await screen.findByRole('link', { name: 'Build guide' });
    expect(link).toHaveAttribute('href', '/problems/1/guide');
  });

  it('opens the build guide page with phases', async () => {
    renderDetail('/problems/1/guide');

    expect(
      await screen.findByRole('heading', {
        name: /build guide · crop disease triage for small farms/i,
        level: 1,
      }),
    ).toBeInTheDocument();
    expect(await screen.findByText(/Phase 1 · Start/i)).toBeInTheDocument();
    expect(await screen.findByText(/Phase 2 · Implement/i)).toBeInTheDocument();
    expect(await screen.findByText(/Phase 3 · Ship/i)).toBeInTheDocument();
    expect(
      screen.getByText(
        'Fine-tune a small CNN on public leaf datasets',
      ),
    ).toBeInTheDocument();
  });

  it('lists submitted projects with progress badges', async () => {
    renderDetail('/problems/1');

    expect(
      await screen.findByText(/Projects in the wild \(1\)/i),
    ).toBeInTheDocument();
    expect(await screen.findByText(/active/i)).toBeInTheDocument();
  });

  it('shows the stale badge for problem 2', async () => {
    renderDetail('/problems/2');

    await screen.findByRole('heading', { name: 'Streetlight outage tracker' });
    expect(await screen.findByText(/stale/i)).toBeInTheDocument();
  });

  it('shows the login CTA when logged out', async () => {
    renderDetail('/problems/1');

    const login = await screen.findByRole('link', {
      name: 'Log in with GitHub',
    });
    expect(login).toHaveAttribute('href', '/api/auth/github/login');
  });

  it('rejects non-GitHub URLs on the client without a network call', async () => {
    let postCalls = 0;
    server.use(
      http.post('*/api/problems/:id/projects', () => {
        postCalls += 1;
        return HttpResponse.json({ detail: 'boom' }, { status: 500 });
      }),
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 9,
          username: 'tester',
          name: 'Testa User',
          avatar_url: null,
        }),
      ),
    );

    const user = userEvent.setup();
    renderDetail('/problems/1');

    await screen.findByRole('heading', { name: 'Submit a project' });
    await user.type(
      screen.getByLabelText('GitHub repo URL'),
      'https://gitlab.com/owner/name',
    );
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(
      await screen.findByText(/Use a GitHub repo URL like/i),
    ).toBeInTheDocument();
    expect(postCalls).toBe(0);
  });

  it('submits a valid repo URL and shows the submitted panel', async () => {
    let postCalls = 0;
    server.use(
      http.post('*/api/problems/:id/projects', () => {
        postCalls += 1;
        return HttpResponse.json({
          id: 11,
          problem_id: 1,
          problem_title: 'Crop disease triage for small farms',
          repo_url: 'https://github.com/tester/new-thing',
          repo_owner: 'tester',
          repo_name: 'new-thing',
          open_for_contributors: true,
          verification_status: 'verified',
          solution_summary: 'An offline capture flow that routes leaf cases to officers.',
          completed_at: null,
          demo_url: null,
          reflection: null,
          relevance_reason: null,
          ownership_basis: null,
          review_note: null,
          owner: { username: 'tester', avatar_url: null },
          progress: null,
          progress_updated_at: null,
        });
      }),
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 9,
          username: 'tester',
          name: 'Testa User',
          avatar_url: null,
        }),
      ),
    );

    const user = userEvent.setup();
    renderDetail('/problems/1');

    await screen.findByRole('heading', { name: 'Submit a project' });
    await user.type(
      screen.getByLabelText('GitHub repo URL'),
      'https://github.com/tester/new-thing/',
    );
    await user.click(screen.getByLabelText('Open for contributors'));
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(await screen.findByText(/is on the board/i)).toBeInTheDocument();
    expect(
      screen.getByText(/github\.com\/tester\/new-thing/i),
    ).toHaveTextContent('https://github.com/tester/new-thing');
    expect(postCalls).toBe(1);
    expect(
      screen.getByRole('link', { name: 'Open project page' }),
    ).toHaveAttribute('href', '/projects/11');
  });

  it('surfaces server-side 422 details', async () => {
    server.use(
      http.post('*/api/problems/:id/projects', () =>
        HttpResponse.json(
          { detail: 'You already claimed this problem' },
          { status: 422 },
        ),
      ),
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 9,
          username: 'tester',
          name: 'Testa User',
          avatar_url: null,
        }),
      ),
    );

    const user = userEvent.setup();
    renderDetail('/problems/1');

    await screen.findByRole('heading', { name: 'Submit a project' });
    await user.type(
      screen.getByLabelText('GitHub repo URL'),
      'https://github.com/tester/again',
    );
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(
      await screen.findByText(/You already claimed this problem/i),
    ).toBeInTheDocument();
  });

  it('renders the 404 page for a missing problem', async () => {
    renderDetail('/problems/999');

    expect(
      await screen.findByRole('heading', { name: /404/i, level: 1 }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'Browse problems' }),
    ).toBeInTheDocument();
  });
});
