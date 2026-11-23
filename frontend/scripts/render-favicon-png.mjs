/**
 * Renders public/favicon.svg to a square PNG so it can be packed into an .ico.
 *
 * Chromium is used because it is already a dev dependency (Playwright e2e), so
 * the icon is rasterised with the same engine a browser will use. Not part of
 * the build: run it by hand when the source SVG changes.
 *
 * Usage: node scripts/render-favicon-png.mjs <out.png> [size]
 */
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const out = path.resolve(process.argv[2] ?? 'favicon-256.png');
const size = Number(process.argv[3] ?? 256);
const svgPath = path.resolve(process.cwd(), 'public/favicon.svg');
const svg = await readFile(svgPath, 'utf8');

const browser = await chromium.launch();
try {
  const page = await browser.newPage({
    viewport: { width: size, height: size },
    deviceScaleFactor: 1,
  });
  await page.setContent(
    `<!doctype html><html><body style="margin:0;background:transparent">
       <div id="icon" style="width:${size}px;height:${size}px">
         ${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}
       </div>
     </body></html>`,
    { waitUntil: 'load' },
  );
  await page.locator('#icon').screenshot({ path: out, omitBackground: true });
  console.log(`wrote ${out} (${size}x${size})`);
} finally {
  await browser.close();
}
