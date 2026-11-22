/**
 * A fullscreen rain wipe between the two themes.
 *
 * Adapted from PinUI's Theme Switch "rain" effect: drops of the next theme's
 * colour fall at terminal velocity, splash, and leave puddles that spread,
 * merge and finally cover the whole viewport. The page theme is flipped only
 * once the puddles have covered every pixel, so the change is seamless.
 *
 * Everything is painted in a fixed overlay above the app; the caller supplies
 * the point the first heavy drop should land on (the theme button).
 */

export type WipeTheme = 'light' | 'dark';

type Origin = { x: number; y: number };

type WipeOptions = {
  /** Theme the wipe lands on. */
  to: WipeTheme;
  /** Where the hero drop lands, in viewport coordinates. */
  origin?: Origin;
  /** Called once the next theme covers the viewport. */
  onCommit: () => void;
  /** Called after the overlay has been removed. */
  onDone?: () => void;
};

/* Mirrors --paper in design/tokens.css so the commit is seamless. */
const THEME_BG: Record<WipeTheme, string> = {
  light: '#ffffff',
  dark: '#070a0e',
};

const RAIN = {
  spawnMs: 900,
  windDeg: 9,
  puddleArea: 85 * 85,
  minPuddles: 30,
  maxPuddles: 170,
  ambientRatio: 1.4,
  spreadTauMs: 260,
  creepPxPerS: 14,
  mergeMs: 460,
  splashGravity: 2400,
  rippleMs: 420,
};

const WATCHDOG_MS = 6000;

type Lobe = { dx: number; dy: number; s: number };

type Spot = {
  x: number;
  y: number;
  born: number;
  r0: number;
  rmax: number;
  lobes: Lobe[];
  tau?: number;
  creep?: number;
};

type Drop = {
  z: number;
  speed: number;
  len: number;
  width: number;
  alpha: number;
  x0: number;
  y0: number;
  landX: number;
  landY: number;
  spawn: number;
  land: number;
  puddle: boolean;
  landed: boolean;
  hero?: boolean;
  spot?: Spot;
};

type Plan = {
  drops: Drop[];
  tan: number;
  scale: number;
  mergeStart: number;
  mergeK: number;
};

const clamp = (v: number, lo: number, hi: number) =>
  Math.max(lo, Math.min(hi, v));
const rand = (a: number, b: number) => a + Math.random() * (b - a);
const easeInOutCubic = (p: number) =>
  p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const easeOutCubic = (p: number) => 1 - Math.pow(1 - p, 3);

/* "#rrggbb" at zero alpha: fading to "transparent" fades through black in some engines */
function transparentOf(hex: string) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, 0)`;
}

function puddleBase(p: Spot, t: number) {
  const age = Math.max(0, t - p.born);
  const tau = p.tau || RAIN.spreadTauMs;
  const creep = p.creep != null ? p.creep : RAIN.creepPxPerS;
  return (
    p.r0 +
    (p.rmax - p.r0) * (1 - Math.exp(-age / tau)) +
    (creep * age) / 1000
  );
}

/*
 * The smallest uniform scale k at which the spots' main circles cover every
 * pixel. Cell centres are sampled with half a cell's diagonal added to each
 * distance, which makes it a bound for every pixel in the cell rather than an
 * estimate. Spots are bucketed and the search stops once no farther bucket
 * could do better, so it is exact without being slow.
 */
function coverageScale(spots: Spot[], t: number, w: number, h: number) {
  const n = spots.length;
  if (!n) return 1;
  const cell = Math.max(40, Math.max(w, h) / 48);
  const cols = Math.ceil(w / cell);
  const rows = Math.ceil(h / cell);
  const half = Math.hypot(w / cols, h / rows) / 2;
  const bases = new Array<number>(n);
  let maxBase = 0;
  for (let i = 0; i < n; i++) {
    bases[i] = puddleBase(spots[i], t);
    if (bases[i] > maxBase) maxBase = bases[i];
  }
  const B = cell * 2;
  const nx = Math.max(1, Math.ceil(w / B));
  const ny = Math.max(1, Math.ceil(h / B));
  const buckets: number[][] = Array.from({ length: nx * ny }, () => []);
  for (let i = 0; i < n; i++) {
    const bx = clamp(Math.floor(spots[i].x / B), 0, nx - 1);
    const by = clamp(Math.floor(spots[i].y / B), 0, ny - 1);
    buckets[by * nx + bx].push(i);
  }
  const maxRing = Math.max(nx, ny);
  let worst = 1;
  for (let iy = 0; iy < rows; iy++) {
    for (let ix = 0; ix < cols; ix++) {
      const x = ((ix + 0.5) * w) / cols;
      const y = ((iy + 0.5) * h) / rows;
      const cbx = clamp(Math.floor(x / B), 0, nx - 1);
      const cby = clamp(Math.floor(y / B), 0, ny - 1);
      let best = Infinity;
      for (let r = 0; r <= maxRing; r++) {
        if (r >= 1 && ((r - 1) * B + half) / maxBase >= best) break;
        for (let gy = cby - r; gy <= cby + r; gy++) {
          if (gy < 0 || gy >= ny) continue;
          for (let gx = cbx - r; gx <= cbx + r; gx++) {
            if (gx < 0 || gx >= nx) continue;
            if (Math.max(Math.abs(gx - cbx), Math.abs(gy - cby)) !== r)
              continue;
            for (const q of buckets[gy * nx + gx]) {
              const need =
                (Math.hypot(x - spots[q].x, y - spots[q].y) + half) /
                bases[q];
              if (need < best) best = need;
            }
          }
        }
      }
      if (best > worst) worst = best;
    }
  }
  return worst * 1.01;
}

/* a jittered grid: random-looking, with no large dry holes */
function stratified(n: number, w: number, h: number) {
  const cols = Math.max(1, Math.round(Math.sqrt((n * w) / h)));
  const rows = Math.max(1, Math.ceil(n / cols));
  const cells: [number, number][] = [];
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) cells.push([c, r]);
  for (let i = cells.length - 1; i > 0; i--) {
    const j = (Math.random() * (i + 1)) | 0;
    [cells[i], cells[j]] = [cells[j], cells[i]];
  }
  const cw = w / cols;
  const ch = h / rows;
  return cells
    .slice(0, n)
    .map(([c, r]) => ({ x: (c + Math.random()) * cw, y: (r + Math.random()) * ch }));
}

/* a wet spot is not a perfect disc: bumps where the splash spread further, and specks flung past its edge */
function makeSpot(d: Drop, scale: number): Spot {
  const lobes: Lobe[] = [];
  const nl = 3 + ((Math.random() * 3) | 0);
  for (let l = 0; l < nl; l++) {
    const a = rand(0, Math.PI * 2);
    const off = rand(0.55, 0.85);
    lobes.push({ dx: Math.cos(a) * off, dy: Math.sin(a) * off, s: rand(0.28, 0.46) });
  }
  const ns = 2 + ((Math.random() * 4) | 0);
  for (let m = 0; m < ns; m++) {
    const a = rand(0, Math.PI * 2);
    const off = rand(1.2, 1.9);
    lobes.push({ dx: Math.cos(a) * off, dy: Math.sin(a) * off, s: rand(0.06, 0.14) });
  }
  return {
    x: d.landX,
    y: d.landY,
    born: d.land,
    lobes,
    r0: 1.5 + 2.5 * d.z,
    /* the button's spot spills well past the icon, so it reads */
    rmax: (d.hero ? 64 : 10 + 38 * d.z) * scale * rand(0.9, 1.15),
  };
}

function planRain(w: number, h: number, origin: Origin): Plan {
  const tan = Math.tan((RAIN.windDeg * Math.PI) / 180);
  const nP = clamp(
    Math.round((w * h) / RAIN.puddleArea),
    RAIN.minPuddles,
    RAIN.maxPuddles,
  );
  const nA = Math.round(nP * RAIN.ambientRatio);
  const scale = clamp(Math.sqrt((w * h) / (1280 * 800)), 0.75, 1.35);
  const drops: Drop[] = [];

  const makeDrop = (
    z: number,
    landX: number,
    landY: number,
    puddle: boolean,
  ): Drop => {
    const speed = 1300 + 1500 * z; // terminal velocity: near drops read faster
    const len = (16 + 40 * z) * scale;
    const y0 = -len - rand(0, 80);
    /* the shower builds: spawn density rises linearly */
    const spawn = RAIN.spawnMs * Math.sqrt(Math.random());
    return {
      z,
      speed,
      len,
      width: 0.8 + 1.4 * z,
      alpha: 0.3 + 0.6 * z,
      x0: landX - tan * (landY - y0),
      y0,
      landX,
      landY,
      spawn,
      land: spawn + ((landY - y0) / speed) * 1000,
      puddle,
      landed: false,
    };
  };

  for (const p of stratified(nP, w, h))
    drops.push(makeDrop(rand(0.55, 1), p.x, p.y, true));
  for (let i = 0; i < nA; i++)
    drops.push(
      makeDrop(rand(0.1, 0.5), rand(-0.05, 1.05) * w, rand(0.05, 1.02) * h, false),
    );

  /* a near drop lands on the button mid-shower, so it changes with the rain */
  const hero = makeDrop(1, origin.x, origin.y, true);
  const travel = ((origin.y - hero.y0) / hero.speed) * 1000;
  hero.land = Math.max(travel + 40, RAIN.spawnMs * 0.55 + travel * 0.5);
  hero.spawn = hero.land - travel;
  hero.hero = true;
  drops.push(hero);

  /* every wet spot is decided now, while nothing moves, so the final merge costs no frame mid-shower */
  let lastLand = 0;
  const spots: Spot[] = [];
  for (const d of drops) {
    if (!d.puddle) continue;
    if (d.land > lastLand) lastLand = d.land;
    d.spot = makeSpot(d, scale);
    spots.push(d.spot);
  }
  const mergeStart = lastLand + 40;
  const mergeK = Math.max(
    1,
    coverageScale(spots, mergeStart + RAIN.mergeMs, w, h),
  );
  return { drops, tan, scale, mergeStart, mergeK };
}

function paintSpots(
  c: CanvasRenderingContext2D,
  w: number,
  h: number,
  spots: Spot[],
  t: number,
  k: number,
  color: string,
) {
  c.clearRect(0, 0, w, h);
  c.fillStyle = color;
  c.beginPath();
  for (const p of spots) {
    const r = puddleBase(p, t) * k;
    c.moveTo(p.x + r, p.y);
    c.arc(p.x, p.y, r, 0, Math.PI * 2);
    for (const lb of p.lobes) {
      const lx = p.x + lb.dx * r;
      const ly = p.y + lb.dy * r;
      const lr = r * lb.s;
      c.moveTo(lx + lr, ly);
      c.arc(lx, ly, lr, 0, Math.PI * 2);
    }
  }
  c.fill('nonzero');
}

let activeOverlay: HTMLElement | null = null;

export function playRainWipe({
  to,
  origin,
  onCommit,
  onDone,
}: WipeOptions): void {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    onCommit();
    onDone?.();
    return;
  }
  if (activeOverlay) return;

  const reduced =
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hidden = document.visibilityState !== 'visible';
  const canPaint = typeof window.CanvasRenderingContext2D !== 'undefined';
  if (reduced || hidden || !canPaint) {
    onCommit();
    onDone?.();
    return;
  }

  const overlay = document.createElement('div');
  overlay.setAttribute('aria-hidden', 'true');
  overlay.style.cssText =
    'position:fixed;inset:0;z-index:9999;overflow:hidden;pointer-events:none;';
  document.body.appendChild(overlay);
  activeOverlay = overlay;

  const w = overlay.clientWidth || window.innerWidth;
  const h = overlay.clientHeight || window.innerHeight;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  const makeCanvas = (z: number) => {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = `position:absolute;inset:0;z-index:${z};display:block;width:100%;height:100%;`;
    canvas.width = Math.max(1, Math.round(w * dpr));
    canvas.height = Math.max(1, Math.round(h * dpr));
    overlay.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { canvas, ctx };
  };

  const wet = makeCanvas(1);
  const sky = makeCanvas(2);

  let done = false;
  let committed = false;
  let watchdog = 0;

  const teardown = () => {
    if (done) return;
    done = true;
    window.clearTimeout(watchdog);
    overlay.remove();
    activeOverlay = null;
    document.documentElement.classList.remove('theme-wipe-committing');
    onDone?.();
  };

  const commit = () => {
    if (committed) return;
    committed = true;
    /* The page has its own colour transitions; freeze them so the theme flips
       instantly under the overlay instead of cross-fading once it is removed. */
    document.documentElement.classList.add('theme-wipe-committing');
    onCommit();
    /* The class flip above is synchronous, so the page is already in the new
       theme. Drop the fully-covered overlay now instead of holding a solid
       colour on screen for another frame, but keep transitions frozen for a
       couple of frames so the repaint cannot cross-fade. */
    overlay.remove();
    activeOverlay = null;
    requestAnimationFrame(() => requestAnimationFrame(teardown));
  };

  if (!wet || !sky) {
    if (!committed) {
      committed = true;
      onCommit();
    }
    teardown();
    return;
  }

  const color = THEME_BG[to];
  const plan = planRain(w, h, origin ?? { x: w / 2, y: h / 2 });
  const { ctx } = sky;
  const wctx = wet.ctx;
  const puddles: Spot[] = [];
  const splashes: {
    x: number;
    y: number;
    vx: number;
    vy: number;
    r: number;
    born: number;
    life: number;
  }[] = [];
  const rings: {
    x: number;
    y: number;
    born: number;
    rmax: number;
    z: number;
  }[] = [];
  const tilt = -Math.atan(plan.tan);
  /* one shared streak gradient in unit space, placed per drop by a transform */
  const streak = ctx.createLinearGradient(0, -1, 0, 0);
  streak.addColorStop(0, transparentOf(color));
  streak.addColorStop(1, color);
  const t0 = performance.now();

  const land = (d: Drop) => {
    const { landX: x, landY: y } = d;
    if (d.puddle && d.spot) puddles.push(d.spot);
    /* a crown splash: droplets thrown up and out, more for near drops */
    const n = Math.round(2 + d.z * 4);
    for (let j = 0; j < n; j++) {
      const ang = rand(-Math.PI * 0.92, -Math.PI * 0.08);
      const v = rand(60, 210) * (0.5 + d.z);
      splashes.push({
        x,
        y,
        vx: Math.cos(ang) * v,
        vy: Math.sin(ang) * v,
        r: rand(0.6, 1.2) * (0.6 + d.z),
        born: d.land,
        life: rand(200, 340),
      });
    }
    /* a ripple only on dry ground: inside a fresh puddle a ring reads as a target, not water */
    if (!d.puddle)
      rings.push({
        x,
        y,
        born: d.land,
        rmax: (5 + 16 * d.z) * plan.scale,
        z: d.z,
      });
  };

  const drawSky = (t: number) => {
    ctx.fillStyle = streak;
    for (const d of plan.drops) {
      if (d.landed || t < d.spawn) continue;
      const y = d.y0 + (d.speed * (t - d.spawn)) / 1000;
      const x = d.x0 + plan.tan * (y - d.y0);
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(tilt);
      ctx.scale(1, d.len);
      ctx.globalAlpha = d.alpha;
      ctx.fillRect(-d.width / 2, -1, d.width, 1);
      ctx.restore();
    }
    /* ripple rings, a little flattened, as seen at an angle */
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    for (let r = rings.length - 1; r >= 0; r--) {
      const g = rings[r];
      const p = (t - g.born) / RAIN.rippleMs;
      if (p >= 1) {
        rings.splice(r, 1);
        continue;
      }
      const rad = 1 + g.rmax * easeOutCubic(p);
      ctx.globalAlpha = (1 - p) * (0.3 + 0.4 * g.z);
      ctx.beginPath();
      ctx.ellipse(g.x, g.y, rad, rad * 0.85, 0, 0, Math.PI * 2);
      ctx.stroke();
    }
    /* crown droplets under gravity */
    ctx.fillStyle = color;
    for (let s = splashes.length - 1; s >= 0; s--) {
      const sp = splashes[s];
      const age = t - sp.born;
      if (age >= sp.life) {
        splashes.splice(s, 1);
        continue;
      }
      const at = age / 1000;
      ctx.globalAlpha = 1 - age / sp.life;
      ctx.beginPath();
      ctx.arc(
        sp.x + sp.vx * at,
        sp.y + sp.vy * at + 0.5 * RAIN.splashGravity * at * at,
        sp.r,
        0,
        Math.PI * 2,
      );
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  };

  const frame = (now: number) => {
    if (done) return;
    const t = now - t0;
    for (const d of plan.drops) {
      if (!d.landed && t >= d.land) {
        d.landed = true;
        land(d);
      }
    }
    let k = 1;
    if (t >= plan.mergeStart) {
      const p = clamp((t - plan.mergeStart) / RAIN.mergeMs, 0, 1);
      k = 1 + (plan.mergeK - 1) * easeInOutCubic(p);
      /*
       * Commit the moment the puddles actually cover the viewport, not when
       * the merge animation ends. The coverage bound is conservative, so the
       * last few percent of the merge would otherwise leave the solid
       * next-theme colour on screen as a blank frame.
       */
      if (p >= 1 || coverageScale(puddles, t, w, h) <= k) {
        paintSpots(wctx, w, h, puddles, t, k, color);
        commit();
        return;
      }
    }
    paintSpots(wctx, w, h, puddles, t, k, color);
    ctx.clearRect(0, 0, w, h);
    drawSky(t);
    requestAnimationFrame(frame);
  };

  watchdog = window.setTimeout(() => {
    if (!committed) {
      committed = true;
      onCommit();
    }
    teardown();
  }, WATCHDOG_MS);

  requestAnimationFrame(frame);
}
