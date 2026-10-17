import { Routes, Route } from 'react-router-dom';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { ProblemDetailPage } from './ProblemDetailPage';
import { renderWithProviders } from '@/test/renderWithProviders';

function renderDetail(route: string) {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path="/problems/:id" element={<ProblemDetailPage />} />
      </Routes>
    </ToastProvider>,
    { route },
  );
}

describe('ProblemDetailPage', () => {
  it('renders the structured brief for problem 1', async () => {
    renderDetail('/problems/1');

    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 1,
      }),
    ).toBeInTheDocument();
    expect(screen.getByText('Smallholder farmers')).toBeInTheDocument();
    expect(
      screen.getByText('Fine-tune a small CNN on public leaf datasets'),
    ).toBeInTheDocument();
    expect(screen.getByText('python')).toBeInTheDocument();
    expect(screen.getByText('Late detection destroys a season of income.')).toBeInTheDocument();
    expect(
      screen.getByText('No dataset attached to this brief.'),
    ).toBeInTheDocument();
    expect(screen.getByText(/no public link/i)).toBeInTheDocument();
  });

  it('shows one AI-SUGGESTED stamp for problem 1 and none for non-AI rows', async () => {
    renderDetail('/problems/1');

    await screen.findByRole('heading', { level: 1 });
    expect(await screen.findAllByText(/ai-suggested/i)).toHaveLength(1);
  });

  it('shows all AI-SUGGESTED stamps for problem 2 (approaches + est hours)', async () => {
    renderDetail('/problems/2');

    await screen.findByRole('heading', { name: 'Streetlight outage tracker' });
    expect(await screen.findAllByText(/ai-suggested/i)).toHaveLength(2);
  });

  it('shows the original statement verbatim', async () => {
    renderDetail('/problems/1');

    const statement = await screen.findByRole('region', {
      name: 'Original statement',
    });
    expect(statement).toHaveTextContent('Crop disease triage for small farms');
  });

  it('lists submitted projects with progress badges', async () => {
    renderDetail('/problems/1');

    expect(
      await screen.findByText(/Projects in the wild \(1\)/i),
    ).toBeInTheDocument();
    expect(await screen.findByText(/14 commits/i)).toBeInTheDocument();
    expect(await screen.findByText(/active/i)).toBeInTheDocument();
  });

  it('shows the stale badge for problem 2', async () => {
    renderDetail('/problems/2');

    expect(await screen.findByText(/3 commits/i)).toBeInTheDocument();
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
