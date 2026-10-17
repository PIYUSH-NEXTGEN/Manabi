import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Markdown } from '@/components/markdown/Markdown';
import { renderWithProviders } from '@/test/renderWithProviders';

describe('Markdown', () => {
  it('renders formatting instead of raw markers', () => {
    renderWithProviders(
      <Markdown>{'## Pick metrics\n\nUse **PR-AUC**:\n\n- one\n- two'}</Markdown>,
    );

    expect(
      screen.getByRole('heading', { name: 'Pick metrics' }),
    ).toBeInTheDocument();
    expect(screen.getByText('PR-AUC').tagName).toBe('STRONG');
    expect(screen.getByText('one').tagName).toBe('LI');
    expect(screen.getByText('two').tagName).toBe('LI');
    expect(screen.queryByText(/\*\*/)).toBeNull();
  });

  it('links [P17] to the problem page when problemsAsLinks is on', () => {
    renderWithProviders(<Markdown problemsAsLinks>{'Start with [P17].'}</Markdown>);

    expect(screen.getByRole('link', { name: 'P17' })).toHaveAttribute(
      'href',
      '/problems/17',
    );
  });

  it('keeps [P17] as plain text by default', () => {
    renderWithProviders(<Markdown>{'Start with [P17].'}</Markdown>);

    expect(screen.queryByRole('link')).toBeNull();
    expect(screen.getByText('Start with [P17].')).toBeInTheDocument();
  });

  it('leaves raw HTML inert', () => {
    renderWithProviders(<Markdown>{'<img src="x"> safe text'}</Markdown>);

    expect(screen.queryByRole('img')).toBeNull();
    expect(screen.getByText(/safe text/)).toBeInTheDocument();
  });
});