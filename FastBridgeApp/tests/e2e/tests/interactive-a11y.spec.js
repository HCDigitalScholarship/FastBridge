// Interactive-control accessibility checks that axe's page scan doesn't fully cover:
//   - every visible button/link has an accessible name (catches icon-only buttons that ship
//     with no name -- the classic saved-lists delete/add/checkbox bug), and
//   - keyboard Tab navigation reaches controls and never lands on a nameless one.
// These are the automated proxy for "a screen reader user can find and operate this"; the
// manual NVDA pass still covers whether the order and names actually make sense.
const { test, expect } = require('@playwright/test');

const PAGES = [
  { name: 'userspace', path: '/userspace/' },   // signed-in via setup storageState
  { name: 'lemmatizer', path: '/lemmatizer/' },
  { name: 'select (Latin)', path: '/select/Latin/' },
];

// Runs in the browser: the accessible-name heuristic screen readers roughly follow.
function browserHelpers() {
  window.__a11y = {
    accName(el) {
      const aria = el.getAttribute('aria-label');
      if (aria && aria.trim()) return aria.trim();
      const labelledby = el.getAttribute('aria-labelledby');
      if (labelledby) {
        const t = labelledby
          .split(/\s+/)
          .map((id) => (document.getElementById(id) || {}).textContent || '')
          .join(' ')
          .trim();
        if (t) return t;
      }
      const text = (el.innerText || el.textContent || '').trim();
      if (text) return text;
      // Associated <label> (explicit for=... or wrapping). el.labels covers both and is how
      // a labeled form control (empty text, no aria) gets its name -- without this, correctly
      // labeled inputs reached by Tab would be reported as nameless.
      if (el.labels && el.labels.length) {
        const t = [...el.labels].map((l) => l.textContent || '').join(' ').trim();
        if (t) return t;
      }
      const img = el.querySelector('img[alt]');
      if (img && img.getAttribute('alt').trim()) return img.getAttribute('alt').trim();
      const title = el.getAttribute('title');
      if (title && title.trim()) return title.trim();
      if (el.tagName === 'INPUT' && el.value && el.value.trim()) return el.value.trim();
      return '';
    },
    visible(el) {
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
    },
  };
}

for (const pageInfo of PAGES) {
  test(`buttons and links have accessible names: ${pageInfo.name}`, async ({ page }) => {
    await page.goto(pageInfo.path);
    await page.evaluate(browserHelpers);

    const offenders = await page.evaluate(() => {
      const controls = [...document.querySelectorAll('button, a[href]')];
      return controls
        .filter(
          (el) =>
            window.__a11y.visible(el) &&
            el.getAttribute('aria-hidden') !== 'true' &&
            !window.__a11y.accName(el)
        )
        .map((el) => el.outerHTML.replace(/\s+/g, ' ').slice(0, 120));
    });

    expect(offenders, `nameless controls:\n${offenders.join('\n')}`).toEqual([]);
  });

  test(`keyboard tab reaches only named controls: ${pageInfo.name}`, async ({ page }) => {
    await page.goto(pageInfo.path);
    await page.evaluate(browserHelpers);

    const focused = [];
    for (let i = 0; i < 25; i++) {
      await page.keyboard.press('Tab');
      const info = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body || el === document.documentElement) return null;
        return { tag: el.tagName, name: window.__a11y.accName(el), html: el.outerHTML.replace(/\s+/g, ' ').slice(0, 120) };
      });
      if (info) focused.push(info);
    }

    // Tab actually moved into the page's controls...
    expect(focused.length, 'Tab did not reach any focusable control').toBeGreaterThan(0);
    // ...and none of the reached controls are nameless.
    const nameless = focused.filter((f) => !f.name).map((f) => f.html);
    expect(nameless, `keyboard focused nameless controls:\n${nameless.join('\n')}`).toEqual([]);
  });
}
