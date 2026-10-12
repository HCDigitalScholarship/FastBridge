// Flashcard flip mode for the study list page. Cards are built from the same
// `data` (render_words) the Browse table uses: each row's `markup` already
// carries every dictionary field as a <td class="COLUMN">, so principal parts,
// definition and part of speech are all read client-side — no server round-trip.
(function () {
  var raw = (typeof data !== 'undefined') ? data : [];
  if (typeof raw === 'string') { try { raw = JSON.parse(raw); } catch (e) { raw = []; } }

  var parser = document.createElement('table');
  function cell(tr, cls) {
    var el = tr.querySelector('td.' + cls);
    return el ? el.textContent.trim() : '';
  }

  // Parse each row's markup once into a flat card record.
  var allCards = [];
  raw.forEach(function (row) {
    if (!row || !row.markup) return;
    parser.innerHTML = '<tbody>' + row.markup + '</tbody>';
    var tr = parser.querySelector('tr');
    if (!tr) return;
    var parts = cell(tr, 'PRINCIPAL_PARTS');
    var title = cell(tr, 'TITLE');
    allCards.push({
      front: parts || title,
      shortDef: cell(tr, 'SHORT_DEFINITION'),
      longDef: cell(tr, 'LONG_DEFINITION'),
      pos: cell(tr, 'PART_OF_SPEECH'),
      // [SIMPLE_LEMMA, SHORT_DEFINITION] — the pair a saved list stores, used as
      // the star identity so homographs with different glosses star separately.
      lemma: tr.getAttribute('data-lemma') || cell(tr, 'SIMPLE_LEMMA') || title
    });
  });

  var ui = document.getElementById('flashcards-ui');
  var emptyMsg = document.getElementById('flashcards-empty');
  if (!ui) return;
  if (allCards.length === 0) {
    if (emptyMsg) emptyMsg.style.display = 'block';
    return;
  }
  ui.style.display = 'block';

  var posFilter = document.getElementById('fc-pos-filter');
  var progress = document.getElementById('fc-progress');
  var cardEl = document.getElementById('fc-card');
  var frontParts = document.getElementById('fc-front-parts');
  var frontFace = document.getElementById('fc-front');
  var backFace = document.getElementById('fc-back');
  var backPos = document.getElementById('fc-back-pos');
  var backDef = document.getElementById('fc-back-def');
  var prevBtn = document.getElementById('fc-prev');
  var flipBtn = document.getElementById('fc-flip');
  var nextBtn = document.getElementById('fc-next');
  var nav = document.querySelector('#mode-flashcards .fc-nav');
  var filteredEmpty = document.getElementById('fc-filtered-empty');
  var starBtn = document.getElementById('fc-star');
  var starredToggle = document.getElementById('fc-starred-only');
  var liveEl = document.getElementById('fc-live');
  var recallToggle = document.getElementById('fc-recall');
  var ratingBar = document.getElementById('fc-rating');
  var ratingBtns = ratingBar.querySelectorAll('[data-rating]');
  var sessionDone = document.getElementById('fc-session-done');
  var doneMsg = document.getElementById('fc-done-msg');
  var dueBadge = document.getElementById('fc-due');
  var saveWarn = document.getElementById('fc-save-warn');
  var restartBtn = document.getElementById('fc-restart');

  // The card content is normal readable text (not buried in a button), but the
  // flip and navigation are silent to a screen reader on their own, so mirror
  // the visible face into a polite live region.
  function announce(msg) { if (liveEl) liveEl.textContent = msg || ''; }

  var S = window.STUDY_LIST || {};
  // Star identity keyed on the [lemma, gloss] pair (NUL delimiter can't collide).
  function keyOf(lemma, def) { return lemma + '\x00' + def; }
  var starred = {};
  (window.STUDY_STARRED || []).forEach(function (w) {
    if (w && w.length >= 2) starred[keyOf(w[0], w[1])] = true;
  });
  // Server-side SM-2 due dates, same key format: "lemma\0gloss" -> ISO date.
  var sched = window.STUDY_PROGRESS || {};

  // POS dropdown from the values actually present in this list, sorted.
  var posSet = {};
  allCards.forEach(function (c) { if (c.pos) posSet[c.pos] = true; });
  ['', ].concat(Object.keys(posSet).sort()).forEach(function (p) {
    var opt = document.createElement('option');
    opt.value = p;
    opt.textContent = p || 'All parts of speech';
    posFilter.appendChild(opt);
  });

  var cards = allCards;
  var idx = 0;

  // 'browse' pages linearly through `cards` by idx; 'recall' works through a
  // shuffled session `queue`, where the head is the current card.
  var mode = 'browse';
  var queue = [];
  var doneCount = 0;
  // Cards already sent to the server this session, so a requeued card is
  // only scheduled once (see saveReview).
  var reviewed = {};
  var RATING_KEYS = { '1': 'again', '2': 'hard', '3': 'good', '4': 'easy' };

  function current() { return mode === 'recall' ? queue[0] : cards[idx]; }

  function dueAt(c) { return Date.parse(sched[keyOf(c.lemma, c.shortDef)] || '') || 0; }

  // 0 = due now, 1 = never reviewed, 2 = scheduled for later. A never-reviewed
  // card sorts after the backlog but still belongs in the session.
  function dueGroup(c, now) {
    if (!sched[keyOf(c.lemma, c.shortDef)]) return 1;
    return dueAt(c) <= now ? 0 : 2;
  }

  function dueCount() {
    var now = Date.now(), n = 0;
    cards.forEach(function (c) { if (dueGroup(c, now) < 2) n++; });
    return n;
  }

  function setRatingEnabled(on) {
    for (var i = 0; i < ratingBtns.length; i++) ratingBtns[i].disabled = !on;
  }

  function paintStar() {
    var c = current();
    var on = !!(c && starred[keyOf(c.lemma, c.shortDef)]);
    starBtn.classList.toggle('starred', on);
    starBtn.setAttribute('aria-pressed', String(on));
  }

  function render() {
    var recall = mode === 'recall';
    dueBadge.textContent = (recall || !cards.length) ? '' : dueCount() + ' due';
    cardEl.classList.remove('flipped');
    frontFace.setAttribute('aria-hidden', 'false');
    backFace.setAttribute('aria-hidden', 'true');
    setRatingEnabled(false);
    sessionDone.style.display = 'none';
    if (cards.length === 0) {
      cardEl.style.display = 'none';
      nav.style.display = 'none';
      ratingBar.style.display = 'none';
      filteredEmpty.style.display = 'block';
      progress.textContent = '';
      announce('No flashcards match these filters.');
      return;
    }
    filteredEmpty.style.display = 'none';
    if (recall && queue.length === 0) {
      cardEl.style.display = 'none';
      nav.style.display = 'none';
      ratingBar.style.display = 'none';
      sessionDone.style.display = 'block';
      // No cards done means nothing was waiting in the first place.
      doneMsg.textContent = doneCount ? 'Session finished.' : 'All caught up.';
      progress.textContent = '0 left · ' + doneCount + ' done';
      announce(doneMsg.textContent);
      return;
    }
    cardEl.style.display = '';
    nav.style.display = recall ? 'none' : 'flex';
    ratingBar.style.display = recall ? 'flex' : 'none';

    var c = current();
    frontParts.textContent = c.front;
    backPos.textContent = c.pos || '';
    backPos.style.display = c.pos ? '' : 'none';
    backDef.textContent = c.shortDef || c.longDef || '(no definition)';

    paintStar();

    if (recall) {
      progress.textContent = queue.length + ' left · ' + doneCount + ' done';
    } else {
      progress.textContent = (idx + 1) + ' / ' + cards.length;
      prevBtn.disabled = idx === 0;
      nextBtn.disabled = idx === cards.length - 1;
    }
    announce(c.front);
  }

  // Shuffled copy of the filtered deck, then stably sorted into due (oldest
  // first), never-seen, scheduled-for-later. Shuffling first keeps stored list
  // order out of each group, so you learn the word and not its position.
  // `ahead` keeps the scheduled-for-later cards; a normal session drops them.
  function buildQueue(ahead) {
    var now = Date.now();
    queue = cards.slice();
    for (var i = queue.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = queue[i]; queue[i] = queue[j]; queue[j] = t;
    }
    queue.sort(function (a, b) {
      return (dueGroup(a, now) - dueGroup(b, now)) || (dueAt(a) - dueAt(b));
    });
    if (!ahead) queue = queue.filter(function (c) { return dueGroup(c, now) < 2; });
    doneCount = 0;
    reviewed = {};
    saveWarn.style.display = 'none';
  }

  function setMode(on) {
    mode = on ? 'recall' : 'browse';
    if (on) buildQueue();
    render();
  }

  // In-session requeue: Again comes back 3 cards later, Hard 7 later, Good/Easy
  // retire the card. Clamping to the queue length puts it at the end of a short
  // deck (a lone card simply comes straight back).
  function rate(g) {
    if (mode !== 'recall' || !queue.length || !cardEl.classList.contains('flipped')) return;
    var c = queue.shift();
    saveReview(c, g);
    if (g === 'again' || g === 'hard') {
      queue.splice(Math.min(g === 'again' ? 3 : 7, queue.length), 0, c);
    } else {
      doneCount++;
    }
    render();
    var label = g.charAt(0).toUpperCase() + g.slice(1);
    announce(label + '. ' + (queue.length ? queue[0].front : 'Session finished.'));
  }

  // The long-term interval is the server's business; the requeue above is the
  // session's, and Anki layers them the same way. Deliberately not awaited and
  // never reverted - undoing a rating mid-session confuses more than dropping
  // one review does. No retry buffer.
  //
  // Only the FIRST rating of a card counts, which is the one that says whether
  // you actually knew it. Posting the requeue passes too would both invert the
  // schedule (Hard then Good would bump `reps` and buy a longer interval than
  // Good alone) and race its own earlier write, since each call is a separate
  // read-modify-write.
  function saveReview(c, g) {
    var key = keyOf(c.lemma, c.shortDef);
    if (reviewed[key]) return;
    reviewed[key] = true;
    fetch('/userspace/submit_review', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: S.language, lemma: c.lemma, gloss: c.shortDef, rating: g,
        tz_offset: new Date().getTimezoneOffset()
      })
    }).then(function (resp) {
      return resp.ok ? resp.json() : Promise.reject();
    }).then(function (d) {
      if (!d.success) return Promise.reject();
      sched[key] = d.due;
    }).catch(function () {
      // Left up for the rest of the session: a later card saving fine says
      // nothing about the review that was lost.
      saveWarn.style.display = '';
    });
  }

  function applyFilter() {
    var pos = posFilter.value;
    var starredOnly = starredToggle && starredToggle.checked;
    cards = allCards.filter(function (c) {
      if (pos && c.pos !== pos) return false;
      if (starredOnly && !starred[keyOf(c.lemma, c.shortDef)]) return false;
      return true;
    });
    idx = 0;
    // The deck contents changed, so a recall session starts over rather than
    // carrying queue/done counts that no longer describe this deck.
    if (mode === 'recall') buildQueue();
    render();
  }

  function flip() {
    var c = current();
    if (!c) return;
    var isFlipped = cardEl.classList.toggle('flipped');
    frontFace.setAttribute('aria-hidden', String(isFlipped));
    backFace.setAttribute('aria-hidden', String(!isFlipped));
    // Rating a card you haven't revealed is how people fool themselves.
    setRatingEnabled(mode === 'recall' && isFlipped);
    if (isFlipped) {
      var def = c.shortDef || c.longDef || '(no definition)';
      announce(c.pos ? c.pos + '. ' + def : def);
    } else {
      announce(c.front);
    }
  }
  function next() { if (idx < cards.length - 1) { idx++; render(); } }
  function prev() { if (idx > 0) { idx--; render(); } }

  // Under "starred only" a star change moves the current card in or out of the
  // deck, so re-filter; otherwise repaint in place to keep the position.
  // A recall session keeps its deck (and the card's flipped state) and only
  // repaints the star.
  function refreshAfterStar() {
    if (mode === 'recall') paintStar();
    else if (starredToggle && starredToggle.checked) applyFilter();
    else render();
  }

  // Toggle the star on the current card. Optimistic: flip local state and UI
  // right away, persist in the background, and revert if the request fails.
  function toggleStar() {
    var c = current();
    if (!c) return;
    var key = keyOf(c.lemma, c.shortDef);
    var willStar = !starred[key];
    if (willStar) starred[key] = true; else delete starred[key];
    refreshAfterStar();

    fetch('/userspace/toggle_star', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        owner_id: S.ownerId, language: S.language, list_name: S.listName,
        word: [c.lemma, c.shortDef], starred: willStar
      })
    }).then(function (resp) {
      if (!resp.ok) throw new Error('save failed');
    }).catch(function () {
      if (willStar) delete starred[key]; else starred[key] = true;
      refreshAfterStar();
    });
  }

  posFilter.addEventListener('change', applyFilter);
  if (starredToggle) starredToggle.addEventListener('change', applyFilter);
  cardEl.addEventListener('click', flip);
  flipBtn.addEventListener('click', function (e) { e.stopPropagation(); flip(); });
  starBtn.addEventListener('click', function (e) { e.stopPropagation(); toggleStar(); });
  prevBtn.addEventListener('click', prev);
  nextBtn.addEventListener('click', next);
  recallToggle.addEventListener('change', function () { setMode(recallToggle.checked); });
  ratingBar.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-rating]');
    if (btn) rate(btn.getAttribute('data-rating'));
  });
  restartBtn.addEventListener('click', function () { buildQueue(true); render(); });

  // Keyboard shortcuts, but only while the Flashcards tab is the visible panel
  // and focus isn't in the POS <select>.
  document.addEventListener('keydown', function (e) {
    var panel = document.getElementById('mode-flashcards');
    if (!panel || panel.style.display === 'none') return;
    var tag = (e.target.tagName || '').toLowerCase();
    // Let native buttons/links handle their own Space/Enter activation; the card
    // itself is a focusable <div> (flip is also on the "Flip card" button) that
    // relies on this handler.
    if (tag === 'input' || tag === 'select' || tag === 'textarea' ||
        tag === 'button' || tag === 'a') return;
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); }
    else if (mode === 'recall') {
      // rate() ignores keys until the card is flipped; arrows do nothing here.
      if (RATING_KEYS[e.key]) { e.preventDefault(); rate(RATING_KEYS[e.key]); }
    }
    else if (e.key === 'ArrowRight') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); }
  });

  render();
})();
