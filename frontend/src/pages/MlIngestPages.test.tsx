import { Routes, Route } from 'react-router-dom';
import type { ReactElement } from 'react';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { IngestPage } from './IngestPage';
import { MlQuestionPage } from './MlQuestionPage';
import { MlQuestionsPage } from './MlQuestionsPage';
import { renderWithProviders } from '@/test/renderWithProviders';

function renderPage(ui: ReactElement, route: string, pattern: string) {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path={pattern} element={ui} />
      </Routes>
    </ToastProvider>,
    { route },
  );
}

const ME_200 = {
  id: 9,
  username: 'ml-learner',
  name: 'Ml Learner',
  avatar_url: null,
};

describe('MlQuestionsPage', () => {
  it('renders the question list with topic, difficulty, attempt state', async () => {
    renderPage(<MlQuestionsPage />, '/ml', '/ml');

    expect(
      await screen.findByRole('heading', { name: 'ML Practice', level: 1 }),
    ).toBeInTheDocument();
    expect(
      await screen.findByRole('heading', {
        name: 'Train or test first? Splitting a tiny dataset',
        level: 2,
      }),
    ).toBeInTheDocument();
    expect(await screen.findByText(/train-test-split/i)).toBeInTheDocument();
    expect(await screen.findAllByText('Not attempted yet')).toHaveLength(5);
  });

  it('marks attempted questions via the attempts/me API when logged in', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/ml/questions/1/attempts/me', () =>
        HttpResponse.json({
          id: 3,
          answer: 'I checked the feature table first.',
          created_at: '2026-10-17T09:00:00Z',
          feedback: {
            covered_count: 1,
            total: 2,
            items: [
              { point: 'Check the traffic split', covered: true },
              { point: 'Add monitoring', covered: false },
            ],
            summary: 'Half of it.',
          },
          explanation: 'The answer.',
        }),
      ),
      http.get('*/api/ml/questions/2/attempts/me', () =>
        HttpResponse.json({ detail: 'No attempt yet' }, { status: 404 }),
      ),
    );

    renderPage(<MlQuestionsPage />, '/ml', '/ml');

    expect(
      await screen.findByText('The model works offline, fails online'),
    ).toBeInTheDocument();
    expect(await screen.findAllByText('Attempted')).toHaveLength(1);
    expect(await screen.findAllByText('Not attempted yet')).toHaveLength(4);
  });
});

describe('MlQuestionPage', () => {
  it('renders the scenario verbatim and hard-stamped from the contract', async () => {
    renderPage(<MlQuestionPage />, '/ml/1', '/ml/:id');

    expect(
      await screen.findByRole('heading', {
        name: 'Train or test first? Splitting a tiny dataset',
        level: 1,
      }),
    ).toBeInTheDocument();
    const scenario = await screen.findByRole('region', {
      name: 'Scenario',
    });
    expect(scenario).toHaveTextContent('800 labeled customer reviews');
    expect(screen.queryByLabelText('Attempt area')).not.toBeInTheDocument();
    expect(screen.getByText(/Log in with GitHub to submit/i)).toBeInTheDocument();
  });

  it('rejects short answers on the client', async () => {
    server.use(http.get('*/api/auth/me', () => HttpResponse.json(ME_200)));

    const user = userEvent.setup();
    renderPage(<MlQuestionPage />, '/ml/1', '/ml/:id');

    await screen.findByRole('heading', { name: 'Your attempt' });
    await user.type(
      screen.getByLabelText(/How would you debug it/i),
      'too short',
    );
    await user.click(screen.getByRole('button', { name: 'Submit attempt' }));

    expect(
      await screen.findByText(/Write at least 20 characters/i),
    ).toBeInTheDocument();
  });

  it('submits the attempt and shows rubric feedback + explanation', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/ml/questions/1/attempts/me', () =>
        HttpResponse.json({ detail: 'No attempt yet' }, { status: 404 }),
      ),
    );

    const user = userEvent.setup();
    renderPage(<MlQuestionPage />, '/ml/1', '/ml/:id');

    await screen.findByRole('heading', { name: 'Your attempt' });
    await user.type(
      screen.getByLabelText(/How would you debug it/i),
      'First I would pull the served predictions and bucket them by day of week to confirm the Monday gap.',
    );
    await user.click(screen.getByRole('button', { name: 'Submit attempt' }));

    expect(
      await screen.findByText(/2 of 4 points covered/i),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/missed the monitoring angle/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Pull the served predictions and bucket by day-of-week/i),
    ).toHaveTextContent(
      'Pull the served predictions and bucket by day-of-week before anything else.',
    );
  });

  it('shows your saved attempt when one exists', async () => {
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.get('*/api/ml/questions/1/attempts/me', () =>
        HttpResponse.json({
          id: 3,
          answer: 'Checked the feature table for leakage first.',
          created_at: '2026-10-01T09:00:00Z',
          feedback: {
            covered_count: 1,
            total: 2,
            items: [{ point: 'Leakage audit', covered: true }],
            summary: 'Core point covered.',
          },
          explanation: 'Correct instinct.',
        }),
      ),
    );

    renderPage(<MlQuestionPage />, '/ml/1', '/ml/:id');

    expect(
      await screen.findByText(/Attempted on 2026-10-01/i),
    ).toBeInTheDocument();
    expect(
      await screen.findByText('Checked the feature table for leakage first.'),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/1 of 2 points covered/i),
    ).toBeInTheDocument();
  });

  it('renders the 404 page for a missing question', async () => {
    renderPage(<MlQuestionPage />, '/ml/999', '/ml/:id');

    expect(
      await screen.findByRole('heading', { name: /404/i, level: 1 }),
    ).toBeInTheDocument();
  });
});

describe('IngestPage', () => {
  it('requires either text or a URL before calling the API', async () => {
    const user = userEvent.setup();
    renderPage(<IngestPage />, '/ingest', '/ingest');

    expect(
      await screen.findByRole('heading', { name: 'Ingest', level: 1 }),
    ).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Draft the card' }));

    expect(
      await screen.findByText(/Paste the problem statement text/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/Structured draft/i)).not.toBeInTheDocument();
  });

  it('shows the AI draft with AI-SUGGESTED stamps and evidence', async () => {
    server.use(http.get('*/api/auth/me', () => HttpResponse.json(ME_200)));
    const user = userEvent.setup();
    renderPage(<IngestPage />, '/ingest', '/ingest');

    await user.type(
      screen.getByLabelText(/Problem statement/i),
      'Farmers photograph leaf blight and lose whole seasons.',
    );
    await user.click(screen.getByRole('button', { name: 'Draft the card' }));

    expect(
      await screen.findByText(/Structured draft/i),
    ).toBeInTheDocument();
    expect(await screen.findAllByText(/ai-suggested/i)).toHaveLength(4);
    expect(
      screen.getByText('Smallholder farmers across three districts'),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/citations behind each AI-drafted field/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/"farmers with <2 hectares in district 4\/5\/8"/i),
    ).toBeInTheDocument();
  });

  it('blocks draft submission with an honest login gate when logged out', async () => {
    const user = userEvent.setup();
    renderPage(<IngestPage />, '/ingest', '/ingest');

    await user.type(
      screen.getByLabelText(/Problem statement/i),
      'Farmers photograph leaf blight and lose whole seasons.',
    );
    await user.click(screen.getByRole('button', { name: 'Draft the card' }));

    expect(
      await screen.findByText(/Log in with GitHub first/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/Structured draft/i)).not.toBeInTheDocument();
  });

  it('publishes the draft to the board when filled', async () => {
    let problemPosts: Array<Record<string, unknown>> = [];
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ME_200)),
      http.post('*/api/problems', async ({ request }) => {
        problemPosts.push((await request.json()) as Record<string, unknown>);
        return HttpResponse.json(
          {
            id: 9,
            title: 'Crop disease triage for small farms',
            summary: 'Pasted.',
            who_affected: 'Someone',
            why_matters: 'It matters',
            field: 'computer-vision',
            domain: 'agriculture',
            difficulty: 'beginner',
            est_hours: 20,
            tech_tags: [],
            datasets: [],
            approaches: [],
            source_name: 'Pasted statement',
            source_id: null,
            source_url: null,
            source_note: null,
            project_count: 0,
            ai_fields: ['who_affected', 'why_matters', 'approaches'],
            projects: [],
            original_text: 'Pasted.',
          },
          { status: 201 },
        );
      }),
    );

    const user = userEvent.setup();
    renderPage(<IngestPage />, '/ingest', '/ingest');

    await user.type(
      screen.getByLabelText(/Problem statement/i),
      'Farmers photograph leaf blight and lose whole seasons.',
    );
    await user.click(screen.getByRole('button', { name: 'Draft the card' }));
    await user.click(
      await screen.findByRole('button', { name: 'Publish to the board' }),
    );

    expect(await screen.findByText(/It is on the board now/i)).toBeInTheDocument();
    expect(problemPosts).toHaveLength(1);
    expect(
      await screen.findByRole('link', { name: 'Open the card' }),
    ).toHaveAttribute('href', '/problems/9');
  });
});
