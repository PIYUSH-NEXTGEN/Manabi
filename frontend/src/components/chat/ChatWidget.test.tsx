import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { beforeEach, describe, expect, it } from 'vitest';
import { server } from '@/api/mocks/server';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { AskManabi } from '@/components/home/AskManabi';
import { renderWithProviders } from '@/test/renderWithProviders';

const LOGGED_IN = {
  id: 1,
  username: 'octocat',
  name: 'Octo Cat',
  avatar_url: null,
};

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
  beforeEach(() => {
    // Chat is login-only: most tests talk to the chatbot as a member.
    server.use(http.get('*/api/auth/me', () => HttpResponse.json(LOGGED_IN)));
  });

  it('asks logged-out visitors to log in before they can chat', async () => {
    server.use(
      http.get('*/api/auth/me', () =>
        HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 }),
      ),
    );
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    expect(screen.getByLabelText('MANABI chat')).toBeInTheDocument();
    expect(
      await screen.findByRole('link', { name: 'Log in with GitHub' }),
    ).toHaveAttribute('href', '/api/auth/github/login');
    expect(
      screen.queryByPlaceholderText(/What do you want to build/i),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Send' })).not.toBeInTheDocument();
  });

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

  it('sends on Enter and inserts a newline on Shift+Enter', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    const box = screen.getByPlaceholderText(/What do you want to build/i);

    await user.type(box, 'first line');
    await user.keyboard('{Enter}');
    expect(await screen.findByText('first line')).toBeInTheDocument();

    await user.type(box, 'second message, part a');
    await user.keyboard('{Shift>}{Enter}{/Shift}');
    await user.keyboard('part b');
    expect(box).toHaveValue('second message, part a\npart b');

    await user.keyboard('{Enter}');
    // sending clears the draft and posts the full two-line message
    expect(await screen.findByText(/part b/)).toBeInTheDocument();
    expect(box).toHaveValue('');
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
          { detail: 'Chat hourly quota exhausted. Try again later.' },
          { status: 429, headers: { 'Retry-After': '300' } },
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
    ).toHaveTextContent('Chat hourly quota exhausted. Try again later.');
    expect(await screen.findByText(/Try again in/)).toHaveTextContent(
      'Try again in 5:00',
    );
    expect(screen.queryByText(/linked under this/i)).not.toBeInTheDocument();
  });

  it('shows a typing indicator while the reply is being generated', async () => {
    let release!: (response: ReturnType<typeof HttpResponse.json>) => void;
    server.use(
      http.post(
        '*/api/chat',
        () =>
          new Promise((resolve) => {
            release = resolve as typeof release;
          }),
      ),
    );
    const user = userEvent.setup();
    renderWithProviders(<ChatWidget />);

    await user.click(screen.getByRole('button', { name: 'Open the MANABI chat' }));
    await user.type(
      screen.getByPlaceholderText(/What do you want to build/i),
      'a question that takes a while',
    );
    await user.click(screen.getByRole('button', { name: 'Send' }));

    expect(
      await screen.findByText('Manabi is typing a reply'),
    ).toBeInTheDocument();

    release(HttpResponse.json(CHAT_200));
    expect(await screen.findByText(/linked under this/i)).toBeInTheDocument();
    await waitFor(() =>
      expect(
        screen.queryByText('Manabi is typing a reply'),
      ).not.toBeInTheDocument(),
    );
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
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
      'this one. Can I do it in a weekend?',
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
