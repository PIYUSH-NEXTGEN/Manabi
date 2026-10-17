export interface HowItWorksStep {
  number: string;
  title: string;
  copy: string;
}

export const HOW_IT_WORKS_STEPS: HowItWorksStep[] = [
  {
    number: '01',
    title: 'Find',
    copy: 'Search real briefs from real sources — every card links back to where it came from.',
  },
  {
    number: '02',
    title: 'Claim',
    copy: 'Pick one. Put your name on it before someone else does.',
  },
  {
    number: '03',
    title: 'Link your repo',
    copy: 'Point MANABI at your GitHub repository.',
  },
  {
    number: '04',
    title: 'Get tracked',
    copy: 'Commits, README, good-first-issues — tracked without you doing anything.',
  },
];
