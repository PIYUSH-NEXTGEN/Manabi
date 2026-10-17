import { Link } from 'react-router-dom';
import { HOW_IT_WORKS_STEPS } from '@/components/home/steps';
import { buttonClasses } from '@/design/primitives';
import { StaticShell } from './StaticShell';

export function HowItWorksPage() {
  return (
    <StaticShell kicker="How it works" title="Four steps, zero ceremony">
      <ol className="grid gap-x-6 gap-y-8 md:grid-cols-2">
        {HOW_IT_WORKS_STEPS.map((step) => (
          <li key={step.number} className="border-t-[3px] border-ink pt-3">
            <span aria-hidden className="block font-display text-7xl leading-none">
              {step.number}
            </span>
            <h2 className="mt-2 font-mono text-xs font-bold uppercase tracking-widest">
              <span className="sr-only">Step {step.number}: </span>
              {step.title}
            </h2>
            <p className="mt-2">{step.copy}</p>
          </li>
        ))}
      </ol>

      <p>
        That is the whole loop. No review gates, no waiting — the problem board
        is open.
      </p>

      <div>
        <Link to="/problems" className={buttonClasses('primary')}>
          Start with a problem
        </Link>
      </div>
    </StaticShell>
  );
}
