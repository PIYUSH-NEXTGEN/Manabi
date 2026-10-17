import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { Dialog } from './Dialog';

describe('Dialog', () => {
  it('opens on trigger click and shows the title', async () => {
    const user = userEvent.setup();
    render(
      <Dialog title="Confirm claim" triggerLabel="Open dialog">
        Claim this problem?
      </Dialog>,
    );

    await user.click(screen.getByRole('button', { name: 'Open dialog' }));

    expect(screen.getByRole('dialog')).toBeVisible();
    expect(screen.getByRole('heading', { name: 'Confirm claim' })).toBeVisible();
    expect(screen.getByText('Claim this problem?')).toBeVisible();
  });

  it('closes on Escape', async () => {
    const user = userEvent.setup();
    render(
      <Dialog title="Confirm claim" triggerLabel="Open dialog">
        Claim this problem?
      </Dialog>,
    );

    await user.click(screen.getByRole('button', { name: 'Open dialog' }));
    expect(screen.getByRole('dialog')).toBeVisible();

    await user.keyboard('{Escape}');
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('closes via the close button', async () => {
    const user = userEvent.setup();
    render(
      <Dialog title="Note" triggerLabel="Open">
        Body
      </Dialog>,
    );

    await user.click(screen.getByRole('button', { name: 'Open' }));
    await user.click(screen.getByRole('button', { name: 'Close dialog' }));

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
