# MANABI mascot

`Mascot` plays one of four states: `idle`, `working`, `thinking`, `celebrating`.
`idle` is the default. Usage:

```tsx
import { Mascot } from '@/components/mascot';

<Mascot state="working" className="w-40" />
<Mascot state="idle" className="w-28" label="MANABI mascot" />
```

`className` controls size and placement. Omit `label` when the mascot is
decorative so assistive technology skips it.

## Current status: PNG fallback

No `.riv` file has been provided yet, so the component renders the layered PNGs
in `frontend/src/assets/mascot/` and animates only the parts, with anime.js:

- the eyes glance around, blink, squint, double-blink and occasionally open wide;
- the hand taps the laptop in the `working` state and stretches or shifts
  occasionally in every state.

The body itself does not move at all. The PNGs have a transparent background
(edge-connected white was removed), so the mascot sits directly on the page and
follows the light/dark background. The layers are `base.png`, `eye-left.png`,
`eye-right.png` and `hand.png`, all on the same 272×241 canvas. The fallback
pauses when scrolled out of view and stays fully static under
`prefers-reduced-motion: reduce`.

## Interactions

- **Nearby cursor**: within roughly one mascot width the eyes follow the pointer
  and open a little, and the hand lifts slightly.
- **Hover**: the eyes open wider, keep tracking the cursor and the hand lifts.
- **Tap / touch**: the eyes flinch through a quick double-squint and the hand
  bounces, then the normal loop resumes.

All reactions live in `MascotFallback` and only touch the eye and hand layers.
The placement wrapper in `AppLayout` sets `pointer-events-auto` on the mascot
because its parent overlay is `pointer-events-none`.

Note: blinks, squints, glances, wide-eyed looks and hand gestures are the limit
of what a flat illustration can articulate. Full hand, eye and face rigging
belongs in the Rive file.

## Required Rive asset

The Rive runtime (`@rive-app/react-canvas`) is installed and wired up, but it
loads only once an asset URL is configured. To enable it:

1. Add the exported file at `frontend/public/rive/manabi-mascot.riv`.
2. Set in `frontend/.env`:

   ```
   VITE_MASCOT_RIVE_SRC=/rive/manabi-mascot.riv
   ```

The file must contain:

| Item | Required name | Notes |
| --- | --- | --- |
| Artboard | `Mascot` | Contains the character |
| State machine | `MascotState` | Blends between the four states |
| Number input | `state` | `0` idle, `1` working, `2` thinking, `3` celebrating |

The names live in `config.ts`; change them there if the Rive file uses
different names. State blending should happen inside the Rive state machine so
transitions stay natural; the app only writes the number input.

Recommended export: one artboard, vector shapes, transparent background, same
272:241 frame as the PNG so layout does not shift. The `working` state should
animate the hands typing on the laptop, plus small eye and face movement. If the
asset is missing or fails to load, the component automatically falls back to the
PNG.

## Performance and accessibility

- Rive is code-split with `React.lazy`; the runtime is not in the main bundle.
- Playback pauses when the mascot is offscreen and under reduced motion.
- Rive listeners are disabled because the mascot is not interactive.
- The `idle` loop is deliberately slow and small; keep new states similarly
  subtle.
