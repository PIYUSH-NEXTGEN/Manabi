import { Routes, Route } from 'react-router-dom';
import { screen } from '@testing-library/react';
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
    );

    renderProject('/projects/2');

    expect(
      await screen.findByText(/Progress unknown — hit refresh/i),
    ).toBeInTheDocument();
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
});
