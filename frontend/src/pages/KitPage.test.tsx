import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { ToastProvider } from '@/design/primitives';
import { KitPage } from './KitPage';

function renderKit() {
  return render(
    <ToastProvider>
      <KitPage />
    </ToastProvider>,
  );
}

describe('KitPage', () => {
  it('renders every primitive section', () => {
    renderKit();

    expect(
      screen.getByRole('heading', { name: 'MANABI /_kit' }),
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Primary' })).toBeInTheDocument();
    expect(screen.getByText('AI-SUGGESTED')).toBeInTheDocument();
    expect(screen.getByText('python')).toBeInTheDocument();
    expect(screen.getByLabelText('Search problems')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Crop disease triage' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'From URL' })).toBeInTheDocument();
    expect(screen.getByLabelText('Sample sources')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Open dialog' })).toBeInTheDocument();
  });

  it('fires a toast from the kit page', async () => {
    const user = userEvent.setup();
    renderKit();

    await user.click(screen.getByRole('button', { name: 'Fire info toast' }));

    expect(screen.getByRole('status')).toHaveTextContent('Saved to the board');
  });

  it('opens the kit dialog', async () => {
    const user = userEvent.setup();
    renderKit();

    await user.click(screen.getByRole('button', { name: 'Open dialog' }));

    expect(screen.getByRole('dialog')).toBeVisible();
  });
});
