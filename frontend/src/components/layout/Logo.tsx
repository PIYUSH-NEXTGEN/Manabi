/**
 * MANABI mark: a catalog record with a folded corner and an M monogram.
 * The small accent rule is the index tab — the same orange marker used
 * throughout the interface to tag a record.
 */
export function Logo({ className }: { className?: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`shrink-0 ${className ?? ''}`}
      aria-hidden
    >
      <path
        d="M4 4h24v17.5L21.5 28H4V4Z"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinejoin="miter"
      />
      <path
        d="M21.5 28v-6.5H28"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinejoin="miter"
      />
      <path
        d="M7 22V10l6 7 6-7v12"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="square"
        strokeLinejoin="miter"
      />
      <rect x="7" y="24.5" width="7" height="2" fill="var(--accent)" />
    </svg>
  );
}
