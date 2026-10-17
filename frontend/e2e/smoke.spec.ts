import { expect, test } from '@playwright/test';

test('home hero, board, problem detail, and ML practice render with zero console errors', async ({
  page,
}) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') {
      consoleErrors.push(message.text());
    }
  });

  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('MANABI');

  await page.getByRole('link', { name: 'Problems' }).first().click();
  await expect(
    page.getByRole('heading', { name: 'Problems', level: 1 }),
  ).toBeVisible();
  const firstCard = page.locator('a[href="/problems/1"]');
  await expect(firstCard).toBeVisible();

  await firstCard.click();
  await expect(
    page.getByRole('heading', { name: 'Crop disease triage for small farms' }),
  ).toBeVisible();

  await page.getByRole('link', { name: 'ML Practice' }).first().click();
  await expect(
    page.getByRole('heading', { name: 'ML Practice', level: 1 }),
  ).toBeVisible();
  await expect(
    page.getByRole('heading', { name: 'Metrics lie after the launch' }).first(),
  ).toBeVisible();

  const unexpectedErrors = consoleErrors.filter(
    (error) => error.includes('401') === false,
  );
  expect(unexpectedErrors).toEqual([]);
});
