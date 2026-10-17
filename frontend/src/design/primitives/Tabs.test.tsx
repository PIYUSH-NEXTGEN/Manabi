import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { Tabs } from './Tabs';

const TABS = [
  { value: 'url', label: 'From URL', content: 'Paste a source URL.' },
  { value: 'text', label: 'Paste text', content: 'Paste raw statement text.' },
];

describe('Tabs', () => {
  it('shows the first tab panel by default', () => {
    render(<Tabs tabs={TABS} />);
    expect(screen.getByText('Paste a source URL.')).toBeVisible();
    expect(screen.queryByText('Paste raw statement text.')).toBeNull();
  });

  it('switches panels when a tab is clicked', async () => {
    const user = userEvent.setup();
    render(<Tabs tabs={TABS} />);

    await user.click(screen.getByRole('tab', { name: 'Paste text' }));

    expect(screen.getByText('Paste raw statement text.')).toBeVisible();
    expect(screen.queryByText('Paste a source URL.')).toBeNull();
  });
});
