import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import { useState, type FormEvent } from 'react';
import { cx } from '@/lib/cx';
import {
  buttonClasses,
  Stamp,
  Tag,
  useToast,
} from '@/design/primitives';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { useMlQuestion } from '@/hooks/useMlQuestion';
import { useMlQuestionAttempt } from '@/hooks/useMlQuestionAttempt';
import { useMe } from '@/hooks/useMe';
import { ApiError, postAttempt, type AttemptOut } from '@/api/client';
import { Markdown } from '@/components/markdown/Markdown';

const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';
const smallMono = 'font-mono text-[10px] font-bold uppercase tracking-widest';
const DIFFICULTY_FILL: Record<string, number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

function ScenarioSlab({ markdown }: { markdown: string }) {
  return (
    <section
      aria-label="Scenario"
      className="border-[3px] border-ink bg-white p-4 shadow-hard"
    >
      <h2 className={panelHeading}>Original scenario</h2>
      <Markdown className="mt-2 leading-relaxed">{markdown}</Markdown>
    </section>
  );
}

function FeedbackPanel({ attempt }: { attempt: AttemptOut }) {
  const { feedback, explanation } = attempt;
  return (
    <section
      aria-label="Attempt feedback"
      className="mt-4 border-[3px] border-ink bg-white p-4 shadow-hard"
    >
      <h3 className={panelHeading}>
        Rubric feedback — {feedback.covered_count} of {feedback.total} points
        covered
      </h3>
      <ul className="mt-2 space-y-2">
        {feedback.items.map((item, index) => (
          <li key={`${item.point}-${index}`} className="flex items-start gap-2">
            {item.covered ? (
              <Stamp tone="active" label="covered" rotate={-2} />
            ) : (
              <Stamp tone="closed" label="missed" rotate={-2} />
            )}
            <div>
              <p className="text-sm leading-snug">{item.point}</p>
              {item.evidence ? (
                <p className={cx(smallMono, 'mt-1 text-ink/70')}>
                  {item.evidence}
                </p>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
      <p
        aria-label="Feedback summary"
        className="mt-3 border-l-4 border-yellow-400 pl-2 text-sm leading-snug"
      >
        {feedback.summary}
      </p>
      <h3 className={cx(panelHeading, 'mt-4')}>Explanation</h3>
      <Markdown className="mt-1 leading-relaxed">{explanation}</Markdown>
    </section>
  );
}

export function MlQuestionPage() {
  const { id } = useParams();
  const questionId = Number(id);

  if (!Number.isInteger(questionId) || questionId <= 0) {
    return <NotFoundPage />;
  }

  return <QuestionView questionId={questionId} />;
}

function QuestionView({ questionId }: { questionId: number }) {
  const question = useMlQuestion(questionId);
  const me = useMe();
  const existing = useMlQuestionAttempt(questionId);
  const toast = useToast();
  const queryClient = useQueryClient();

  const [answer, setAnswer] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [attempt, setAttempt] = useState<AttemptOut | null>(null);

  const submit = useMutation<AttemptOut, Error, string>({
    mutationFn: () => postAttempt(questionId, { answer: answer.trim() }),
    onSuccess: (value) => {
      setAttempt(value);
      setAnswer('');
      setValidationError(null);
      queryClient.setQueryData(['ml', 'attempt', questionId], value);
      toast('Attempt graded — see the rubric feedback below.');
    },
    onError: (error) => {
      toast(
        error instanceof ApiError
          ? error.detail
          : 'Grading failed — try again.',
        'error',
      );
    },
  });

  if (question.isPending) {
    return (
      <main className="border-b-[3px] border-ink">
        <div className="mx-auto w-[min(760px,96vw)] animate-pulse space-y-4 py-16">
          <div className="h-3 w-32 rounded bg-ink/20" />
          <div className="h-10 w-2/3 rounded bg-ink/20" />
          <div className="h-48 w-full rounded bg-ink/20" />
        </div>
      </main>
    );
  }

  if (question.isError) {
    if (question.error.status === 404) {
      return <NotFoundPage />;
    }
    return (
      <main className="border-b-[3px] border-ink">
        <div className="mx-auto w-[min(760px,96vw)] space-y-4 py-16">
          <h1 className="font-display text-3xl uppercase">
            Could not load this question
          </h1>
          <p>{question.error.message}</p>
          <Link to="/ml" className="font-mono text-xs font-bold underline">
            Back to practice
          </Link>
        </div>
      </main>
    );
  }

  const data = question.data;
  const shownAttempt = attempt ?? existing.data;
  const filled = DIFFICULTY_FILL[data.difficulty] ?? 0;
  const squares = `${'■'.repeat(filled)}${'□'.repeat(3 - filled)}`;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setValidationError(null);

    const trimmed = answer.trim();
    if (trimmed.length < 20) {
      setValidationError('Write at least 20 characters — no lazy attempts.');
      return;
    }
    if (trimmed.length > 4000) {
      setValidationError('Keep the answer under 4000 characters.');
      return;
    }
    submit.mutate(trimmed);
  }

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(760px,96vw)] py-12">
        <p className={smallMono}>{data.topic}</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-tight">
          {data.title}
        </h1>
        <div className="mt-3 flex items-center gap-2">
          <Tag>{data.difficulty}</Tag>
          <span>
            <span aria-hidden>{squares}</span>
            <span className="sr-only">difficulty {data.difficulty}</span>
          </span>
        </div>

        <div className="mt-8">
          <ScenarioSlab markdown={data.scenario} />
        </div>

        {me.data ? (
          <section
            aria-label="Attempt area"
            className="mt-6 border-[3px] border-ink bg-white p-4 shadow-hard"
          >
            <h2 className={panelHeading}>Your attempt</h2>
            {shownAttempt ? (
              <div className="mt-3">
                <p className={cx(smallMono, 'text-ink/70')}>
                  Attempted on {shownAttempt.created_at.slice(0, 10)} —
                  submitting again replaces your answer.
                </p>
                <p className="mt-2 whitespace-pre-wrap text-sm leading-snug">
                  {shownAttempt.answer}
                </p>
              </div>
            ) : null}
            <form noValidate onSubmit={handleSubmit} className="mt-3">
              <label
                htmlFor="attempt-answer"
                className={cx(smallMono, 'mb-2 block')}
              >
                How would you debug it? (min 20 characters)
              </label>
              <textarea
                id="attempt-answer"
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                rows={6}
                placeholder="Walk through your checks, in order, and say how you would confirm each one."
                maxLength={4000}
                aria-invalid={validationError ? true : undefined}
                aria-describedby={validationError ? 'attempt-answer-error' : undefined}
                className="field w-full"
              />
              {validationError ? (
                <p
                  id="attempt-answer-error"
                  role="alert"
                  className={cx(smallMono, 'mt-2 text-red')}
                >
                  {validationError}
                </p>
              ) : null}
              <button
                type="submit"
                disabled={submit.isPending}
                className={cx(buttonClasses('primary'), 'mt-3 self-start')}
              >
                {submit.isPending
                  ? 'Grading against the rubric…'
                  : 'Submit attempt'}
              </button>
            </form>
            {shownAttempt ? (
              <FeedbackPanel attempt={shownAttempt} />
            ) : null}
          </section>
        ) : (
          <section
            aria-label="Attempt login"
            className="mt-6 border-[3px] border-ink bg-white p-4 shadow-hard"
          >
            <h2 className={panelHeading}>Attempt this question</h2>
            <p className="mt-2 text-sm leading-snug">
              Log in with GitHub to submit your answer and get rubric feedback
              (the expert explanation stays visible either way).
            </p>
            <a
              href="/api/auth/github/login"
              className={cx(buttonClasses('primary'), 'mt-3 self-start')}
            >
              Log in with GitHub
            </a>
          </section>
        )}

        <Link
          to="/ml"
          className={cx(smallMono, 'mt-8 inline-block underline underline-offset-4')}
        >
          ← Back to practice
        </Link>
      </div>
    </main>
  );
}
