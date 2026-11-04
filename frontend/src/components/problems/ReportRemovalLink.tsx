import { Link } from 'react-router-dom';

const CONTACT_EMAIL = import.meta.env.VITE_CONTACT_EMAIL as string | undefined;

export function ReportRemovalLink({
  sourceName,
  sourceId,
}: {
  sourceName: string;
  sourceId?: string | null;
}) {
  const label = 'Report / request removal';
  if (CONTACT_EMAIL) {
    const subject = encodeURIComponent(
      `Removal request: ${sourceName}${sourceId ? ` ${sourceId}` : ''}`,
    );
    return (
      <a
        href={`mailto:${CONTACT_EMAIL}?subject=${subject}`}
        className="font-mono text-[11px] font-bold uppercase tracking-widest text-accent underline underline-offset-4"
      >
        {label}
      </a>
    );
  }
  return (
    <Link
      to="/contact"
      className="font-mono text-[11px] font-bold uppercase tracking-widest text-accent underline underline-offset-4"
    >
      {label}
    </Link>
  );
}
