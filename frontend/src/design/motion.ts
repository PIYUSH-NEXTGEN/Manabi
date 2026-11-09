export const EASE_SNAP: [number, number, number, number] = [0.2, 0.9, 0.2, 1];

export const slideUpReveal = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.28, ease: EASE_SNAP } },
};
