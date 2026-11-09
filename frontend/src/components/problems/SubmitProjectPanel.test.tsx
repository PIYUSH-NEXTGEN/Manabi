import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { SubmitProjectPanel } from './SubmitProjectPanel';
import { renderWithProviders } from '@/test/renderWithProviders';

const LOGGED_IN = {
  id: 9,
  username: 'demo-farmer',
  name: 'Demo Farmer',
  avatar_url: null,
};

function renderPanel() {
  return renderWithProviders(
    <ToastProvider>
      <SubmitProjectPanel problemId={1} />
    </ToastProvider>,
  );
}

const REPO_LABEL = /GitHub repo URL/i;

describe('SubmitProjectPanel', () => {
  it('asks logged-out visitors to log in with GitHub', async () => {
    renderPanel();

    expect(
      await screen.findByRole('link', { name: 'Log in with GitHub' }),
    ).toHaveAttribute('href', '/api/auth/github/login');
    expect(screen.queryByRole('button', { name: 'Submit project' })).not.toBeInTheDocument();
  });

  it('blocks non-GitHub URLs before touching the network', async () => {
    const user = userEvent.setup();
    let networkCalled = false;
    server.use(
      http.post('*/api/problems/1/projects', () => {
        networkCalled = true;
        return HttpResponse.json({ ok: true }, { status: 201 });
      }),
    );
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)),
    );
    renderPanel();

    await screen.findByLabelText(REPO_LABEL);
    await user.type(screen.getByLabelText(REPO_LABEL), 'https://gitlab.com/owner/name');
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Use a GitHub repo URL like https://github.com/owner/name',
    );
    await waitFor(() => expect(networkCalled).toBe(false));
  });

  it('blocks invalid demo links before touching the network', async () => {
    const user = userEvent.setup();
    let networkCalled = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)),
      http.post('*/api/problems/1/projects', () => {
        networkCalled = true;
        return HttpResponse.json({ ok: true }, { status: 201 });
      }),
    );
    renderPanel();

    await screen.findByLabelText(REPO_LABEL);
    await user.type(screen.getByLabelText(REPO_LABEL), 'https://github.com/owner/name');
    await user.type(screen.getByLabelText(/Deployed link/i), 'not-a-url');
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'The deployed link must start with http:// or https://',
    );
    await waitFor(() => expect(networkCalled).toBe(false));
  });

  it('maps the backend error codes to plain language per case', async () => {
    const user = userEvent.setup();
    let attempts = 0;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)),
      http.post('*/api/problems/1/projects', () => {
        attempts += 1;
        const cases: Array<[number, { detail: { code: string; message: string } }]> = [
          [403, { detail: { code: 'not_repo_owner', message: 'You can only submit repositories you own' } }],
          [409, { detail: { code: 'already_submitted', message: 'You already linked this repository to this problem.' } }],
          [409, { detail: { code: 'invalid_demo_url', message: 'Demo link must be a plain http(s) URL.' } }],
        ];
        const next = cases[(attempts - 1) % cases.length]!;
        return HttpResponse.json(next[1], { status: next[0] });
      }),
    );
    renderPanel();

    await screen.findByLabelText(REPO_LABEL);
    await user.type(screen.getByLabelText(REPO_LABEL), 'https://github.com/owner/name');
    await user.click(await screen.findByRole('button', { name: 'Submit project' }));
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'You can only submit repositories you own',
    );

    // The form is swapped for the progress card while pending, so the button
    // is remounted each time the panel returns to the submission state.
    await user.click(
      await screen.findByRole('button', { name: 'Submit project' }),
    );
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'You already linked this repository to this problem.',
    );

    await user.click(
      await screen.findByRole('button', { name: 'Submit project' }),
    );
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'The deployed link must be a plain http(s) URL, at most 500 characters.',
    );
  });

  it('shows the catch-all wording for 429 bursts', async () => {
    const user = userEvent.setup();
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)),
      http.post('*/api/problems/1/projects', () =>
        HttpResponse.json(
          { detail: { code: 'rate_limited', message: 'Too many submissions this hour - try again later.' } },
          { status: 429 },
        ),
      ),
    );
    renderPanel();

    await screen.findByLabelText(REPO_LABEL);
    await user.type(screen.getByLabelText(REPO_LABEL), 'https://github.com/owner/name');
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Too many attempts — wait a bit before trying again.',
    );
  });

  it('shows the accepted panel with a link to the project page', async () => {
    const user = userEvent.setup();
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)),
      http.post('*/api/problems/1/projects', () =>
        HttpResponse.json(
          {
            id: 77,
            problem_id: 1,
            problem_title: 'Crop disease triage for small farms',
            repo_url: 'https://github.com/demo-farmer/crop-triage',
            repo_owner: 'demo-farmer',
            repo_name: 'crop-triage',
            open_for_contributors: false,
            verification_status: 'needs_review',
            solution_summary: null,
            completed_at: null,
            demo_url: null,
            reflection: null,
            relevance_reason: 'Automatic check could not fully confirm relevance',
            ownership_basis: 'push_access',
            review_note: null,
            owner: { username: 'demo-farmer', avatar_url: null },
            progress: null,
            progress_updated_at: null,
          },
          { status: 201 },
        ),
      ),
    );
    renderPanel();

    await screen.findByLabelText(REPO_LABEL);
    await user.type(screen.getByLabelText(REPO_LABEL), 'https://github.com/demo-farmer/crop-triage');
    await user.click(screen.getByRole('button', { name: 'Submit project' }));

    expect(await screen.findByRole('heading', { name: 'Submitted' })).toBeInTheDocument();
    expect(
      screen.getByText(/awaiting review and will go public once the check confirms it/i),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open project page' })).toHaveAttribute(
      'href',
      '/projects/77',
    );
    expect(await screen.findByRole('status')).toHaveTextContent('Submission received.');
  });
});
