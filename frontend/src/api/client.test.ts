import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ApiError, apiFetch, getHealth, getProblems, getStats } from './client';

describe('apiFetch', () => {
  it('parses JSON on success', async () => {
    const health = await getHealth();
    expect(health).toEqual({ status: 'ok' });
  });

  it('throws an ApiError carrying detail and status on failure', async () => {
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 }),
      ),
    );

    const failure = apiFetch('/api/auth/me');
    await expect(failure).rejects.toBeInstanceOf(ApiError);
    await expect(failure).rejects.toMatchObject({
      status: 401,
      detail: 'Not authenticated',
    });
  });

  it('falls back to a generic detail when the body is not JSON', async () => {
    server.use(
      http.get('*/api/broken', () => new HttpResponse('nope', { status: 502 })),
    );

    await expect(apiFetch('/api/broken')).rejects.toMatchObject({
      status: 502,
      detail: 'Request failed with status 502',
    });
  });

  it('sends JSON content-type when a body is provided', async () => {
    let seenContentType: string | null = null;
    server.use(
      http.post('*/api/echo', async ({ request }) => {
        seenContentType = request.headers.get('content-type');
        return HttpResponse.json({ ok: true });
      }),
    );

    await apiFetch('/api/echo', { method: 'POST', body: '{"a":1}' });

    expect(seenContentType).toContain('application/json');
  });

  it('getStats returns the StatsOut shape', async () => {
    const stats = await getStats();

    expect(stats).toMatchObject({
      problems: 6,
      sources: 3,
      fields: 5,
      projects: 2,
      ml_questions: 2,
    });
  });

  it('getProblems serializes filters including repeatable tech', async () => {
    let search = '';
    server.use(
      http.get('*/api/problems', ({ request }) => {
        search = new URL(request.url).search;
        return HttpResponse.json({ items: [], total: 0 });
      }),
    );

    await getProblems({
      q: 'crop',
      tech: ['python', 'pandas'],
      sort: 'popular',
      limit: 6,
      offset: 3,
    });

    const params = new URLSearchParams(search);
    expect(params.get('q')).toBe('crop');
    expect(params.getAll('tech')).toEqual(['python', 'pandas']);
    expect(params.get('sort')).toBe('popular');
    expect(params.get('limit')).toBe('6');
    expect(params.get('offset')).toBe('3');
  });
});
