/**
 * Cloudflare Pages Function: proxy /api/* to the Render API.
 *
 * Browser apps and their API must share one origin for the session cookie to
 * be sent reliably. `*.pages.dev` and `*.onrender.com` are different sites, so
 * a direct cross-origin call is a third-party request and the cookie is
 * dropped. Proxying through this Function makes every API call same-origin.
 *
 * Anonymous reads of the public catalog are also cached here. Render runs a
 * single small instance a long network hop away, so a cached board or stat
 * payload turns a ~400-600 ms round trip into an edge hit. Only requests with
 * no Cookie or Authorization header are ever cached: a logged-in list carries
 * `starred_by_me`, and personal responses must never be shared.
 *
 * Consequences for configuration (see DEPLOY.md):
 * - `VITE_API_BASE_URL` must be empty so the browser calls relative `/api/...`.
 * - The API's `BASE_URL` must be this Pages origin, so the OAuth redirect URI
 *   points back through the proxy and the OAuth state cookie is readable.
 */

interface Env {
  /** Render API origin, e.g. https://manabi-yu9f.onrender.com */
  API_ORIGIN?: string;
}

const DEFAULT_API_ORIGIN = 'https://manabi-yu9f.onrender.com';

/**
 * Public, viewer-independent GET paths and their edge lifetime. Everything
 * else (auth, dashboard, project progress, problem detail) is proxied straight
 * through: those responses depend on the viewer.
 */
const EDGE_CACHE_SECONDS: Record<string, number> = {
  '/api/stats': 60,
  '/api/problems': 30,
  '/api/problems/facets': 60,
};

interface PagesContext {
  request: Request;
  env: Env;
  waitUntil: (promise: Promise<unknown>) => void;
}

export const onRequest = async ({
  request,
  env,
  waitUntil,
}: PagesContext): Promise<Response> => {
  const origin = (env.API_ORIGIN || DEFAULT_API_ORIGIN).replace(/\/+$/, '');
  const incoming = new URL(request.url);
  const ttl = EDGE_CACHE_SECONDS[incoming.pathname];

  // The Cache API is not part of the DOM typings this repo compiles against.
  const edgeCache = (caches as unknown as { default: Cache }).default;
  const personalRequest =
    request.headers.has('cookie') || request.headers.has('authorization');
  const cacheable = request.method === 'GET' && ttl > 0 && !personalRequest;

  const cacheKey = cacheable
    ? new Request(incoming.toString(), { method: 'GET' })
    : null;
  if (cacheKey) {
    const hit = await edgeCache.match(cacheKey);
    if (hit) return hit;
  }

  const upstream = await fetch(`${origin}${incoming.pathname}${incoming.search}`, buildInit(request));

  const responseHeaders = new Headers(upstream.headers);
  // The runtime may have decompressed the body, so the original encoding and
  // length no longer describe it.
  responseHeaders.delete('content-encoding');
  responseHeaders.delete('content-length');

  if (!cacheKey || !upstream.ok || !upstream.body) {
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: responseHeaders,
    });
  }

  // Buffer only the small catalog payloads: a cached body must be stored whole,
  // and a streamed response cannot be replayed from the edge cache.
  const body = await upstream.arrayBuffer();
  responseHeaders.delete('set-cookie');
  responseHeaders.set(
    'cache-control',
    `public, max-age=0, s-maxage=${ttl}, stale-while-revalidate=${ttl * 4}`,
  );
  const cacheable_response = new Response(body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: responseHeaders,
  });
  waitUntil(edgeCache.put(cacheKey, cacheable_response.clone()));
  return cacheable_response;
};

function buildInit(request: Request): RequestInit {
  const headers = new Headers(request.headers);
  headers.delete('host');
  // Preserve the end-user address so per-IP rate limits see real clients
  // instead of one shared Cloudflare egress address.
  const clientIp = request.headers.get('cf-connecting-ip');
  if (clientIp) headers.set('x-forwarded-for', clientIp);
  headers.set('x-forwarded-proto', 'https');

  const bodyAllowed = request.method !== 'GET' && request.method !== 'HEAD';
  return {
    method: request.method,
    headers,
    body: bodyAllowed ? request.body : undefined,
    // Hand redirects back to the browser untouched: the OAuth flow relies on
    // the redirect to github.com, and login relies on the redirect to the app.
    redirect: 'manual',
    duplex: 'half',
  } as RequestInit;
}
