var rows = data,
    search = document.getElementById('search');

/* Fill array with data
 *
 * Params:
 * values *array*  - value of each field (in case use of table)
 *        example: ['1st TD content', '2nd TD content'] for table
 *                 ['list's LI item content'] for list
 * markup *string* - markup that will be added to the DOM
 * active *bool*   - specifies if row is suitable by search phrase
*/


/*
* Fetch suitable rows
*/
var filterRows = function(rows) {
  var results = [];
  for(var i = 0, ii = rows.length; i < ii; i++) {
    if(rows[i].active) results.push(rows[i].markup)
  }
  return results;
}

/*
* Init clusterize.js
*/
var clusterize = new Clusterize({
  rows: filterRows(rows),
  scrollId: 'scrollArea',
  contentId: 'contentArea'
});

/*
* Attach listener to search input tag and filter list on change
*/
var onSearch = function() {
  for(var i = 0, ii = rows.length; i < ii; i++) {
    var suitable = false;
    for(var j = 0, jj = rows[i].values.length; j < jj; j++) {
      if(rows[i].values[j].toString().indexOf(search.value) + 1)
        suitable = true;
    }
    rows[i].active = suitable;
  }
  clusterize.update(filterRows(rows));
}
search.oninput = onSearch;

// Slideout show
slideOut = document.getElementById('slideOut')
tab = document.getElementById('slideOutTab')
tab.onclick = (function() {slideOut.classList.toggle('showSlideOut'); });

//from old bridge. Somethings weren't broken
function printData()
{
   var divToPrint=document.getElementById("export_wrapper");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}


// Quick and simple export target #table_id into a csv
function download_table_as_csv() {
    // Select rows from table_id
    var rows = document.querySelectorAll('div#export_wrapper tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(','));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = 'export_vocabulary_list_' + new Date().toLocaleDateString() + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


function isHidden(el) {
    return (el.offsetParent === null)
}
var first_visible_row = document.getElementById('main_table').rows[0]

function get_first_visible_row() {
  var rows = document.getElementById('main_table').rows;
  var j = 0;
  while (isHidden(rows[j])){
    j++
    first_visible_row = rows[j]
    ;
  }
  return first_visible_row
}
//line up headers
function line_up_header_columns()
{
  headers = document.getElementsByTagName('th');
  for (var i = 0; i < headers.length; i++) {
    width = get_first_visible_row().cells[i].offsetWidth +"px"
    headers[i].style.width = width
  }
}


//sorting – not sure how compatible this is with clusterize

function sortTable(n) {
  console.log("resorting")
  resorted_rows = rows
  console.log(n)
  console.log(rows[0].values[n])

  resorted_rows.sort(function(a, b){ if (parseInt(a.values[n]))
     {
       return (parseInt(a.values[n]) < parseInt(b.values[n])) ? 1 : -1
     }
    else
     {
        return (a.values[n].toLowerCase() > b.values[n].toLowerCase()) ? 1 : -1
      }
    }
  )
  clusterize.update(filterRows(resorted_rows));

}
//row and column filter functions
function hide_show_column(col_name)
{
 var checkbox_val=document.getElementById(col_name).value;
 if(checkbox_val=="hide")
 {
  var all_col=document.getElementsByClassName(col_name);
  for(var i=0;i<all_col.length;i++)
  {
   all_col[i].style.display="none";
  }
  document.getElementById(col_name+"_head").style.display="none";
  document.getElementById(col_name).value="show";
 }

 else
 {
  var all_col=document.getElementsByClassName(col_name);
  for(var i=0;i<all_col.length;i++)
  {
   all_col[i].style.display="table-cell";
  }
  document.getElementById(col_name+"_head").style.display="table-cell";
  document.getElementById(col_name).value="hide";
 }
 setTimeout(line_up_header_columns,0);
}

function hide_show_row(row_value){
  //console.log(row_value)
  var checkbox_val=document.getElementById(row_value).value
  var all_col=document.getElementsByClassName(row_value);
  var children = false;
  var parent = document.getElementById(row_value+"extra");
  if (parent) {
    //console.log(row_value+"extra", "success")
    children = document.getElementById(row_value+"extra").childNodes
    //console.log(children)
  }
  console.log(children)
  if(checkbox_val=="hide")
  {
    for(var i=0;i<all_col.length;i++){
      all_col[i].style.display = "none"

     }
     if (children){
     for (var i = 0; i < children.length; i++) {
       children[i].childNodes[1].childNodes[1].checked=""

       children[i].childNodes[1].childNodes[1].value="show"
       children[i].childNodes[1].childNodes[1].disabled="true"
     }
   }
  document.getElementById(row_value).value="show";
  }
  else
  {
    for(var i=0;i<all_col.length;i++){
      all_col[i].style.display = "table-row"
      //all_col[i].classList.add(row_value+"_show");
     }
     if(children){
     for (var i = 0; i < children.length; i++) {
       console.log(children[i].childNodes[1].childNodes[1])
       children[i].childNodes[1].childNodes[1].checked="true"
       children[i].childNodes[1].childNodes[1].value="hide"
       children[i].childNodes[1].childNodes[1].disabled=""
     }
   }
   document.getElementById(row_value).value="hide";
 }
}
setTimeout(line_up_header_columns,0)
