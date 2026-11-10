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
  const TECH_SECTION_TITLES = new Set([
    'Why it matters',
    "What concepts you'll learn",
    'Tech stack',
    'Team plan',
    'Pitch guide',
  ]);

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

  it('derives build-guide phases from approaches when there is no curated guide', async () => {
    renderDetail('/problems/1');

    await screen.findByRole('heading', { level: 1 });
    expect(
      await screen.findByRole('heading', { name: 'Build guide' }),
    ).toBeInTheDocument();
    expect(
      await screen.findByText('Fine-tune a small CNN on public leaf datasets'),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Build an offline-first mobile capture flow'),
    ).toBeInTheDocument();
  });

  it('renders the curated build guide with numbered phase steps', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 1,
          title: 'Crop disease triage for small farms',
          summary: 'Farmers photograph leaf blight.',
          who_affected: 'Smallholder farmers',
          why_matters: 'Late detection destroys a season of income.',
          field: 'aiml',
          domain: 'agriculture',
          difficulty: 'beginner',
          est_hours: 20,
          tech_tags: ['python'],
          datasets: [],
          approaches: [],
          source_name: 'SIH 2026',
          source_id: 'SIH26017',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          build_guide: [
            {
              title: 'Model the data',
              summary: 'Decide what a report and a case look like.',
              steps: ['List the fields a report needs', 'Design the log as append-only'],
            },
            {
              title: 'Build the scheduler',
              summary: '',
              steps: [],
            },
          ],
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/1');
    await screen.findByRole('heading', { level: 1 });
    expect(
      await screen.findByRole('heading', { name: 'Build guide' }),
    ).toBeInTheDocument();
    expect(screen.getByText('Model the data')).toBeInTheDocument();
    expect(
      screen.getByText('Decide what a report and a case look like.'),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Design the log as append-only'),
    ).toBeInTheDocument();
    expect(screen.getByText('Build the scheduler')).toBeInTheDocument();
    expect(
      screen.queryByText(/No phased guide for this brief yet/i),
    ).not.toBeInTheDocument();
  });

  it('shows the no-guide fallback when there is neither a curated guide nor approaches', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 1,
          title: 'Crop disease triage for small farms',
          summary: 'Farmers photograph leaf blight.',
          who_affected: 'Smallholder farmers',
          why_matters: 'Late detection destroys a season of income.',
          field: 'aiml',
          domain: 'agriculture',
          difficulty: 'beginner',
          est_hours: 20,
          tech_tags: ['python'],
          datasets: [],
          approaches: [],
          source_name: 'SIH 2026',
          source_id: 'SIH26017',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/1');
    await screen.findByRole('heading', { level: 1 });

    expect(
      await screen.findByText(/No phased guide for this brief yet/i),
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

  it('renders a multi-paragraph description from the summary', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 1,
          title: 'Crop disease triage for small farms',
          summary:
            'Farmers photograph leaf blight; a triage flow routes cases.\n\n' +
            'Wire the capture flow to the officer queue so nothing is retryped.',
          who_affected: 'Smallholder farmers',
          why_matters: 'Late detection destroys a season of income.',
          field: 'aiml',
          domain: 'agriculture',
          difficulty: 'beginner',
          est_hours: 20,
          tech_tags: ['python'],
          datasets: [],
          approaches: [],
          source_name: 'SIH 2026',
          source_id: 'SIH26017',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/1');
    await screen.findByRole('heading', { level: 1 });

    expect(
      await screen.findByText(
        /Farmers photograph leaf blight; a triage flow routes cases\./,
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /Wire the capture flow to the officer queue so nothing is retryped\./,
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/This project is for smallholder farmers\./),
    ).toBeInTheDocument();
  });

  it('does not render a building count line under the description', async () => {
    renderDetail('/problems/1');
    await screen.findByRole('heading', { level: 1 });

    expect(screen.queryByText(/0 building/i)).not.toBeInTheDocument();
  });

  it('replaces the description with problem-statement blocks for a hackathon brief', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 42,
          title: 'Streetlight outage tracker',
          summary: 'Citizens report dead streetlights and nothing comes back.',
          who_affected: 'Municipal ward offices',
          why_matters: 'Dark streets cost money and feel unsafe.',
          field: 'web-dev',
          domain: 'governance',
          difficulty: 'intermediate',
          est_hours: 40,
          tech_tags: ['typescript', 'react', 'postgres'],
          datasets: [],
          approaches: ['Dedupe reports by pole', 'Escalate stale SLAs'],
          source_name: 'TCOE',
          source_id: 'TCOE PS12',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          goal: 'hackathon',
          team_plan: null,
          pitch_guide: null,
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/42');
    await screen.findByRole('heading', { level: 1 });

    expect(await screen.findByText('The problem')).toBeInTheDocument();
    expect(screen.getByText('Who faces it, and how')).toBeInTheDocument();
    expect(screen.getByText('How it gets fixed')).toBeInTheDocument();
    expect(screen.getByText('Citizens report dead streetlights and nothing comes back.')).toBeInTheDocument();
    expect(
      screen.getAllByText('Dedupe reports by pole').length,
    ).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText(/This project is for/)).not.toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Why it matters' }),
    ).not.toBeInTheDocument();
    // Team plan and pitch guide stay hidden when there is no curated data.
    expect(
      screen.queryByRole('heading', { name: 'Team plan' }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Pitch guide' }),
    ).not.toBeInTheDocument();
    // Build guide is still there and comes after the tech stack.
    expect(
      screen.getByRole('heading', { name: 'Build guide' }),
    ).toBeInTheDocument();
  });

  it('renders the team plan and pitch guide for a hackathon brief with a pitch kit', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 42,
          title: 'Streetlight outage tracker',
          summary: 'Citizens report dead streetlights and nothing comes back.',
          who_affected: 'Municipal ward offices',
          why_matters: 'Dark streets cost money and feel unsafe.',
          field: 'web-dev',
          domain: 'governance',
          difficulty: 'intermediate',
          est_hours: 40,
          tech_tags: ['typescript', 'react', 'postgres'],
          datasets: [],
          approaches: ['Dedupe reports by pole'],
          source_name: 'TCOE',
          source_id: 'TCOE PS12',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          goal: 'hackathon',
          team_plan: {
            note: '3 people, 24 hours.',
            roles: [
              { role: 'API', covers: 'Reports + statuses.' },
              { role: 'Web app', covers: 'Forms and dashboards.' },
            ],
            milestones: ['Hour 8: demo path works.'],
          },
          pitch_guide: {
            one_liner: 'Complaints become trackable tickets.',
            beats: [
              { heading: 'Hook', text: 'Have you reported a pothole and never heard back?' },
              { heading: 'Demo', text: 'File, assign, resolve, live.' },
            ],
            judge_questions: [
              {
                question: 'Why would a municipality adopt this?',
                answer: 'It replaces a phone log at zero cost to try.',
              },
            ],
          },
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/42');
    await screen.findByRole('heading', { level: 1 });

    expect(
      await screen.findByRole('heading', { name: 'Team plan' }),
    ).toBeInTheDocument();
    expect(screen.getByText('3 people, 24 hours.')).toBeInTheDocument();
    expect(screen.getByText('API')).toBeInTheDocument();
    expect(screen.getByText('Reports + statuses.')).toBeInTheDocument();
    expect(screen.getByText('Hour 8: demo path works.')).toBeInTheDocument();

    expect(
      screen.getByRole('heading', { name: 'Pitch guide' }),
    ).toBeInTheDocument();
    expect(screen.getByText('Complaints become trackable tickets.')).toBeInTheDocument();
    expect(screen.getByText('Have you reported a pothole and never heard back?')).toBeInTheDocument();
    expect(
      screen.getByText('Questions the judges may ask'),
    ).toBeInTheDocument();
    expect(
      screen.getByText('Why would a municipality adopt this?'),
    ).toBeInTheDocument();

    // Build guide renders last among the numbered article sections.
    const headings = screen.getAllByRole('heading', { level: 2 });
    const numberedTitles = headings
      .map((heading) => heading.textContent ?? '')
      .filter((title) => TECH_SECTION_TITLES.has(title) || title === 'Build guide');
    expect(numberedTitles[numberedTitles.length - 1]).toBe('Build guide');
  });

  it('renders the resume kit sections for a resume brief in order', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 42,
          title: 'Attendance pipeline that fails loudly',
          summary:
            'Biometric attendance CSVs go silent when rows drop mid-way.',
          who_affected: 'School network administrators',
          why_matters: 'Silent data loss hides absent children.',
          field: 'data-science',
          domain: 'developer-tools',
          difficulty: 'advanced',
          est_hours: 90,
          tech_tags: ['python', 'alerting'],
          datasets: [],
          approaches: ['Row-count reconciliation'],
          source_name: 'MANABI Curated',
          source_id: 'manabi-ds-advanced-007',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          goal: 'resume',
          resume_kit: {
            scope_levels: [
              {
                level: 'Good enough (MVP)',
                text: 'One pipeline wired to one alerts feed.',
                checks: ['Freshness check per table', 'Row counts stored per run'],
              },
              {
                level: 'Impressive',
                text: 'Baselines and named downstream impact.',
                checks: ['Distribution checks'],
              },
            ],
            target_roles: [
              { role: 'Data engineer', how_it_helps: 'Monitoring is the day job.' },
              { role: 'DevOps / SRE', how_it_helps: 'Alert fatigue, runbooks.' },
            ],
            resume_bullets: [
              {
                bullet: 'Built a monitor covering {N} feeds.',
                example: 'Built a monitor covering 5 feeds.',
              },
            ],
            interview_points: [
              {
                question: "How do you decide what counts as 'bad data'?",
                answer: 'Freshness, completeness, validity, distribution.',
              },
            ],
            differentiators: ['Write the runbook.'],
          },
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/42');
    await screen.findByRole('heading', { level: 1 });

    // Section headings appear in the fixed resume order...
    const headline = await screen.findByText('Good enough (MVP)');
    expect(headline).toBeInTheDocument();

    expect(
      screen.getByRole('heading', { name: 'MVP vs standout' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Roles it helps with' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Resume bullet template' }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: 'Interview talking points' }),
    ).toBeInTheDocument();

    // ...nothing renders for the removed or non-resume sections...
    expect(
      screen.queryByRole('heading', { name: 'How to stand out' }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Why it matters' }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Tech stack' }),
    ).not.toBeInTheDocument();
    expect(screen.getByText('Monitoring is the day job.')).toBeInTheDocument();
    expect(screen.getByText('Built a monitor covering 5 feeds.')).toBeInTheDocument();

    // ...and Build guide is the last numbered section.
    const headings = screen.getAllByRole('heading', { level: 2 });
    const numberedTitles = headings
      .map((heading) => heading.textContent ?? '')
      .filter((title) => TECH_SECTION_TITLES.has(title) || title === 'Build guide');
    expect(numberedTitles[numberedTitles.length - 1]).toBe('Build guide');
  });

  it('stars a submitted project straight from the brief page', async () => {
    const user = userEvent.setup();
    let starCalls = 0;
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 9,
          username: 'just-looking',
          name: 'Just Looking',
          avatar_url: null,
        }),
      ),
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 42,
          title: 'Attendance pipeline that fails loudly',
          summary: 'Biometric attendance CSVs go silent when rows drop.',
          who_affected: 'School network administrators',
          why_matters: 'Silent data loss hides absent children.',
          field: 'data-science',
          domain: 'developer-tools',
          difficulty: 'advanced',
          est_hours: 90,
          tech_tags: ['python'],
          datasets: [],
          approaches: ['Row-count reconciliation'],
          source_name: 'MANABI Curated',
          source_id: 'manabi-ds-advanced-007',
          source_url: null,
          source_note: null,
          project_count: 1,
          completed_count: 0,
          ai_fields: [],
          goal: null,
          projects: [
            {
              id: 11,
              problem_id: 42,
              problem_title: 'Attendance pipeline that fails loudly',
              repo_url: 'https://github.com/school-ops/attendance-loud',
              repo_owner: 'school-ops',
              repo_name: 'attendance-loud',
              open_for_contributors: true,
              owner: { username: 'school-ops', avatar_url: null },
              progress: null,
              progress_updated_at: null,
              verification_status: 'verified',
              solution_summary: null,
              completed_at: null,
              demo_url: null,
              reflection: null,
              relevance_reason: null,
              ownership_basis: null,
              review_note: null,
              star_count: 1,
              starred_by_me: false,
            },
          ],
          display_policy: 'summary_plus_excerpt',
          original_text: 'verbatim',
        }),
      ),
      http.post('*/api/projects/11/star', () => {
        starCalls += 1;
        return HttpResponse.json({ ok: true, star_count: 2 }, { status: 201 });
      }),
    );

    renderDetail('/problems/42');
    await screen.findByRole('heading', { level: 1 });

    const button = await screen.findByRole('button', {
      name: 'Star this project',
    });
    expect(screen.getByText('1')).toBeInTheDocument();
    await user.click(button);

    expect(
      await screen.findByRole('status'),
    ).toHaveTextContent('Starred. Thanks for the signal.');
    expect(starCalls).toBe(1);
  });

  it('keeps the paragraph description and no pitch sections for the learning brief', async () => {
    server.use(
      http.get('*/api/problems/:id', () =>
        HttpResponse.json({
          id: 3,
          title: 'Study Flashcards App',
          summary: 'Cards return right before you forget them.',
          who_affected: 'Self-learners',
          why_matters: 'Cramming fades; spacing sticks.',
          field: 'web-dev',
          domain: 'education',
          difficulty: 'beginner',
          est_hours: 30,
          tech_tags: ['react'],
          datasets: [],
          approaches: ['Implement SM-2'],
          source_name: 'MANABI Curated',
          source_id: 'manabi-learning-001',
          source_url: null,
          source_note: null,
          project_count: 0,
          completed_count: 0,
          ai_fields: [],
          goal: 'learning',
          team_plan: {
            note: 'Should not show on learning briefs.',
            roles: [],
            milestones: [],
          },
          pitch_guide: {
            one_liner: 'Should not show on learning briefs.',
            beats: [],
            judge_questions: [],
          },
          build_guide: [
            { title: 'Model the data', summary: 'Three shapes.', steps: ['Card', 'Deck'] },
          ],
          projects: [],
        }),
      ),
    );

    renderDetail('/problems/3');
    await screen.findByRole('heading', { level: 1 });

    expect(
      await screen.findByText(/This project is for self-learners/),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Team plan' }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Pitch guide' }),
    ).not.toBeInTheDocument();
    expect(screen.getByText('Model the data')).toBeInTheDocument();
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

    expect(
      await screen.findByText(/added to the problem board with a progress badge/i),
    ).toBeInTheDocument();
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
