import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import posthog from 'posthog-js';

vi.mock('posthog-js', () => {
  const client = {
    init: vi.fn(),
    capture: vi.fn(),
    identify: vi.fn(),
    reset: vi.fn(),
    opt_in_capturing: vi.fn(),
    opt_out_capturing: vi.fn(),
    stopSessionRecording: vi.fn(),
    sessionRecordingStarted: vi.fn(() => false),
    logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  };
  return { default: client };
});

// The real recorder is a browser bundle that defines globals on import; the
// tests only care that it is requested before init and sent nothing itself.
vi.mock('posthog-js/dist/posthog-recorder', () => ({}));

/** Reloads the module so the env snapshot and consent state start clean. */
async function loadAnalytics() {
  vi.resetModules();
  return import('@/lib/analytics');
}

beforeEach(() => {
  window.localStorage.clear();
  vi.clearAllMocks();
  vi.stubEnv('VITE_POSTHOG_KEY', 'phc_test');
  vi.stubEnv('VITE_POSTHOG_HOST', 'https://us.i.posthog.com');
});

afterEach(() => {
  vi.unstubAllEnvs();
});

describe('analytics consent gate', () => {
  it('loads nothing and sends nothing before a decision', async () => {
    const analytics = await loadAnalytics();

    analytics.track('login_started');
    analytics.identifyUser(7, { username: 'ada' });
    analytics.initAnalytics();
    await Promise.resolve();

    expect(analytics.getConsent()).toBeNull();
    expect(posthog.init).not.toHaveBeenCalled();
    expect(posthog.capture).not.toHaveBeenCalled();
    expect(posthog.identify).not.toHaveBeenCalled();
  });

  it('honours a decline and remembers it', async () => {
    const analytics = await loadAnalytics();

    analytics.setConsent('denied');
    analytics.track('login_started');
    await Promise.resolve();

    expect(window.localStorage.getItem('manabi-analytics-consent')).toBe(
      'denied',
    );
    expect(posthog.init).not.toHaveBeenCalled();
    expect(posthog.capture).not.toHaveBeenCalled();
  });

  it('initialises privately and captures only after consent', async () => {
    const analytics = await loadAnalytics();

    analytics.setConsent('granted');
    await vi.waitFor(() => expect(posthog.init).toHaveBeenCalledTimes(1));

    const [, options] = vi.mocked(posthog.init).mock.calls[0];
    expect(options).toMatchObject({
      api_host: 'https://us.i.posthog.com',
      capture_pageview: false,
      persistence: 'localStorage',
      session_recording: {
        maskAllInputs: true,
        maskTextSelector: '.ph-mask',
      },
    });

    analytics.track('problem_starred', { target_id: 3 });
    expect(posthog.capture).toHaveBeenCalledWith('problem_starred', {
      target_id: 3,
    });
  });

  it('stops capture and forgets the identity when consent is withdrawn', async () => {
    const analytics = await loadAnalytics();

    analytics.setConsent('granted');
    await vi.waitFor(() => expect(posthog.init).toHaveBeenCalledTimes(1));

    analytics.clearConsent();
    analytics.track('project_submitted');
    await Promise.resolve();

    expect(window.localStorage.getItem('manabi-analytics-consent')).toBeNull();
    expect(posthog.reset).toHaveBeenCalled();
    expect(posthog.opt_out_capturing).toHaveBeenCalled();
    expect(posthog.capture).not.toHaveBeenCalledWith(
      'project_submitted',
      expect.anything(),
    );
  });
});
