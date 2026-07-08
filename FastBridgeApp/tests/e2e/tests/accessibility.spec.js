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

for (const pageInfo of PAGES) {
  test(`no serious or critical a11y violations: ${pageInfo.name}`, async ({ page }) => {
    await page.goto(pageInfo.path);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    const blocking = results.violations.filter(
      (v) => v.impact === 'serious' || v.impact === 'critical'
    );

    // Print details so the CI log is actually useful when this fails.
    for (const v of blocking) {
      console.log(`[${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} element(s))`);
    }

    expect(blocking, blocking.map((v) => v.id).join(', ')).toEqual([]);
  });
}
