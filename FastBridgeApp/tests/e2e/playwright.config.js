// Playwright config for FastBridge's e2e + accessibility checks.
//
// It boots a test-only app (harness/e2e_app.py) that mounts the app routers, so it runs
// without a Firebase config or the torch NLP stack. It needs a local MongoDB on port 27017.
//
// A one-time `setup` project hits the harness's /e2e-login to mint a Mongo-backed session and
// saves it as storageState, so the chromium project runs signed-in (needed for /userspace).
const { defineConfig, devices } = require('@playwright/test');

const STORAGE_STATE = 'playwright/.auth/user.json';

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'setup', testMatch: /auth\.setup\.js/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: STORAGE_STATE },
      dependencies: ['setup'],
    },
  ],
  webServer: {
    command: 'python -m uvicorn e2e_app:app --app-dir harness --host 127.0.0.1 --port 8000',
    url: 'http://127.0.0.1:8000/',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
    env: {
      MONGO_URI: 'mongodb://localhost:27017',
      MONGO_TLS: 'false',
    },
  },
});
