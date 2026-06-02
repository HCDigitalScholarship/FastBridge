/**
 * save-search.js
 * Shared logic for the "Save Search" and "My Saved Searches" UI on LISTS, STATS, and ORACLE result pages.
 */

(function () {
    const APP_MAP = { select: 'LISTS', stats: 'STATS', oracle: 'ORACLE' };

    function getAppAndLanguage() {
        const parts = window.location.pathname.split('/').filter(Boolean);
        const app = APP_MAP[parts[0]] || null;
        const language = parts[1] || null;
        return { app, language };
    }

    function isLoggedIn() {
        return document.cookie.split(';').some(c => c.trim().startsWith('session_name='));
    }

    function escSS(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function initSaveSearch() {
        const container = document.getElementById('save-search-container');
        if (!container || !isLoggedIn()) return;

        container.style.display = 'block';

        document.getElementById('save-search-btn').addEventListener('click', async () => {
            const nameInput = document.getElementById('save-search-name');
            const msgEl     = document.getElementById('save-search-message');
            const name = nameInput.value.trim();

            if (!name) {
                msgEl.textContent = 'Please enter a name.';
                return;
            }

            const { app, language } = getAppAndLanguage();
            if (!app || !language) {
                msgEl.textContent = 'Could not determine app or language from URL.';
                return;
            }

            msgEl.textContent = 'Saving…';

            try {
                const res = await fetch('/userspace/save_search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ name, app, language, url: window.location.pathname })
                });
                if (res.status === 401) {
                    msgEl.style.color = '#ffb366';
                    msgEl.textContent = 'Please sign in to save searches.';
                    return;
                }
                const data = await res.json();
                if (data.success) {
                    msgEl.style.color = '#66ffb3';
                    msgEl.textContent = `Saved as "${data.message.match(/'(.+?)'/)?.[1] || name}"`;
                    nameInput.value = '';
                    initLoadSearches(); // refresh the dropdown
                } else {
                    msgEl.style.color = '#ffb366';
                    msgEl.textContent = data.detail || 'Failed to save.';
                }
            } catch {
                msgEl.style.color = '#ff6b6b';
                msgEl.textContent = 'Network error — please try again.';
            }
        });
    }

    async function initLoadSearches() {
        const container = document.getElementById('load-search-container');
        if (!container || !isLoggedIn()) return;

        const { app, language } = getAppAndLanguage();
        if (!app || !language) return;

        try {
            const params = new URLSearchParams({ app, language });
            const resp = await fetch(`/userspace/saved_searches?${params}`, { credentials: 'include' });
            if (!resp.ok) return;
            const data = await resp.json();

            if (!data.success || !data.searches.length) {
                container.innerHTML = '';
                return;
            }

            const items = data.searches.map(s =>
                `<a href="${escSS(s.url)}"
                    style="display:block; padding:7px 14px; color:#fff; text-decoration:none; border-bottom:1px solid #333; font-size:0.9rem;"
                    onmouseover="this.style.background='#2a4a4a'" onmouseout="this.style.background=''">${escSS(s.name)}</a>`
            ).join('');

            container.innerHTML = `
                <div style="position:relative; display:inline-block; margin-bottom:12px;">
                    <button type="button" id="load-search-toggle"
                            style="background:#1a3333; color:#22b3b3; border:1px solid #22b3b3; border-radius:6px; padding:6px 14px; cursor:pointer; font-size:0.9rem;">
                        My Saved Searches &#9660;
                    </button>
                    <div id="load-search-dropdown"
                         style="display:none; position:absolute; top:100%; left:0; min-width:220px; background:#1a2a2a; border:1px solid #22b3b3; border-radius:6px; z-index:100; max-height:260px; overflow-y:auto; box-shadow:0 4px 12px rgba(0,0,0,0.4);">
                        ${items}
                    </div>
                </div>`;

            document.getElementById('load-search-toggle').addEventListener('click', (e) => {
                e.stopPropagation();
                const dd = document.getElementById('load-search-dropdown');
                dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
            });

            document.addEventListener('click', function closeDD() {
                const dd = document.getElementById('load-search-dropdown');
                if (dd) dd.style.display = 'none';
            });
        } catch {
            // silent fail — load searches is a nice-to-have
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { initSaveSearch(); initLoadSearches(); });
    } else {
        initSaveSearch();
        initLoadSearches();
    }
})();
