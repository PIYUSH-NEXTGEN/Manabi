import { motion } from 'motion/react';
import { slideUpReveal } from '@/design/motion';
import { HOW_IT_WORKS_STEPS } from './steps';

export function HowItWorks() {
  return (
    <section className="border-b-[3px] border-ink">
      <div className="mx-auto w-[min(1200px,96vw)] py-12">
        <h2 className="mb-8 font-mono text-sm font-bold uppercase tracking-widest">
          How it works
        </h2>
        <ol className="grid gap-8 md:grid-cols-4">
          {HOW_IT_WORKS_STEPS.map((step, index) => (
            <motion.li
              key={step.number}
              variants={slideUpReveal}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.3 }}
              transition={{ delay: index * 0.06 }}
              className="border-t-[3px] border-ink pt-3"
            >
              <span
                aria-hidden
                className="block font-display text-6xl leading-none text-ink md:text-7xl"
              >
                {step.number}
              </span>
              <h3 className="mt-2 font-mono text-xs font-bold uppercase tracking-widest">
                <span className="sr-only">Step {step.number}: </span>
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-snug">{step.copy}</p>
            </motion.li>
          ))}
        </ol>
      </div>
    </section>
  );
}
