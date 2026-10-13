// Accessibility smoke checks: load each page and run axe-core, failing on serious or
// critical WCAG violations. 
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const PAGES = [
  { name: 'home', path: '/' },
  { name: 'select (Latin)', path: '/select/Latin/' },
  { name: 'about', path: '/about/' },
  // /help/ has no route (user_help only defines /user_guide, /collaborate, /lemmatize);
  // the old '/help/' entry was a silent 404. Point at the real help page.
  { name: 'help', path: '/help/user_guide' },
  // Interactive pages, where nameless controls hide. /userspace/ needs the signed-in
  // storageState from the setup project (see playwright.config.js).
  { name: 'userspace', path: '/userspace/' },
  { name: 'lemmatizer', path: '/lemmatizer/' },
];

// `within` limits the scan to one subtree. Without it a page-wide scan is dominated by the
// site-wide problems (the unnamed footer logo links, the missing <html lang>), which every
// page here already fails on - so a scan of one panel would say nothing about that panel.
async function scan(page, label, within) {
  let builder = new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']);
  if (within) builder = builder.include(within);
  const results = await builder.analyze();

  const blocking = results.violations.filter(
    (v) => v.impact === 'serious' || v.impact === 'critical'
  );

  // Print details so the CI log is actually useful when this fails.
  for (const v of blocking) {
    console.log(`[${label}] [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} element(s))`);
  }

  expect(blocking, `${label}: ${blocking.map((v) => v.id).join(', ')}`).toEqual([]);
}

for (const pageInfo of PAGES) {
  test(`no serious or critical a11y violations: ${pageInfo.name}`, async ({ page }) => {
    await page.goto(pageInfo.path);
    await scan(page, pageInfo.name);
  });
}

// The study page needs a seeded list, and its Flashcards panel starts display:none - axe
// skips hidden content, so the flashcard and recall controls have to be revealed a step at a
// time and scanned at each one. Scoped to the flashcard panel: this is here to catch nameless
// controls, unlabelled inputs and broken ARIA in the flashcard UI, and a page-wide scan would
// just re-report the site-wide failures the tests above already cover.
test('no serious or critical a11y violations: list study flashcards panel', async ({ page }) => {
  const seeded = await page.request.get('/e2e-seed-list');
  expect(seeded.ok(), 'could not seed the E2E study list').toBeTruthy();
  const { list_name: listName } = await seeded.json();

  await page.goto(`/userspace/list/Latin/${encodeURIComponent(listName)}`);
  await page.locator('#tab-flashcards').click();
  await expect(page.locator('#fc-card')).toBeVisible();
  await scan(page, 'flashcards', '#mode-flashcards');

  // Recall mode adds the rating group, the explainer and the reset control.
  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-rating')).toBeVisible();
  await expect(page.locator('#fc-recall-help')).toBeVisible();
  await scan(page, 'flashcards / recall', '#mode-flashcards');

  // Flipping enables the rating buttons; a disabled control is exempt from some
  // checks, so scan them in their live state too.
  await page.locator('#fc-card').click();
  await expect(page.locator('[data-rating="good"]')).toBeEnabled();
  await scan(page, 'flashcards / recall, card flipped', '#mode-flashcards');
});
