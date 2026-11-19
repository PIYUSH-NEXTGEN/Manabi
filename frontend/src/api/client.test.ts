import { http, HttpResponse } from 'msw';
import { describe, expect, it, vi } from 'vitest';
import { server } from '@/api/mocks/server';
import { ApiError, apiFetch, deleteProject, getProblems, getStats } from './client';

describe('apiFetch', () => {
  it('parses JSON on success', async () => {
    const response = await apiFetch<{ status: string }>('/api/health');
    expect(response).toEqual({ status: 'ok' });
  });

  it('resolves without parsing a body on 204 no content (project delete)', async () => {
    let deleted = false;
    server.use(
      http.delete('*/api/projects/7', () => {
        deleted = true;
        return new HttpResponse(null, { status: 204 });
      }),
    );

    await expect(deleteProject(7)).resolves.toBeUndefined();
    expect(deleted).toBe(true);
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

  it('normalizes a network failure into an ApiError', async () => {
    server.use(http.get('*/api/offline', () => HttpResponse.error()));

    await expect(apiFetch('/api/offline')).rejects.toMatchObject({
      status: 0,
      code: 'network_error',
      detail: 'Could not reach the server. Check your connection and try again.',
    });
  });

  it('times out a stalled request instead of waiting forever', async () => {
    vi.stubGlobal(
      'fetch',
      ((_input: RequestInfo | URL, init?: RequestInit) =>
        new Promise((_resolve, reject) => {
          init?.signal?.addEventListener('abort', () =>
            reject(new DOMException('Aborted', 'AbortError')),
          );
        })) as typeof fetch,
    );

    try {
      await expect(
        apiFetch('/api/slow', { timeoutMs: 5 }),
      ).rejects.toMatchObject({ status: 0, code: 'timeout' });
    } finally {
      vi.unstubAllGlobals();
    }
  });

  it('rejects an unreadable successful body safely', async () => {
    server.use(
      http.get('*/api/unreadable', () => new HttpResponse('not json', { status: 200 })),
    );

    await expect(apiFetch('/api/unreadable')).rejects.toMatchObject({
      status: 200,
      code: 'invalid_response',
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
      problems: 5,
      sources: 3,
      fields: 2,
      projects: 1,
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
      goal: 'resume',
      tech: ['python', 'pandas'],
      sort: 'discover',
      seed: 4242,
      distinct: 'field',
      limit: 6,
      offset: 3,
    });

    const params = new URLSearchParams(search);
    expect(params.get('q')).toBe('crop');
    expect(params.get('goal')).toBe('resume');
    expect(params.getAll('tech')).toEqual(['python', 'pandas']);
    expect(params.get('sort')).toBe('discover');
    expect(params.get('seed')).toBe('4242');
    expect(params.get('distinct')).toBe('field');
    expect(params.get('limit')).toBe('6');
    expect(params.get('offset')).toBe('3');
  });
});
