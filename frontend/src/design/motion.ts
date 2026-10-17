export const EASE_SNAP: [number, number, number, number] = [0.2, 0.9, 0.2, 1];
export const DURATION_PAGE_WIPE = 0.35;

export const letterDrop = {
  hidden: { opacity: 0, y: -48 },
  show: (index: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: index * 0.05, duration: 0.28, ease: EASE_SNAP },
  }),
};

export const slideUpReveal = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.28, ease: EASE_SNAP } },
};

export const wobble = {
  rest: { rotate: 0 },
  hover: { rotate: 3, transition: { duration: 0.12, ease: EASE_SNAP } },
};
