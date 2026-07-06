// Playwright config for FastBridge's e2e + accessibility checks.
//
// It boots a test-only app (harness/e2e_app.py) that mounts the non-auth routers, so it
// runs without a Firebase config. It needs a local MongoDB on port 27017.
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
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
