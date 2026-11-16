import type { MascotState } from './types';

/**
 * Rive asset setup.
 *
 * The `.riv` file is intentionally not in the repo. To switch the mascot from
 * the PNG fallback to Rive:
 *
 *   1. Add `frontend/public/rive/manabi-mascot.riv`.
 *   2. Set `VITE_MASCOT_RIVE_SRC=/rive/manabi-mascot.riv` in `frontend/.env`.
 *
 * The file must contain an artboard named `Mascot` with a state machine named
 * `MascotState`. That state machine needs one number input named `state` whose
 * values map to the entries below. State transitions and blending live inside
 * the Rive file, so the app only sets the number.
 *
 * See `README.md` in this folder for the full asset checklist.
 */
export const MASCOT_RIVE_SRC = (
  import.meta.env.VITE_MASCOT_RIVE_SRC ?? ''
).trim();

export const MASCOT_RIVE = {
  artboard: 'Mascot',
  stateMachine: 'MascotState',
  stateInput: 'state',
  stateValues: {
    idle: 0,
    working: 1,
    thinking: 2,
    celebrating: 3,
  } satisfies Record<MascotState, number>,
} as const;
