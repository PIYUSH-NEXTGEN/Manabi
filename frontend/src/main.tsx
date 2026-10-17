import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/archivo-black';
import '@fontsource/archivo/400.css';
import '@fontsource/archivo/600.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/700.css';
import './index.css';
import { App } from './App';

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

void prepare().then(() => {
  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
});
