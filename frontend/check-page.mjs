import { chromium } from '@playwright/test';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
page.on('console', (message) => console.log('CONSOLE', message.type(), message.text()));
page.on('pageerror', (error) => console.log('PAGEERROR', error.message));
page.on('requestfailed', (request) =>
  console.log('REQUESTFAILED', request.url(), request.failure()?.errorText),
);

await page.goto('http://127.0.0.1:5178/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1500);

console.log('TITLE', await page.title());
console.log('BODY_START');
console.log((await page.locator('body').innerText()).slice(0, 3000));
console.log('BODY_END');

await page.screenshot({ path: 'home-check.png', fullPage: true });
await browser.close();
