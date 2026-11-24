import { isPostHogConfigured, posthog } from './posthog';

/**
 * The only browser logs exported to PostHog. Keep attributes operational and
 * non-user-specific so this dedicated logger never forwards existing console output.
 */
export const posthogLogs = {
  applicationStarted(): void {
    if (!isPostHogConfigured) return;

    posthog.logger.info('application_started', {
      runtime: 'browser',
    });
  },

  preparationFailed(): void {
    if (!isPostHogConfigured) return;

    posthog.logger.warn('application_preparation_failed', {
      preparation: 'mock_worker',
    });
  },

  uiRenderFailed(): void {
    if (!isPostHogConfigured) return;

    posthog.logger.error('ui_render_failed', {
      error_source: 'react_error_boundary',
    });
  },
};
