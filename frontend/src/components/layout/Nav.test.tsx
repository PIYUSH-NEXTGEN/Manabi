import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ToastProvider } from '@/design/primitives';
import { Nav } from './Nav';
import { renderWithProviders } from '@/test/renderWithProviders';

function renderNav() {
  return renderWithProviders(
    <ToastProvider>
      <Nav />
    </ToastProvider>,
  );
}

describe('Nav', () => {
  it('renders the wordmark and every section 11.3 link', () => {
    renderNav();

    expect(
      screen.getByRole('link', { name: 'MANABI' }),
    ).toHaveAttribute('href', '/');
    expect(screen.getAllByRole('link', { name: 'Problems' })[0]).toHaveAttribute(
      'href',
      '/problems',
    );
    expect(screen.getAllByRole('link', { name: 'ML Practice' })[0]).toHaveAttribute(
      'href',
      '/ml',
    );
    expect(screen.getAllByRole('link', { name: 'Ingest' })[0]).toHaveAttribute(
      'href',
      '/ingest',
    );
    expect(
      screen.getAllByRole('link', { name: 'How it works' })[0],
    ).toHaveAttribute('href', '/how-it-works');
  });

  it('shows the login button when nobody is logged in', async () => {
    renderNav();

    expect(
      await screen.findByRole('button', { name: 'Log in with GitHub' }),
    ).toBeInTheDocument();
    expect(screen.queryByText('demo-farmer')).not.toBeInTheDocument();
  });

  it('shows the signed-in username when the API returns a user', async () => {
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 7,
          username: 'demo-farmer',
          name: 'Demo Farmer',
          avatar_url: null,
        }),
      ),
    );

    renderWithProviders(
      <ToastProvider>
        <Nav />
      </ToastProvider>,
    );

    const userLink = await screen.findByRole('link', { name: 'demo-farmer' });
    expect(userLink).toHaveAttribute('href', '/me');
    expect(
      screen.queryByRole('button', { name: 'Log in with GitHub' }),
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: 'Log out' }),
    ).toBeInTheDocument();
  });

  it('logs out, posts to the API, and returns to the logged-out nav', async () => {
    const user = userEvent.setup();
    let logoutCalls = 0;
    let session = true;
    server.use(
      http.post('*/api/auth/logout', () => {
        logoutCalls += 1;
        session = false;
        return HttpResponse.json({});
      }),
      http.get('*/api/auth/me', () => {
        if (!session) {
          return HttpResponse.json(
            { detail: 'Not authenticated' },
            { status: 401 },
          );
        }
        return HttpResponse.json({
          id: 7,
          username: 'demo-farmer',
          name: 'Demo Farmer',
          avatar_url: null,
        });
      }),
    );

    renderWithProviders(
      <ToastProvider>
        <Nav />
      </ToastProvider>,
    );

    await screen.findByRole('button', { name: 'Log out' });
    await user.click(screen.getByRole('button', { name: 'Log out' }));

    expect(await screen.findByRole('button', { name: 'Log in with GitHub' }))
      .toBeInTheDocument();
    expect(
      await screen.findByText(/Logged out/i),
    ).toBeInTheDocument();
    expect(logoutCalls).toBe(1);
  });

  it('shows an error toast when logout fails', async () => {
    const user = userEvent.setup();
    server.use(
      http.post('*/api/auth/logout', () =>
        HttpResponse.json({ detail: 'session already gone' }, { status: 500 }),
      ),
      http.get('*/api/auth/me', () =>
        HttpResponse.json({
          id: 7,
          username: 'demo-farmer',
          name: 'Demo Farmer',
          avatar_url: null,
        }),
      ),
    );

    renderWithProviders(
      <ToastProvider>
        <Nav />
      </ToastProvider>,
    );

    await screen.findByRole('button', { name: 'Log out' });
    await user.click(screen.getByRole('button', { name: 'Log out' }));

    expect(
      await screen.findByText(/Log out failed/i),
    ).toBeInTheDocument();
  });
});
