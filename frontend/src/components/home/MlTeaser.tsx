import { Link } from 'react-router-dom';
import { buttonClasses } from '@/design/primitives';
import { useMlQuestion } from '@/hooks/useMlQuestion';
import { useMlQuestions } from '@/hooks/useMlQuestions';
import { markdownExcerpt } from '@/lib/markdownExcerpt';

export function MlTeaser() {
  const list = useMlQuestions();
  const firstId = list.data?.[0]?.id ?? null;
  const detail = useMlQuestion(firstId);

  return (
    <section className="border-b-[3px] border-ink bg-blue text-white">
      <div className="mx-auto grid w-[min(1200px,96vw)] gap-8 py-12 md:grid-cols-2">
        <div className="flex flex-col items-start gap-4">
          <p className="font-mono text-xs font-bold uppercase tracking-widest">
            ML practice
          </p>
          <h2 className="font-display text-3xl uppercase leading-none md:text-4xl">
            Production bugs, not puzzles
          </h2>
          <p className="max-w-md text-sm leading-snug">
            Real debugging scenarios — leakage, skew, drift, silent pipeline
            failures — answered in prose and graded against a hidden rubric.
          </p>
          <Link to="/ml" className={buttonClasses('secondary')}>
            Start practicing
          </Link>
        </div>

        <div className="border-[3px] border-ink bg-white p-5 text-ink shadow-hard">
          {detail.isLoading ? (
            <div className="skeleton h-32" aria-hidden />
          ) : detail.data ? (
            <>
              <p className="mb-2 font-mono text-[11px] font-bold uppercase tracking-widest">
                {detail.data.title} · {detail.data.topic}
              </p>
              <p className="text-sm leading-snug">
                {markdownExcerpt(detail.data.scenario)}
              </p>
            </>
          ) : (
            <p className="font-mono text-xs uppercase tracking-widest">
              Scenario loads when the ML API is up.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
