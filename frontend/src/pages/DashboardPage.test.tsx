import { Routes, Route } from 'react-router-dom';
import { screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { RequireAuth } from '@/components/auth/RequireAuth';
import { HomePage } from './HomePage';
import { DashboardPage } from './DashboardPage';
import { ToastProvider } from '@/design/primitives';
import { renderWithProviders } from '@/test/renderWithProviders';

const ME_200 = {
  id: 9,
  username: 'ml-learner',
  name: 'Ml Learner',
  avatar_url: null,
};

const MY_PROJECTS = [
  {
    id: 1,
    problem_id: 1,
    problem_title: 'Crop disease triage for small farms',
    repo_url: 'https://github.com/ml-learner/crop-triage',
    repo_owner: 'ml-learner',
    repo_name: 'crop-triage',
    open_for_contributors: true,
    verification_status: 'verified',
    solution_summary: 'Triage flow description long enough for verification tests here.',
    completed_at: null,
    demo_url: null,
    reflection: null,
    relevance_reason: null,
    ownership_basis: null,
    review_note: null,
    owner: { username: 'ml-learner', avatar_url: null },
    progress: null,
    progress_updated_at: null,
  },
];

function renderDashboard() {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path="/me" element={<DashboardPage />} />
      </Routes>
    </ToastProvider>,
    { route: '/me' },
  );
}

describe('DashboardPage', () => {
  it('shows greeting, own projects by name with progress badges, and the GitHub heatmap', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json(MY_PROJECTS)),
      http.get('*/api/projects/1/progress', () =>
        HttpResponse.json({
          status: 'active',
          commit_count: 14,
          last_commit_at: '2026-10-16T09:24:00Z',
          has_readme: true,
          recent_commits: [],
          open_issues: [],
        }),
      ),
      http.get('*/api/me/github-heatmap', () =>
        HttpResponse.json({
          days: [
            { date: '2026-11-01', count: 3 },
            { date: '2026-11-02', count: 0 },
          ],
          total: 3,
          window_days: 91,
        }),
      ),
    );
    renderDashboard();

    expect(await screen.findByText('Logged in as Ml Learner')).toBeInTheDocument();
    const logOut = await screen.findByRole('button', { name: 'Log out' });
    // top right: not nested inside the greeting paragraph anymore
    expect(logOut.closest('p')).toBeNull();

    expect(
      await screen.findByRole('link', { name: 'crop-triage' }),
    ).toHaveAttribute('href', '/projects/1');
    expect(screen.queryByRole('link', { name: 'ml-learner' })).not.toBeInTheDocument();
    expect(screen.getByText('Crop disease triage for small farms')).toBeInTheDocument();
    expect(await screen.findByText('ACTIVE')).toBeInTheDocument();

    expect(await screen.findByText('GitHub activity')).toBeInTheDocument();
    expect(screen.getByText('3 pushes · public · last 13 weeks')).toBeInTheDocument();
    expect(
      screen.getByText(/Public pushes by ml-learner/i),
    ).toBeInTheDocument();

    expect(screen.queryByRole('heading', { name: 'For you' })).not.toBeInTheDocument();
  });

  it('shows honest empty states when there are no projects', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json([])),
      http.get('*/api/me/github-heatmap', () =>
        HttpResponse.json({ days: [], total: 0, window_days: 91 }),
      ),
    );
    renderDashboard();

    expect(await screen.findByText(/No projects yet/i)).toBeInTheDocument();
    expect(await screen.findByText('GitHub activity')).toBeInTheDocument();
    expect(await screen.findByText('0 pushes · public · last 13 weeks')).toBeInTheDocument();
  });

  it('shows the backend error detail honestly when GitHub activity fails', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () =>
        HttpResponse.json({ detail: 'GitHub token expired' }, { status: 401 }),
      ),
      http.get('*/api/me/github-heatmap', () =>
        HttpResponse.json({ detail: 'GitHub rate limit reached' }, { status: 403 }),
      ),
    );
    renderDashboard();

    expect(await screen.findByText('GitHub token expired')).toBeInTheDocument();
    expect(await screen.findByText('GitHub rate limit reached')).toBeInTheDocument();
  });

  it('redirects anonymous visitors to the home catalog and never renders the dashboard', async () => {
    renderWithProviders(
      <ToastProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/me"
            element={
              <RequireAuth>
                <DashboardPage />
              </RequireAuth>
            }
          />
        </Routes>
      </ToastProvider>,
      { route: '/me' },
    );

    expect(
      await screen.findByText('Log in with GitHub to reach your dashboard.'),
    ).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 1 })).not.toHaveTextContent(
      'Dashboard',
    );
  });
});
