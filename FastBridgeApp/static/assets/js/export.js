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
