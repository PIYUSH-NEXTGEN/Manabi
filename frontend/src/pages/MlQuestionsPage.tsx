import { Link } from 'react-router-dom';
import { cx } from '@/lib/cx';
import { Tag } from '@/design/primitives';
import { useMlQuestions } from '@/hooks/useMlQuestions';
import { useMlQuestionAttempt } from '@/hooks/useMlQuestionAttempt';
import type { MlQuestionCard } from '@/api/client';

const smallMono = 'font-mono text-[10px] font-bold uppercase tracking-widest';
const panelHeading = 'font-mono text-xs font-bold uppercase tracking-widest';

const DIFFICULTY_FILL: Record<string, number> = {
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

function QuestionCard({ question }: { question: MlQuestionCard }) {
  const attempt = useMlQuestionAttempt(question.id);
  const filled = DIFFICULTY_FILL[question.difficulty] ?? 0;
  const squares = `${'■'.repeat(filled)}${'□'.repeat(3 - filled)}`;
  const attempted = question.attempted || attempt.data != null;

  return (
    <Link
      to={`/ml/${question.id}`}
      className="block border-[3px] border-ink bg-white p-4 shadow-hard transition-transform duration-100 hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-lg"
    >
      <div className="flex items-center justify-between gap-3">
        <span className={smallMono}>{question.topic}</span>
        <span>
          <span aria-hidden>{squares}</span>
          <span className="sr-only">{question.difficulty}</span>
        </span>
      </div>
      <h2 className="mt-3 font-display text-xl uppercase leading-snug">
        {question.title}
      </h2>
      <div className="mt-3 flex items-center justify-between gap-2">
        <Tag>{question.difficulty}</Tag>
        {attempted ? (
          <span className={cx(smallMono, 'text-blue')}>Attempted</span>
        ) : (
          <span className={cx(smallMono, 'text-ink/60')}>
            Not attempted yet
          </span>
        )}
      </div>
    </Link>
  );
}

export function MlQuestionsPage() {
  const questions = useMlQuestions();

  return (
    <main className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(900px,96vw)] py-12">
        <p className={panelHeading}>ML practice</p>
        <h1 className="mt-2 font-display text-4xl uppercase leading-none md:text-6xl">
          ML Practice
        </h1>
        <p className="mt-3 max-w-2xl text-lg leading-snug">
          Real debugging scenarios, not toy datasets. Write how you would
          investigate it — the backend grades your answer against a rubric and
          always shows the expert explanation.
        </p>

        {questions.isError && !questions.data ? (
          <section className="mt-8 border-[3px] border-ink bg-white p-6 shadow-hard">
            <p>
              The question list could not be loaded. That is a backend or
              network problem and it will not heal by refreshing harder.
            </p>
          </section>
        ) : (questions.data ?? []).length === 0 ? (
          <section className="mt-8 border-[3px] border-ink bg-white p-6 shadow-hard">
            <p>
              No questions in the catalog yet. They are seeded on the backend.
            </p>
          </section>
        ) : (
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {(questions.data ?? []).map((question) => (
              <QuestionCard key={question.id} question={question} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
