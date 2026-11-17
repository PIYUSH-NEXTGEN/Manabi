import type { ProblemOut } from '@/api/client';

export const GOAL_LABELS = {
  resume: 'Resume',
  hackathon: 'Hackathon',
  learning: 'Learning',
} as const;

export type GoalValue = keyof typeof GOAL_LABELS;

export function goalLabel(goal: ProblemOut['goal'] | null | undefined): string | null {
  if (!goal) return null;
  return GOAL_LABELS[goal] ?? null;
}
