/** The six problem fields MANABI keeps, with their display labels. */
export const FIELD_VALUES = [
  'web-dev',
  'app-dev',
  'aiml',
  'cyber-security',
  'devops-cloud',
  'blockchain',
] as const;

export type FieldValue = (typeof FIELD_VALUES)[number];

export const FIELD_LABELS: Record<FieldValue, string> = {
  'web-dev': 'Web Dev',
  'app-dev': 'App Dev',
  aiml: 'AI / ML',
  'cyber-security': 'Cyber Security',
  'devops-cloud': 'DevOps Cloud',
  blockchain: 'Blockchain',
};

export function fieldLabel(value: string): string {
  return FIELD_LABELS[value as FieldValue] ?? value;
}
