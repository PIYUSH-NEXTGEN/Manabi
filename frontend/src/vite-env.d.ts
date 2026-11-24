/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_USE_MOCKS?: string;
  readonly VITE_CONTACT_EMAIL?: string;
  readonly VITE_GITHUB_ISSUES_URL?: string;
  readonly VITE_MASCOT_RIVE_SRC?: string;
  readonly VITE_APP_VERSION?: string;
  readonly VITE_POSTHOG_KEY?: string;
  readonly VITE_POSTHOG_HOST?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
