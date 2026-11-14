import { Routes, Route } from 'react-router-dom';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
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
  it('shows greeting and own projects by name with progress badges', async () => {
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

    expect(screen.queryByRole('heading', { name: 'For you' })).not.toBeInTheDocument();
  });

  it('shows honest empty states when there are no projects', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json([])),
    );
    renderDashboard();

    expect(await screen.findByText(/No projects yet/i)).toBeInTheDocument();
  });

  it('shows the backend error detail honestly when GitHub activity fails', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () =>
        HttpResponse.json({ detail: 'GitHub token expired' }, { status: 401 }),
      ),
      );
    renderDashboard();

    expect(await screen.findByText('GitHub token expired')).toBeInTheDocument();
  });

  it('saves edits, clears fields with an empty string, and closes the dialog', async () => {
    const user = userEvent.setup();
    const bodies: Array<Record<string, unknown>> = [];
    const project = { ...MY_PROJECTS[0], demo_url: 'https://example.com/demo' };
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json([project])),
      http.patch('*/api/projects/1', async ({ request }) => {
        const body = (await request.json()) as Record<string, unknown>;
        bodies.push(body);
        return HttpResponse.json({ ...project, ...body });
      }),
    );
    renderDashboard();

    await user.click(await screen.findByRole('button', { name: 'Edit' }));
    expect(screen.getByRole('dialog')).toBeVisible();

    await user.clear(screen.getByRole('textbox', { name: /Description/ }));
    await user.clear(screen.getByLabelText(/Demo URL/));
    await user.click(screen.getByRole('button', { name: 'Save changes' }));

    await waitFor(() =>
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument(),
    );
    expect(bodies).toEqual([
      {
        solution_summary: '',
        demo_url: '',
        open_for_contributors: true,
      },
    ]);
    expect(await screen.findByRole('status')).toHaveTextContent('Project saved.');
  });

  it('removes a project from the board and closes the confirm dialog', async () => {
    const user = userEvent.setup();
    let rows = [...MY_PROJECTS];
    let deleted = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () => HttpResponse.json(rows)),
      http.delete('*/api/projects/1', () => {
        deleted = true;
        rows = [];
        return new HttpResponse(null, { status: 204 });
      }),
    );
    renderDashboard();

    await user.click(await screen.findByRole('button', { name: 'Remove' }));
    expect(screen.getByRole('dialog')).toBeVisible();
    await user.click(screen.getByRole('button', { name: 'Yes, remove it' }));

    await waitFor(() =>
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument(),
    );
    expect(deleted).toBe(true);
    expect(await screen.findByText(/No projects yet/)).toBeInTheDocument();
    expect(await screen.findByRole('status')).toHaveTextContent(
      'crop-triage removed.',
    );
  });

  it('never shows mark-complete, reopen, or completed UI', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/me/projects', () =>
        HttpResponse.json([
          {
            ...MY_PROJECTS[0],
            completed_at: '2026-11-01T10:00:00Z',
          },
        ]),
      ),
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

    await screen.findByText('Logged in as Ml Learner');
    expect(
      screen.queryByRole('button', { name: 'Mark complete' }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Reopen' })).not.toBeInTheDocument();
    expect(screen.queryByText('✓ Completed')).not.toBeInTheDocument();
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
    // The redirect to the home catalog may complete after the toast appears.
    await waitFor(
      () =>
        expect(screen.getByRole('heading', { level: 1 })).not.toHaveTextContent(
          'Dashboard',
        ),
      { timeout: 5000 },
    );
  });
});
