
this.$slideOut = $('#slideOut');
// Slideout show
this.$slideOut.find('.slideOutTab').on('click', function() {
  $("#slideOut").toggleClass('showSlideOut');
});
function hide_show_column(col_name)
{
  console.log(col_name);
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
}

function hide_show_row(row_value){
  console.log(row_value)
  var checkbox_val=document.getElementById(row_value).value
  if(checkbox_val=="hide")
  {
   var all_col=document.getElementsByClassName(row_value);
   for(var i=0;i<all_col.length;i++)
   {
    all_col[i].style.display="none";
   }
   document.getElementById(row_value).value="show";
  }

  else
  {
   var all_col=document.getElementsByClassName(row_value);
   for(var i=0;i<all_col.length;i++)
   {
    all_col[i].style.display="table-row";
   }
   document.getElementById(row_value).value="hide";
  }
}
