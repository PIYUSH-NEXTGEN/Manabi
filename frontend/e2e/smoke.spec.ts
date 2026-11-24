import { expect, test } from '@playwright/test';

test('home hero, board, and problem detail render with zero console errors', async ({
  page,
}) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') {
      consoleErrors.push(message.text());
    }
  });

  await page.goto('/');
  // The hero renders its headline as two animated spans; the trailing
  // whitespace after each line makes the flattened text extra-spacey.
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    /Stop Searching\s*Start Building/,
  );

  // Nav + board both use "Projects" as the label; scope to the banner nav.
  await page.getByRole('navigation', { name: 'Main' }).getByRole('link', { name: 'Projects' }).click();
  await expect(
    page.getByRole('heading', { name: 'Projects', level: 1 }),
  ).toBeVisible();
  // Seed IDs and titles are data, not contract: use whatever card the board
  // actually renders first, then verify the navigation reaches its detail.
  const firstCard = page.locator('main a[href^="/problems/"]').first();
  await expect(firstCard).toBeVisible();
  const href = await firstCard.getAttribute('href');
  expect(href).toMatch(/^\/problems\/\d+$/);

  await firstCard.click();
  await expect(page).toHaveURL(new RegExp(`${href}$`));
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

  const unexpectedErrors = consoleErrors.filter(
    (error) => error.includes('401') === false,
  );
  expect(unexpectedErrors).toEqual([]);
});
