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
      <label><input type="checkbox" id="fc-recall"> Recall mode</label>
      <span id="fc-due"></span>
      <span id="fc-progress"></span>
      <span id="fc-save-warn" role="status"></span>
      <div id="fc-card" class="fc-card" tabindex="0">
        <button id="fc-star" aria-pressed="false">star</button>
        <div id="fc-front"><div id="fc-front-parts"></div></div>
        <div id="fc-back"><div id="fc-back-pos"></div><div id="fc-back-def"></div></div>
      </div>
      <div class="fc-nav"><button id="fc-prev">Previous</button><button id="fc-flip">Flip card</button><button id="fc-next">Next</button></div>
      <div id="fc-rating" style="display:none">
        <button data-rating="again">Again</button><button data-rating="hard">Hard</button>
        <button data-rating="good">Good</button><button data-rating="easy">Easy</button>
      </div>
      <p id="fc-recall-help" style="display:none">
        Recall mode shows the words you're due to review based on how confident you are with them.
        <button id="fc-reset">Reset progress for this list</button>
      </p>
      <p id="fc-session-done" style="display:none"><span id="fc-done-msg">Session finished.</span> <button id="fc-restart">Study ahead</button></p>
      <p id="fc-filtered-empty" style="display:none">No flashcards match this filter.</p>
    </div>
    <p id="flashcards-empty" style="display:none">This list has no words to study yet.</p>
  </div>`;

function row(principalParts, definition, pos, lemma) {
  return {
    markup: `<tr data-lemma="${lemma || principalParts}"><td class="PRINCIPAL_PARTS">${principalParts}</td><td class="SHORT_DEFINITION">${definition}</td><td class="PART_OF_SPEECH">${pos}</td></tr>`,
  };
}

// ISO date `days` from now, for seeding STUDY_PROGRESS. Negative = overdue.
function dueIn(days) {
  return new Date(Date.now() + days * 86400000).toISOString();
}

async function loadFlashcards(page, words, opts = {}) {
  await page.setContent(flashcardPanel);
  await page.evaluate(({ cards, starred, progress, failSaves }) => {
    window.data = cards;
    window.STUDY_LIST = { ownerId: 'owner1', language: 'Latin', listName: 'My List' };
    window.STUDY_STARRED = starred || [];
    window.STUDY_PROGRESS = progress || {};
    // Record every POST the page makes (toggle_star and submit_review) without
    // a backend. `failSaves` exercises the "keep going on a failed save" path.
    window.__starCalls = [];
    window.fetch = (url, init) => {
      window.__starCalls.push({ url, body: JSON.parse(init.body) });
      if (failSaves) return Promise.resolve({ ok: false });
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          success: true,
          due: new Date(Date.now() + 86400000).toISOString(),
          interval: 1,
        }),
      });
    };
  }, {
    cards: words, starred: opts.starred,
    progress: opts.progress, failSaves: opts.failSaves,
  });
  await page.addScriptTag({ path: flashcardScript });
}

// STUDY_PROGRESS keys are "lemma\0gloss", the same pair keyOf() builds.
function progressKey(lemma, gloss) {
  return lemma + '\u0000' + gloss;
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

test('recall mode: rating buttons and 1-4 keys only work once the card is flipped', async ({ page }) => {
  await loadFlashcards(page, [row('alpha', 'first', 'Noun'), row('beta', 'second', 'Noun')]);

  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-rating')).toBeVisible();
  await expect(page.locator('.fc-nav')).toBeHidden();
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  await expect(page.locator('[data-rating="good"]')).toBeDisabled();

  const front = await page.locator('#fc-front-parts').textContent();
  await page.locator('#fc-card').focus();
  await page.keyboard.press('3');
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  await expect(page.locator('#fc-front-parts')).toHaveText(front);

  await page.keyboard.press('Space');
  await expect(page.locator('[data-rating="good"]')).toBeEnabled();
  await page.keyboard.press('3');
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');
  await expect(page.locator('#fc-card')).not.toHaveClass(/flipped/);
  await expect(page.locator('[data-rating="good"]')).toBeDisabled();
});

test('recall mode: Again requeues the card, Good retires it, and the session finishes', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun'),
    row('beta', 'second', 'Noun'),
    row('gamma', 'third', 'Noun'),
  ]);
  await page.locator('#fc-recall').check();

  const front = page.locator('#fc-front-parts');
  const missed = await front.textContent();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="again"]').click();
  await expect(page.locator('#fc-progress')).toHaveText('3 left · 0 done');
  await expect(front).not.toHaveText(missed);

  for (const counts of ['2 left · 1 done', '1 left · 2 done']) {
    await page.locator('#fc-card').click();
    await page.locator('[data-rating="good"]').click();
    await expect(page.locator('#fc-progress')).toHaveText(counts);
  }
  // In a short deck the Again card lands at the end, so it's the last one left.
  await expect(front).toHaveText(missed);

  await page.locator('#fc-card').click();
  await page.locator('[data-rating="easy"]').click();
  await expect(page.locator('#fc-progress')).toHaveText('0 left · 3 done');
  await expect(page.locator('#fc-session-done')).toBeVisible();
  await expect(page.locator('#fc-card')).toBeHidden();
  await expect(page.locator('#fc-rating')).toBeHidden();

  // Every card in the deck has now been rated, so there is nothing left to pull
  // forward and the button that would hand back an empty deck is gone. (This
  // assertion used to expect "Study ahead" to re-serve all 3 cards, which was
  // the replay bug: it handed back the cards just finished and let a second
  // rating compound the interval. The behaviour changed, so the test did.)
  await expect(page.locator('#fc-restart')).toBeHidden();
  await expect(page.locator('#fc-done-msg')).toHaveText('Session finished.');
});

test('recall mode: Study ahead pulls forward only the cards not yet rated', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ], {
    // alpha is due, beta is not, so the normal session is alpha alone.
    progress: {
      [progressKey('alpha', 'first')]: dueIn(-1),
      [progressKey('beta', 'second')]: dueIn(6),
    },
  });

  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 0 done');
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(page.locator('#fc-done-msg')).toHaveText('Session finished.');

  // beta was never rated, so it is the one card Study ahead has to offer.
  await page.locator('#fc-restart').click();
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 0 done');
  await expect(page.locator('#fc-front-parts')).toHaveText('beta');

  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(page.locator('#fc-restart')).toBeHidden();
  // One POST per card, not one per session: alpha was not offered a second time.
  const calls = await page.evaluate(() => window.__starCalls);
  expect(calls.map((c) => c.body.lemma).sort()).toEqual(['alpha', 'beta']);
});

test('recall mode: the session is what is due plus what is new, due cards first', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
    row('gamma', 'third', 'Noun', 'gamma'),
  ], {
    progress: {
      [progressKey('alpha', 'first')]: dueIn(-3),   // overdue
      [progressKey('gamma', 'third')]: dueIn(7),    // scheduled for later
      // beta has never been reviewed
    },
  });

  // gamma isn't waiting on anything, so it's not in the count or the session.
  await expect(page.locator('#fc-due')).toHaveText('2 due');

  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  // Overdue cards sort ahead of never-seen ones regardless of the shuffle.
  await expect(page.locator('#fc-front-parts')).toHaveText('alpha');

  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(page.locator('#fc-front-parts')).toHaveText('beta');
});

test('recall mode: nothing due shows "All caught up" and Study ahead adds the rest', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ], {
    progress: {
      [progressKey('alpha', 'first')]: dueIn(5),
      [progressKey('beta', 'second')]: dueIn(9),
    },
  });

  await expect(page.locator('#fc-due')).toHaveText('0 due');

  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-session-done')).toBeVisible();
  await expect(page.locator('#fc-done-msg')).toHaveText('All caught up.');
  await expect(page.locator('#fc-card')).toBeHidden();

  await page.locator('#fc-restart').click();
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  await expect(page.locator('#fc-card')).toBeVisible();
});

test('recall mode: each rating posts to submit_review with the lemma/gloss pair', async ({ page }) => {
  await loadFlashcards(page, [row('amō, amāre, amāvī, amātus', 'to love', 'Verb', 'amo')]);

  await page.locator('#fc-recall').check();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="hard"]').click();

  const calls = await page.evaluate(() => window.__starCalls);
  expect(calls).toHaveLength(1);
  expect(calls[0].url).toContain('/userspace/submit_review');
  // No list_name and no owner_id: progress is per user, per language, per word.
  expect(calls[0].body).toEqual({
    language: 'Latin', lemma: 'amo', gloss: 'to love', rating: 'hard',
    tz_offset: expect.any(Number),
  });
});

test('recall mode: a requeued card is only scheduled once', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ]);
  await page.locator('#fc-recall').check();

  const front = page.locator('#fc-front-parts');
  const missed = await front.textContent();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="again"]').click();

  // Rate the other card, then the requeued one a second time.
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(front).toHaveText(missed);
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();

  // Three ratings, two cards, two POSTs: the second pass over the Again card is
  // a relearning step, not a new schedule.
  const calls = await page.evaluate(() => window.__starCalls);
  expect(calls).toHaveLength(2);
  expect(calls.map((c) => c.body.rating).sort()).toEqual(['again', 'good']);
});

test('recall mode: a failed save warns but does not interrupt the session', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ], { failSaves: true });

  await page.locator('#fc-recall').check();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();

  await expect(page.locator('#fc-save-warn')).toHaveText("Couldn't save your last review.");
  // The rating still counted locally - the card is not put back or re-shown.
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');
  await expect(page.locator('#fc-card')).toBeVisible();
});

test('the recall explainer and reset link appear only in recall mode', async ({ page }) => {
  await loadFlashcards(page, [row('alpha', 'first', 'Noun')]);

  await expect(page.locator('#fc-recall-help')).toBeHidden();
  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-recall-help')).toBeVisible();
  await expect(page.locator('#fc-reset')).toBeVisible();
  await page.locator('#fc-recall').uncheck();
  await expect(page.locator('#fc-recall-help')).toBeHidden();
});

test('reset progress clears the stored schedule and restarts the session', async ({ page }) => {
  page.on('dialog', (d) => d.accept());
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ], {
    // Both scheduled for later, so nothing is due and the session is empty.
    progress: {
      [progressKey('alpha', 'first')]: dueIn(4),
      [progressKey('beta', 'second')]: dueIn(9),
    },
  });

  await expect(page.locator('#fc-due')).toHaveText('0 due');
  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-done-msg')).toHaveText('All caught up.');

  await page.locator('#fc-reset').click();
  // With the schedule gone both words read as never-reviewed, so they are back
  // in the session without having to "study ahead" to reach them.
  await expect(page.locator('#fc-progress')).toHaveText('2 left · 0 done');
  await expect(page.locator('#fc-card')).toBeVisible();

  const calls = await page.evaluate(() => window.__starCalls);
  expect(calls).toHaveLength(1);
  expect(calls[0].url).toContain('/userspace/reset_progress');
  expect(calls[0].body).toEqual({ language: 'Latin', list_name: 'My List', shared: false });

  await page.locator('#fc-recall').uncheck();
  await expect(page.locator('#fc-due')).toHaveText('2 due');
});

test('reset progress leaves the schedule alone when the request fails', async ({ page }) => {
  page.on('dialog', (d) => d.accept());
  await loadFlashcards(page, [row('alpha', 'first', 'Noun', 'alpha')], {
    progress: { [progressKey('alpha', 'first')]: dueIn(4) },
    failSaves: true,
  });

  await page.locator('#fc-recall').check();
  await page.locator('#fc-reset').click();

  await expect(page.locator('#fc-save-warn')).toHaveText("Couldn't reset your progress.");
  await expect(page.locator('#fc-done-msg')).toHaveText('All caught up.');
  // Re-enabled, so a failed reset can be retried.
  await expect(page.locator('#fc-reset')).toBeEnabled();
});

test('cancelling the reset confirmation posts nothing', async ({ page }) => {
  page.on('dialog', (d) => d.dismiss());
  await loadFlashcards(page, [row('alpha', 'first', 'Noun', 'alpha')], {
    progress: { [progressKey('alpha', 'first')]: dueIn(4) },
  });

  await page.locator('#fc-recall').check();
  await page.locator('#fc-reset').click();

  expect(await page.evaluate(() => window.__starCalls.length)).toBe(0);
  await expect(page.locator('#fc-done-msg')).toHaveText('All caught up.');
});

test('recall mode: toggling off and on drops the cards already rated', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ]);

  await page.locator('#fc-recall').check();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 1 done');

  // Leaving recall mode shows the browse-mode count, which the save just moved.
  await page.locator('#fc-recall').uncheck();
  await expect(page.locator('#fc-due')).toHaveText('1 due');

  // A new session is the one card still waiting, counted from zero.
  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 0 done');
});

test('recall mode: changing the part-of-speech filter restarts the session', async ({ page }) => {
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Verb', 'beta'),
    row('gamma', 'third', 'Noun', 'gamma'),
  ]);

  await page.locator('#fc-recall').check();
  await expect(page.locator('#fc-progress')).toHaveText('3 left · 0 done');

  await page.locator('#fc-pos-filter').selectOption('Verb');
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 0 done');
  await expect(page.locator('#fc-front-parts')).toHaveText('beta');

  await page.locator('#fc-pos-filter').selectOption('');
  await expect(page.locator('#fc-progress')).toHaveText('3 left · 0 done');
});

test('recall mode: clicking a rating then using the 1-4 keys still works', async ({ page }) => {
  // Clicking a rating leaves focus on a button, where the key handler bails out.
  // Disabling that button on re-render hands focus back to the body, so the
  // keyboard path has to stay live after a mouse rating.
  await loadFlashcards(page, [
    row('alpha', 'first', 'Noun', 'alpha'),
    row('beta', 'second', 'Noun', 'beta'),
  ]);

  await page.locator('#fc-recall').check();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();

  await page.keyboard.press('Space');
  await page.keyboard.press('3');
  await expect(page.locator('#fc-progress')).toHaveText('0 left · 2 done');
});

test('recall mode: a lone card rated Again comes straight back', async ({ page }) => {
  await loadFlashcards(page, [row('alpha', 'first', 'Noun', 'alpha')]);

  await page.locator('#fc-recall').check();
  await page.locator('#fc-card').click();
  await page.locator('[data-rating="again"]').click();

  // Requeued into a one-card deck, unflipped, with the session still open.
  await expect(page.locator('#fc-progress')).toHaveText('1 left · 0 done');
  await expect(page.locator('#fc-card')).not.toHaveClass(/flipped/);
  await expect(page.locator('[data-rating="good"]')).toBeDisabled();

  await page.locator('#fc-card').click();
  await page.locator('[data-rating="good"]').click();
  await expect(page.locator('#fc-progress')).toHaveText('0 left · 1 done');
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
