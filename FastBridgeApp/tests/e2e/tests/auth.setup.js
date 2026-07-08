// One-time auth setup: hit the harness's test-only /e2e-login so the response sets the
// session cookies, then persist them as storageState for the chromium project to reuse.
// This mints a real Mongo-backed session (no Firebase), so authed pages load as a signed-in
// fixture user. See harness/e2e_app.py:e2e_login.
const { test: setup } = require('@playwright/test');

const STORAGE_STATE = 'playwright/.auth/user.json';

setup('authenticate', async ({ page, context }) => {
  const resp = await page.goto('/e2e-login');
  if (!resp || !resp.ok()) {
    throw new Error(`/e2e-login failed: ${resp ? resp.status() : 'no response'}`);
  }
  await context.storageState({ path: STORAGE_STATE });
});
