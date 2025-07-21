function current_selections() {
  filters = [
    "running",
    "toggle_all",
    "Adjective",
    "Adverb",
    "Conjunction",
    "Idiom",
    "Interjection",
    "Noun",
    "Number",
    "Preposition",
    "Pronoun",
    "Verb",
    "CONJUNCTION_Verb_1",
    "CONJUNCTION_Verb_2",
    "CONJUNCTION_Verb_3",
    "CONJUNCTION_Verb_4",
    "CONJUNCTION_Verb_99", // irregular
    "STOPWORD_Verb_0", // stopword verb
    "CONJUGATION",
    "DECLENSION",
    "PROPER",
    "REGULAR",
    "STOPWORD",
    "PRINCIPAL_PARTS_NO_DIACRITICALS",
    "PRINCIPAL_PARTS",
    "SHORT_DEFINITION",
    "LONG_DEFINITION",
    "SIMPLE_LEMMA",
    "PART_OF_SPEECH",
    "LOGEION_LINK",
    "FORCELLINI_LINK",
    "Total_Count_in_Text",
    "Count_in_Selection",
    "Location",
    "Source_Text",
  ];

  let result = "{";
  for (i = 0; i < filters.length - 1; i++) {
    let filter = "#" + filters[i];
    let value = $(filter).val();
    console.log(filter, value);
    result += '"' + filters[i] + '":"' + value + '",';
    console.log(result);
  }
  let filter = "#" + filters[filters.length - 1];
  let value = $(filter).val();
  result += '"' + filters[filters.length - 1] + '":"' + value + '"}';
  return JSON.parse(result);
}

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
        ([name, [index]]) => classList.contains(name)
      );

      if (matchingCol) {
        const [name, [index]] = matchingCol;
        return { name, index };
      }

      return null;
    })
    .filter(col => col !== null)
    .sort((a, b) => a.index - b.index);

  const headerCSV = visibleColumns.map(col => `"${col.name}"`).join(",");

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
