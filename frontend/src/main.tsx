import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/archivo-black';
import '@fontsource/archivo/400.css';
import '@fontsource/archivo/600.css';
import '@fontsource/inter/500.css';
import '@fontsource/instrument-serif/400-italic.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/700.css';
import './index.css';
import { App } from './App';
import { ErrorBoundary } from './components/ErrorBoundary';
import { installGlobalErrorReporting } from './lib/errorReporting';
import { analyticsLogs, initAnalytics } from './lib/analytics';

installGlobalErrorReporting();
initAnalytics();

async function prepare(): Promise<void> {
  if (import.meta.env.VITE_USE_MOCKS === 'true') {
    const { worker } = await import('./api/mocks/browser');
    await worker.start({ onUnhandledRequest: 'bypass' });
  }
}

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Root element #root not found');
}
const root = rootElement;

async function start(): Promise<void> {
  try {
    await prepare();
  } catch (error) {
    // Mock-worker startup is development-only; a failure must not blank the
    // whole app. The real API will still be used if it is reachable.
    console.error('App preparation failed; rendering without mocks', error);
    analyticsLogs.preparationFailed();
  }
  createRoot(root).render(
    <StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </StrictMode>,
  );
  analyticsLogs.applicationStarted();
}

void start();
