/**
 * MANABI mark: the minimal emblem from the favicon. A red brush stroke sits
 * inside a ringed disc. The ring inherits the current text colour so the mark
 * settles onto both light and dark surfaces.
 */
export function Logo({
  className,
  size = 22,
}: {
  className?: string;
  size?: number;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`shrink-0 ${className ?? ''}`}
      aria-hidden
    >
      <circle cx="32" cy="32" r="29" fill="var(--paper)" />
      <circle cx="32" cy="32" r="29" stroke="currentColor" strokeWidth="5" />
      <path
        fill="var(--danger)"
        transform="translate(-14.45 -14.45) scale(1.4)"
        d="M22 22C30 24 38 30 44 38C46 41 45 45 41 45C37 45 33 41 30 36C27 31 24 27 22 22Z"
      />
    </svg>
  );
}
