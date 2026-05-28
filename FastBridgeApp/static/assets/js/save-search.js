/**
 * save-search.js
 * Shared logic for the "Save Search" UI on LISTS, STATS, and ORACLE result pages.
 * Determines the app from the URL prefix, checks auth, shows the UI, and POSTs to /userspace/save_search.
 */

(function () {
    const APP_MAP = { select: 'LISTS', stats: 'STATS', oracle: 'ORACLE' };

    function getAppAndLanguage() {
        const parts = window.location.pathname.split('/').filter(Boolean);
        // parts[0] = app prefix (select|stats|oracle), parts[1] = language
        const app = APP_MAP[parts[0]] || null;
        const language = parts[1] || null;
        return { app, language };
    }

    async function initSaveSearch() {
        const container = document.getElementById('save-search-container');
        if (!container) return;

        // Only show UI if user is authenticated
        try {
            const resp = await fetch('/account/protected', { credentials: 'include' });
            if (!resp.ok) return; // not logged in — leave container hidden
        } catch {
            return;
        }

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
                    body: JSON.stringify({
                        name,
                        app,
                        language,
                        url: window.location.pathname
                    })
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

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSaveSearch);
    } else {
        initSaveSearch();
    }
})();
