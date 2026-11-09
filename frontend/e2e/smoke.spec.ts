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
  // The hero renders its headline as three animated spans; the trailing
  // whitespace after each line makes the flattened text extra-spacey.
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    /Pick a project\.\s*Ship it\.\s*Prove it\./,
  );

  // Nav + board both use "Projects" as the label; scope to the banner nav.
  await page.getByRole('navigation', { name: 'Main' }).getByRole('link', { name: 'Projects' }).click();
  await expect(
    page.getByRole('heading', { name: 'Projects', level: 1 }),
  ).toBeVisible();
  const firstCard = page.locator('a[href="/problems/1"]');
  await expect(firstCard).toBeVisible();

  await firstCard.click();
  await expect(
    page.getByRole('heading', { name: 'Crop disease triage for small farms' }),
  ).toBeVisible();

  const unexpectedErrors = consoleErrors.filter(
    (error) => error.includes('401') === false,
  );
  expect(unexpectedErrors).toEqual([]);
});
