import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { afterEach, describe, expect, it } from 'vitest';
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

afterEach(() => {
  document.documentElement.classList.remove('dark');
  document.documentElement.style.colorScheme = '';
  window.localStorage.clear();
});

describe('Nav', () => {
  it('renders the wordmark and every section link', () => {
    renderNav();

    expect(
      screen.getByRole('link', { name: 'MANABI' }),
    ).toHaveAttribute('href', '/');
    expect(screen.getAllByRole('link', { name: 'Projects' })[0]).toHaveAttribute(
      'href',
      '/problems',
    );
    expect(
      screen.getAllByRole('link', { name: 'Repo Analyzer' })[0],
    ).toHaveAttribute('href', '/repo-analyzer');
    expect(
      screen.getAllByRole('link', { name: 'Dashboard' })[0],
    ).toHaveAttribute('href', '/me');
  });

  it('switches between day and night mode', async () => {
    renderNav();

    await userEvent.click(
      await screen.findByRole('button', { name: 'Switch to dark theme' }),
    );
    expect(document.documentElement).toHaveClass('dark');
    expect(window.localStorage.getItem('manabi-theme')).toBe('dark');

    await userEvent.click(
      screen.getByRole('button', { name: 'Switch to light theme' }),
    );
    expect(document.documentElement).not.toHaveClass('dark');
    expect(window.localStorage.getItem('manabi-theme')).toBe('light');
  });

  it('shows the GitHub button when nobody is logged in', async () => {
    renderNav();

    expect(
      await screen.findByRole('button', { name: 'GitHub login' }),
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
      screen.queryByRole('button', { name: 'GitHub login' }),
    ).not.toBeInTheDocument();
  });
});
