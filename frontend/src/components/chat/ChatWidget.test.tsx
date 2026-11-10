import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { AskManabi } from '@/components/home/AskManabi';
import { renderWithProviders } from '@/test/renderWithProviders';

const CHAT_200 = {
  reply:
    'The closest catalog problems to what you described are linked under this message.',
  problems: [
    {
      id: 5,
      title: 'Attendance pipeline that fails loudly',
      field: 'data-science',
      difficulty: 'beginner',
    },
  ],
};

describe('ChatWidget', () => {
  it('opens from the floating dock and closes back to it', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    expect(screen.queryByLabelText('MANABI chat')).not.toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    expect(screen.getByLabelText('MANABI chat')).toBeInTheDocument();
    expect(
      screen.getByText(/only ever points at real problems already in the index/i),
    ).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Close the chat' }));
    expect(screen.queryByLabelText('MANABI chat')).not.toBeInTheDocument();
  });

  it('opens from the home Ask MANABI section button', async () => {
    const user = userEvent.setup();
    renderWithProviders(
      <>
        <AskManabi />
        <ChatWidget />
      </>,
    );

    await user.click(screen.getByRole('button', { name: 'Open the chat' }));
    expect(screen.getByLabelText('MANABI chat')).toBeInTheDocument();
  });

  it('sends a message and renders the reply with catalog problem links', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      'I know python and pandas, weekend build',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(
      await screen.findByText(/linked under this/i),
    ).toBeInTheDocument();
    const userBubble = screen.getByText(
      'I know python and pandas, weekend build',
    );
    expect(userBubble).toBeInTheDocument();
    expect(screen.getByText('Attendance pipeline that fails loudly')).toHaveAttribute(
      'href',
      '/problems/5',
    );
    expect(screen.getByText(/data science · beginner/i)).toBeInTheDocument();
  });

  it('renders markdown replies as formatted elements with inline problem links', async () => {
    server.use(
      http.post('*/api/chat', () =>
        HttpResponse.json({
          reply:
            'Prefer **PR-AUC** over accuracy for rare events:\n\n- Drop standard accuracy\n- Tune the decision threshold\n\nStart with [P17].',
          problems: [
            {
              id: 17,
              title: 'Sepsis early-warning from ICU vitals',
              field: 'aiml',
              difficulty: 'advanced',
            },
          ],
        }),
      ),
    );
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      'imbalanced classification',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect((await screen.findByText('PR-AUC')).tagName).toBe('STRONG');
    expect(screen.getByText('Drop standard accuracy')).toBeInTheDocument();
    expect(screen.getByText('Tune the decision threshold')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'P17' })).toHaveAttribute(
      'href',
      '/problems/17',
    );
    expect(screen.getByText('Sepsis early-warning from ICU vitals')).toHaveAttribute(
      'href',
      '/problems/17',
    );
    expect(screen.queryByText(/\*\*/)).toBeNull();
  });

  it('whitespace-only messages are never sent', async () => {
    const user = userEvent.setup();
    let called = 0;
    server.use(
      http.post('*/api/chat', () => {
        called += 1;
        return HttpResponse.json(CHAT_200);
      }),
    );
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      '   ',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => expect(called).toBe(0));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(screen.getByText(/Tell it what you know/i)).toBeInTheDocument();
  });

  it('caps the wire history at 6 messages in long conversations', async () => {
    const user = userEvent.setup();
    const historyLengths: number[] = [];
    server.use(
      http.post('*/api/chat', async ({ request }) => {
        const body = (await request.json()) as {
          messages?: Array<{ role: string; content: string }>;
        };
        historyLengths.push(body.messages!.length);
        const latest = body.messages![body.messages!.length - 1]!.content;
        return HttpResponse.json({
          reply: `echo: ${latest}`,
          problems: [],
        });
      }),
    );
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    const box = screen.getByPlaceholderText(/What do you want to build/i);
    for (let i = 0; i < 4; i += 1) {
      await user.type(box, `question number ${i + 1}`);
      await user.click(screen.getByRole('button', { name: 'Send' }));
      // waiting for this turn's reply guarantees the mutation completed, so
      // the recorded history lengths line up with turns.
      expect(
        await screen.findByText(`echo: question number ${i + 1}`),
      ).toBeInTheDocument();
    }

    expect(historyLengths).toEqual([1, 3, 5, 6]);
  });

  it('shows honest errors when the chat API is rate limited', async () => {
    server.use(
      http.post('*/api/chat', () =>
        HttpResponse.json(
          { detail: 'Chat hourly quota exhausted — try again later.' },
          { status: 429 },
        ),
      ),
    );
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      'another question',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(
      await screen.findByRole('alert'),
    ).toHaveTextContent('Chat hourly quota exhausted — try again later.');
    expect(screen.queryByText(/linked under this/i)).not.toBeInTheDocument();
  });

  it('passes the current problem page as page_context when chatting there', async () => {
    let capturedBody: Record<string, unknown> | null = null;
    server.use(
      http.post('*/api/chat', async ({ request }) => {
        capturedBody = (await request.json()) as Record<string, unknown>;
        return HttpResponse.json(CHAT_200);
      }),
    );
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />, { route: '/problems/3' });

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      'this one — can I do it in a weekend?',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(
      await screen.findByText(/linked under this/i),
    ).toBeInTheDocument();
    await waitFor(() => {
      expect(capturedBody).not.toBeNull();
      expect(capturedBody).toMatchObject({
        page_context: { problem_id: 3 },
      });
    });
  });
});
