import { Route, Routes } from 'react-router-dom';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { renderWithProviders } from '@/test/renderWithProviders';
import { AdminReviewPage } from './AdminReviewPage';

const ADMIN = {
  id: 1,
  username: 'admin',
  name: 'Admin',
  avatar_url: null,
  is_admin: true,
};

const PENDING_SUBMISSION = {
  id: 42,
  problem_id: 3,
  problem_title: 'Fraud pattern walkthrough for UPI micro-transactions',
  repo_url: 'https://github.com/demo-farmer/crop-triage',
  repo_owner: 'demo-farmer',
  repo_name: 'crop-triage',
  submitter: 'demo-farmer',
  submitter_avatar_url: null,
  verification_status: 'needs_review',
  ownership_basis: 'contributor',
  relevance_score: 0.42,
  relevance_reason: 'Linked to the problem by keywords',
  solution_summary: 'Drift baselines notebook for micro-transaction fraud.',
  review_note: null,
  demo_url: null,
  reflection: null,
  open_for_contributors: true,
  report_count: 0,
  created_at: '2026-11-04T08:00:00Z',
  completed_at: null,
};

function renderPage() {
  return renderWithProviders(
    <ToastProvider>
      <Routes>
        <Route path="/admin/review" element={<AdminReviewPage />} />
      </Routes>
    </ToastProvider>,
    { route: '/admin/review' },
  );
}

describe('AdminReviewPage', () => {
  it('lists submissions with evidence and approves them', async () => {
    let approved = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ADMIN)),
      http.get('*/api/admin/submissions', ({ request }) => {
        expect(new URL(request.url).searchParams.get('status')).toBe('needs_review');
        return HttpResponse.json({ items: [PENDING_SUBMISSION], total: 1 });
      }),
      http.post('*/api/admin/submissions/42/approve', () => {
        approved = true;
        return HttpResponse.json({
          ok: true,
          project_id: 42,
          verification_status: 'verified',
        });
      }),
    );

    renderPage();

    expect(
      await screen.findByRole('heading', { name: 'Fraud pattern walkthrough for UPI micro-transactions' }),
    ).toBeInTheDocument();
    expect(screen.getByText('contributor')).toBeInTheDocument();
    expect(screen.getByText('relevance 0.42')).toBeInTheDocument();
    expect(screen.getByText(/Drift baselines notebook/)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Approve' }));
    await waitFor(() => expect(approved).toBe(true));
  });

  it('rejects from the needs_review queue', async () => {
    let rejected = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ADMIN)),
      http.get('*/api/admin/submissions', () =>
        HttpResponse.json({ items: [PENDING_SUBMISSION], total: 1 }),
      ),
      http.post('*/api/admin/submissions/42/reject', () => {
        rejected = true;
        return HttpResponse.json({
          ok: true,
          project_id: 42,
          verification_status: 'rejected',
        });
      }),
    );

    renderPage();

    fireEvent.click(await screen.findByRole('button', { name: 'Reject' }));
    await waitFor(() => expect(rejected).toBe(true));
  });

  it('can switch the queue to the rejected filter', async () => {
    let askedForRejected = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ADMIN)),
      http.get('*/api/admin/submissions', ({ request }) => {
        const status = new URL(request.url).searchParams.get('status');
        if (status === 'rejected') {
          askedForRejected = true;
          return HttpResponse.json({ items: [], total: 0 });
        }
        return HttpResponse.json({ items: [PENDING_SUBMISSION], total: 1 });
      }),
    );

    renderPage();

    fireEvent.click(await screen.findByRole('button', { name: 'Rejected' }));
    await waitFor(() => expect(askedForRejected).toBe(true));
    expect(await screen.findByText(/Nothing in this queue/i)).toBeInTheDocument();
  });

  it('hides moderation controls from non-admins', async () => {
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({ ...ADMIN, username: 'student', is_admin: false }),
      ),
    );
    renderPage();
    expect(
      await screen.findByText(/Admin access required/),
    ).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Approve' })).not.toBeInTheDocument();
  });
});
