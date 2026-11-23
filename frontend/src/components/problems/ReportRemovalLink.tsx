import { CONTACT_EMAIL } from '@/lib/contact';

export function ReportRemovalLink({
  sourceName,
  sourceId,
}: {
  sourceName: string;
  sourceId?: string | null;
}) {
  const label = 'Report / request removal';
  const subject = encodeURIComponent(
    `Removal request: ${sourceName}${sourceId ? ` ${sourceId}` : ''}`,
  );
  return (
    <a
      href={`mailto:${CONTACT_EMAIL}?subject=${subject}`}
      className="font-mono text-label font-bold uppercase tracking-widest text-accent underline underline-offset-4"
    >
      {label}
    </a>
  );
}
