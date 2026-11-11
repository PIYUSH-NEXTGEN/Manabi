import { useEffect, useReducer, useRef, type KeyboardEvent, type PointerEvent } from 'react';
import { usePrefersReducedMotion } from '@/lib/usePrefersReducedMotion';

/**
 * A tiny arcade screen for the submission-progress card while the checks run.
 * The ship auto-fires on its own (and gently picks its own targets), but the
 * pointer or arrow keys hand control to the player. Everything is plain SVG so
 * it stays crisp at any size and inherits the print-poster look of the app.
 */

const VIEW_W = 320;
const VIEW_H = 180;

const ENEMY_UNIT = 1.6;
const ENEMY_COLS = 5;
const ENEMY_ROWS = 3;
const ENEMY_GAP_X = 34;
const ENEMY_GAP_Y = 21;
const ENEMY_W = 11 * ENEMY_UNIT;
const ENEMY_H = 8 * ENEMY_UNIT;
const FORMATION_TOP = 30;
const FORMATION_LEFT = (VIEW_W - (ENEMY_COLS - 1) * ENEMY_GAP_X - ENEMY_W) / 2;

const SHIP_UNIT = 2.2;
const SHIP_W = 11 * SHIP_UNIT;
const SHIP_H = 7 * SHIP_UNIT;
const SHIP_Y = 152;

const BULLET_SPEED = 260;
const MAX_SWAY = 22;

const CREAM = '#efe7d5';
const ACCENT = '#ec6a34';

const ENEMY_A = [
  '..X.....X..',
  '...X...X...',
  '..XXXXXXX..',
  '.XX.XXX.XX.',
  'XXXXXXXXXXX',
  'X.XXXXXXX.X',
  'X.X.....X.X',
  '...XX.XX...',
];

const ENEMY_B = [
  '..X.....X..',
  'X..X...X..X',
  'X.XXXXXXX.X',
  'XXX.XXX.XXX',
  'XXXXXXXXXXX',
  '.XXXXXXXXX.',
  '..X.....X..',
  '.X.......X.',
];

const SHIP_ROWS = [
  '.....X.....',
  '....XXX....',
  '....XOX....',
  '..XXXXXXX..',
  'XXXXXXXXXXX',
  'XX.XXXXX.XX',
  'X...X.X...X',
];

function bitmapPath(rows: string[], unit: number, mark = 'X'): string {
  const parts: string[] = [];
  for (let y = 0; y < rows.length; y += 1) {
    const row = rows[y]!;
    let x = 0;
    while (x < row.length) {
      if (row[x] === mark) {
        let run = 1;
        while (row[x + run] === mark) run += 1;
        const w = (run * unit).toFixed(1);
        parts.push(
          `M${(x * unit).toFixed(1)} ${(y * unit).toFixed(1)}h${w}v${unit.toFixed(1)}h-${w}Z`,
        );
        x += run;
      } else {
        x += 1;
      }
    }
  }
  return parts.join('');
}

const ENEMY_A_PATH = bitmapPath(ENEMY_A, ENEMY_UNIT);
const ENEMY_B_PATH = bitmapPath(ENEMY_B, ENEMY_UNIT);
const SHIP_PATH = bitmapPath(SHIP_ROWS, SHIP_UNIT);
const SHIP_COCKPIT_PATH = bitmapPath(SHIP_ROWS, SHIP_UNIT, 'O');

function pseudoRandom(seed: number): number {
  const value = Math.sin(seed * 12.9898) * 43758.5453;
  return value - Math.floor(value);
}

const STARS = Array.from({ length: 28 }, (_, index) => ({
  x: 6 + pseudoRandom(index + 1) * (VIEW_W - 12),
  y: pseudoRandom(index + 9.3) * VIEW_H,
  radius: pseudoRandom(index + 3.7) < 0.84 ? 0.7 : 1.3,
  speed: 3 + pseudoRandom(index + 5.1) * 8,
  opacity: 0.16 + pseudoRandom(index + 7.7) * 0.42,
  warm: index % 7 === 0,
}));

interface Enemy {
  key: string;
  col: number;
  row: number;
  variant: number;
  alive: boolean;
}

interface Bullet {
  id: number;
  x: number;
  y: number;
}

interface Spark {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  max: number;
  hot: boolean;
}

interface Game {
  time: number;
  enemies: Enemy[];
  bullets: Bullet[];
  sparks: Spark[];
  score: number;
  wave: number;
  shipX: number;
  aimX: number;
  lastInput: number;
  nextFire: number;
  nextBullet: number;
  nextSpark: number;
  waveRestart: number;
  lastShot: number;
}

function makeEnemies(wave: number): Enemy[] {
  const enemies: Enemy[] = [];
  for (let row = 0; row < ENEMY_ROWS; row += 1) {
    for (let col = 0; col < ENEMY_COLS; col += 1) {
      enemies.push({
        key: `w${wave}-${row}-${col}`,
        col,
        row,
        variant: (row + col) % 2,
        alive: true,
      });
    }
  }
  return enemies;
}

function makeGame(): Game {
  return {
    time: 0,
    enemies: makeEnemies(1),
    bullets: [],
    sparks: [],
    score: 0,
    wave: 1,
    shipX: VIEW_W / 2,
    aimX: VIEW_W / 2,
    lastInput: Number.NEGATIVE_INFINITY,
    nextFire: 0,
    nextBullet: 1,
    nextSpark: 1,
    waveRestart: 0,
    lastShot: -1000,
  };
}

function swayAmplitude(wave: number): number {
  return Math.min(MAX_SWAY, 12 + wave * 2);
}

function enemyX(enemy: Enemy, time: number, wave: number): number {
  return (
    FORMATION_LEFT +
    enemy.col * ENEMY_GAP_X +
    Math.sin(time * (0.7 + wave * 0.06)) * swayAmplitude(wave)
  );
}

function enemyY(enemy: Enemy, time: number): number {
  return FORMATION_TOP + enemy.row * ENEMY_GAP_Y + Math.sin(time * 1.7 + enemy.row * 0.8) * 1.8;
}

function nearestTargetX(game: Game): number {
  let target = VIEW_W / 2;
  let closest = Number.POSITIVE_INFINITY;
  for (const enemy of game.enemies) {
    if (!enemy.alive) continue;
    const center = enemyX(enemy, game.time, game.wave) + ENEMY_W / 2;
    const distance = Math.abs(center - game.shipX);
    if (distance < closest) {
      closest = distance;
      target = center;
    }
  }
  return target;
}

function spawnSparks(game: Game, x: number, y: number, hot: boolean): void {
  const count = hot ? 10 : 7;
  for (let index = 0; index < count; index += 1) {
    const angle = (Math.PI * 2 * index) / count + Math.random() * 0.5;
    const speed = 28 + Math.random() * 58;
    game.sparks.push({
      id: game.nextSpark++,
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 0.45,
      max: 0.45,
      hot: hot || index % 3 === 0,
    });
  }
}

function step(game: Game, dt: number, now: number): void {
  game.time = now / 1000;

  const autopilot = now - game.lastInput > 2000;
  const target = autopilot ? nearestTargetX(game) : game.aimX;
  game.shipX += (target - game.shipX) * Math.min(1, dt * 10);

  if (now >= game.nextFire) {
    game.bullets.push({ id: game.nextBullet++, x: game.shipX, y: SHIP_Y - 2 });
    game.lastShot = now;
    game.nextFire = now + Math.max(240, 460 - game.wave * 30);
  }

  const travel = BULLET_SPEED * dt;
  for (const bullet of game.bullets) bullet.y -= travel;
  game.bullets = game.bullets.filter((bullet) => bullet.y > 4);

  const spent = new Set<number>();
  for (const bullet of game.bullets) {
    for (const enemy of game.enemies) {
      if (!enemy.alive) continue;
      const ex = enemyX(enemy, game.time, game.wave);
      const ey = enemyY(enemy, game.time);
      if (
        bullet.x >= ex - 1 &&
        bullet.x <= ex + ENEMY_W + 1 &&
        bullet.y <= ey + ENEMY_H &&
        bullet.y >= ey - 2
      ) {
        enemy.alive = false;
        spent.add(bullet.id);
        const commander = enemy.row === 0;
        game.score += commander ? 30 : 10;
        spawnSparks(game, ex + ENEMY_W / 2, ey + ENEMY_H / 2, commander);
        break;
      }
    }
  }
  if (spent.size > 0) {
    game.bullets = game.bullets.filter((bullet) => !spent.has(bullet.id));
  }

  for (const spark of game.sparks) {
    spark.x += spark.vx * dt;
    spark.y += spark.vy * dt;
    spark.vy += 55 * dt;
    spark.life -= dt;
  }
  game.sparks = game.sparks.filter((spark) => spark.life > 0);

  if (game.waveRestart === 0 && game.enemies.every((enemy) => !enemy.alive)) {
    game.waveRestart = now + 900;
  } else if (game.waveRestart > 0 && now >= game.waveRestart) {
    game.wave += 1;
    game.enemies = makeEnemies(game.wave);
    game.sparks = [];
    game.score += 50;
    game.waveRestart = 0;
  }
}

export function SpaceShooter() {
  const reduced = usePrefersReducedMotion();
  const gameRef = useRef<Game>(makeGame());
  const svgRef = useRef<SVGSVGElement>(null);
  const [, bump] = useReducer((revision: number) => revision + 1, 0);

  useEffect(() => {
    if (reduced) return;
    const game = gameRef.current;
    let frame = 0;
    let last = performance.now();
    const loop = (now: number) => {
      const dt = Math.min(0.05, Math.max(0, (now - last) / 1000));
      last = now;
      step(game, dt, now);
      bump();
      frame = requestAnimationFrame(loop);
    };
    frame = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(frame);
  }, [bump, reduced]);

  function viewX(clientX: number): number | null {
    const svg = svgRef.current;
    if (!svg) return null;
    const rect = svg.getBoundingClientRect();
    if (rect.width <= 0) return null;
    const x = ((clientX - rect.left) / rect.width) * VIEW_W;
    return Math.min(VIEW_W - 18, Math.max(18, x));
  }

  function aim(event: PointerEvent<SVGSVGElement>): void {
    if (reduced) return;
    const x = viewX(event.clientX);
    if (x === null) return;
    const game = gameRef.current;
    game.aimX = x;
    game.lastInput = performance.now();
  }

  function handlePointerDown(event: PointerEvent<SVGSVGElement>): void {
    aim(event);
    if (reduced) return;
    gameRef.current.nextFire = 0;
  }

  function handleKeyDown(event: KeyboardEvent<SVGSVGElement>): void {
    if (reduced) return;
    const game = gameRef.current;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      const delta = event.key === 'ArrowLeft' ? -20 : 20;
      game.aimX = Math.min(VIEW_W - 18, Math.max(18, game.aimX + delta));
      game.lastInput = performance.now();
      event.preventDefault();
    } else if (event.key === ' ' || event.key === 'Enter') {
      game.nextFire = 0;
      game.lastInput = performance.now();
      event.preventDefault();
    }
  }

  const game = gameRef.current;
  const time = reduced ? 0 : game.time;
  const tilt = Math.max(-8, Math.min(8, (game.aimX - game.shipX) * 0.45));
  const firing = !reduced && game.time * 1000 - game.lastShot < 80;
  const thruster = Math.abs(Math.sin(time * 26));

  return (
    <div className="flex flex-col gap-1.5">
      <div className="relative overflow-hidden border border-ink bg-[#0a0806]">
        <svg
          ref={svgRef}
          viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
          className="block w-full touch-pan-y select-none"
          role="application"
          tabIndex={reduced ? -1 : 0}
          aria-label="Space shooter mini-game. Move the ship with the arrow keys and press space to fire."
          onPointerMove={aim}
          onPointerDown={handlePointerDown}
          onKeyDown={handleKeyDown}
        >
          <defs>
            <radialGradient id="arcade-bg" cx="50%" cy="42%" r="72%">
              <stop offset="0%" stopColor="#191410" />
              <stop offset="58%" stopColor="#0e0b07" />
              <stop offset="100%" stopColor="#070504" />
            </radialGradient>
            <radialGradient id="arcade-thruster" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor={ACCENT} stopOpacity="0.35" />
              <stop offset="100%" stopColor={ACCENT} stopOpacity="0" />
            </radialGradient>
          </defs>

          <rect width={VIEW_W} height={VIEW_H} fill="url(#arcade-bg)" />

          {STARS.map((star, index) => {
            const y = (((star.y + time * star.speed) % VIEW_H) + VIEW_H) % VIEW_H;
            return (
              <circle
                key={index}
                cx={star.x}
                cy={y}
                r={star.radius}
                fill={star.warm ? ACCENT : CREAM}
                opacity={star.opacity}
              />
            );
          })}

          <g className="font-mono" fontSize={8} letterSpacing="1">
            <text x={10} y={13} fill={CREAM} opacity={0.45}>
              SCORE
            </text>
            <text x={44} y={13} fill={CREAM}>
              {String(game.score).padStart(4, '0')}
            </text>
            <text x={VIEW_W - 40} y={13} textAnchor="end" fill={CREAM} opacity={0.45}>
              WAVE
            </text>
            <text x={VIEW_W - 10} y={13} textAnchor="end" fill={CREAM}>
              {String(game.wave).padStart(2, '0')}
            </text>
            <line x1={10} x2={VIEW_W - 10} y1={19} y2={19} stroke={CREAM} strokeOpacity={0.12} />
          </g>

          {game.enemies.map((enemy) => {
            if (!enemy.alive) return null;
            const x = enemyX(enemy, time, game.wave);
            const y = enemyY(enemy, time);
            const commander = enemy.row === 0;
            return (
              <path
                key={enemy.key}
                d={enemy.variant === 0 ? ENEMY_A_PATH : ENEMY_B_PATH}
                fill={commander ? ACCENT : CREAM}
                opacity={commander ? 0.94 : 0.82}
                transform={`translate(${x.toFixed(1)} ${y.toFixed(1)})`}
              />
            );
          })}

          {game.sparks.map((spark) => (
            <rect
              key={spark.id}
              x={spark.x}
              y={spark.y}
              width={2}
              height={2}
              fill={spark.hot ? ACCENT : CREAM}
              opacity={Math.max(0, spark.life / spark.max)}
            />
          ))}

          {game.bullets.map((bullet) => (
            <g key={bullet.id}>
              <line
                x1={bullet.x}
                y1={bullet.y - 7}
                x2={bullet.x}
                y2={bullet.y}
                stroke={ACCENT}
                strokeWidth={2.6}
                strokeLinecap="round"
                opacity={0.28}
              />
              <line
                x1={bullet.x}
                y1={bullet.y - 7}
                x2={bullet.x}
                y2={bullet.y}
                stroke={CREAM}
                strokeWidth={1.1}
                strokeLinecap="round"
              />
            </g>
          ))}

          <ellipse
            cx={game.shipX}
            cy={SHIP_Y + SHIP_H + 3}
            rx={18}
            ry={4}
            fill="url(#arcade-thruster)"
          />

          <g
            transform={`translate(${game.shipX} ${SHIP_Y + SHIP_H / 2}) rotate(${tilt.toFixed(1)}) translate(${-SHIP_W / 2} ${-SHIP_H / 2})`}
          >
            <path d={SHIP_PATH} fill={CREAM} />
            <path d={SHIP_COCKPIT_PATH} fill={ACCENT} />
          </g>

          <g>
            <rect
              x={game.shipX - 3}
              y={SHIP_Y + SHIP_H}
              width={6}
              height={1.6 + thruster * 2}
              fill={ACCENT}
              opacity={0.5}
            />
            <rect
              x={game.shipX - 1}
              y={SHIP_Y + SHIP_H}
              width={2}
              height={2 + thruster * 2.4}
              fill={CREAM}
              opacity={0.8}
            />
          </g>

          {firing ? (
            <rect
              x={game.shipX - 1.4}
              y={SHIP_Y - 9}
              width={2.8}
              height={7}
              fill={CREAM}
              opacity={0.9}
            />
          ) : null}

          <rect
            x={0.5}
            y={0.5}
            width={VIEW_W - 1}
            height={VIEW_H - 1}
            fill="none"
            stroke={CREAM}
            strokeOpacity={0.08}
          />
        </svg>
        <div aria-hidden="true" className="arcade-scanlines pointer-events-none absolute inset-0" />
        <div aria-hidden="true" className="arcade-vignette pointer-events-none absolute inset-0" />
      </div>
      <p className="font-mono text-[9px] uppercase tracking-[0.14em] text-muted">
        {reduced ? 'Reduced motion — mini-game paused' : 'Move to aim · click to fire'}
      </p>
    </div>
  );
}
