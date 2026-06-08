var rows = data,
  search = document.getElementById("search");
var display_len = document.getElementById("len");

// --- word selection (Phase 2) ---
// Rows are virtualized by Clusterize, so selection can't live in the DOM.
// We track selected SIMPLE_LEMMA values in a Set and re-apply the highlight
// class to whatever rows are currently rendered (on scroll, filter, etc.).
var selectedLemmas = new Set();
var _colDef = (typeof columns === "string") ? JSON.parse(columns) : columns;
var simpleLemmaIndex = Object.keys(_colDef).indexOf("SIMPLE_LEMMA");

function _selectionLoggedIn() {
  return document.cookie.split(";").some(function (c) {
    return c.trim().indexOf("session_name=") === 0;
  });
}

function lemmaOfRow(row) {
  return simpleLemmaIndex > -1 ? row.values[simpleLemmaIndex] : null;
}

function applySelectionClasses() {
  var area = document.getElementById("contentArea");
  if (!area) return;
  var trs = area.querySelectorAll("tr[data-lemma]");
  for (var i = 0; i < trs.length; i++) {
    trs[i].classList.toggle("row-selected", selectedLemmas.has(trs[i].getAttribute("data-lemma")));
  }
}

function updateActionBar() {
  // Gmail-style: the floating bar is only present while something is selected
  var bar = document.getElementById("floating-action-bar");
  if (bar) bar.style.display = selectedLemmas.size > 0 ? "flex" : "none";
}

function updateSelectionCount() {
  var el = document.getElementById("selection-count");
  if (el) el.textContent = selectedLemmas.size + " selected";
  updateActionBar();
}

function selectAllActive() {
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].active) {
      var l = lemmaOfRow(rows[i]);
      if (l != null) selectedLemmas.add(l);
    }
  }
  updateSelectionCount();
  applySelectionClasses();
}

function clearSelection() {
  selectedLemmas.clear();
  updateSelectionCount();
  applySelectionClasses();
}

function invertSelection() {
  for (var i = 0; i < rows.length; i++) {
    if (!rows[i].active) continue;
    var l = lemmaOfRow(rows[i]);
    if (l == null) continue;
    if (selectedLemmas.has(l)) selectedLemmas.delete(l);
    else selectedLemmas.add(l);
  }
  updateSelectionCount();
  applySelectionClasses();
}

//Clusterize Stuff
/*
 * Fetch suitable rows
 */
var filterRows = function (rows) {
  var results = [];
  for (var i = 0, ii = rows.length; i < ii; i++) {
    if (rows[i].active) results.push(rows[i].markup);
  }
  if (display_len) {
    display_len.innerText = rows.length;
  }
  return results;
};

/*
 * Init clusterize.js
 */
var clusterize = new Clusterize({
  rows: filterRows(rows),
  scrollId: "scrollArea",
  contentId: "contentArea",
  callbacks: {
    // Re-apply selection highlight to rows as they get (re-)rendered on scroll
    clusterChanged: applySelectionClasses,
  },
});

/*
 * Attach listener to search input tag and filter list on change
 */
var onSearch = function () {
  for (var i = 0, ii = rows.length; i < ii; i++) {
    var suitable = false;
    for (var j = 0, jj = rows[i].values.length; j < jj; j++) {
      if (
        rows[i].values[j]
          .toString()
          .toLowerCase()
          .indexOf(search.value.toLowerCase()) + 1
      )
        suitable = true;
    }
    rows[i].active = suitable;
  }
  clusterize.update(filterRows(rows));
};
search.oninput = onSearch;
// end clusterize stuff
// Slideout show
slideOut = document.getElementById("slideOut");
tab = document.getElementById("slideOutTab");
if (tab) {
  tab.onclick = function () {
    slideOut.classList.toggle("showSlideOut");
  };
}

function show_full_list(id) {
  var ths = document.getElementById(id);
  var value = ths.value;
  if (value == "show") {
    rows = full_data;
    clusterize.update(filterRows(rows));
    ths.value = "hide";
  } else if (value == "hide") {
    rows = data;
    clusterize.update(filterRows(rows));
    ths.value = "show";
  }
}

function isHidden(el) {
  return el.offsetParent === null;
}

var first_visible_row = document.getElementById("main_table").rows[0];

function get_first_visible_row() {
  var rows = document.getElementById("main_table").rows;
  var j = 0;
  while (isHidden(rows[j])) {
    j++;
    first_visible_row = rows[j];
  }
  return rows[0];
}
//line up headers
function line_up_header_columns() {
  headers = document.getElementsByTagName("th");
  for (var i = 0; i < headers.length; i++) {
    width = get_first_visible_row().cells[i].offsetWidth + "px";
    headers[i].style.width = width;
  }
}

//sorting – not sure how compatible this is with clusterize

function sortTable(col, n) {
  asc = columns[col][1];
  //checks if this is an int or a string. Thank you implicit typing
  if (typeof rows[0].values[n] == "number") {
    if (asc) {
      rows.sort(function (a, b) {
        {
          return a.values[n] > b.values[n] ? 1 : -1;
        }
      });
    } else {
      rows.sort(function (a, b) {
        {
          return a.values[n] < b.values[n] ? 1 : -1;
        }
      });
    }
  } else {
    if (asc) {
      rows.sort(function (a, b) {
        return a.values[n].toLowerCase() > b.values[n].toLowerCase() ? 1 : -1;
      });
    } else {
      rows.sort(function (a, b) {
        return a.values[n].toLowerCase() < b.values[n].toLowerCase() ? 1 : -1;
      });
    }
  }
  columns[col][1] = !asc;
  clusterize.update(filterRows(rows));
  setTimeout(line_up_header_columns, 0);
}

//row and column filter functions
function toggle_all_filters(id) {
  var ths = document.getElementById(id);
  if (ths.value == "hide") {
    rows = [];
    ths.value = "show";
  } else {
    rows = data;
    ths.value = "hide";
  }
  var checkBoxes = document.querySelectorAll("input[name=filterChecks]");
  for (var i = 0; i < checkBoxes.length; i++) {
    checkBoxes[i].value = ths.value;
    checkBoxes[i].checked = ths.checked;
  }

  clusterize.update(filterRows(rows));
}

function global_filter(filter_id) {
  var to_toggle = document.getElementsByClassName(filter_id);
  for (var i = 0; i < to_toggle.length; i++) {
    to_toggle[i].value = document.getElementById(filter_id).value;
    to_toggle[i].checked = document.getElementById(filter_id).checked;
    hide_show_row(to_toggle[i].id);
  }
  if (document.getElementById(filter_id).value == "hide") {
    document.getElementById(filter_id).value = "show";
  } else {
    document.getElementById(filter_id).value = "hide";
  }
}

//try using the element
function hide_show_column(col_name) {
  var stylesheet = document.styleSheets[8];
  var end = stylesheet.cssRules.length;
  var checkbox_val = document.getElementById(col_name).value;
  if (checkbox_val == "hide") {
    var rule = `.${col_name} { display : none !important} `;
    stylesheet.insertRule(rule, end);
    columns[col_name][0] = end;
    document.getElementById(col_name + "_head").style.display = "none";
    document.getElementById(col_name).value = "show";
  } else {
    if (columns[col_name][0] != end - 1) {
      for (const [key, value] of Object.entries(columns)) {
        if (value[0] > columns[col_name][0]) {
          columns[key] = [columns[key][0] - 1, true]; //bool is for sorting, this makes is smallest to largest
        }
      }
    }
    stylesheet.deleteRule(columns[col_name][0]);
    document.getElementById(col_name + "_head").style.display = "table-cell";
    document.getElementById(col_name).value = "hide";
  }
  setTimeout(line_up_header_columns, 0);
}

function hide_show_row(row_value) {
  var checkbox_val = document.getElementById(row_value).value;
  var children = false;
  var parent = document.getElementById(row_value + "extra");
  if (parent) {
    children = document.getElementById(row_value + "extra").childNodes;
  }

  if (checkbox_val == "hide") {
    rows = rows.filter((element) => !element.values.includes(row_value));
    if (children) {
      for (var i = 0; i < children.length; i++) {
        children[i].childNodes[1].childNodes[1].checked = "";

        children[i].childNodes[1].childNodes[1].value = "show";
        children[i].childNodes[1].childNodes[1].disabled = "true";
      }
    }
    document.getElementById(row_value).value = "show";
  } else {
    rows = data;
    if (children) {
      for (var i = 0; i < children.length; i++) {
        children[i].childNodes[1].childNodes[1].checked = "true";
        children[i].childNodes[1].childNodes[1].value = "hide";
        children[i].childNodes[1].childNodes[1].disabled = "";
      }
    }
    var checkBoxes = document.querySelectorAll(
      "input[name=filterChecks]:not(:checked)"
    );
    for (var i = 0; i < checkBoxes.length; i++) {
      checkBoxes[i].value = "hide";
      hide_show_row(checkBoxes[i].id);
    }

    document.getElementById(row_value).value = "hide";
  }
  clusterize.update(filterRows(rows));
  setTimeout(line_up_header_columns, 0);
}
setTimeout(line_up_header_columns, 0);

// Wire row-click selection only when logged in (selection feeds the save/add-to-list actions)
if (_selectionLoggedIn()) {
  var _selAllBtn = document.getElementById("select-all-terms-btn");
  if (_selAllBtn) _selAllBtn.style.display = "";
  var _contentArea = document.getElementById("contentArea");
  if (_contentArea) {
    _contentArea.addEventListener("click", function (e) {
      if (e.target.closest("a")) return; // don't hijack external-link clicks
      var tr = e.target.closest("tr[data-lemma]");
      if (!tr) return;
      var lemma = tr.getAttribute("data-lemma");
      if (selectedLemmas.has(lemma)) selectedLemmas.delete(lemma);
      else selectedLemmas.add(lemma);
      tr.classList.toggle("row-selected", selectedLemmas.has(lemma));
      updateSelectionCount();
    });
  }
}

// Restore Options state from a saved search URL (?hp=ID1,ID2) by replaying the
// same unchecks the user made — clicking each checkbox fires hide_show_row.
(function restoreSavedFilters() {
  var hp = new URLSearchParams(window.location.search).get("hp");
  if (!hp) return;
  hp.split(",").forEach(function (id) {
    if (!id) return;
    var cb = document.getElementById(decodeURIComponent(id));
    if (cb && cb.checked && !cb.disabled) cb.click();
  });
})();
