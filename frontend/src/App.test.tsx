import { render, screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { App } from './App';

const STATIC_ROUTE_TARGETS: Array<[string, string]> = [
  ['/', 'MANABI'],
  ['/_kit', 'MANABI /_kit'],
  ['/about', 'About MANABI'],
  ['/how-it-works', 'Four steps, zero ceremony'],
  ['/sources', 'Sources'],
  ['/faq', 'Straight answers'],
  ['/contribute', "Build on someone else's repo"],
  ['/contact', 'Talk to us'],
  ['/privacy', 'Privacy, in plain English'],
  ['/sources#credits', 'Sources'],
];

const PLACEHOLDER_ROUTE_TARGETS: Array<[string, string]> = [];

const DEAD_TARGETS = [
  '/nope',
  '/problems/1/extra',
  '/ingest/none',
];

describe('Route table (no dead links)', () => {
  it.each(STATIC_ROUTE_TARGETS)('%s renders %s', async (path, title) => {
    window.history.pushState({}, '', path);

    render(<App />);

    expect(
      await screen.findByRole('heading', { name: title, level: 1 }),
    ).toBeInTheDocument();
  });

  it.each(PLACEHOLDER_ROUTE_TARGETS)('%s resolves to a placeholder page', (path, title) => {
    window.history.pushState({}, '', path);

    render(<App />);

    expect(
      screen.getByRole('heading', { name: title, level: 1 }),
    ).toBeInTheDocument();
    expect(screen.queryByText('404')).not.toBeInTheDocument();
  });

  it('/problems renders the board', async () => {
    window.history.pushState({}, '', '/problems');

    render(<App />);

    expect(await screen.findByRole('heading', { name: 'Problems', level: 1 }))
      .toBeInTheDocument();
    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 3,
      }),
    ).toBeInTheDocument();
  });

  it('/problems/:id renders the problem detail', async () => {
    window.history.pushState({}, '', '/problems/1');

    render(<App />);

    expect(
      await screen.findByRole('heading', {
        name: 'Crop disease triage for small farms',
        level: 1,
      }),
    ).toBeInTheDocument();
  });

  it('/projects/:id renders the project page', async () => {
    window.history.pushState({}, '', '/projects/1');

    render(<App />);

    expect(
      await screen.findByRole('heading', { name: 'crop-triage', level: 1 }),
    ).toBeInTheDocument();
    expect(screen.queryByText('404')).not.toBeInTheDocument();
  });

  it('/me redirects to home when logged out', async () => {
    window.history.pushState({}, '', '/me');

    render(<App />);

    expect(await screen.findByRole('heading', { name: 'MANABI', level: 1 }))
      .toBeInTheDocument();
    expect(screen.queryByText('Dashboard')).not.toBeInTheDocument();
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
      await screen.findByRole('heading', { name: '404 — page not found', level: 1 }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Browse problems' })).toBeInTheDocument();
  });

  it('renders the footer link columns', () => {
    window.history.pushState({}, '', '/');

    render(<App />);

    for (const heading of ['Explore', 'Build', 'MANABI', 'Legal']) {
      expect(
        screen.getByRole('heading', { name: heading, level: 2 }),
      ).toBeInTheDocument();
    }
  });
});
