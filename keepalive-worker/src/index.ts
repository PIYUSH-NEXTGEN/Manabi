interface Env {
  /** Public origin that reaches the API, without a trailing slash. */
  TARGET_URL: string;
}

const LIVE_PATH = '/api/health/live';
const READY_PATH = '/api/health/ready';

function stripTrailingSlashes(value: string): string {
  let end = value.length;
  while (end > 0 && value[end - 1] === '/') {
    end -= 1;
  }
  return value.slice(0, end);
}

async function ping(base: string, path: string): Promise<void> {
  const url = `${stripTrailingSlashes(base)}${path}`;
  const response = await fetch(url, {
    headers: { 'user-agent': 'manabi-keepalive/1.0' },
  });
  console.log(`${path} -> ${response.status}`);
}

export default {
  // Cron triggers do not use this handler, but a Worker with no fetch handler
  // throws Error 1101 when its URL is opened. Return a tiny status page so
  // manual checks are clean.
  async fetch(): Promise<Response> {
    return new Response('manabi-keepalive: ok\n', {
      status: 200,
      headers: { 'content-type': 'text/plain; charset=utf-8' },
    });
  },

  async scheduled(
    controller: ScheduledController,
    env: Env,
    ctx: ExecutionContext,
  ): Promise<void> {
    // Every 10 minutes: liveness only, so Render never reaches its 15-minute
    // idle timeout. This intentionally skips the database.
    if (controller.cron === '*/10 * * * *') {
      ctx.waitUntil(ping(env.TARGET_URL, LIVE_PATH));
      return;
    }

    // Once a day: readiness runs a query, which counts as database activity
    // and keeps a free Supabase project from pausing.
    ctx.waitUntil(ping(env.TARGET_URL, READY_PATH));
  },
};
