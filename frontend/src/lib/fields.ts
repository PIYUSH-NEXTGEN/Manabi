/** Fields with live catalog entries. */
export const FIELD_VALUES = ['web-dev', 'aiml'] as const;

/** Field names shown as disabled placeholders until their packs return. */
export const UPCOMING_FIELD_VALUES = [
  'app-dev',
  'cyber-security',
  'devops-cloud',
  'blockchain',
] as const;

export type FieldValue = (typeof FIELD_VALUES)[number];
export type UpcomingFieldValue = (typeof UPCOMING_FIELD_VALUES)[number];
export type KnownFieldValue = FieldValue | UpcomingFieldValue;

export const FIELD_LABELS: Record<KnownFieldValue, string> = {
  'web-dev': 'Web Dev',
  'app-dev': 'App Dev',
  aiml: 'AI / ML',
  'cyber-security': 'Cyber Security',
  'devops-cloud': 'DevOps Cloud',
  blockchain: 'Blockchain',
};

export function isActiveField(value: string): value is FieldValue {
  return (FIELD_VALUES as readonly string[]).includes(value);
}

export function fieldLabel(value: string): string {
  return FIELD_LABELS[value as KnownFieldValue] ?? value;
}
