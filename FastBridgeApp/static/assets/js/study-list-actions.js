// Study-page list actions: Add Word, Delete selected words, Share, Manage
// Permissions, Delete List. These moved off the userspace inline panel onto the
// dedicated list page. Selection state (selectedLemmas) comes from
// select-result.js, which is loaded before this file.

(function () {
  var S = window.STUDY_LIST || {};

  function debounce(fn, delay) {
    var t;
    return function () {
      var ctx = this, args = arguments;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(ctx, args); }, delay);
    };
  }

  // Word-search modal used by "Add Word" (ported from userspace.js).
  function showWordSelectModal(opts) {
    var lang = opts.lang, onSave = opts.onSave;
    var saveLabel = opts.saveLabel || 'Save', cancelLabel = opts.cancelLabel || 'Cancel';
    var title = opts.title || 'Add Words', list = opts.list;

    var modal = document.createElement('div');
    modal.className = 'word-select-modal';
    modal.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.6); z-index:9999; display:flex; align-items:center; justify-content:center;';
    modal.innerHTML =
      "<div role='dialog' aria-modal='true' aria-labelledby='word-select-title' style='background:#222; color:#fff; border-radius:12px; padding:32px 36px; min-width:340px; max-width:520px; box-shadow:0 2px 16px rgba(34,179,179,0.18); position:relative;'>" +
      "<h3 id='word-select-title' style='color:#22b3b3; margin-bottom:18px;'>" + title + (list ? " <span style='color:#ffb366;'>" + list + "</span>" : "") + " (" + lang + ")</h3>" +
      "<input id='word-select-search' type='text' placeholder='Search for a word...' aria-label='Search for words to add' style='width:100%; padding:8px 12px; border-radius:6px; border:none; margin-bottom:12px; font-size:1rem;'>" +
      "<div id='word-select-table-container' style='max-height:220px; overflow-y:auto; margin-bottom:12px;'></div>" +
      "<div id='word-select-message' role='status' aria-live='polite' style='color:#ffb366; margin-bottom:10px;'></div>" +
      "<div style='display:flex; gap:12px; justify-content:flex-end;'>" +
      "<button id='word-select-save-btn' style='background:#22b3b3; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>" + saveLabel + "</button>" +
      "<button id='word-select-cancel-btn' style='background:#ff6666; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>" + cancelLabel + "</button>" +
      "</div></div>";
    document.body.appendChild(modal);

    var selected = [];
    var searchInput = modal.querySelector('#word-select-search');
    var tableContainer = modal.querySelector('#word-select-table-container');
    var messageDiv = modal.querySelector('#word-select-message');
    var saveBtn = modal.querySelector('#word-select-save-btn');
    var cancelBtn = modal.querySelector('#word-select-cancel-btn');

    function renderTable(wordsArr) {
      var html = "<table style='width:100%; border-collapse:collapse;'><thead><tr><th style='color:#22b3b3; padding:6px;'>Word</th><th style='color:#22b3b3; padding:6px;'>Definition</th><th></th></tr></thead><tbody>";
      wordsArr.forEach(function (wordArr, idx) {
        var checked = selected.some(function (w) { return w[0] === wordArr[0] && w[1] === wordArr[1]; });
        html += "<tr><td style='padding:6px;'>" + wordArr[0] + "</td><td style='padding:6px;'>" + wordArr[1] + "</td><td style='padding:6px;'><input type='checkbox' class='word-select-checkbox' data-idx='" + idx + "' " + (checked ? 'checked' : '') + "></td></tr>";
      });
      html += "</tbody></table>";
      tableContainer.innerHTML = html;
    }

    searchInput.addEventListener('input', debounce(async function () {
      var query = searchInput.value.trim();
      if (!query) { tableContainer.innerHTML = ''; return; }
      messageDiv.textContent = 'Searching...';
      try {
        var resp = await fetch('/userspace/words?language=' + lang + '&query=' + encodeURIComponent(query));
        var data = await resp.json();
        renderTable(data.words || []);
        messageDiv.textContent = '';
      } catch (e) { messageDiv.textContent = 'Error searching words.'; }
    }, 500));

    tableContainer.addEventListener('change', function (e) {
      if (!e.target.classList.contains('word-select-checkbox')) return;
      var idx = e.target.getAttribute('data-idx');
      var row = tableContainer.querySelectorAll('tbody tr')[idx];
      var word = row.children[0].textContent, def = row.children[1].textContent;
      if (e.target.checked) {
        if (!selected.some(function (w) { return w[0] === word && w[1] === def; })) selected.push([word, def]);
      } else {
        selected = selected.filter(function (w) { return !(w[0] === word && w[1] === def); });
      }
    });

    saveBtn.addEventListener('click', async function () {
      if (selected.length === 0) { messageDiv.textContent = 'Please select at least one word.'; return; }
      await onSave(selected, { modal: modal, messageDiv: messageDiv, saveBtn: saveBtn });
    });
    cancelBtn.addEventListener('click', function () { document.body.removeChild(modal); });
  }

  // --- Add Word ---
  var addBtn = document.getElementById('add-word-btn');
  if (addBtn) {
    addBtn.addEventListener('click', function () {
      showWordSelectModal({
        lang: S.language, list: S.listName, title: 'Add New Word to',
        onSave: async function (selected, ctx) {
          ctx.saveBtn.textContent = 'Saving...';
          ctx.saveBtn.disabled = true;
          try {
            var resp = await fetch('/userspace/add_words', {
              method: 'POST', headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ list_name: S.listName, language: S.language, words: selected, shared: S.shared })
            });
            var data = await resp.json();
            if (data.success) {
              ctx.messageDiv.textContent = 'Words added!';
              setTimeout(function () { window.location.reload(); }, 1000);
            } else {
              ctx.messageDiv.textContent = 'Error adding words.';
              ctx.saveBtn.disabled = false; ctx.saveBtn.textContent = 'Save';
            }
          } catch (e) {
            ctx.messageDiv.textContent = 'Error adding words.';
            ctx.saveBtn.disabled = false; ctx.saveBtn.textContent = 'Save';
          }
        }
      });
    });
  }

  // --- Delete selected words (uses selectedLemmas from select-result.js) ---
  var delSelBtn = document.getElementById('delete-selected-btn');
  if (delSelBtn) {
    delSelBtn.addEventListener('click', async function () {
      var lemmas = (typeof selectedLemmas !== 'undefined') ? Array.from(selectedLemmas) : [];
      if (lemmas.length === 0) return;
      if (!confirm('Delete ' + lemmas.length + ' selected word(s) from this list? This cannot be undone.')) return;
      delSelBtn.disabled = true;
      var original = delSelBtn.innerHTML;
      delSelBtn.textContent = 'Deleting...';
      try {
        var resp = await fetch('/userspace/delete_words', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ list_name: S.listName, language: S.language, words_to_delete: lemmas, owner_id: S.ownerId })
        });
        var data = await resp.json();
        if (data.success || resp.ok) {
          window.location.reload();
        } else {
          delSelBtn.disabled = false; delSelBtn.innerHTML = original;
          alert('Error deleting words.');
        }
      } catch (e) {
        delSelBtn.disabled = false; delSelBtn.innerHTML = original;
        alert('Error deleting words.');
      }
    });
  }

  // --- Manage Permissions (redirect to settings) ---
  var permBtn = document.getElementById('manage-permissions-btn');
  if (permBtn) {
    permBtn.addEventListener('click', function () { window.location.href = '/account/settings#sharing'; });
  }

  // --- Delete Entire List ---
  var delListBtn = document.getElementById('delete-list-btn');
  if (delListBtn) {
    delListBtn.addEventListener('click', async function () {
      if (!confirm('Delete the entire list "' + S.listName + '"? This cannot be undone.')) return;
      delListBtn.disabled = true;
      delListBtn.textContent = 'Deleting...';
      try {
        var resp = await fetch('/userspace/delete_list', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ list_name: S.listName, language: S.language })
        });
        var data = await resp.json();
        if (data.success) {
          window.location.href = '/userspace';
        } else {
          delListBtn.disabled = false;
          delListBtn.innerHTML = "<i class='fas fa-trash-alt'></i> Delete List";
          alert('Error deleting list.');
        }
      } catch (e) {
        delListBtn.disabled = false;
        delListBtn.innerHTML = "<i class='fas fa-trash-alt'></i> Delete List";
        alert('Error deleting list.');
      }
    });
  }

  // --- Share List (ported from userspace.js) ---
  var shareBtn = document.getElementById('share-list-btn');
  if (shareBtn) {
    shareBtn.addEventListener('click', function () {
      var modal = document.createElement('div');
      modal.className = 'share-list-modal';
      modal.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.6); z-index:9999; display:flex; align-items:center; justify-content:center;';
      modal.innerHTML =
        "<div role='dialog' aria-modal='true' aria-labelledby='share-modal-title' style='background:#222; color:#fff; border-radius:12px; padding:32px 36px; min-width:340px; max-width:460px; box-shadow:0 2px 16px rgba(34,179,179,0.18);'>" +
        "<h3 id='share-modal-title' style='color:#22b3b3; margin-bottom:18px;'>Share List: <span style='color:#ffb366;'>" + S.listName + "</span> (" + S.language + ")</h3>" +
        "<div style='margin-bottom:18px;'><label style='font-weight:600; color:#fff;'>Choose sharing mode:</label><br>" +
        "<input type='radio' name='share-mode' id='share-copy' value='copy' checked> <label for='share-copy' style='color:#22b3b3;'>Copy Share (makes a copy for new users)</label><br>" +
        "<input type='radio' name='share-mode' id='share-editable' value='editable'> <label for='share-editable' style='color:#22b3b3;'>Linked Share (shared reference with permissions)</label></div>" +
        "<div id='permission-select-div' style='margin-bottom:18px; display:none;'>" +
        "<label for='share-permission' style='font-weight:600; color:#fff;'>Default Permission for Linked Share:</label><br>" +
        "<select id='share-permission' style='width:100%; padding:8px; border-radius:4px; border:1px solid #22b3b3; background:#222; color:#fff; margin-top:6px;'>" +
        "<option value='view'>View only (see words)</option><option value='edit' selected>Edit (view + add words)</option><option value='admin'>Admin (edit + remove words + manage access)</option></select></div>" +
        "<div id='share-list-message' role='status' aria-live='polite' style='color:#ffb366; margin-bottom:10px;'></div>" +
        "<div style='display:flex; gap:12px; justify-content:flex-end;'>" +
        "<button id='share-list-confirm-btn' style='background:#22b3b3; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>Get Share Link</button>" +
        "<button id='share-list-cancel-btn' style='background:#ff6666; color:#fff; border:none; border-radius:6px; padding:8px 18px; font-size:1rem; font-weight:600; cursor:pointer;'>Cancel</button>" +
        "</div></div>";
      document.body.appendChild(modal);

      var confirmBtn = modal.querySelector('#share-list-confirm-btn');
      var cancelBtn = modal.querySelector('#share-list-cancel-btn');
      var messageDiv = modal.querySelector('#share-list-message');
      var permissionDiv = modal.querySelector('#permission-select-div');

      modal.querySelectorAll('input[name="share-mode"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
          permissionDiv.style.display = radio.value === 'editable' ? 'block' : 'none';
        });
      });

      confirmBtn.addEventListener('click', async function () {
        var mode = modal.querySelector('input[name="share-mode"]:checked').value;
        var permission = mode === 'editable' ? modal.querySelector('#share-permission').value : undefined;
        confirmBtn.textContent = 'Generating...';
        confirmBtn.disabled = true;
        try {
          var resp = await fetch('/userspace/get_share_id', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ list_name: S.listName, sharing_mode: mode, language: S.language, permission: permission })
          });
          var data = await resp.json();
          if (data.success && data.share_url) {
            messageDiv.innerHTML = "<span style='color:#22b3b3;'>Share Link:</span> <input type='text' value='" + data.share_url + "' style='width:70%; padding:6px; border-radius:6px; border:none; background:#333; color:#fff;' readonly> <button id='copy-share-link-btn' style='background:#228383; color:#fff; border:none; border-radius:6px; padding:6px 12px; font-weight:600; cursor:pointer;'>Copy</button>";
            messageDiv.querySelector('#copy-share-link-btn').addEventListener('click', function () {
              navigator.clipboard.writeText(data.share_url);
            });
            confirmBtn.style.display = 'none';
          } else {
            messageDiv.textContent = 'Error generating share link.';
            confirmBtn.disabled = false; confirmBtn.textContent = 'Get Share Link';
          }
        } catch (e) {
          messageDiv.textContent = 'Error generating share link.';
          confirmBtn.disabled = false; confirmBtn.textContent = 'Get Share Link';
        }
      });
      cancelBtn.addEventListener('click', function () { document.body.removeChild(modal); });
    });
  }
})();
