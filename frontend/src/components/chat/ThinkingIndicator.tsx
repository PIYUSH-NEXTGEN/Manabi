/** Assistant-side "typing" bubble shown while the reply is being generated. */
export function ThinkingIndicator() {
  return (
    <li
      role="status"
      className="max-w-[92%] border border-ink bg-sheet p-2"
    >
      <p className="sr-only">Manabi is typing a reply</p>
      <div aria-hidden="true" className="flex items-center gap-1.5 px-1 py-0.5">
        <span className="thinking-dot inline-block h-1.5 w-1.5 bg-ink" />
        <span className="thinking-dot inline-block h-1.5 w-1.5 bg-ink" />
        <span className="thinking-dot inline-block h-1.5 w-1.5 bg-ink" />
      </div>
    </li>
  );
}
