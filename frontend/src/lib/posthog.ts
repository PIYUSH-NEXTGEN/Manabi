import type { PostHog } from 'posthog-js';

const projectToken = import.meta.env.VITE_POSTHOG_KEY?.trim();
const apiHost = import.meta.env.VITE_POSTHOG_HOST?.trim();

/** True when both public PostHog variables were compiled in at build time. */
export const isPostHogConfigured = Boolean(projectToken && apiHost);

let client: PostHog | null = null;
let loading: Promise<PostHog | null> | null = null;

/** The initialized SDK, or null while analytics has not been allowed yet. */
export function loadedPosthog(): PostHog | null {
  return client;
}

/**
 * Loads and initializes posthog-js on demand. Nothing is imported, initialized
 * or sent until consent is granted, so the SDK stays out of the critical path.
 */
export function loadPosthog(): Promise<PostHog | null> {
  if (!isPostHogConfigured) return Promise.resolve(null);
  if (client) return Promise.resolve(client);
  if (loading) return loading;

  // posthog-js fetches its session-recording recorder as a separate script from
  // PostHog's CDN. Ad blockers and strict network policies kill that request,
  // and the SDK then reports `$sdk_debug_recording_script_not_loaded` with no
  // replay captured. Shipping the recorder ourselves defines the globals the
  // SDK checks for, which is its "recorder already loaded" path, so no external
  // script is ever requested. A failure here must not cost us analytics.
  const recorder = import('posthog-js/dist/posthog-recorder').catch(
    (error: unknown) => {
      console.warn('PostHog recorder could not be bundled', error);
      return null;
    },
  );

  loading = Promise.all([import('posthog-js'), recorder])
    .then(([{ default: posthog }]) => {
      posthog.init(projectToken as string, {
        api_host: apiHost as string,
        defaults: '2026-08-30',
        person_profiles: 'identified_only',
        // Route changes are captured by trackPageview, once per path.
        capture_pageview: false,
        // Local storage only: analytics never writes a cookie.
        persistence: 'localStorage',
        session_recording: {
          maskAllInputs: true,
          // Public briefs stay readable; chat text carries `.ph-mask`.
          maskTextSelector: '.ph-mask',
        },
        capture_exceptions: {
          capture_unhandled_errors: true,
          capture_unhandled_rejections: true,
          capture_console_errors: false,
        },
        logs: {
          serviceName: 'manabi-frontend',
          environment: import.meta.env.MODE,
        },
      });
      // A visitor who withdrew earlier left an opt-out flag behind; granting
      // again must clear it, or capture would stay silently off.
      posthog.opt_in_capturing();
      client = posthog;
      return posthog;
    })
    .catch((error: unknown) => {
      // A blocked download or an ad blocker must not break the page.
      console.warn('PostHog could not be loaded', error);
      loading = null;
      return null;
    });

  return loading;
}

/** Stops capture and clears local identifiers when consent is withdrawn. */
export function unloadPosthog(): void {
  const posthog = client;
  client = null;
  loading = null;
  if (!posthog) return;

  try {
    if (posthog.sessionRecordingStarted?.()) posthog.stopSessionRecording();
    posthog.reset();
    posthog.opt_out_capturing();
  } catch (error) {
    console.warn('PostHog could not be stopped cleanly', error);
  }
}
