# End-to-end and accessibility tests

Playwright drives the real pages in a browser and runs axe-core accessibility checks.

For now this is non-blocking, and that's on purpose. Expect it to fail at first. Those
failures are the point: they surface real bugs and accessibility problems to fix. The plan
is to turn it into a required check for bug fixes next semester, once it's reliably green, so
nothing ships badly broken.

## What it does today

- Boots a test-only app (`harness/e2e_app.py`) that mounts the app routers (home, select,
  about, help, userspace, lemmatizer). It stubs Firebase and the heavy NLP/Google libraries
  at import, so it runs without a Firebase config or the torch stack.
- Signs in a fixture user for the pages that need it. The harness has a test-only
  `/e2e-login` route that mints a real Mongo-backed session (no Firebase), and a Playwright
  setup project (`tests/auth.setup.js`) saves that session as storageState so `/userspace/`
  loads logged in.
- Loads each page and runs axe-core, failing on serious or critical WCAG violations
  (`tests/accessibility.spec.js`).
- Checks interactive controls (`tests/interactive-a11y.spec.js`): every button and link has
  an accessible name, and keyboard Tab never lands on a nameless control.

## Running it locally

Needs Node, and a local MongoDB on port 27017:

    docker run -d --rm -p 27017:27017 mongo:7
    cd FastBridgeApp/tests/e2e
    npm install
    npx playwright install chromium
    npm test

Playwright starts the harness app itself (see `webServer` in `playwright.config.js`), so
you don't need to run uvicorn separately. Python needs the web + Mongo libraries installed
(fastapi, jinja2, python-multipart, pymongo, python-dotenv, uvicorn, email-validator,
requests).

## Not covered yet

- Full user journeys (pick a text, build a vocab list, export). These need a seeded fixture
  corpus and the multi-step form in `select-vocab-step-form.js`.
- The stats and oracle pages (not mounted in the harness yet).

## Accessibility

Automated axe catches maybe 30 to 40 percent of real problems. `ACCESSIBILITY.md` has the
manual checklist (keyboard and screen-reader passes) for the rest.
