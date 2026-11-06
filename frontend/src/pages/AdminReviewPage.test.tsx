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

const PENDING = {
  id: 42,
  title: 'Landslide warning system',
  summary: 'A generated summary.',
  who_affected: 'District teams',
  why_matters: 'Warnings save lives.',
  field: 'geospatial',
  domain: 'disaster-management',
  difficulty: 'intermediate',
  est_hours: 40,
  tech_tags: ['python'],
  datasets: [],
  approaches: [],
  source_name: 'Smart India Hackathon 2026',
  source_id: 'SIH26001',
  source_url: 'https://sih.gov.in/sih2026PS#SIH26001',
  source_note: null,
  ai_fields: [],
  project_count: 0,
  origin: 'manual',
  source_year: 2026,
  organisation: 'MDoNER',
  deadline: null,
  status: 'pending_review',
  created_at: '2026-11-03T10:00:00Z',
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
  it('shows pending items with evidence and sends moderation actions', async () => {
    let approved = false;
    server.use(
      http.get('*/api/auth/me', () => HttpResponse.json(ADMIN)),
      http.get('*/api/admin/review', () =>
        HttpResponse.json({ items: [PENDING], total: 1 }),
      ),
      http.post('*/api/admin/problems/42/approve', () => {
        approved = true;
        return HttpResponse.json({ ok: true, problem_id: 42, status: 'published' });
      }),
    );

    renderPage();

    expect(
      await screen.findByRole('heading', { name: 'Landslide warning system' }),
    ).toBeInTheDocument();
    expect(screen.getByText('SIH26001')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /View original/ })).toHaveAttribute(
      'href',
      PENDING.source_url,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Approve' }));
    await waitFor(() => expect(approved).toBe(true));
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
