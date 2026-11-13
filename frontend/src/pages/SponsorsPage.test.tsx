import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { renderWithProviders } from '@/test/renderWithProviders';
import { SponsorsPage } from './SponsorsPage';
import {
  FAQ,
  HOW_IT_WORKS,
  OFFER,
  SPONSOR_EMAIL,
  SPONSOR_EMAIL_BODY,
  SPONSOR_EMAIL_SUBJECT,
} from './sponsors/sponsorContent';

function renderPage() {
  return renderWithProviders(<SponsorsPage />, { route: '/sponsors' });
}

describe('SponsorsPage', () => {
  it('renders the hero with a call to action aimed at the offer', () => {
    renderPage();

    expect(
      screen.getByRole('heading', { level: 1, name: 'Partner with MANABI.' }),
    ).toBeInTheDocument();

    const cta = screen.getByRole('link', { name: 'Become a sponsor' });
    expect(cta).toHaveAttribute('href', '#offer');
    expect(document.getElementById('offer')).not.toBeNull();

    expect(
      screen.getByText(/founding sponsors get founding pricing/i),
    ).toBeInTheDocument();
  });

  it('shows the three audience cards and drops the old four-card copy', () => {
    renderPage();

    for (const title of [
      'Students and resume builders',
      'Hackathon participants',
      'Beginners and early-career developers',
    ]) {
      expect(screen.getByRole('heading', { name: title })).toBeInTheDocument();
    }

    expect(screen.queryByText('Final-year students')).not.toBeInTheDocument();
    expect(
      screen.queryByText('Resume and hackathon builders'),
    ).not.toBeInTheDocument();
  });

  it('renders only live stats in the numbers strip', async () => {
    renderPage();

    expect(await screen.findByText('6 project ideas')).toBeInTheDocument();
    expect(screen.getByText('3 fields')).toBeInTheDocument();
    expect(screen.getByText('Today on MANABI')).toBeInTheDocument();
  });

  it('hides the numbers strip when stats fail', async () => {
    server.use(
      http.get('*/api/stats', () => new HttpResponse(null, { status: 500 })),
    );

    renderPage();

    await waitFor(() =>
      expect(screen.queryByText('Today on MANABI')).not.toBeInTheDocument(),
    );
  });

  it('hides the numbers strip when stats are empty', async () => {
    server.use(
      http.get('*/api/stats', () =>
        HttpResponse.json({ problems: 0, sources: 0, fields: 0, projects: 0 }),
      ),
    );

    renderPage();

    await waitFor(() =>
      expect(screen.queryByText('Today on MANABI')).not.toBeInTheDocument(),
    );
  });

  it('renders the offer, preview slots and promise', () => {
    renderPage();

    expect(
      screen.getByRole('heading', { name: 'One placement. Five slots.' }),
    ).toBeInTheDocument();
    expect(screen.getByText('₹999')).toBeInTheDocument();
    expect(screen.getByText('/ month')).toBeInTheDocument();
    expect(screen.getByText('Founding price')).toBeInTheDocument();
    expect(screen.queryByText(/on request/i)).not.toBeInTheDocument();

    for (const bullet of OFFER.bullets) {
      expect(screen.getByText(bullet)).toBeInTheDocument();
    }

    expect(screen.getByText(OFFER.previewCaption)).toBeInTheDocument();
    expect(screen.getByText('Your logo here')).toBeInTheDocument();
    expect(screen.getAllByText('Available')).toHaveLength(4);

    expect(
      screen.getByRole('heading', { name: 'Our promise to students' }),
    ).toBeInTheDocument();
  });

  it('renders all four steps and all nine questions', () => {
    renderPage();

    expect(
      screen.getByRole('heading', { name: HOW_IT_WORKS.title }),
    ).toBeInTheDocument();
    for (const step of HOW_IT_WORKS.steps) {
      expect(screen.getByRole('heading', { name: step.title })).toBeInTheDocument();
    }

    expect(FAQ.items).toHaveLength(9);
    for (const item of FAQ.items) {
      expect(
        screen.getByRole('button', { name: item.question }),
      ).toBeInTheDocument();
    }
  });

  it('reveals an answer on click and with the keyboard', async () => {
    const user = userEvent.setup();
    renderPage();

    const first = FAQ.items[0];
    const trigger = screen.getByRole('button', { name: first.question });
    const panel = document.getElementById(
      trigger.getAttribute('aria-controls') ?? '',
    );

    expect(trigger).toHaveAttribute('aria-expanded', 'false');
    expect(panel).not.toBeNull();
    expect(panel).not.toBeVisible();

    await user.click(trigger);
    expect(trigger).toHaveAttribute('aria-expanded', 'true');
    expect(panel).toBeVisible();
    expect(within(panel as HTMLElement).getByText(first.answer)).toBeVisible();

    const second = FAQ.items[1];
    const keyboardTrigger = screen.getByRole('button', {
      name: second.question,
    });
    keyboardTrigger.focus();
    await user.keyboard('{Enter}');

    expect(keyboardTrigger).toHaveAttribute('aria-expanded', 'true');
    expect(trigger).toHaveAttribute('aria-expanded', 'false');
  });

  it('uses the sponsor email for every contact link', () => {
    renderPage();

    const mailtoLinks = screen
      .getAllByRole('link')
      .filter((link) => link.getAttribute('href')?.startsWith('mailto:'));

    expect(mailtoLinks.length).toBeGreaterThan(0);
    for (const link of mailtoLinks) {
      const href = link.getAttribute('href') ?? '';
      expect(href.startsWith(`mailto:${SPONSOR_EMAIL}?subject=`)).toBe(true);
      expect(href).toContain(encodeURIComponent(SPONSOR_EMAIL_SUBJECT));
      expect(href).toContain(encodeURIComponent(SPONSOR_EMAIL_BODY));
      expect(href).toContain('%0A');
    }

    expect(document.body.textContent).not.toContain('piyush.intech@gmail.com');
  });

  it('makes no traffic or reporting promises', () => {
    renderPage();

    const text = document.body.textContent ?? '';
    expect(text).not.toMatch(/monthly report/i);
    expect(text).not.toMatch(
      /\b\d[\d,.]*\s*\+?\s*(views|clicks|impressions|visitors)\b/i,
    );
  });
});
