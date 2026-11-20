/**
 * Cloudflare Pages Function: proxy /api/* to the Render API.
 *
 * Browser apps and their API must share one origin for the session cookie to
 * be sent reliably. `*.pages.dev` and `*.onrender.com` are different sites, so
 * a direct cross-origin call is a third-party request and the cookie is
 * dropped. Proxying through this Function makes every API call same-origin.
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

interface PagesContext {
  request: Request;
  env: Env;
}

export const onRequest = async ({ request, env }: PagesContext): Promise<Response> => {
  const origin = (env.API_ORIGIN || DEFAULT_API_ORIGIN).replace(/\/+$/, '');
  const incoming = new URL(request.url);
  const target = `${origin}${incoming.pathname}${incoming.search}`;

  const headers = new Headers(request.headers);
  headers.delete('host');
  // Preserve the end-user address so per-IP rate limits see real clients
  // instead of one shared Cloudflare egress address.
  const clientIp = request.headers.get('cf-connecting-ip');
  if (clientIp) headers.set('x-forwarded-for', clientIp);
  headers.set('x-forwarded-proto', 'https');

  const bodyAllowed = request.method !== 'GET' && request.method !== 'HEAD';
  const init = {
    method: request.method,
    headers,
    body: bodyAllowed ? request.body : undefined,
    // Hand redirects back to the browser untouched: the OAuth flow relies on
    // the redirect to github.com, and login relies on the redirect to the app.
    redirect: 'manual',
    duplex: 'half',
  } as RequestInit;

  const upstream = await fetch(target, init);

  const responseHeaders = new Headers(upstream.headers);
  // The runtime may have decompressed the body, so the original encoding and
  // length no longer describe it.
  responseHeaders.delete('content-encoding');
  responseHeaders.delete('content-length');

  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: responseHeaders,
  });
};
