function exportVisibleDataToCSV() {
  const colMap = typeof columns === "string" ? JSON.parse(columns) : columns;
  const checkbox = document.getElementById("running");

  const rowDataRaw = checkbox.checked ? full_data : rows;
  const rowData = typeof rowDataRaw === "string" ? JSON.parse(rowDataRaw) : rowDataRaw;

  const ths = Array.from(document.querySelector("thead tr").children);

  const visibleColumns = ths
  .map((th, idx) => {
    const style = getComputedStyle(th);
    if (style.display === "none" || style.visibility === "hidden") return null;

    const classList = th.classList;
    const matchingCol = Object.entries(colMap).find(
      ([name]) => classList.contains(name)
    );

    if (matchingCol) {
      const [name] = matchingCol;
      return { name, index: idx }; 
    }

    return null;
  })
  .filter(col => col !== null)

  const renaming_dict = {
    "Location": "FIRST_APPEARANCE_IN_SELECTION",
    "SHORT_DEFINITION": "GLOSS",
    "LONG_DEFINITION": "DEFINITION",
    "TITLE": "HEADWORD"
  };

  const headerCSV = visibleColumns
    .map(col => {
      const renamed = renaming_dict[col.name] || col.name; 
      return `"${renamed.replace(/_/g, " ")}"`;
    })
    .join(",");

  const csvRows = rowData
    .filter(row => row.active)
    .map(row => {
      return visibleColumns.map(col => {
        let val = row.values[col.index];
        if (val === undefined || val === null) val = "";
        val = String(val).replace(/"/g, '""');
        return `"${val}"`;
      }).join(",");
    });

  const csvString = [headerCSV, ...csvRows].join("\n");
  const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "export_vocabulary_list_" + new Date().toLocaleDateString() + ".csv";;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function printData() {
  const colMap = typeof columns === "string" ? JSON.parse(columns) : columns;
  const checkbox = document.getElementById("running");

  // get the active rows according to toggle
  const rowDataRaw = checkbox.checked ? full_data : rows;
  const rowData = typeof rowDataRaw === "string" ? JSON.parse(rowDataRaw) : rowDataRaw;

  const ths = Array.from(document.querySelector("thead tr").children);

  // only columns currently visible
  const visibleColumns = ths
    .map((th, idx) => {
      const style = getComputedStyle(th);
      if (style.display === "none" || style.visibility === "hidden") return null;

      const classList = th.classList;
      const matchingCol = Object.entries(colMap).find(
        ([name]) => classList.contains(name)
      );

      if (matchingCol) {
        const [name] = matchingCol;
        return { name, index: idx }; 
      }

      return null;
    })
    .filter(col => col !== null);

  const renaming_dict = {
    "Location": "FIRST_APPEARANCE_IN_SELECTION",
    "SHORT_DEFINITION": "GLOSS",
    "LONG_DEFINITION": "DEFINITION",
    "TITLE": "HEADWORD"
  };

  // build table
  const table = document.createElement("table");
  table.className = "table table-striped";

  // create thead
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  visibleColumns.forEach(col => {
    const th = document.createElement("th");
    const renamed = renaming_dict[col.name] || col.name;
    th.innerText = renamed.replace(/_/g, " ");
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // create tbody with only active rows
  const tbody = document.createElement("tbody");
  rowData
    .filter(row => row.active)
    .forEach(row => {
      const tr = document.createElement("tr");
      visibleColumns.forEach(col => {
        const td = document.createElement("td");
        let val = row.values[col.index];
        if (val === undefined || val === null) val = "";
        td.innerText = val;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  table.appendChild(tbody);

  // print
  const newWin = window.open("");
  newWin.document.write(`
    <html>
      <head>
        <title>Print Table</title>
        <style>
          table { border-collapse: collapse; width: 100%; }
          th, td { border: 1px solid #ccc; padding: 4px; text-align: left; }
        </style>
      </head>
      <body>
        ${table.outerHTML}
      </body>
    </html>
  `);

  newWin.document.close();
  newWin.focus();
  newWin.print();
  newWin.close();
}

(function initSaveList() {
  const isLoggedIn = document.cookie.split(';').some(c => c.trim().startsWith('session_name='));
  if (!isLoggedIn) return;

  document.getElementById('save-list-container').style.display = '';

  const urlParts = window.location.pathname.split('/');
  const language = urlParts[urlParts.indexOf('select') + 1] || '';

  fetch(`/userspace/list_names?language=${encodeURIComponent(language)}`, { credentials: 'include' })
    .then(r => r.json())
    .then(lists => {
      if (!lists || lists.length === 0) return;
      const select = document.getElementById('add-to-list-select');
      lists.forEach(lst => {
        const opt = document.createElement('option');
        opt.value = lst.name;
        opt.textContent = lst.name;
        select.appendChild(opt);
      });
      document.getElementById('add-to-list-section').style.display = '';
    })
    .catch(() => {});
})();

// Extract [lemma, gloss] pairs to save. If the user has hand-picked rows
// (selectedLemmas, from select-result.js), save only those; otherwise save
// all currently filtered rows.
function collectWordsForSave(rowData, simpleLemmaIndex, glossIndex) {
  let chosen = (rowData || []).filter(row => row.active);
  if (typeof selectedLemmas !== "undefined" && selectedLemmas.size > 0) {
    chosen = chosen.filter(row => selectedLemmas.has(row.values[simpleLemmaIndex]));
  }
  return chosen.map(row => [row.values[simpleLemmaIndex], row.values[glossIndex]]);
}

document.getElementById('save-list-btn').addEventListener('click', async () => {
  const listName = document.getElementById('save-list-name').value.trim();
  if (!listName) {
    document.getElementById('save-list-message').textContent = 'Please enter a list name.';
    return;
  }

  const checkbox = document.getElementById("running");
  const colMap = typeof columns === "string" ? JSON.parse(columns) : columns;
  const simpleLemmaIndex = Object.keys(colMap).indexOf("SIMPLE_LEMMA");
  const glossIndex = Object.keys(colMap).indexOf("SHORT_DEFINITION");
  const rowDataRaw = checkbox.checked ? full_data : rows;
  const rowData = typeof rowDataRaw === "string" ? JSON.parse(rowDataRaw) : rowDataRaw;

  if (simpleLemmaIndex === -1 || glossIndex === -1) {
    document.getElementById('save-list-message').textContent = 'Required columns not found.';
    return;
  }
  
  // Filter active rows and extract only SIMPLE_LEMMA and GLOSS (selection-aware)
  const words = collectWordsForSave(rowData, simpleLemmaIndex, glossIndex);

  // Get the language from the URL (after /select/)
  const urlParts = window.location.pathname.split('/');
  const langIndex = urlParts.indexOf('select') + 1;
  const language = urlParts[langIndex] || '';
  
  document.getElementById('save-list-message').textContent = 'Saving...';
  console.log("List Name:", listName, "length:", words.length, "Language:", language, words.slice(0,5));
  try {
    const resp = await fetch('/userspace/create_list', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        list_name: listName,
        words: words,
        language: language
      })
    });

    const result = await resp.json();
    if (result.success) {
      document.getElementById('save-list-message').textContent = 'List saved!';
      document.getElementById('save-list-name').value = '';
    } else {
      document.getElementById('save-list-message').textContent = 'Error saving list.';
    }
  } catch {
    document.getElementById('save-list-message').textContent = 'Error saving list.';
  }
});

document.getElementById('add-to-list-btn').addEventListener('click', async () => {
  const listName = document.getElementById('add-to-list-select').value;
  if (!listName) {
    document.getElementById('add-to-list-message').textContent = 'Please select a list.';
    return;
  }

  const checkbox = document.getElementById("running");
  const colMap = typeof columns === "string" ? JSON.parse(columns) : columns;
  const simpleLemmaIndex = Object.keys(colMap).indexOf("SIMPLE_LEMMA");
  const glossIndex = Object.keys(colMap).indexOf("SHORT_DEFINITION");
  const rowDataRaw = checkbox.checked ? full_data : rows;
  const rowData = typeof rowDataRaw === "string" ? JSON.parse(rowDataRaw) : rowDataRaw;

  const words = collectWordsForSave(rowData, simpleLemmaIndex, glossIndex);

  const urlParts = window.location.pathname.split('/');
  const language = urlParts[urlParts.indexOf('select') + 1] || '';

  document.getElementById('add-to-list-message').textContent = 'Adding...';
  try {
    const resp = await fetch('/userspace/add_words', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ list_name: listName, language, words })
    });
    const result = await resp.json();
    document.getElementById('add-to-list-message').textContent = result.success
      ? result.message
      : 'Error adding words.';
  } catch {
    document.getElementById('add-to-list-message').textContent = 'Error adding words.';
  }
});
