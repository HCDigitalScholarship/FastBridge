
// Slideout show
slideOut = document.getElementById('slideOut')
tab = document.getElementById('slideOutTab')
tab.onclick = (function() {slideOut.classList.toggle('showSlideOut'); });


//clusterize, allows for the quick loading and scrolling.
var clusterize = new Clusterize({
  rows: data,
  rows_in_block: 100,
  scrollId: 'scrollArea',
  contentId: 'contentArea',
});


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
  if(checkbox_val=="hide")
  {
    for(var i=0;i<all_col.length;i++){
      all_col[i].classList.toggle(row_value+"_hide");
      //all_col[i].classList.remove(row_value+"_show");

     }
     for (var i = 0; i < children.length; i++) {
       children[i].childNodes[1].childNodes[1].checked=""
       children[i].childNodes[1].childNodes[1].disabled="true"
     }
  document.getElementById(row_value).value="show";
  }
  else
  {
    for(var i=0;i<all_col.length;i++){
      all_col[i].classList.remove(row_value+"_hide");
      //all_col[i].classList.add(row_value+"_show");
     }
     for (var i = 0; i < children.length; i++) {
       console.log(children[i].childNodes[1].childNodes[1])
       children[i].childNodes[1].childNodes[1].checked="true"
       children[i].childNodes[1].childNodes[1].disabled=""
     }
   document.getElementById(row_value).value="hide";
 }
}
