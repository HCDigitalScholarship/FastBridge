// End-to-end checks against the *real* study page, driven through the harness app and a
// local Mongo. study-flashcards.spec.js covers the browser logic against a mirrored panel
// with a stubbed fetch; this file is for the things only a real round trip can show - that
// the server actually hands the page the state the script expects, and that a review
// survives a reload.
const { test, expect } = require('@playwright/test');

async function openRecall(page, listName) {
  await page.goto(`/userspace/list/Latin/${encodeURIComponent(listName)}`);
  await page.locator('#tab-flashcards').click();
  await expect(page.locator('#fc-card')).toBeVisible();
  await page.locator('#fc-recall').check();
}

async function rateCurrent(page, rating) {
  await page.locator('#fc-card').click();
  await expect(page.locator(`[data-rating="${rating}"]`)).toBeEnabled();
  await page.locator(`[data-rating="${rating}"]`).click();
}

test('a review survives a reload: the done tally is restored from the server', async ({ page }) => {
  // Seeding also clears this user's study_meta, so the list starts with nothing reviewed.
  const seeded = await page.request.get('/e2e-seed-list');
  expect(seeded.ok(), 'could not seed the E2E study list').toBeTruthy();
  const { list_name: listName } = await seeded.json();

  await openRecall(page, listName);
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');

  // Rate one word for real - this POSTs to /userspace/submit_review and writes study_meta.
  await rateCurrent(page, 'good');
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');
  await expect(page.locator('#fc-save-warn')).toHaveText('');

  // The reload is the whole point. "left" was always durable; "done" used to come back as
  // zero because it only ever lived in the page.
  await page.reload();
  await openRecall(page, listName);
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');

  // And the schedule itself came back too: Good on a new card books it a day out, so the
  // word that was rated is no longer in the session.
  const progress = await page.evaluate(() => window.STUDY_PROGRESS);
  const reviewed = await page.evaluate(() => window.STUDY_REVIEWED);
  expect(Object.keys(progress)).toHaveLength(1);
  expect(Object.keys(reviewed)).toHaveLength(1);
  expect(Object.keys(reviewed)[0]).toBe(Object.keys(progress)[0]);
  expect(Date.parse(reviewed[Object.keys(reviewed)[0]])).toBeLessThan(Date.now() + 1000);
});

test('Reset Progress clears the schedule and the tally on the real page', async ({ page }) => {
  const seeded = await page.request.get('/e2e-seed-list');
  expect(seeded.ok()).toBeTruthy();
  const { list_name: listName } = await seeded.json();

  await openRecall(page, listName);
  await rateCurrent(page, 'good');
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');

  page.on('dialog', (d) => d.accept());
  await page.locator('#fc-reset').click();
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');

  // Reload to prove the delete reached Mongo rather than only the page.
  await page.reload();
  await openRecall(page, listName);
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  expect(await page.evaluate(() => window.STUDY_PROGRESS)).toEqual({});
  expect(await page.evaluate(() => window.STUDY_REVIEWED)).toEqual({});
});
