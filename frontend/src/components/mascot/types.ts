export type MascotState = 'idle' | 'working' | 'thinking' | 'celebrating';

export type MascotProps = {
  /** Which animation the mascot plays. Defaults to `idle`. */
  state?: MascotState;
  /** Sizing and placement classes for the wrapper element. */
  className?: string;
  /**
   * Accessible label. Omit it when the mascot is purely decorative so screen
   * readers skip it.
   */
  label?: string;
};
