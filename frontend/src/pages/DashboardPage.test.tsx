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
    owner: { username: 'ml-learner', avatar_url: null },
    progress: null,
    progress_updated_at: null,
  },
];

const RECOMMENDATIONS = {
  items: [
    {
      problem: {
        id: 5,
        title: 'Attendance pipeline that fails loudly',
        summary:
          'A school network imports biometric attendance CSVs; silent row drops must become alerts.',
        who_affected: 'School network administrators',
        why_matters: 'Silent data loss hides absent children.',
        field: 'data-engineering',
        domain: 'education',
        difficulty: 'beginner',
        est_hours: 24,
        tech_tags: ['python', 'airflow', 'pytest'],
        datasets: [],
        approaches: [],
        source_name: 'TCOE',
        source_id: 'TCOE PS03',
        source_url: null,
        source_note: null,
        project_count: 0,
        ai_fields: [],
      },
      score: 3,
      reasons: ['Matches your python and pytest tags', 'Beginner fits your level'],
    },
  ],
};

function renderDashboard() {
  return renderWithProviders(
    <Routes>
      <Route path="/me" element={<DashboardPage />} />
    </Routes>,
    { route: '/me' },
  );
}

describe('DashboardPage', () => {
  it('shows greeting, own projects with progress badges, and scored recommendations', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json(MY_PROJECTS)),
      http.get('*/api/recommendations', () => HttpResponse.json(RECOMMENDATIONS)),
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
    );
    renderDashboard();

    expect(await screen.findByText('Logged in as Ml Learner')).toBeInTheDocument();
    expect(
      await screen.findByRole('link', { name: 'ml-learner' }),
    ).toHaveAttribute('href', '/projects/1');
    expect(await screen.findByText('ACTIVE')).toBeInTheDocument();

    expect(
      await screen.findByText('Attendance pipeline that fails loudly'),
    ).toBeInTheDocument();
    expect(screen.getByText('score 3')).toBeInTheDocument();
    expect(
      screen.getByText('+ Matches your python and pytest tags'),
    ).toBeInTheDocument();
    expect(
      screen.getByText('+ Beginner fits your level'),
    ).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'For you', level: 2 })).toBeInTheDocument();
  });

  it('shows honest empty states when there are no projects and no matches', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json([])),
      http.get('*/api/recommendations', () => HttpResponse.json({ items: [] })),
    );
    renderDashboard();

    expect(await screen.findByText(/No projects yet/i)).toBeInTheDocument();
    expect(
      await screen.findByText(/Nothing matched yet/i),
    ).toBeInTheDocument();
    expect(screen.queryByText('score 0')).not.toBeInTheDocument();
  });

  it('shows the backend error detail honestly when recommendations fail', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () =>
        HttpResponse.json({ detail: 'GitHub token expired' }, { status: 401 }),
      ),
      http.get('*/api/recommendations', () =>
        HttpResponse.json({ detail: 'Scoring failed' }, { status: 500 }),
      ),
    );
    renderDashboard();

    expect(await screen.findByText('GitHub token expired')).toBeInTheDocument();
    expect(await screen.findByText('Scoring failed')).toBeInTheDocument();
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
