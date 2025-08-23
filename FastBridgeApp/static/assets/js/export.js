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

fetch('/account/protected', { credentials: 'include' })
  .then((resp) => {
    if (!resp.ok) throw new Error('Not authenticated')
    return resp.json()
  })
  .then((data) => {
    document.getElementById('save-list-container').style.display = ''
  })
  .catch((err) => {
    document.getElementById('save-list-container').style.display = 'none'
  })

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
  
  // Filter active rows and extract only SIMPLE_LEMMA and GLOSS
  const words = (rowData || []).filter(row => row.active)
    .map(row => [
      row.values[simpleLemmaIndex],
      row.values[glossIndex]
    ]);

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
    } else {
      document.getElementById('save-list-message').textContent = 'Error saving list.';
    }
  } catch {
    document.getElementById('save-list-message').textContent = 'Error saving list.';
  }
});
