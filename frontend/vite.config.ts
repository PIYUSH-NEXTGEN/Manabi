import path from 'node:path';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

// Cloudflare Pages exposes the deployed commit as CF_PAGES_COMMIT_SHA. Stamping
// it into the bundle turns a user's crash report into a specific release
// instead of the literal "web"; local builds keep the empty fallback.
const appVersion =
  process.env.VITE_APP_VERSION ??
  (process.env.CF_PAGES_COMMIT_SHA ?? '').slice(0, 7);

export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: appVersion
    ? { 'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion) }
    : {},
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
