const tabs = document.querySelectorAll('.user-tab');
const contents = document.querySelectorAll('.tab-content > div');
const fetchWordsBtn = document.getElementById('fetch-words-btn');
const fetchAllWordsBtn = document.getElementById('fetch-all-words-btn');
const languageSelect = document.getElementById('language-select');
const wordsSearchContainer = document.getElementById('words-search-container');
const wordSearch = document.getElementById('word-search');
const wordsTable = document.getElementById('words-table');
const selectedWordsContainer = document.getElementById('selected-words-container');
const saveListBtn = document.getElementById('save-list-btn');
const listNameInput = document.getElementById('list-name');
const createListMessage = document.getElementById('create-list-message');
const searchWordGroup = document.getElementById('search-word-group');

let allWords = [];
let filteredWords = [];
let selectedWords = [];
// Tab data cache
const tabDataCache = {};

// Helper to fetch and display data (with cache and event re-attachment)
async function fetchTabData(route, contentDiv) {
if (tabDataCache[route]) {
    contentDiv.innerHTML = tabDataCache[route];
    // Re-attach event listeners for vocab list boxes
    setTimeout(() => {
    attachVocabListEvents();
    }, 0);
    return;
}
contentDiv.innerHTML = '<p style="color:#fff;">Loading...</p>';
try {
    const resp = await fetch(route);
    const data = await resp.json();
    let html = '';
    if (data.notes) {
    html = `<pre style='color:#fff; background:transparent; text-align:left;'>${JSON.stringify(data.notes, null, 2)}</pre>`;
    } else if (data.vocab) {
    // Expecting {language: [list names]}
    html = '';
    Object.entries(data.vocab).forEach(([lang, lists]) => {
        html += `<div style='margin-bottom:18px; text-align:left;'>`;
        html += `<h4 style='color:#22b3b3; margin-bottom:8px; text-align:left;'>${lang}</h4>`;
        html += `<div class='vocab-list-col' style='display:flex; flex-direction:column; gap:12px; justify-content:flex-start;'>`;
        lists.forEach(listName => {
        html += `
            <div style='display:flex; flex-direction:column; align-items:flex-start;'>
            <div class='vocab-list-box' data-lang='${lang}' data-list='${listName}' style='background:#222; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(34,179,179,0.10); font-weight:500; transition:background 0.2s, color 0.2s; margin-bottom:4px;'>${listName}</div>
            <div class='vocab-list-details' style='display:none; width:100%;'></div>
            </div>
        `;
        });
        html += `</div></div>`;
    });
    tabDataCache[route] = html;
    // Add hover effect and click listeners
    setTimeout(() => {
        attachVocabListEvents();
    }, 0);
    } else if (data.media) {
    html = `<pre style='color:#fff; background:transparent; text-align:left;'>${JSON.stringify(data.media, null, 2)}</pre>`;
    } else {
    html = '<p style="color:#fff;">No data found.</p>';
    }
    contentDiv.innerHTML = html;
} catch {
    contentDiv.innerHTML = '<p style="color:#fff;">Error loading data.</p>';
}
}

// Attach hover and click events for vocab list boxes
function attachVocabListEvents() {
document.querySelectorAll('.vocab-list-box').forEach(box => {
    box.addEventListener('mouseenter', () => {
    box.style.background = '#228383';
    box.style.color = '#fff';
    });
    box.addEventListener('mouseleave', () => {
    box.style.background = '#222';
    box.style.color = '#fff';
    });
    box.addEventListener('click', async () => {
    const lang = box.getAttribute('data-lang');
    const list = box.getAttribute('data-list');
    const detailsDiv = box.parentNode.querySelector('.vocab-list-details');
    // Toggle: if details are visible and loaded, hide them and return
    if (detailsDiv.style.display === 'block' && detailsDiv.innerHTML.trim() !== '') {
        detailsDiv.style.display = 'none';
        return;
    }
    box.textContent = 'Loading...';
    try {
        const resp = await fetch(`/userspace/list_details?language=${encodeURIComponent(lang)}&list_name=${encodeURIComponent(list)}`);
        const data = await resp.json();
        box.textContent = `${list}`;
        // Display details in the details div below the box as flash cards
        detailsDiv.style.display = 'block';
        detailsDiv.style.color = '#fff';
        detailsDiv.style.marginTop = '6px';
        detailsDiv.style.padding = '8px 12px';
        detailsDiv.style.borderRadius = '6px';
        // Track retained and deleted words
        let retainedWords = Object.values(data).map(info => [info['SIMPLE LEMMA'], info['SHORT DEFINITION']]);
        let deletedWords = [];
        // Display flash cards
        let cardsHtml = '<div id="flashcard-list" style="display:flex; flex-wrap:wrap; gap:16px;">';
        Object.entries(data).forEach(([word, info]) => {
        const simpleLemma = info['SIMPLE LEMMA'];
        cardsHtml += `<div class='flashcard' data-word='${simpleLemma}' style='background:#222; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(34,179,179,0.15); padding:18px 22px; min-width:fit-content; max-width:fit-content; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative;'>`;
        cardsHtml += `<div style='font-size:1.2rem; font-weight:700; color:#22b3b3; margin-bottom:8px;'>${word}</div>`;
        Object.entries(info).forEach(([key, val]) => {
            cardsHtml += `<div style='margin-bottom:4px;'><span style='font-weight:600; color:#ffb366;'>${key}:</span> <span style='color:#fff;'>${val}</span></div>`;
        });
        cardsHtml += `<button class='delete-flashcard-btn' data-word='${simpleLemma}' style='position:absolute; top:10px; right:10px; background:#ff6666; color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:0.95rem; font-weight:600; cursor:pointer;'>Delete</button>`;
        cardsHtml += `</div>`;
        });
        cardsHtml += '</div>';
        // Deleted words summary and Save Changes button (initially hidden)
        cardsHtml += `<div id='deleted-words-summary' style='margin-top:18px;'></div>`;
        cardsHtml += `<div style='display:flex; gap:12px; align-items:center; margin-top:12px;'>`;
        cardsHtml += `<button id='save-changes-btn' style='background:#228383; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(34,179,179,0.15); transition:background 0.2s; display:none;'>Save Changes</button>`;
        cardsHtml += `<button id='delete-list-btn' style='background:#ff6666; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(255,102,102,0.15); transition:background 0.2s;'>Delete List</button>`;
        cardsHtml += `</div>`;
        detailsDiv.innerHTML = cardsHtml;

        // Delete button logic
        const flashcardList = detailsDiv.querySelector('#flashcard-list');
        flashcardList.querySelectorAll('.delete-flashcard-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const word = btn.getAttribute('data-word');
            // Remove card from UI
            const card = btn.closest('.flashcard');
            if (card) card.remove();
            // Remove from retainedWords, add to deletedWords
            const idx = retainedWords.findIndex(w => w[0] === word);
            if (idx !== -1) {
            const removed = retainedWords.splice(idx, 1)[0];
            if (!deletedWords.some(dw => dw[0] === removed[0] && dw[1] === removed[1])) {
                deletedWords.push(removed);
            }
            }
            // Update deleted words summary
            updateDeletedWordsSummary();
        });
        });

        function updateDeletedWordsSummary() {
        const summaryDiv = detailsDiv.querySelector('#deleted-words-summary');
        const saveBtn = detailsDiv.querySelector('#save-changes-btn');
        if (deletedWords.length > 0) {
            let undoHtml = `<span style='color:#ffb366; font-weight:600;'>Words to delete:</span> `;
            deletedWords.forEach(wordArr => {
            undoHtml += `<span style='color:#fff; margin-right:8px;'>${wordArr[0]} <button class='undo-delete-btn' data-word='${wordArr[0]}' style='background:#228383; color:#fff; border:none; border-radius:4px; padding:2px 8px; font-size:0.9rem; margin-left:4px; cursor:pointer;'>Undo</button></span>`;
            });
            summaryDiv.innerHTML = undoHtml;
            saveBtn.style.display = '';
            // Add undo listeners
            summaryDiv.querySelectorAll('.undo-delete-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const word = btn.getAttribute('data-word');
                // Remove from deletedWords
                const idx = deletedWords.findIndex(w => w[0] === word);
                if (idx !== -1) {
                const restored = deletedWords.splice(idx, 1)[0];
                if (!retainedWords.some(rw => rw[0] === restored[0] && rw[1] === restored[1])) {
                    retainedWords.push(restored);
                    // Re-render flashcard (add back to UI)
                    const info = data[word];
                    if (info) {
                    const cardHtml = `<div class='flashcard' data-word='${word}' style='background:#222; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(34,179,179,0.15); padding:18px 22px; min-width:fit-content; max-width:fit-content; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative;'>` +
                        `<div style='font-size:1.2rem; font-weight:700; color:#22b3b3; margin-bottom:8px;'>${word}</div>` +
                        Object.entries(info).map(([key, val]) => `<div style='margin-bottom:4px;'><span style='font-weight:600; color:#ffb366;'>${key}:</span> <span style='color:#fff;'>${val}</span></div>`).join('') +
                        `<button class='delete-flashcard-btn' data-word='${word}' style='position:absolute; top:10px; right:10px; background:#ff6666; color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:0.95rem; font-weight:600; cursor:pointer;'>Delete</button>` +
                        `</div>`;
                    const flashcardList = detailsDiv.querySelector('#flashcard-list');
                    // Only add if not already present
                    if (!flashcardList.querySelector(`[data-word='${word}']`)) {
                        flashcardList.insertAdjacentHTML('beforeend', cardHtml);
                        // Re-add delete logic
                        const newBtn = flashcardList.querySelector(`.delete-flashcard-btn[data-word='${word}']`);
                        if (newBtn) {
                        newBtn.addEventListener('click', () => {
                            const card = newBtn.closest('.flashcard');
                            if (card) card.remove();
                            const idx = retainedWords.findIndex(w => w[0] === word);
                            if (idx !== -1) {
                            const removed = retainedWords.splice(idx, 1)[0];
                            if (!deletedWords.some(dw => dw[0] === removed[0] && dw[1] === removed[1])) {
                                deletedWords.push(removed);
                            }
                            }
                            updateDeletedWordsSummary();
                        });
                        }
                    }
                    }
                }
                }
                updateDeletedWordsSummary();
            });
            });
        } else {
            summaryDiv.innerHTML = '';
            saveBtn.style.display = 'none';
        }
        }

        // Save Changes button logic
        const saveBtn = detailsDiv.querySelector('#save-changes-btn');
        saveBtn.addEventListener('click', async () => {
        saveBtn.textContent = 'Saving...';
        saveBtn.disabled = true;
        // Send retainedWords to backend as 2D array
        try {
            const resp = await fetch(`/userspace/update_list`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                list_name: list,
                language: lang,
                words: retainedWords
            })
            });
            const result = await resp.json();
            if (result.success) {
            saveBtn.textContent = 'Saved!';
            setTimeout(() => { detailsDiv.style.display = 'none'; }, 1500);
            } else {
            saveBtn.textContent = 'Error!';
            }
        } catch {
            saveBtn.textContent = 'Error!';
        }
        });

        // Delete List button logic
        const deleteListBtn = detailsDiv.querySelector('#delete-list-btn');
        deleteListBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete the entire list? This action cannot be undone.')) return;
        deleteListBtn.textContent = 'Deleting...';
        deleteListBtn.disabled = true;
        try {
            const resp = await fetch(`/userspace/delete_list`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                list_name: list,
                language: lang
            })
            });
            const result = await resp.json();
            if (result.success) {
            deleteListBtn.textContent = 'Deleted!';
            setTimeout(() => {
                window.location.reload();
            }, 1200);
            } else {
            deleteListBtn.textContent = 'Error!';
            }
        } catch {
            deleteListBtn.textContent = 'Error!';
        }
        });
    } catch {
        box.textContent = `${list}`;
        alert('Error loading list details');
    }
    });
});
}

tabs.forEach((tab, idx) => {
tab.addEventListener('click', (e) => {
    e.preventDefault();
    tabs.forEach(t => {
    t.classList.remove('active');
    t.style.borderBottom = 'none';
    t.style.color = '#ccc';
    });
    // Only show Vocabulary and Create List
    contents.forEach((c, i) => {
    if (tabs[i].getAttribute('href') === '/userspace/vocab' || tabs[i].getAttribute('href') === '#') {
        c.style.display = 'none';
    }
    });

    tab.classList.add('active');
    tab.style.borderBottom = '3px solid #228383';
    tab.style.color = '#fff';
    // Show only the relevant tab content
    if (tab.getAttribute('href') === '/userspace/vocab') {
    contents[idx].style.display = 'block';
    fetchTabData(tab.getAttribute('href'), contents[idx]);
    } else if (tab.getAttribute('href') === '#') {
    contents[idx].style.display = 'block';
    }
});
});

// Initial load for Vocabulary tab
tabs.forEach((t, i) => {
    if (t.getAttribute('href') === '/userspace/vocab') {
    t.classList.add('active');
    t.style.borderBottom = '3px solid #228383';
    t.style.color = '#fff';
    contents[i].style.display = 'block';
    fetchTabData(t.getAttribute('href'), contents[i]);
    } else if (t.getAttribute('href') === '#') {
    t.classList.remove('active');
    t.style.borderBottom = 'none';
    t.style.color = '#ccc';
    contents[i].style.display = 'none';
    }
});



// Reset state when language changes
languageSelect.addEventListener('change', () => {
selectedWords = [];
renderSelectedWords();
wordsSearchContainer.style.display = 'none';
searchWordGroup.style.display = 'none';
const tbody = wordsTable.querySelector('tbody');
tbody.innerHTML = '';
wordSearch.value = '';
allWords = [];
filteredWords = [];
createListMessage.textContent = '';
});

// Fetch words by language
fetchWordsBtn.addEventListener('click', async () => {
const lang = languageSelect.value;
if (!lang) {
    createListMessage.textContent = 'Please select a language.';
    return;
}
wordsSearchContainer.style.display = 'block';
searchWordGroup.style.display = 'flex';
createListMessage.textContent = 'Type in the search bar to load words.';
});

// Live search (prefix query to backend)
function debounce(fn, delay) {
let timeout;
return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
};
}
// Render words table
function renderWordsTable(wordsArr) {
const tbody = wordsTable.querySelector('tbody');
tbody.innerHTML = '';
wordsArr.forEach((wordArr, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
    <td style="padding:8px;">${wordArr[0]}</td>
    <td style="padding:8px;">${wordArr[1]}</td>
    <td style="padding:8px;"><input type="checkbox" class="word-select-checkbox" data-idx="${idx}" ${selectedWords.some(w => w[0] === wordArr[0] && w[1] === wordArr[1]) ? 'checked' : ''}></td>
    `;
    tbody.appendChild(tr);
});
}

wordSearch.addEventListener('input', debounce(async () => {
const query = wordSearch.value.trim();
if (!query) {
    const tbody = wordsTable.querySelector('tbody');
    tbody.innerHTML = '';
    return;
}
createListMessage.textContent = 'Searching...';
try {
    const resp = await fetch(`/userspace/words?language=${languageSelect.value}&query=${encodeURIComponent(query)}`);
    const data = await resp.json();
    filteredWords = data.words || [];
    renderWordsTable(filteredWords);
    createListMessage.textContent = '';
} catch (error) {
    createListMessage.textContent = 'Error searching words.';
}
}, 500));


// Fetch ALL words (slow)
fetchAllWordsBtn.addEventListener('click', async () => {
const lang = languageSelect.value;
if (!lang) {
    createListMessage.textContent = 'Please select a language first.';
    return;
}
createListMessage.textContent = 'Fetching ALL words (may be slow)...';
try {
    const resp = await fetch(`/userspace/words?language=${lang}`);
    const data = await resp.json();
    allWords = data.words || [];
    filteredWords = allWords;
    renderWordsTable(filteredWords);
    createListMessage.textContent = '';
} catch {
    createListMessage.textContent = 'Error fetching words.';
}
});

wordsTable.addEventListener('change', (e) => {
if (e.target.classList.contains('word-select-checkbox')) {
    const idx = e.target.getAttribute('data-idx');
    const wordArr = filteredWords[idx];
    if (e.target.checked) {
    if (!selectedWords.some(w => w[0] === wordArr[0] && w[1] === wordArr[1])) {
        selectedWords.push(wordArr);
    }
    } else {
    selectedWords = selectedWords.filter(w => !(w[0] === wordArr[0] && w[1] === wordArr[1]));
    }
    renderSelectedWords();
}
});
// Render selected words as tags
function renderSelectedWords() {
selectedWordsContainer.innerHTML = '';
selectedWords.forEach(wordArr => {
    const box = document.createElement('span');
    box.textContent = `${wordArr[0]} (${wordArr[1]})`;
    box.style.display = 'inline-flex';
    box.style.alignItems = 'center';
    box.style.background = 'linear-gradient(90deg,#22b3b3 60%,#228383 100%)';
    box.style.color = '#fff';
    box.style.padding = '6px 14px 6px 10px';
    box.style.margin = '2px';
    box.style.borderRadius = '18px';
    box.style.fontWeight = '500';
    box.style.fontSize = '1rem';
    box.style.boxShadow = '0 1px 4px rgba(34,179,179,0.12)';
    const x = document.createElement('span');
    x.textContent = ' ×';
    x.style.cursor = 'pointer';
    x.style.color = '#fff';
    x.style.background = '#ff6666';
    x.style.borderRadius = '50%';
    x.style.marginLeft = '8px';
    x.style.padding = '2px 8px';
    x.style.fontWeight = 'bold';
    x.onmouseover = () => { x.style.background = '#ff3333'; };
    x.onmouseout = () => { x.style.background = '#ff6666'; };
    x.onclick = () => {
    selectedWords = selectedWords.filter(w => !(w[0] === wordArr[0] && w[1] === wordArr[1]));
    renderSelectedWords();
    };
    box.appendChild(x);
    selectedWordsContainer.appendChild(box);
});
}

// Save list to backend
saveListBtn.addEventListener('click', async () => {
const listName = listNameInput.value.trim();
const lang = languageSelect.value;
if (!listName) {
    createListMessage.textContent = 'Please enter a list name.';
    return;
}
if (!lang) {
    createListMessage.textContent = 'Please select a language.';
    return;
}
if (selectedWords.length === 0) {
    createListMessage.textContent = 'Please select at least one word.';
    return;
}
createListMessage.textContent = 'Saving list...';
try {
    const resp = await fetch('/userspace/create_list', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        list_name: listName,
        language: lang,
        words: selectedWords
    })
    });
    const data = await resp.json();
    if (data.success) {
    createListMessage.textContent = 'List created successfully! Refreshing page in 3 seconds...';
    listNameInput.value = '';
    languageSelect.value = '';
    wordsSearchContainer.style.display = 'none';
    selectedWords = [];
    renderSelectedWords();
    setTimeout(() => {
        window.location.reload();
    }, 3000);
    } else {
    createListMessage.textContent = 'Error creating list.';
    }
} catch {
    createListMessage.textContent = 'Error creating list.';
}
});

// Hide search group by default
searchWordGroup.style.display = 'none';