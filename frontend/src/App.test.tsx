import { render, screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { App } from './App';

const STATIC_ROUTE_TARGETS: Array<[string, string]> = [
  ['/', 'Pick a project. Ship it Prove it.'],
  ['/_kit', 'MANABI /_kit'],
  ['/about', 'About MANABI'],
  ['/faq', 'Straight answers'],
  ['/contribute', "Build on someone else's repo"],
  ['/contact', 'Talk to us'],
  ['/privacy', 'Privacy, in plain English'],
  ['/terms', 'Terms, in plain English'],
];

const DEAD_TARGETS = [
  '/nope',
  '/problems/1/extra',
  '/projects',
  '/projects/webhooks',
  '/projects/tenant-security',
  '/projects/analytics',
  '/projects/workflows',
];

// Every test here mounts the entire <App /> and resolves lazy route chunks.
// Under a fully parallel suite run on a loaded machine a single render can
// outlive the 5s default test timeout, which flagged as a flake twice; give
// these integration-style tests explicit headroom instead.
describe('Route table (no dead links)', () => {
  it.each(STATIC_ROUTE_TARGETS)('%s renders %s', async (path, title) => {
    window.history.pushState({}, '', path);

    render(<App />);

    expect(
      await screen.findByRole(
        'heading',
        { name: title, level: 1 },
        { timeout: 15000 },
      ),
    ).toBeInTheDocument();
  }, 20000);

  it('/problems renders the board', async () => {
    window.history.pushState({}, '', '/problems');

    render(<App />);

    expect(await screen.findByRole('heading', { name: 'Projects', level: 1 }, { timeout: 15000 }))
      .toBeInTheDocument();
    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 3,
      }),
    ).toBeInTheDocument();
  }, 20000);

  it('/problems/:id renders the problem detail', async () => {
    window.history.pushState({}, '', '/problems/1');

    render(<App />);

    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 1,
      }, { timeout: 15000 }),
    ).toBeInTheDocument();
  }, 20000);

  it('/projects/:id renders the project page', async () => {
    window.history.pushState({}, '', '/projects/1');

    render(<App />);

    expect(
      await screen.findByRole('heading', { name: 'crop-triage', level: 1 }, { timeout: 15000 }),
    ).toBeInTheDocument();
    expect(screen.queryByText('404')).not.toBeInTheDocument();
  }, 20000);

  it('/me redirects to home when logged out', async () => {
    window.history.pushState({}, '', '/me');

    render(<App />);

    expect(
      await screen.findByRole(
        'heading',
        {
          name: 'Pick a project. Ship it Prove it.',
          level: 1,
        },
        { timeout: 5000 },
      ),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole('heading', { name: 'Dashboard', level: 1 }),
    ).not.toBeInTheDocument();
  });

  it('/me shows the dashboard when logged in', async () => {
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
    window.history.pushState({}, '', '/me');

    render(<App />);

    expect(await screen.findByText('demo-farmer')).toBeInTheDocument();
    expect(
      await screen.findByRole('heading', { name: 'Dashboard', level: 1 }),
    ).toBeInTheDocument();
  });

  it.each(DEAD_TARGETS)('%s hits the custom 404 page', async (path) => {
    window.history.pushState({}, '', path);

    render(<App />);

    expect(
      await screen.findByRole('heading', { name: '404. Page not found', level: 1 }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Browse problems' })).toBeInTheDocument();
  });

  it('renders the footer link columns', () => {
    window.history.pushState({}, '', '/');

    render(<App />);

    for (const heading of ['MANABI', 'Legal']) {
      expect(
        screen.getByRole('heading', { name: heading, level: 2 }),
      ).toBeInTheDocument();
    }
  });
});
