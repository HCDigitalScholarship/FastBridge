// Import Shared List logic
const importSharedBtn = document.getElementById('import-shared-btn');
if (importSharedBtn) {
    importSharedBtn.addEventListener('click', () => {
        const raw = document.getElementById('import-shared-link').value.trim();
        const messageDiv = document.getElementById('import-shared-message');
        if (!raw) {
            messageDiv.textContent = 'Please paste a share link.';
            return;
        }
        // Accept a full URL or a bare share_id
        let target;
        try {
            const url = new URL(raw);
            target = url.pathname;
        } catch {
            target = `/userspace/accept-list/${raw}`;
        }
        window.location.href = target;
    });
}
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
        <div role='dialog' aria-modal='true' aria-labelledby='word-select-title' style='background:#222; color:#fff; border-radius:12px; padding:32px 36px; min-width:340px; max-width:520px; box-shadow:0 2px 16px rgba(34,179,179,0.18); position:relative;'>
            <h3 id='word-select-title' style='color:#22b3b3; margin-bottom:18px;'>${title}${list ? ` <span style='color:#ffb366;'>${list}</span>` : ''} (${lang})</h3>
            <input id='word-select-search' type='text' placeholder='Search for a word...' aria-label='Search for words to add' style='width:100%; padding:8px 12px; border-radius:6px; border:none; margin-bottom:12px; font-size:1rem;'>
            <div id='word-select-table-container' style='max-height:220px; overflow-y:auto; margin-bottom:12px;'></div>
            <div id='word-select-message' role='status' aria-live='polite' style='color:#ffb366; margin-bottom:10px;'></div>
            <div style='display:flex; gap:12px; justify-content:flex-end;'>
                <button id='word-select-save-btn' aria-label='Save selected words to list' style='background:#22b3b3; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>${saveLabel}</button>
                <button id='word-select-cancel-btn' aria-label='Cancel and close word selection' style='background:#ff6666; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>${cancelLabel}</button>
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

// Helper to fetch and display data
async function fetchTabData(route, contentDiv) {
    // Don't cache paginated results
    contentDiv.innerHTML = '<p style="color:#fff;">Loading...</p>';
    try {
        const resp = await fetch(route);
        const data = await resp.json();
        let html = '';

        if (data.vocab) {
            // Add pagination info at top if available
            if (data.pagination) {
                const p = data.pagination;
                html += `<div style="margin-bottom:16px; color:#fff; text-align:center;">
                    <span>Showing ${p.total_lists > 0 ? ((p.current_page - 1) * p.limit + 1) : 0} - ${Math.min(p.current_page * p.limit, p.total_lists)} of ${p.total_lists} lists</span>
                </div>`;
            }

            // User lists
            Object.entries(data.vocab).forEach(([lang, lists]) => {
                html += `<div style='margin-bottom:18px; text-align:left;'>
                    <h4 style='color:#22b3b3; margin-bottom:8px;'>${lang}</h4>
                    <div class='vocab-list-row' style='display:flex; flex-direction:row; gap:12px; flex-wrap:wrap; justify-content:flex-start; margin-bottom:12px;'>`;
                lists.forEach(listItem => {
                    // Handle both old format (string) and new format (object)
                    const listName = typeof listItem === 'string' ? listItem : listItem.name;
                    const wordCount = typeof listItem === 'object' ? ` (${listItem.word_count} words)` : '';
                    const wordCountNum = typeof listItem === 'object' ? listItem.word_count : 0;
                    html += `
                        <a class='vocab-list-link' href='/userspace/list/${encodeURIComponent(lang)}/${encodeURIComponent(listName)}' aria-label='Open vocabulary list ${listName} (${wordCountNum} words)' style='display:inline-flex; align-items:center; background:#222; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(34,179,179,0.10); font-weight:500; text-decoration:none;'>${listName}${wordCount}</a>
                    `;
                });
                html += `</div>
                </div>`;
            });

            // Shared lists section
            if (data.shared_vocab) {
                html += `<div style="margin-bottom:32px;">
                    <h3 style="color:#ffb366; margin-bottom:12px;">Shared Lists</h3>`;
                Object.entries(data.shared_vocab).forEach(([lang, lists]) => {
                    html += `<div style='margin-bottom:18px; text-align:left;'>
                        <h4 style='color:#22b3b3; margin-bottom:8px;'>${lang}</h4>
                        <div class='shared-list-row' style='display:flex; flex-direction:row; gap:12px; flex-wrap:wrap; justify-content:flex-start; margin-bottom:12px;'>`;
                    lists.forEach(listItem => {
                        // Handle both old format (string) and new format (object)
                        const listName = typeof listItem === 'string' ? listItem : listItem.name;
                        const wordCount = typeof listItem === 'object' ? ` (${listItem.word_count} words)` : '';
                        const wordCountNum = typeof listItem === 'object' ? listItem.word_count : 0;
                        html += `
                            <a class='shared-list-link' href='/userspace/list/${encodeURIComponent(lang)}/${encodeURIComponent(listName)}?shared=true' aria-label='Open shared vocabulary list ${listName} (${wordCountNum} words)' style='display:inline-flex; align-items:center; background:#333; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(255,179,102,0.10); font-weight:500; text-decoration:none;'>${listName}${wordCount}</a>
                        `;
                    });
                    html += `</div>
                    </div>`;
                });
                html += '</div>';
            }

            // Add pagination controls at bottom
            if (data.pagination && data.pagination.total_pages > 1) {
                const p = data.pagination;
                html += `<div style="display:flex; justify-content:center; align-items:center; gap:8px; margin-top:24px; color:#fff;">`;

                // Previous button
                if (p.has_prev) {
                    html += `<button class="pagination-btn" data-page="${p.current_page - 1}" aria-label="Go to previous page" style="background:#228383; color:#fff; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; font-size:0.9rem;">Previous</button>`;
                }

                // Page numbers
                const startPage = Math.max(1, p.current_page - 2);
                const endPage = Math.min(p.total_pages, p.current_page + 2);

                for (let i = startPage; i <= endPage; i++) {
                    const isActive = i === p.current_page;
                    html += `<button class="pagination-btn" data-page="${i}" aria-label="Go to page ${i}" aria-current="${isActive ? 'page' : 'false'}" ${isActive ? 'disabled' : ''} style="background:${isActive ? '#22b3b3' : '#444'}; color:#fff; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; font-size:0.9rem; font-weight:${isActive ? '600' : '400'};">${i}</button>`;
                }

                // Next button
                if (p.has_next) {
                    html += `<button class="pagination-btn" data-page="${p.current_page + 1}" aria-label="Go to next page" style="background:#228383; color:#fff; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; font-size:0.9rem;">Next</button>`;
                }

                html += `</div>`;
            }

            setTimeout(() => {
                // List names are now links straight to the dedicated study page,
                // so the old inline card/expansion panel is no longer wired up.
                attachPaginationEvents(route, contentDiv);
            }, 0);
        }
        contentDiv.innerHTML = html;
    } catch {
        contentDiv.innerHTML = '<p style="color:#fff;">Error loading data.</p>';
    }
}

tabs.forEach((tab, idx) => {
if (tab.id === 'saved-searches-tab') return; // has its own dedicated handler below
tab.addEventListener('click', (e) => {
    e.preventDefault();
    tabs.forEach(t => {
    t.classList.remove('active');
    t.style.borderBottom = 'none';
    t.style.color = '#ccc';
    t.setAttribute('aria-selected', 'false');
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
    tab.setAttribute('aria-selected', 'true');
    // Show only the relevant tab content
    if (tab.getAttribute('href') === '/userspace/vocab') {
    contents[idx].style.display = 'block';
    fetchTabData(tab.getAttribute('href'), document.getElementById('vocabulary-content'));
    } else if (tab.getAttribute('href') === '#') {
    contents[idx].style.display = 'block';
    }
});
});

// Initial load for Vocabulary tab
tabs.forEach((t, i) => {
    if (t.id === 'saved-searches-tab') return; // managed by its own handler
    if (t.getAttribute('href') === '/userspace/vocab') {
    t.classList.add('active');
    t.style.borderBottom = '3px solid #228383';
    t.style.color = '#fff';
    contents[i].style.display = 'block';
    fetchTabData(t.getAttribute('href'), document.getElementById('vocabulary-content'));
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

// Reload the vocabulary list when the language filter changes.
document.addEventListener('DOMContentLoaded', () => {
    const languageFilter = document.getElementById('vocab-language-filter');
    if (languageFilter) {
        languageFilter.addEventListener('change', () => {
            updateVocabWithFilters();
        });
    }
});

function updateVocabWithFilters() {
    const languageFilter = document.getElementById('vocab-language-filter');
    const vocabContent = document.getElementById('vocabulary-content');

    if (!languageFilter || !vocabContent) return;

    const params = new URLSearchParams();
    if (languageFilter.value) {
        params.set('language_filter', languageFilter.value);
    }

    const query = params.toString();
    fetchTabData(query ? `/userspace/vocab?${query}` : '/userspace/vocab', vocabContent);
}

function attachPaginationEvents(currentRoute, contentDiv) {
    document.querySelectorAll('.pagination-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const page = btn.getAttribute('data-page');

            // Parse current route to preserve filters
            const url = new URL(currentRoute, window.location.origin);
            url.searchParams.set('page', page);

            // If no filter in current route, check UI for the current filter value
            if (!url.searchParams.has('language_filter')) {
                const languageFilter = document.getElementById('vocab-language-filter');
                if (languageFilter && languageFilter.value) {
                    url.searchParams.set('language_filter', languageFilter.value);
                }
            }

            const newRoute = url.pathname + url.search;
            await fetchTabData(newRoute, contentDiv);
        });
    });
}

// Saved Searches tab

async function loadSavedSearches() {
    const appFilter  = document.getElementById('search-app-filter')?.value  || '';
    const langFilter = document.getElementById('search-lang-filter')?.value || '';
    const nameFilter = document.getElementById('search-name-filter')?.value || '';
    const container  = document.getElementById('saved-searches-content');
    if (!container) return;

    const params = new URLSearchParams();
    if (appFilter)  params.set('app', appFilter);
    if (langFilter) params.set('language', langFilter);
    if (nameFilter) params.set('name', nameFilter);

    try {
        const resp = await fetch(`/userspace/saved_searches?${params}`, { credentials: 'include' });
        const data = await resp.json();

        if (!data.success || !data.searches.length) {
            container.innerHTML = '<p style="color:#ccc;">No saved searches yet. Run a search in Lists, Stats, or Oracle and click "Save Search".</p>';
            return;
        }

        const rows = data.searches.map(s => `
            <tr>
                <td style="color:#fff; padding:8px;">${escapeHtml(s.name)}</td>
                <td style="color:#ccc; padding:8px;">${s.app}</td>
                <td style="color:#ccc; padding:8px;">${s.language}</td>
                <td style="color:#ccc; padding:8px;">${s.created_at ? s.created_at.slice(0,10) : ''}</td>
                <td style="padding:8px;">
                    <button type="button" aria-label="Load search: ${escapeHtml(s.name)}" onclick="window.location.href='${escapeHtml(s.url)}'"
                            style="background:#228383; color:#fff; border:none; border-radius:5px; padding:5px 12px; cursor:pointer; margin-right:6px;">
                        Load
                    </button>
                    <button type="button" aria-label="Share search: ${escapeHtml(s.name)}" onclick="shareSearch('${escapeHtml(s.search_id)}')"
                            style="background:#1a5276; color:#fff; border:none; border-radius:5px; padding:5px 12px; cursor:pointer; margin-right:6px;">
                        Share
                    </button>
                    <button type="button" aria-label="Delete search: ${escapeHtml(s.name)}" onclick="deleteSavedSearch('${s.search_id}')"
                            style="background:#dc3545; color:#fff; border:none; border-radius:5px; padding:5px 12px; cursor:pointer;">
                        Delete
                    </button>
                </td>
            </tr>`).join('');

        container.innerHTML = `
            <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead>
                    <tr style="border-bottom:1px solid #444;">
                        <th scope="col" style="color:#22b3b3; padding:8px;">Name</th>
                        <th scope="col" style="color:#22b3b3; padding:8px;">App</th>
                        <th scope="col" style="color:#22b3b3; padding:8px;">Language</th>
                        <th scope="col" style="color:#22b3b3; padding:8px;">Saved</th>
                        <th scope="col" style="color:#22b3b3; padding:8px;">Actions</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>`;
    } catch (err) {
        container.innerHTML = '<p style="color:#ff6b6b;">Failed to load saved searches.</p>';
    }
}

async function shareSearch(searchId) {
    try {
        const resp = await fetch(`/userspace/get_search_share_link?search_id=${encodeURIComponent(searchId)}`, {
            credentials: 'include'
        });
        const data = await resp.json();
        if (!data.success) { alert('Could not generate share link.'); return; }

        let modal = document.getElementById('search-share-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'search-share-modal';
            modal.style.cssText = 'position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:9999; display:flex; align-items:center; justify-content:center;';
            document.body.appendChild(modal);
        }
        modal.innerHTML = `
            <div style="background:#1a2a2a; border:1px solid #22b3b3; border-radius:10px; padding:28px 32px; min-width:340px; max-width:480px; position:relative;">
                <button onclick="document.getElementById('search-share-modal').style.display='none'"
                        style="position:absolute; top:12px; right:16px; background:none; border:none; color:#ccc; font-size:1.3rem; cursor:pointer;" aria-label="Close">&#x2715;</button>
                <h5 style="color:#22b3b3; margin:0 0 16px;">Share Search</h5>
                <p style="color:#ccc; font-size:0.9rem; margin:0 0 12px;">Anyone with this link can add a copy of this search to their account.</p>
                <div style="display:flex; gap:8px; align-items:center;">
                    <input id="search-share-url" type="text" readonly value="${escapeHtml(data.share_url)}"
                           style="flex:1; padding:8px; border-radius:6px; border:1px solid #22b3b3; background:#222; color:#fff; font-size:0.85rem;" />
                    <button onclick="navigator.clipboard.writeText(document.getElementById('search-share-url').value).then(()=>{this.textContent='Copied!'; setTimeout(()=>this.textContent='Copy',1500)})"
                            style="background:#228383; color:#fff; border:none; border-radius:6px; padding:8px 14px; cursor:pointer; white-space:nowrap;">
                        Copy
                    </button>
                </div>
            </div>`;
        modal.style.display = 'flex';

        // Close on backdrop click
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = 'none'; }, { once: true });
    } catch {
        alert('Failed to generate share link. Please try again.');
    }
}

async function deleteSavedSearch(searchId) {
    if (!confirm('Delete this saved search?')) return;
    try {
        const resp = await fetch('/userspace/delete_search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ search_id: searchId })
        });
        const data = await resp.json();
        if (data.success) loadSavedSearches();
    } catch (err) {
        alert('Failed to delete search.');
    }
}

function escapeHtml(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Wire up Saved Searches tab click and filters
(function() {
    const tab = document.getElementById('saved-searches-tab');
    if (!tab) return;

    tab.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('vocabulary').style.display = 'none';
        document.getElementById('create').style.display = 'none';
        document.getElementById('saved-searches').style.display = 'block';
        document.querySelectorAll('.user-tab').forEach(t => {
            t.style.color = '#ccc';
            t.style.borderBottom = 'none';
            t.setAttribute('aria-selected', 'false');
        });
        tab.style.color = '#fff';
        tab.style.borderBottom = '3px solid #228383';
        tab.setAttribute('aria-selected', 'true');
        loadSavedSearches();
    });

    document.getElementById('search-app-filter')?.addEventListener('change', loadSavedSearches);
    document.getElementById('search-lang-filter')?.addEventListener('change', loadSavedSearches);

    let nameFilterTimer;
    document.getElementById('search-name-filter')?.addEventListener('input', () => {
        clearTimeout(nameFilterTimer);
        nameFilterTimer = setTimeout(loadSavedSearches, 300);
    });
})();
