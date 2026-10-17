import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

/**
 * Renders a Markdown string (LLM reply or seeded scenario) in the brutalist
 * design language. Raw HTML stays inert — react-markdown ignores it by default,
 * per agent.md ("react-markdown, no raw HTML").
 *
 * With `problemsAsLinks`, catalog tokens like [P17] become links to the problem
 * detail page, per the chat contract (agent.md §8.8).
 */
export function Markdown({
  children,
  problemsAsLinks = false,
  className,
}: {
  children: string;
  problemsAsLinks?: boolean;
  className?: string;
}) {
  const source = problemsAsLinks
    ? children.replace(/\[P(\d+)\](?!\()/g, '[P$1](/problems/$1)')
    : children;

  return (
    <div className={className}>
      <ReactMarkdown components={components}>{source}</ReactMarkdown>
    </div>
  );
}

const linkClass = 'font-bold underline decoration-2 underline-offset-2';
const headingClass =
  'mt-3 mb-1 font-mono text-xs font-bold uppercase tracking-widest first:mt-0';

function heading(Tag: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6') {
  return ({ children }: { children?: ReactNode }) => (
    <Tag className={headingClass}>{children}</Tag>
  );
}

const components = {
  p: ({ children }: { children?: ReactNode }) => (
    <p className="mb-2 text-sm last:mb-0">{children}</p>
  ),
  a: ({ href, children }: { href?: string; children?: ReactNode }) => {
    if (href && href.startsWith('/')) {
      return (
        <Link to={href} className={linkClass}>
          {children}
        </Link>
      );
    }
    const external = Boolean(href && /^https?:/i.test(href));
    return (
      <a
        href={href}
        className={linkClass}
        target={external ? '_blank' : undefined}
        rel={external ? 'noreferrer' : undefined}
      >
        {children}
      </a>
    );
  },
  ul: ({ children }: { children?: ReactNode }) => (
    <ul className="mb-2 list-disc space-y-1 pl-5 last:mb-0">{children}</ul>
  ),
  ol: ({ children }: { children?: ReactNode }) => (
    <ol className="mb-2 list-decimal space-y-1 pl-5 last:mb-0">{children}</ol>
  ),
  li: ({ children }: { children?: ReactNode }) => <li>{children}</li>,
  h1: heading('h1'),
  h2: heading('h2'),
  h3: heading('h3'),
  h4: heading('h4'),
  h5: heading('h5'),
  h6: heading('h6'),
  strong: ({ children }: { children?: ReactNode }) => <strong>{children}</strong>,
  em: ({ children }: { children?: ReactNode }) => <em>{children}</em>,
  blockquote: ({ children }: { children?: ReactNode }) => (
    <blockquote className="mb-2 border-l-4 border-yellow pl-2 last:mb-0">
      {children}
    </blockquote>
  ),
  hr: () => <hr className="my-3 border-t-[3px] border-ink" />,
  code: ({ children }: { children?: ReactNode }) => (
    <code className="bg-yellow/40 px-1 font-mono">{children}</code>
  ),
  pre: ({ children }: { children?: ReactNode }) => (
    <pre className="mb-2 overflow-x-auto border-[3px] border-ink bg-paper p-2 font-mono text-xs last:mb-0">
      {children}
    </pre>
  ),
  table: ({ children }: { children?: ReactNode }) => (
    <table className="mb-2 w-full border-collapse text-left last:mb-0">
      {children}
    </table>
  ),
  th: ({ children }: { children?: ReactNode }) => (
    <th className="border-[2px] border-ink bg-paper px-2 py-1 font-bold">
      {children}
    </th>
  ),
  td: ({ children }: { children?: ReactNode }) => (
    <td className="border-[2px] border-ink px-2 py-1">{children}</td>
  ),
};