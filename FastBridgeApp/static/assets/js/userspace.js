// Reusable modal for word selection
function showWordSelectModal({lang, list, onSave, saveLabel = 'Save', cancelLabel = 'Cancel', title = 'Add Words'}) {
    let modal = document.createElement('div');
    modal.className = 'word-select-modal';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.6)';
    modal.style.zIndex = '9999';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.innerHTML = `
        <div style='background:#222; color:#fff; border-radius:12px; padding:32px 36px; min-width:340px; max-width:520px; box-shadow:0 2px 16px rgba(34,179,179,0.18); position:relative;'>
            <h3 style='color:#22b3b3; margin-bottom:18px;'>${title}${list ? ` <span style='color:#ffb366;'>${list}</span>` : ''} (${lang})</h3>
            <input id='word-select-search' type='text' placeholder='Search for a word...' style='width:100%; padding:8px 12px; border-radius:6px; border:none; margin-bottom:12px; font-size:1rem;'>
            <div id='word-select-table-container' style='max-height:220px; overflow-y:auto; margin-bottom:12px;'></div>
            <div id='word-select-message' style='color:#ffb366; margin-bottom:10px;'></div>
            <div style='display:flex; gap:12px; justify-content:flex-end;'>
                <button id='word-select-save-btn' style='background:#22b3b3; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>${saveLabel}</button>
                <button id='word-select-cancel-btn' style='background:#ff6666; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>${cancelLabel}</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    let selected = [];
    const searchInput = modal.querySelector('#word-select-search');
    const tableContainer = modal.querySelector('#word-select-table-container');
    const messageDiv = modal.querySelector('#word-select-message');
    const saveBtn = modal.querySelector('#word-select-save-btn');
    const cancelBtn = modal.querySelector('#word-select-cancel-btn');

    function renderTable(wordsArr) {
        let html = `<table style='width:100%; border-collapse:collapse;'>`;
        html += `<thead><tr><th style='color:#22b3b3; padding:6px;'>Word</th><th style='color:#22b3b3; padding:6px;'>Definition</th><th></th></tr></thead><tbody>`;
        wordsArr.forEach((wordArr, idx) => {
            html += `<tr><td style='padding:6px;'>${wordArr[0]}</td><td style='padding:6px;'>${wordArr[1]}</td><td style='padding:6px;'><input type='checkbox' class='word-select-checkbox' data-idx='${idx}' ${selected.some(w => w[0] === wordArr[0] && w[1] === wordArr[1]) ? 'checked' : ''}></td></tr>`;
        });
        html += `</tbody></table>`;
        tableContainer.innerHTML = html;
    }

    searchInput.addEventListener('input', debounce(async () => {
        const query = searchInput.value.trim();
        if (!query) {
            tableContainer.innerHTML = '';
            return;
        }
        messageDiv.textContent = 'Searching...';
        try {
            const resp = await fetch(`/userspace/words?language=${lang}&query=${encodeURIComponent(query)}`);
            const data = await resp.json();
            const words = data.words || [];
            renderTable(words);
            messageDiv.textContent = '';
        } catch {
            messageDiv.textContent = 'Error searching words.';
        }
    }, 500));

    tableContainer.addEventListener('change', (e) => {
        if (e.target.classList.contains('word-select-checkbox')) {
            const idx = e.target.getAttribute('data-idx');
            const wordArr = (tableContainer.querySelectorAll('tbody tr'))[idx];
            const word = wordArr.children[0].textContent;
            const def = wordArr.children[1].textContent;
            if (e.target.checked) {
                if (!selected.some(w => w[0] === word && w[1] === def)) {
                    selected.push([word, def]);
                }
            } else {
                selected = selected.filter(w => !(w[0] === word && w[1] === def));
            }
        }
    });

    saveBtn.addEventListener('click', async () => {
        if (selected.length === 0) {
            messageDiv.textContent = 'Please select at least one word.';
            return;
        }
        await onSave(selected, {modal, messageDiv, saveBtn});
    });

    cancelBtn.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
}
const tabs = document.querySelectorAll('.user-tab');
const contents = document.querySelectorAll('.tab-content > div');
const fetchWordsBtn = document.getElementById('fetch-words-btn');
const languageSelect = document.getElementById('language-select');
const selectedWordsContainer = document.getElementById('selected-words-container');
const saveListBtn = document.getElementById('save-list-btn');
const listNameInput = document.getElementById('list-name');
const createListMessage = document.getElementById('create-list-message');

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
        // Flex row for list buttons
        html += `<div class='vocab-list-row' style='display:flex; flex-direction:row; gap:12px; flex-wrap:wrap; justify-content:flex-start; margin-bottom:12px;'>`;
        lists.forEach(listName => {
            html += `
                <button class='vocab-list-btn' data-lang='${lang}' data-list='${listName}' style='background:#222; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(34,179,179,0.10); font-weight:500; transition:background 0.2s, color 0.2s; border:none;'>${listName}</button>
                <button class='add-word-btn' data-lang='${lang}' data-list='${listName}' style='background:#228383; color:#fff; border-radius:8px; padding:10px 14px; margin-left:4px; cursor:pointer; font-weight:500; border:none;'>+ Add New Word</button>
            `;
        });
        html += `</div>`;
        // Dedicated details area below all buttons
        html += `<div class='vocab-list-details-area' style='width:100%; margin-top:10px;'></div>`;
        html += `</div>`;
    });
    tabDataCache[route] = html;
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
    // Add New Word modal logic (refactored)
    document.querySelectorAll('.add-word-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-lang');
            const list = btn.getAttribute('data-list');
            showWordSelectModal({
                lang,
                list,
                title: 'Add New Word to',
                saveLabel: 'Save',
                cancelLabel: 'Cancel',
                onSave: async (selected, {modal, messageDiv, saveBtn}) => {
                    saveBtn.textContent = 'Saving...';
                    saveBtn.disabled = true;
                    try {
                        const resp = await fetch('/userspace/add_words', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                list_name: list,
                                language: lang,
                                words: selected
                            })
                        });
                        const data = await resp.json();
                        if (data.success) {
                            messageDiv.textContent = 'Words added!';
                            setTimeout(() => { window.location.reload(); }, 1200);
                        } else {
                            messageDiv.textContent = 'Error adding words.';
                            saveBtn.disabled = false;
                            saveBtn.textContent = 'Save';
                        }
                    } catch {
                        messageDiv.textContent = 'Error adding words.';
                        saveBtn.disabled = false;
                        saveBtn.textContent = 'Save';
                    }
                }
            });
        });
    });
    // No caching for list details
    let activeBtn = null;
    document.querySelectorAll('.vocab-list-btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            if (btn !== activeBtn) {
                btn.style.background = '#228383';
                btn.style.color = '#fff';
            }
        });
        btn.addEventListener('mouseleave', () => {
            if (btn !== activeBtn) {
                btn.style.background = '#222';
                btn.style.color = '#fff';
            }
        });
        btn.addEventListener('click', async () => {
            const lang = btn.getAttribute('data-lang');
            const list = btn.getAttribute('data-list');
            // Highlight active button
            if (activeBtn) {
                activeBtn.style.background = '#222';
                activeBtn.style.color = '#fff';
            }
            btn.style.background = '#22b3b3';
            btn.style.color = '#fff';
            activeBtn = btn;
            // Find details area
            const detailsArea = btn.closest('div').parentNode.querySelector('.vocab-list-details-area');
            // Hide details in all details areas for this language
            btn.closest('div').parentNode.querySelectorAll('.vocab-list-details-area').forEach(area => {
                area.innerHTML = '';
            });
            detailsArea.innerHTML = '<p style="color:#fff;">Loading...</p>';
            try {
                const resp = await fetch(`/userspace/list_details?language=${encodeURIComponent(lang)}&list_name=${encodeURIComponent(list)}`);
                const data = await resp.json();
                // Track retained and deleted words
                let retainedWords = Object.entries(data).map(([word, info]) => info);
                let deletedWords = [];
                // Display flash cards
                let cardsHtml = '<div id="flashcard-list" style="display:flex; flex-wrap:wrap; gap:16px;">';
                Object.entries(data).forEach(([word, info]) => {
                    const simpleLemma = info['SIMPLE LEMMA'];
                    cardsHtml += `<div class='flashcard' data-word='${simpleLemma}' style='background:#222; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(34,179,179,0.15); padding:18px 22px; min-width:180px; max-width:320px; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative; word-break:break-word; overflow-wrap:break-word;'>`;
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
                cardsHtml += `<button id='delete-list-btn' style='background:#ff6666; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(255,102,102,0.15); transition:background 0.2s;'>Delete Entire List</button>`;
                cardsHtml += `</div>`;
                detailsArea.innerHTML = cardsHtml;
                // Delete button logic for flashcards
                const flashcardList = detailsArea.querySelector('#flashcard-list');
                flashcardList.querySelectorAll('.delete-flashcard-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const word = btn.getAttribute('data-word');
                        // Remove card from UI
                        const card = btn.closest('.flashcard');
                        if (card) card.remove();
                        // Remove from retainedWords, add to deletedWords
                        const idx = retainedWords.findIndex(w => w['SIMPLE LEMMA'] === word);
                        if (idx !== -1) {
                            const removed = retainedWords.splice(idx, 1)[0];
                            if (!deletedWords.some(dw => dw['SIMPLE LEMMA'] === removed['SIMPLE LEMMA'])) {
                                deletedWords.push(removed);
                            }
                        }
                        updateDeletedWordsSummary();
                    });
                });

                // Delete Entire List button logic
                const deleteListBtn = detailsArea.querySelector('#delete-list-btn');
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
                            deleteListBtn.disabled = false;
                        }
                    } catch {
                        deleteListBtn.textContent = 'Error!';
                        deleteListBtn.disabled = false;
                    }
                });
                function updateDeletedWordsSummary() {
                    const summaryDiv = detailsArea.querySelector('#deleted-words-summary');
                    const saveBtn = detailsArea.querySelector('#save-changes-btn');
                    saveBtn.onclick = async function() {
                        saveBtn.textContent = 'Saving...';
                        saveBtn.disabled = true;
                        // Only pass SIMPLE LEMMA and SHORT DEFINITION to backend
                        const wordsToSave = retainedWords.map(w => [w['SIMPLE LEMMA'], w['SHORT DEFINITION']]);
                        try {
                            const resp = await fetch(`/userspace/update_list`, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    list_name: list,
                                    language: lang,
                                    words: wordsToSave
                                })
                            });
                            const result = await resp.json();
                            if (result.success) {
                                saveBtn.textContent = 'Saved!';
                                // Clear deletedWords and update summary so nothing to undo
                                deletedWords = [];
                                setTimeout(() => {
                                    updateDeletedWordsSummary(); // This will hide the button
                                    saveBtn.textContent = 'Save Changes';
                                    saveBtn.disabled = false;
                                }, 1500);
                            } else {
                                saveBtn.textContent = 'Error!';
                                saveBtn.disabled = false;
                            }
                        } catch {
                            saveBtn.textContent = 'Error!';
                            saveBtn.disabled = false;
                        }
                    };
                    if (deletedWords.length > 0) {
                        let undoHtml = `<span style='color:#ffb366; font-weight:600;'>Words to delete:</span> `;
                        deletedWords.forEach(info => {
                            undoHtml += `<span style='color:#fff; margin-right:8px;'>${info['SIMPLE LEMMA']} <button class='undo-delete-btn' data-word='${info['SIMPLE LEMMA']}' style='background:#228383; color:#fff; border:none; border-radius:4px; padding:2px 8px; font-size:0.9rem; margin-left:4px; cursor:pointer;'>Undo</button></span>`;
                        });
                        summaryDiv.innerHTML = undoHtml;
                        saveBtn.style.display = '';
                        // Add undo listeners
                        summaryDiv.querySelectorAll('.undo-delete-btn').forEach(btn => {
                            btn.addEventListener('click', () => {
                                const word = btn.getAttribute('data-word');
                                const idx = deletedWords.findIndex(w => w['SIMPLE LEMMA'] === word);
                                if (idx !== -1) {
                                    const restored = deletedWords.splice(idx, 1)[0];
                                    retainedWords.push(restored);
                                    // Re-render flashcard with full info
                                    let cardHtml = `<div class='flashcard' data-word='${restored['SIMPLE LEMMA']}' style='background:#222; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(34,179,179,0.15); padding:18px 22px; min-width:180px; max-width:320px; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative; word-break:break-word; overflow-wrap:break-word;'>`;
                                    cardHtml += `<div style='font-size:1.2rem; font-weight:700; color:#22b3b3; margin-bottom:8px;'>${restored['SIMPLE LEMMA']}</div>`;
                                    Object.entries(restored).forEach(([key, val]) => {
                                        cardHtml += `<div style='margin-bottom:4px;'><span style='font-weight:600; color:#ffb366;'>${key}:</span> <span style='color:#fff;'>${val}</span></div>`;
                                    });
                                    cardHtml += `<button class='delete-flashcard-btn' data-word='${restored['SIMPLE LEMMA']}' style='position:absolute; top:10px; right:10px; background:#ff6666; color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:0.95rem; font-weight:600; cursor:pointer;'>Delete</button>`;
                                    cardHtml += `</div>`;
                                    flashcardList.insertAdjacentHTML('beforeend', cardHtml);
                                    // Re-attach delete listener
                                    flashcardList.querySelectorAll('.delete-flashcard-btn').forEach(btn => {
                                        btn.onclick = null;
                                        btn.addEventListener('click', () => {
                                            const word = btn.getAttribute('data-word');
                                            const card = btn.closest('.flashcard');
                                            if (card) card.remove();
                                            const idx = retainedWords.findIndex(w => w['SIMPLE LEMMA'] === word);
                                            if (idx !== -1) {
                                                const removed = retainedWords.splice(idx, 1)[0];
                                                if (!deletedWords.some(dw => dw['SIMPLE LEMMA'] === removed['SIMPLE LEMMA'])) {
                                                    deletedWords.push(removed);
                                                }
                                            }
                                            updateDeletedWordsSummary();
                                        });
                                    });
                                    updateDeletedWordsSummary();
                                }
                            });
                        });
                    } else {
                        summaryDiv.innerHTML = '';
                        saveBtn.style.display = 'none';
                    }
                }
            } catch {
                detailsArea.innerHTML = '<p style="color:#fff;">Error loading details.</p>';
            }
        });
    });
// All new flex/caching logic is now inside the previous patch block
// Remove duplicate/old logic and close function
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
tbody.innerHTML = '';
allWords = [];
filteredWords = [];
createListMessage.textContent = '';
});

// Modal-based Add Words for Create List
fetchWordsBtn.addEventListener('click', () => {
    const lang = languageSelect.value;
    if (!lang) {
        createListMessage.textContent = 'Please select a language.';
        return;
    }
    showWordSelectModal({
        lang,
        title: 'Add Words',
        saveLabel: 'Add Selected',
        cancelLabel: 'Cancel',
        onSave: (selected, {modal}) => {
            selected.forEach(wordArr => {
                if (!selectedWords.some(w => w[0] === wordArr[0] && w[1] === wordArr[1])) {
                    selectedWords.push(wordArr);
                }
            });
            renderSelectedWords();
            document.body.removeChild(modal);
        }
    });
});

// Live search (prefix query to backend)
function debounce(fn, delay) {
let timeout;
return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
};
}

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
