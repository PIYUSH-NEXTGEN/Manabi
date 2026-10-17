/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_USE_MOCKS?: string;
  readonly VITE_CONTACT_EMAIL?: string;
  readonly VITE_GITHUB_ISSUES_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
