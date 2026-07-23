const path = require('path');
const { test, expect } = require('@playwright/test');

const flashcardScript = path.resolve(
  __dirname,
  '../../../static/assets/js/study-flashcards.js'
);

// This mirrors the flashcard panel in list_study.html.  Keeping the word data in
// the same rendered-row shape as the production page exercises the browser-side
// parsing path without requiring a MongoDB fixture.
const flashcardPanel = `
  <div id="mode-flashcards" style="display:block">
    <div id="flashcards-ui" style="display:none">
      <select id="fc-pos-filter"></select>
      <label><input type="checkbox" id="fc-starred-only"> Starred only</label>
      <span id="fc-progress"></span>
      <div id="fc-card" class="fc-card" tabindex="0">
        <button id="fc-star" aria-pressed="false">star</button>
        <div id="fc-front"><div id="fc-front-parts"></div></div>
        <div id="fc-back"><div id="fc-back-pos"></div><div id="fc-back-def"></div></div>
      </div>
      <div class="fc-nav"><button id="fc-prev">Previous</button><button id="fc-flip">Flip card</button><button id="fc-next">Next</button></div>
      <p id="fc-filtered-empty" style="display:none">No flashcards match this filter.</p>
    </div>
    <p id="flashcards-empty" style="display:none">This list has no words to study yet.</p>
  </div>`;

function row(principalParts, definition, pos, lemma) {
  return {
    markup: `<tr data-lemma="${lemma || principalParts}"><td class="PRINCIPAL_PARTS">${principalParts}</td><td class="SHORT_DEFINITION">${definition}</td><td class="PART_OF_SPEECH">${pos}</td></tr>`,
  };
}

async function loadFlashcards(page, words, opts = {}) {
  await page.setContent(flashcardPanel);
  await page.evaluate(({ cards, starred }) => {
    window.data = cards;
    window.STUDY_LIST = { ownerId: 'owner1', language: 'Latin', listName: 'My List' };
    window.STUDY_STARRED = starred || [];
    // Record toggle_star calls without a backend.
    window.__starCalls = [];
    window.fetch = (url, init) => {
      window.__starCalls.push({ url, body: JSON.parse(init.body) });
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ success: true }) });
    };
  }, { cards: words, starred: opts.starred });
  await page.addScriptTag({ path: flashcardScript });
}

test('Latin cards flip, navigate, and filter by part of speech', async ({ page }) => {
  await loadFlashcards(page, [
    row('loquor, loquī, locūtus sum', 'to speak', 'Verb'),
    row('puella, puellae, f.', 'girl', 'Noun'),
    row('ferō, ferre, tulī, lātus', 'to carry', 'Verb'),
  ]);

  await expect(page.locator('#fc-front-parts')).toHaveText('loquor, loquī, locūtus sum');
  await expect(page.locator('#fc-progress')).toHaveText('1 / 3');

  await page.locator('#fc-card').click();
  await expect(page.locator('#fc-card')).toHaveClass(/flipped/);
  await expect(page.locator('#fc-back-def')).toHaveText('to speak');

  await page.locator('#fc-next').click();
  await expect(page.locator('#fc-front-parts')).toHaveText('puella, puellae, f.');
  await expect(page.locator('#fc-card')).not.toHaveClass(/flipped/);

  await page.locator('#fc-pos-filter').selectOption('Verb');
  await expect(page.locator('#fc-progress')).toHaveText('1 / 2');
  await expect(page.locator('#fc-front-parts')).toHaveText('loquor, loquī, locūtus sum');
  await page.locator('#fc-card').focus();
  await page.keyboard.press('Space');
  await expect(page.locator('#fc-card')).toHaveClass(/flipped/);
});

test('Space/Enter on a focused nav button activates it instead of flipping', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun'),
    row('beta', 'second', 'Noun'),
  ]);

  // Focused nav button must keep its native keyboard activation
  await page.locator('#fc-next').focus();
  await page.keyboard.press('Space');
  await expect(page.locator('#fc-progress')).toHaveText('2 / 2');
  await expect(page.locator('#fc-card')).not.toHaveClass(/flipped/);

  // The card (a div role=button) still flips via the keyboard handler
  await page.locator('#fc-card').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#fc-card')).toHaveClass(/flipped/);
});

test('starring a card updates the button and persists via toggle_star', async ({ page }) => {
  await loadFlashcards(page, [
    row('loquor, loquī, locūtus sum', 'to speak', 'Verb', 'loquor'),
  ]);

  const star = page.locator('#fc-star');
  await expect(star).toHaveAttribute('aria-pressed', 'false');

  await star.click();
  await expect(star).toHaveClass(/starred/);
  await expect(star).toHaveAttribute('aria-pressed', 'true');

  const calls = await page.evaluate(() => window.__starCalls);
  expect(calls).toHaveLength(1);
  expect(calls[0].url).toContain('/userspace/toggle_star');
  expect(calls[0].body).toMatchObject({
    owner_id: 'owner1', language: 'Latin', list_name: 'My List',
    word: ['loquor', 'to speak'], starred: true,
  });
});

test('seeded stars render as starred and "starred only" filters to them', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ], { starred: [['beta', 'second']] });

  // First card (alpha) is not one of the seeded stars
  await expect(page.locator('#fc-star')).not.toHaveClass(/starred/);

  await page.locator('#fc-starred-only').check();
  await expect(page.locator('#fc-progress')).toHaveText('1 / 1');
  await expect(page.locator('#fc-front-parts')).toHaveText('beta');
  await expect(page.locator('#fc-star')).toHaveClass(/starred/);
});

test('"starred only" with no stars shows the empty state', async ({ page }) => {
  await loadFlashcards(page, [row('alpha', 'first', 'Noun', 'alpha')]);

  await page.locator('#fc-starred-only').check();
  await expect(page.locator('#fc-filtered-empty')).toBeVisible();
  await expect(page.locator('#fc-card')).toBeHidden();
});

test('Greek Unicode principal parts and definitions render without rewriting', async ({ page }) => {
  await loadFlashcards(page, [
    row('γίγνομαι, γενήσομαι, ἐγενόμην, γέγονα, γεγένημαι', 'to become, happen', 'Verb'),
    row('ἡμέρα, -ας, ἡ', 'day', 'Noun'),
  ]);

  await expect(page.locator('#fc-front-parts')).toHaveText('γίγνομαι, γενήσομαι, ἐγενόμην, γέγονα, γεγένημαι');
  await page.locator('#fc-flip').click();
  await expect(page.locator('#fc-back-def')).toHaveText('to become, happen');
});
