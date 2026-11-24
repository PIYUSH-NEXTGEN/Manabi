import posthog from 'posthog-js';

const projectToken = import.meta.env.VITE_POSTHOG_KEY?.trim();
const apiHost = import.meta.env.VITE_POSTHOG_HOST?.trim();
const isPostHogConfigured = Boolean(projectToken && apiHost);

function reportMissingConfiguration(variable: string): void {
  if (import.meta.env.DEV) {
    console.error(
      new Error(
        `${variable} variable required by PostHog is missing or un-configured, this causes events to be silently missed. This error stops appearing once ${variable} is configured`,
      ),
    );
  }
}

if (!projectToken) {
  reportMissingConfiguration('VITE_POSTHOG_KEY');
} else if (!apiHost) {
  reportMissingConfiguration('VITE_POSTHOG_HOST');
} else {
  posthog.init(projectToken, {
    api_host: apiHost,
    defaults: '2026-08-30',
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
}

export { isPostHogConfigured, posthog };
