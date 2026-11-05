/**
 * MANABI mark: a solid geometric M cut from the same grid as the interface.
 * The accent square on the baseline is the record tab — the same orange
 * marker used across the UI to tag a record.
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
        fill="currentColor"
        d="M3 26V6h4.4l8.6 8.4L24.6 6H29v20h-4.4V12l-8.6 8.8L7.4 12v14H3Z"
      />
      <rect x="14.4" y="22.4" width="3.2" height="3.6" fill="var(--accent)" />
    </svg>
  );
}
