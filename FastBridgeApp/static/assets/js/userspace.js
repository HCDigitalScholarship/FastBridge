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
                        <button class='vocab-list-btn' data-lang='${lang}' data-list='${listName}' aria-label='View vocabulary list: ${listName} (${wordCountNum} words)' aria-expanded='false' style='background:#222; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(34,179,179,0.10); font-weight:500; transition:background 0.2s, color 0.2s; border:none;'>${listName}${wordCount}</button>
                        <button class='add-word-btn' data-lang='${lang}' data-list='${listName}' aria-label='Add new words to ${listName} list' style='background:#228383; color:#fff; border-radius:8px; padding:10px 14px; margin-left:4px; cursor:pointer; font-weight:500; border:none;'><i class='fas fa-plus' aria-hidden='true'></i> Add New Word</button>
                    `;
                });
                html += `</div>
                    <div class='vocab-list-details-area' style='width:100%; margin-top:10px;'></div>
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
                            <button class='shared-list-btn' data-lang='${lang}' data-list='${listName}' aria-label='View shared vocabulary list: ${listName} (${wordCountNum} words)' aria-expanded='false' style='background:#333; color:#fff; border-radius:8px; padding:10px 18px; cursor:pointer; box-shadow:0 1px 6px rgba(255,179,102,0.10); font-weight:500; transition:background 0.2s, color 0.2s; border:none;'>${listName}${wordCount}</button>
                        `;
                    });
                    html += `</div>
                        <div class='shared-list-details-area' style='width:100%; margin-top:10px;'></div>
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
                attachVocabListEvents();
                attachSharedListEvents();
                attachPaginationEvents(route, contentDiv);
            }, 0);
        }
        contentDiv.innerHTML = html;
    } catch {
        contentDiv.innerHTML = '<p style="color:#fff;">Error loading data.</p>';
    }
}

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

            // Function to load words with pagination
            const loadWordDetails = async (page = 1, limit = 20) => {
                detailsArea.innerHTML = '<p style="color:#fff;">Loading...</p>';
                try {
                    const resp = await fetch(`/userspace/list_details?language=${encodeURIComponent(lang)}&list_name=${encodeURIComponent(list)}&page=${page}&limit=${limit}`);
                    const response = await resp.json();

                    // Handle both old format (direct words) and new format (with pagination)
                    const data = response.words || response;
                    const pagination = response.pagination || null;

                    // Track retained and deleted words
                    let retainedWords = Object.entries(data).map(([word, info]) => info);
                    let deletedWords = [];

                    // Add pagination controls at top if available
                    let paginationHtml = '';
                    if (pagination && pagination.total_pages > 1) {
                        const p = pagination;
                        paginationHtml = `<div style="margin-bottom:16px; display:flex; align-items:center; justify-content:center; gap:8px; color:#fff; flex-wrap:wrap;">
                            <span>Showing ${Object.keys(data).length} of ${p.total_words} words (Page ${p.current_page} of ${p.total_pages})</span>
                            <select id="words-per-page" style="padding:4px 8px; border-radius:4px; border:1px solid #22b3b3; background:#222; color:#fff; margin:0 8px;">
                                <option value="10" ${p.limit === 10 ? 'selected' : ''}>10 per page</option>
                                <option value="20" ${p.limit === 20 ? 'selected' : ''}>20 per page</option>
                                <option value="50" ${p.limit === 50 ? 'selected' : ''}>50 per page</option>
                                <option value="100" ${p.limit === 100 ? 'selected' : ''}>100 per page</option>
                            </select>
                            <div style="display:flex; gap:4px; flex-wrap:wrap;">`;

                        // Previous button
                        if (p.has_prev) {
                            paginationHtml += `<button class="word-page-btn" data-page="${p.current_page - 1}" style="background:#228383; color:#fff; border:none; border-radius:4px; padding:6px 12px; cursor:pointer; font-size:0.9rem;">Previous</button>`;
                        }

                        // Page numbers (show up to 5 pages around current)
                        const startPage = Math.max(1, p.current_page - 2);
                        const endPage = Math.min(p.total_pages, p.current_page + 2);

                        for (let i = startPage; i <= endPage; i++) {
                            const isActive = i === p.current_page;
                            paginationHtml += `<button class="word-page-btn" data-page="${i}" aria-label="Go to page ${i}" aria-current="${isActive ? 'page' : 'false'}" ${isActive ? 'disabled' : ''} style="background:${isActive ? '#22b3b3' : '#444'}; color:#fff; border:none; border-radius:4px; padding:6px 10px; cursor:pointer; font-size:0.9rem; font-weight:${isActive ? '600' : '400'};">${i}</button>`;
                        }

                        // Next button
                        if (p.has_next) {
                            paginationHtml += `<button class="word-page-btn" data-page="${p.current_page + 1}" aria-label="Go to next page" style="background:#228383; color:#fff; border:none; border-radius:4px; padding:6px 12px; cursor:pointer; font-size:0.9rem;">Next</button>`;
                        }

                        paginationHtml += `</div></div>`;
                    }

                    // Display flash cards
                    let cardsHtml = paginationHtml + '<div id="flashcard-list" style="display:flex; flex-wrap:wrap; gap:16px;">';
                    Object.entries(data).forEach(([word, info]) => {
                    const simpleLemma = info['SIMPLE LEMMA'];
                    cardsHtml += `<div class='flashcard' data-word='${simpleLemma}' style='background:#222; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(34,179,179,0.15); padding:18px 22px; min-width:180px; max-width:320px; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative; word-break:break-word; overflow-wrap:break-word;'>`;
                    cardsHtml += `<div style='font-size:1.2rem; font-weight:700; color:#22b3b3; margin-bottom:8px;'>${word}</div>`;
                    Object.entries(info).forEach(([key, val]) => {
                        cardsHtml += `<div style='margin-bottom:4px;'><span style='font-weight:600; color:#ffb366;'>${key}:</span> <span style='color:#fff;'>${val}</span></div>`;
                    });
                    cardsHtml += `<button class='delete-flashcard-btn' data-word='${simpleLemma}' aria-label='Delete word ${word} from list' style='position:absolute; top:10px; right:10px; background:#ff6666; color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:0.95rem; font-weight:600; cursor:pointer;'><i class='fas fa-trash' aria-hidden='true'></i><span class='sr-only'>Delete</span></button>`;
                    cardsHtml += `</div>`;
                });
                cardsHtml += '</div>';
                // Deleted words summary and Save Changes button (initially hidden)
                cardsHtml += `<div id='deleted-words-summary' style='margin-top:18px;'></div>`;
                cardsHtml += `<div role='group' aria-label='List actions' style='display:flex; gap:12px; align-items:center; margin-top:12px; flex-wrap:wrap;'>`;
                cardsHtml += `<button id='share-list-btn' aria-label='Share ${list} list with others' style='background:#22b3b3; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(34,179,179,0.15); transition:background 0.2s;'><i class='fas fa-share-alt' aria-hidden='true'></i> Share List</button>`;
                cardsHtml += `<button id='manage-permissions-btn' aria-label='Manage permissions for ${list} list' style='background:#ffb366; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(255,179,102,0.15); transition:background 0.2s;'><i class='fas fa-user-shield' aria-hidden='true'></i> Manage Permissions</button>`;
                cardsHtml += `<button id='save-changes-btn' aria-label='Save changes to ${list} list' style='background:#228383; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(34,179,179,0.15); transition:background 0.2s; display:none;'><i class='fas fa-save' aria-hidden='true'></i> Save Changes</button>`;
                cardsHtml += `<button id='delete-list-btn' aria-label='Delete entire ${list} list' style='background:#ff6666; color:#fff; padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 2px 8px rgba(255,102,102,0.15); transition:background 0.2s;'><i class='fas fa-trash-alt' aria-hidden='true'></i> Delete Entire List</button>`;
                cardsHtml += `</div>`;
                detailsArea.innerHTML = cardsHtml;

                // Add word pagination event listeners
                const wordPageButtons = detailsArea.querySelectorAll('.word-page-btn');
                wordPageButtons.forEach(btn => {
                    btn.addEventListener('click', () => {
                        const newPage = parseInt(btn.getAttribute('data-page'));
                        const currentLimit = parseInt(detailsArea.querySelector('#words-per-page')?.value || (pagination ? pagination.limit : 20));
                        loadWordDetails(newPage, currentLimit);
                    });
                });

                const wordsPerPageSelect = detailsArea.querySelector('#words-per-page');
                if (wordsPerPageSelect) {
                    wordsPerPageSelect.addEventListener('change', () => {
                        const newLimit = parseInt(wordsPerPageSelect.value);
                        loadWordDetails(1, newLimit); // Reset to page 1 when changing limit
                    });
                }

                const shareListBtn = detailsArea.querySelector('#share-list-btn');
                shareListBtn.addEventListener('click', () => {
                    // Show modal for share options
                    let modal = document.createElement('div');
                    modal.className = 'share-list-modal';
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
                        <div role='dialog' aria-modal='true' aria-labelledby='share-modal-title' style='background:#222; color:#fff; border-radius:12px; padding:32px 36px; min-width:340px; max-width:460px; box-shadow:0 2px 16px rgba(34,179,179,0.18); position:relative;'>
                            <h3 id='share-modal-title' style='color:#22b3b3; margin-bottom:18px;'>Share List: <span style='color:#ffb366;'>${list}</span> (${lang})</h3>
                            <div style='margin-bottom:18px;'>
                                <label style='font-weight:600; color:#fff;'>Choose sharing mode:</label><br>
                                <input type='radio' name='share-mode' id='share-copy' value='copy' checked> <label for='share-copy' style='color:#22b3b3;'>Copy Share (makes a copy for new users)</label><br>
                                <input type='radio' name='share-mode' id='share-editable' value='editable'> <label for='share-editable' style='color:#22b3b3;'>Linked Share (shared reference with permissions)</label>
                            </div>
                            <div id='permission-select-div' style='margin-bottom:18px; display:none;'>
                                <label for='share-permission' style='font-weight:600; color:#fff;'>Default Permission for Linked Share:</label><br>
                                <select id='share-permission' aria-label='Default permission level for linked share' style='width:100%; padding:8px; border-radius:4px; border:1px solid #22b3b3; background:#222; color:#fff; margin-top:6px;'>
                                    <option value='view'>View Only (see words)</option>
                                    <option value='edit' selected>Edit (view + add words)</option>
                                    <option value='admin'>Admin (edit + delete + manage permissions)</option>
                                </select>
                                <small style='color:#aaa; display:block; margin-top:4px;'>You can change individual permissions later</small>
                            </div>
                            <div id='share-list-message' role='status' aria-live='polite' style='color:#ffb366; margin-bottom:10px;'></div>
                            <div style='display:flex; gap:12px; justify-content:flex-end;'>
                                <button id='share-list-confirm-btn' aria-label='Generate share link for this list' style='background:#22b3b3; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>Get Share Link</button>
                                <button id='share-list-cancel-btn' aria-label='Cancel and close share dialog' style='background:#ff6666; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>Cancel</button>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(modal);
                    const confirmBtn = modal.querySelector('#share-list-confirm-btn');
                    const cancelBtn = modal.querySelector('#share-list-cancel-btn');
                    const messageDiv = modal.querySelector('#share-list-message');

                    // Show/hide permission selector based on mode
                    const permissionDiv = modal.querySelector('#permission-select-div');
                    modal.querySelectorAll('input[name="share-mode"]').forEach(radio => {
                        radio.addEventListener('change', () => {
                            if (radio.value === 'editable') {
                                permissionDiv.style.display = 'block';
                            } else {
                                permissionDiv.style.display = 'none';
                            }
                        });
                    });

                    confirmBtn.addEventListener('click', async () => {
                        const mode = modal.querySelector('input[name="share-mode"]:checked').value;
                        // Only linked shares carry a permission level; copy shares ignore it.
                        const permission = mode === 'editable'
                            ? modal.querySelector('#share-permission').value
                            : undefined;
                        confirmBtn.textContent = 'Generating...';
                        confirmBtn.disabled = true;
                        try {
                            const resp = await fetch('/userspace/get_share_id', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    list_name: list,
                                    sharing_mode: mode,
                                    language: lang,
                                    permission: permission
                                })
                            });
                            const data = await resp.json();
                            if (data.success && data.share_url) {
                                messageDiv.innerHTML = `<span style='color:#22b3b3;'>Share Link:</span> <input type='text' value='${data.share_url}' style='width:70%; padding:6px; border-radius:6px; border:none; background:#333; color:#fff; font-size:1rem;' readonly> <button id='copy-share-link-btn' style='background:#228383; color:#fff; border:none; border-radius:6px; padding:6px 12px; font-size:0.95rem; font-weight:600; cursor:pointer;'>Copy</button>`;
                                const copyBtn = messageDiv.querySelector('#copy-share-link-btn');
                                copyBtn.addEventListener('click', () => {
                                    navigator.clipboard.writeText(data.share_url).then(() => {
                                        copyBtn.textContent = 'Copied!';
                                        setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1200);
                                    });
                                });
                                confirmBtn.style.display = 'none';
                            } else {
                                messageDiv.textContent = 'Error generating share link.';
                                confirmBtn.disabled = false;
                                confirmBtn.textContent = 'Get Share Link';
                            }
                        } catch {
                            messageDiv.textContent = 'Error generating share link.';
                            confirmBtn.disabled = false;
                            confirmBtn.textContent = 'Get Share Link';
                        }
                    });
                    cancelBtn.addEventListener('click', () => {
                        document.body.removeChild(modal);
                    });
                });

                // Manage Permissions button logic
                const managePermissionsBtn = detailsArea.querySelector('#manage-permissions-btn');
                if (managePermissionsBtn) {
                    managePermissionsBtn.addEventListener('click', () => {
                        // Redirect to settings page with sharing tab
                        window.location.href = '/account/settings#sharing';
                    });
                }

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
                } catch (error) {
                    console.error('Error loading word details:', error);
                    detailsArea.innerHTML = '<p style="color:#fff;">Error loading word details.</p>';
                }
            };

            // Initial load of first page
            await loadWordDetails(1, 20);
        });
    });
}

function attachSharedListEvents() {
    document.querySelectorAll('.shared-list-btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.background = '#ffb366';
            btn.style.color = '#222';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.background = '#333';
            btn.style.color = '#fff';
        });
        btn.addEventListener('click', async () => {
            const lang = btn.getAttribute('data-lang');
            const list = btn.getAttribute('data-list');
            // Highlight active button
            document.querySelectorAll('.shared-list-btn').forEach(b => {
                b.style.background = '#333';
                b.style.color = '#fff';
            });
            btn.style.background = '#ffb366';
            btn.style.color = '#222';
            // Find details area
            const detailsArea = btn.closest('div').parentNode.querySelector('.shared-list-details-area');
            // Hide details in all details areas for this language
            btn.closest('div').parentNode.querySelectorAll('.shared-list-details-area').forEach(area => {
                area.innerHTML = '';
            });
            detailsArea.innerHTML = '<p style="color:#fff;">Loading...</p>';
            try {
                const resp = await fetch(`/userspace/list_details?language=${encodeURIComponent(lang)}&list_name=${encodeURIComponent(list)}&shared=true`);
                const response = await resp.json();

                // Extract data (words, pagination, permission info)
                const { words, pagination, permission, is_owner } = response;
                const data = words || response; // Backwards compatibility

                // Permission level check
                const permissionLevel = permission || 'edit'; // Default to edit for backwards compatibility
                const canEdit = ['edit', 'admin'].includes(permissionLevel);
                const canDelete = permissionLevel === 'admin'; // Only admin can delete
                const canManagePermissions = permissionLevel === 'admin'; // Only admin can manage permissions

                // Display flash cards with permission-based controls
                let cardsHtml = '<div id="flashcard-list" style="display:flex; flex-wrap:wrap; gap:16px;">';
                Object.entries(data).forEach(([word, info]) => {
                    if (word !== 'pagination' && word !== 'permission' && word !== 'is_owner') {
                        cardsHtml += `<div class='flashcard' data-word='${info['SIMPLE LEMMA']}' style='background:#333; color:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(255,179,102,0.15); padding:18px 22px; min-width:180px; max-width:320px; margin-bottom:10px; display:flex; flex-direction:column; align-items:flex-start; position:relative; word-break:break-word; overflow-wrap:break-word;'>`;
                        cardsHtml += `<div style='font-size:1.2rem; font-weight:700; color:#ffb366; margin-bottom:8px;'>${word}</div>`;
                        Object.entries(info).forEach(([key, val]) => {
                            cardsHtml += `<div style='margin-bottom:4px;'><span style='font-weight:600; color:#22b3b3;'>${key}:</span> <span style='color:#fff;'>${val}</span></div>`;
                        });

                        // Add delete button for admin users
                        if (canDelete) {
                            cardsHtml += `<button class='delete-shared-word-btn' data-word='${info['SIMPLE LEMMA']}' style='position:absolute; top:10px; right:10px; background:#ff6666; color:#fff; border:none; border-radius:6px; padding:4px 10px; font-size:0.95rem; font-weight:600; cursor:pointer;'>Delete</button>`;
                        }

                        cardsHtml += `</div>`;
                    }
                });
                cardsHtml += '</div>';

                // Permission indicator and action buttons
                const permissionColor = permissionLevel === 'admin' ? '#22b3b3' : permissionLevel === 'edit' ? '#ffb366' : '#ccc';
                const permissionIcon = permissionLevel === 'admin' ? '👑' : permissionLevel === 'edit' ? '✏️' : '👁️';

                cardsHtml += `<div style='margin-top:16px; padding:12px; background:#444; border-radius:6px;'>`;
                cardsHtml += `<span style='color:${permissionColor}; font-weight:600; font-size:1rem;'>${permissionIcon} Your Permission: ${permissionLevel.toUpperCase()}</span>`;

                if (canEdit) {
                    cardsHtml += `<button class='add-word-btn' data-lang='${lang}' data-list='${list}' data-shared='true' style='background:#228383; color:#fff; border-radius:6px; padding:8px 16px; margin-left:12px; cursor:pointer; font-weight:500; border:none;'>+ Add New Word</button>`;
                }

                if (canManagePermissions) {
                    cardsHtml += `<button class='manage-permissions-shared-btn' data-lang='${lang}' data-list='${list}' style='background:#ffb366; color:#fff; border-radius:6px; padding:8px 16px; margin-left:12px; cursor:pointer; font-weight:500; border:none;'>Manage Permissions</button>`;
                }

                cardsHtml += `<button class='unlink-shared-btn' data-lang='${lang}' data-list='${list}' style='background:#ff6666; color:#fff; border-radius:6px; padding:8px 16px; margin-left:12px; cursor:pointer; font-weight:500; border:none;'>Unlink List</button>`;
                cardsHtml += `</div>`;

                detailsArea.innerHTML = cardsHtml;

                // Attach Add New Word modal logic for shared lists
                const addWordBtn = detailsArea.querySelector('.add-word-btn');
                if (addWordBtn) {
                    addWordBtn.addEventListener('click', () => {
                        showWordSelectModal({
                            lang,
                            list,
                            title: 'Add New Word to Shared List',
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
                                            words: selected,
                                            shared: true
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
                }

                // Attach Unlink button logic for shared lists
                const unlinkBtn = detailsArea.querySelector('.unlink-shared-btn');
                if (unlinkBtn) {
                    unlinkBtn.addEventListener('click', async () => {
                        if (!confirm(`Are you sure you want to unlink "${list}"? You will lose access to this shared list.`)) {
                            return;
                        }

                        try {
                            // Get owner_id from shared_with_me by fetching shared lists
                            const sharedResp = await fetch('/userspace/permissions/shared-with-me', {
                                credentials: 'include'
                            });
                            const sharedData = await sharedResp.json();

                            // Find the owner_id for this list
                            let ownerId = null;
                            if (sharedData.success) {
                                const matchingList = sharedData.shared_lists.find(
                                    sl => sl.list_name === list && sl.language === lang
                                );
                                if (matchingList) {
                                    ownerId = matchingList.owner_id;
                                }
                            }

                            if (!ownerId) {
                                alert('Could not find owner information for this list.');
                                return;
                            }

                            // Unlink the list
                            const resp = await fetch('/userspace/permissions/unlink', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                credentials: 'include',
                                body: JSON.stringify({
                                    list_name: list,
                                    language: lang,
                                    owner_id: ownerId
                                })
                            });

                            const data = await resp.json();
                            if (data.success) {
                                alert('List unlinked successfully. Refreshing page...');
                                window.location.reload();
                            } else {
                                alert('Failed to unlink list');
                            }
                        } catch (err) {
                            alert('Failed to unlink list');
                            console.error(err);
                        }
                    });
                }

                // Attach Delete word button listeners for admin users
                const deleteWordBtns = detailsArea.querySelectorAll('.delete-shared-word-btn');
                if (deleteWordBtns.length > 0) {
                    deleteWordBtns.forEach(btn => {
                        btn.addEventListener('click', async () => {
                            const wordToDelete = btn.getAttribute('data-word');
                            if (!confirm(`Are you sure you want to delete "${wordToDelete}" from this shared list?`)) {
                                return;
                            }

                            try {
                                // Get owner_id first
                                const sharedResp = await fetch('/userspace/permissions/shared-with-me', {
                                    credentials: 'include'
                                });
                                const sharedData = await sharedResp.json();

                                let ownerId = null;
                                if (sharedData.success) {
                                    const matchingList = sharedData.shared_lists.find(
                                        sl => sl.list_name === list && sl.language === lang
                                    );
                                    if (matchingList) {
                                        ownerId = matchingList.owner_id;
                                    }
                                }

                                if (!ownerId) {
                                    alert('Could not find owner information for this list.');
                                    return;
                                }

                                // Delete the word
                                const resp = await fetch('/userspace/delete_words', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    credentials: 'include',
                                    body: JSON.stringify({
                                        list_name: list,
                                        language: lang,
                                        words_to_delete: [wordToDelete],
                                        owner_id: ownerId
                                    })
                                });

                                const data = await resp.json();
                                if (data.success) {
                                    alert('Word deleted successfully. Refreshing...');
                                    window.location.reload();
                                } else {
                                    alert('Failed to delete word: ' + (data.message || 'Unknown error'));
                                }
                            } catch (err) {
                                alert('Failed to delete word');
                                console.error(err);
                            }
                        });
                    });
                }

                // Attach Manage Permissions button listener for admin users
                const managePermsBtn = detailsArea.querySelector('.manage-permissions-shared-btn');
                if (managePermsBtn) {
                    managePermsBtn.addEventListener('click', async () => {
                        // Get owner_id first
                        try {
                            const sharedResp = await fetch('/userspace/permissions/shared-with-me', {
                                credentials: 'include'
                            });
                            const sharedData = await sharedResp.json();

                            let ownerId = null;
                            if (sharedData.success) {
                                const matchingList = sharedData.shared_lists.find(
                                    sl => sl.list_name === list && sl.language === lang
                                );
                                if (matchingList) {
                                    ownerId = matchingList.owner_id;
                                }
                            }

                            if (!ownerId) {
                                alert('Could not find owner information for this list.');
                                return;
                            }

                            // Redirect to user settings with the list info
                            window.location.href = `/account/settings#sharing?list=${encodeURIComponent(list)}&lang=${encodeURIComponent(lang)}&owner=${encodeURIComponent(ownerId)}`;
                        } catch (err) {
                            alert('Failed to open permissions management');
                            console.error(err);
                        }
                    });
                }
            } catch {
                detailsArea.innerHTML = '<p style="color:#fff;">Error loading details.</p>';
            }
        });
    });
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

// Add filter event listeners for vocabulary list pagination
document.addEventListener('DOMContentLoaded', () => {
    const languageFilter = document.getElementById('vocab-language-filter');
    const pageLimitSelect = document.getElementById('vocab-page-limit');

    if (languageFilter) {
        languageFilter.addEventListener('change', () => {
            updateVocabWithFilters();
        });
    }

    if (pageLimitSelect) {
        pageLimitSelect.addEventListener('change', () => {
            updateVocabWithFilters();
        });
    }
});

function updateVocabWithFilters() {
    const languageFilter = document.getElementById('vocab-language-filter');
    const pageLimitSelect = document.getElementById('vocab-page-limit');
    const vocabContent = document.getElementById('vocabulary-content');

    if (!languageFilter || !pageLimitSelect || !vocabContent) return;

    const params = new URLSearchParams({
        page: '1',
        limit: pageLimitSelect.value,
    });

    if (languageFilter.value) {
        params.set('language_filter', languageFilter.value);
    }

    const route = `/userspace/vocab?${params.toString()}`;
    fetchTabData(route, vocabContent);
}

function attachPaginationEvents(currentRoute, contentDiv) {
    document.querySelectorAll('.pagination-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const page = btn.getAttribute('data-page');

            // Parse current route to preserve filters
            const url = new URL(currentRoute, window.location.origin);
            url.searchParams.set('page', page);

            // If no filters in current route, check UI for current filter values
            if (!url.searchParams.has('language_filter') && !url.searchParams.has('limit')) {
                const languageFilter = document.getElementById('vocab-language-filter');
                const pageLimitSelect = document.getElementById('vocab-page-limit');

                if (languageFilter && languageFilter.value) {
                    url.searchParams.set('language_filter', languageFilter.value);
                }

                if (pageLimitSelect) {
                    url.searchParams.set('limit', pageLimitSelect.value);
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
