import { Routes, Route } from 'react-router-dom';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { ProjectDetailPage } from './ProjectDetailPage';
import { renderWithProviders } from '@/test/renderWithProviders';

function renderProject(route: string) {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path="/projects/:id" element={<ProjectDetailPage />} />
      </Routes>
    </ToastProvider>,
    { route },
  );
}

describe('ProjectDetailPage', () => {
  it('renders repo info, badges, and the problem back-link', async () => {
    renderProject('/projects/1');

    expect(
      await screen.findByRole('heading', { name: 'crop-triage', level: 1 }),
    ).toBeInTheDocument();
    expect(screen.getByText(/by demo-farmer/i)).toBeInTheDocument();
    expect(screen.getByText('open for contributors')).toBeInTheDocument();

    const repoLink = screen.getByRole('link', {
      name: /github\.com\/demo-farmer\/crop-triage/i,
    });
    expect(repoLink).toHaveAttribute(
      'href',
      'https://github.com/demo-farmer/crop-triage',
    );

    const problemLink = screen.getByRole('link', {
      name: 'Crop disease triage for small farms',
    });
    expect(problemLink).toHaveAttribute('href', '/problems/1');
  });

  it('shows the active progress badge and commit stats', async () => {
    renderProject('/projects/1');

    expect(await screen.findByText(/14 commits/i)).toBeInTheDocument();
    expect(
      await screen.findByText('Last commit'),
    ).toBeInTheDocument();
  });

  it('lists recent commits and open issues from the mocked API', async () => {
    renderProject('/projects/1');

    expect(
      await screen.findByText(/Add offline capture queue/i),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/Leaf classifier v0/i),
    ).toBeInTheDocument();
    const issueLink = await screen.findByRole('link', {
      name: /#7 handle low-light photos/i,
    });
    expect(issueLink).toHaveAttribute(
      'href',
      'https://github.com/demo-farmer/crop-triage/issues/7',
    );
    expect(screen.getByText('good first issue')).toBeInTheDocument();
  });

  it('shows honest empty states when progress has no data', async () => {
    server.use(
      http.get('*/api/projects/:id', () =>
        HttpResponse.json({
          id: 2,
          problem_id: 1,
          problem_title: 'Crop disease triage for small farms',
          repo_url: 'https://github.com/fresh/new-repo',
          repo_owner: 'fresh',
          repo_name: 'new-repo',
          open_for_contributors: false,
          owner: { username: 'fresh', avatar_url: null },
          progress: null,
          progress_updated_at: null,
        }),
      ),
      // The automatic first fetch also fails, so the page falls back to
      // the honest "unknown" line.
      http.get('*/api/projects/2/progress', () =>
        HttpResponse.json({ detail: 'Project not found' }, { status: 404 }),
      ),
    );

    renderProject('/projects/2');

    expect(
      await screen.findByText(/Progress unknown. Hit refresh/i),
    ).toBeInTheDocument();
  });

  it('pulls progress from GitHub automatically when no stored progress exists', async () => {
    server.use(
      http.get('*/api/projects/:id', () =>
        HttpResponse.json({
          id: 2,
          problem_id: 1,
          problem_title: 'Crop disease triage for small farms',
          repo_url: 'https://github.com/fresh/new-repo',
          repo_owner: 'fresh',
          repo_name: 'new-repo',
          open_for_contributors: false,
          owner: { username: 'fresh', avatar_url: null },
          progress: null,
          progress_updated_at: null,
        }),
      ),
      http.get('*/api/projects/2/progress', () =>
        HttpResponse.json({
          status: 'active',
          commit_count: 6,
          last_commit_at: '2026-11-11T09:00:00Z',
          has_readme: true,
          recent_commits: [],
          open_issues: [],
        }),
      ),
    );

    renderProject('/projects/2');

    // No manual click: the page fetches the missing progress on arrival.
    expect(await screen.findByText(/6 commits/i)).toBeInTheDocument();
    expect(
      screen.queryByText(/Progress unknown. Hit refresh/i),
    ).not.toBeInTheDocument();
  });

  it('empty commits and issues render the honest lines', async () => {
    server.use(
      http.get('*/api/projects/:id', () =>
        HttpResponse.json({
          id: 3,
          problem_id: 1,
          problem_title: 'Crop disease triage for small farms',
          repo_url: 'https://github.com/fresh/empty-repo',
          repo_owner: 'fresh',
          repo_name: 'empty-repo',
          open_for_contributors: false,
          owner: { username: 'fresh', avatar_url: null },
          progress: {
            status: 'not_started',
            commit_count: 22,
            last_commit_at: null,
            has_readme: false,
            recent_commits: [],
            open_issues: [],
          },
          progress_updated_at: null,
        }),
      ),
    );

    renderProject('/projects/3');

    expect(
      await screen.findByText('No commits recorded yet.'),
    ).toBeInTheDocument();
    expect(screen.getByText('No open issues right now.')).toBeInTheDocument();
  });

  it('refresh pulls updated progress and re-renders the stats', async () => {
    const user = userEvent.setup();
    let refreshCalls = 0;
    server.use(
      http.get('*/api/projects/:id/progress', ({ request }) => {
        expect(
          new URL(request.url).searchParams.get('refresh'),
        ).toBe('true');
        refreshCalls += 1;
        return HttpResponse.json({
          status: 'active',
          commit_count: 15,
          last_commit_at: '2026-10-17T08:00:00Z',
          has_readme: true,
          recent_commits: [],
          open_issues: [],
        });
      }),
    );

    renderProject('/projects/1');

    await screen.findByText(/14 commits/i);
    await user.click(screen.getByRole('button', { name: 'Refresh progress' }));

    expect(await screen.findByText('15')).toBeInTheDocument();
    expect(
      await screen.findByText(/Progress refreshed from GitHub/i),
    ).toBeInTheDocument();
    expect(refreshCalls).toBe(1);
  });

  it('shows the stale badge for project 2', async () => {
    renderProject('/projects/2');

    expect(await screen.findByText(/3 commits/i)).toBeInTheDocument();
    expect((await screen.findAllByText(/stale/i)).length).toBeGreaterThan(0);
    expect(
      await screen.findByText(/Streetlight outage tracker/i),
    ).toBeInTheDocument();
  });

  it('renders the 404 page for a missing project', async () => {
    renderProject('/projects/999');

    expect(
      await screen.findByRole('heading', { name: /404/i, level: 1 }),
    ).toBeInTheDocument();
  });

  it('reports a submission: client validation, success toast, then a clean form', async () => {
    const user = userEvent.setup();
    let bodies: Array<Record<string, unknown>> = [];
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json(ME_LOGGED_IN_VIEWER),
      ),
      http.post('*/api/projects/1/report', async ({ request }) => {
        bodies.push((await request.json()) as Record<string, unknown>);
        return HttpResponse.json({ ok: true, report_count: 1 }, { status: 201 });
      }),
    );
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    const reportButton = screen.getByRole('button', { name: 'Report submission' });

    // viewer is not the owner -> the report row is visible
    await user.type(screen.getByLabelText(/Something wrong with this submission/i), 'short');
    await user.click(reportButton);
    expect(
      await screen.findByText(/Add a short reason \(10\+ characters\)/i),
    ).toBeInTheDocument();
    expect(bodies).toEqual([]);

    await user.clear(screen.getByLabelText(/Something wrong with this submission/i));
    await user.type(
      screen.getByLabelText(/Something wrong with this submission/i),
      'The demo link goes to a parking page.',
    );
    await user.click(reportButton);

    expect(
      await screen.findByRole('status'),
    ).toHaveTextContent('Report sent. Thanks. A maintainer will take a look.');
    expect(bodies).toEqual([
      { reason: 'The demo link goes to a parking page.' },
    ]);
    expect(screen.getByLabelText(/Something wrong with this submission/i)).toHaveValue('');
  });

  it('maps report errors honestly: 409 already reported, 429 rate limited', async () => {
    const user = userEvent.setup();
    let attempts = 0;
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json(ME_LOGGED_IN_VIEWER),
      ),
      http.post('*/api/projects/1/report', () => {
        attempts += 1;
        if (attempts === 1) {
          return HttpResponse.json(
            { detail: { code: 'already_reported', message: 'You already reported this project.' } },
            { status: 409 },
          );
        }
        return HttpResponse.json(
          {
            detail: {
              code: 'rate_limited',
              message: 'Too many reports this hour. Try again in about 37 minutes.',
            },
          },
          { status: 429, headers: { 'Retry-After': '2220' } },
        );
      }),
    );
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    await user.type(
      screen.getByLabelText(/Something wrong with this submission/i),
      'The progress numbers look stale to me.',
    );
    await user.click(screen.getByRole('button', { name: 'Report submission' }));

    expect(
      await screen.findByText('You already reported this project.'),
    ).toBeInTheDocument();

    await user.clear(screen.getByLabelText(/Something wrong with this submission/i));
    await user.type(
      screen.getByLabelText(/Something wrong with this submission/i),
      'Another concrete reason to try again.',
    );
    await user.click(screen.getByRole('button', { name: 'Report submission' }));

    expect(
      await screen.findByText(
        'Too many reports this hour. Try again in about 37 minutes.',
      ),
    ).toBeInTheDocument();
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('hides the report row from the owner and from logged-out visitors', async () => {
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    expect(
      screen.queryByLabelText(/Something wrong with this submission/i),
    ).not.toBeInTheDocument();
  });

  it('hides the report row from the project owner even when logged in', async () => {
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 5,
          username: 'demo-farmer',
          name: 'Demo Farmer',
          avatar_url: null,
        }),
      ),
    );
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    expect(
      screen.queryByLabelText(/Something wrong with this submission/i),
    ).not.toBeInTheDocument();
  });

  it('sends a logged-out visitor to GitHub login when they try to star', async () => {
    renderProject('/projects/1');

    expect(
      await screen.findByRole('heading', { name: 'crop-triage', level: 1 }),
    ).toBeInTheDocument();
    const loginLink = screen.getByRole('link', {
      name: 'Log in to star this project',
    });
    expect(loginLink).toHaveAttribute('href', '/api/auth/github/login');
  });

  it('stars a project once the visitor is logged in', async () => {
    const user = userEvent.setup();
    let starCalls = 0;
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json(ME_LOGGED_IN_VIEWER),
      ),
      http.post('*/api/projects/1/star', () => {
        starCalls += 1;
        return HttpResponse.json({ ok: true, star_count: 3 }, { status: 201 });
      }),
    );
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    await user.click(screen.getByRole('button', { name: 'Star this project' }));

    expect(
      await screen.findByRole('status'),
    ).toHaveTextContent('Starred. Thanks for the signal.');
    expect(starCalls).toBe(1);
  });

  it('marks the project as starred and un-stars it on a second click', async () => {
    const user = userEvent.setup();
    const deleteCalls: number[] = [];
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json(ME_LOGGED_IN_VIEWER),
      ),
      http.get('*/api/projects/1', () =>
        HttpResponse.json({
          ...sampleStarredProject(),
        }),
      ),
      http.delete('*/api/projects/1/star', () => {
        deleteCalls.push(1);
        return new HttpResponse(null, { status: 204 });
      }),
    );
    renderProject('/projects/1');

    await screen.findByRole('heading', { name: 'crop-triage', level: 1 });
    const button = screen.getByRole('button', { name: 'Un-star this project' });
    expect(button).toHaveAttribute('aria-pressed', 'true');

    await user.click(button);
    await waitFor(() => expect(deleteCalls).toEqual([1]));
  });
});

function sampleStarredProject() {
  return {
    id: 1,
    problem_id: 1,
    problem_title: 'Crop disease triage for small farms',
    repo_url: 'https://github.com/demo-farmer/crop-triage',
    repo_owner: 'demo-farmer',
    repo_name: 'crop-triage',
    open_for_contributors: true,
    verification_status: 'verified',
    solution_summary: 'A phone-first triage flow with an offline capture queue.',
    completed_at: null,
    demo_url: null,
    reflection: null,
    relevance_reason: null,
    ownership_basis: null,
    review_note: null,
    owner: { username: 'demo-farmer', avatar_url: null },
    progress: null,
    progress_updated_at: null,
    star_count: 3,
    starred_by_me: true,
  };
}

const ME_LOGGED_IN_VIEWER = {
  id: 9,
  username: 'just-looking',
  name: 'Just Looking',
  avatar_url: null,
};
