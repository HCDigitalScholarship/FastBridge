/*
step form structure
source: https://www.w3schools.com/howto/howto_js_form_steps.asp
*/
var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab, true); // Display the current tab
// This function will display the specified tab of the form ...
function showTab(n, isNext) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  var prev = document.getElementById("myPrev");
  var next = document.getElementById("myNext");
  var open1 = document.getElementById("openModal1");
  var open2 = document.getElementById("openModal2");
  var len1 = document.getElementById("bridge-result-table1").rows.length;
  var len2 = document.getElementById("bridge-result-table2").rows.length;
  // fix previous and add buttons
  if (n == 0) {
    prev.disabled = true;
    open1.style.display = "";
    open2.style.display = "none";
    if (len1 <= 3) {
        next.disabled = true;
    } else {
        next.disabled = false;
    }
    document.getElementById('page-buttons').style.marginTop="-30px";
  } else {
    prev.disabled = false;
    open2.style.display = "";
    open1.style.display = "none";
    if (len2 <= 3) {
        next.disabled = true;
    } else {
        next.disabled = false;
    }
    document.getElementById('page-buttons').style.marginTop="-50px";
  }
  // fix next button
  if (n == (x.length - 1)) {
    next.innerHTML = '<i class="fas fa-check"></i>';
  } else {
    next.innerHTML = '<i class="fas fa-angle-double-right"></i>';
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n);
}

// This function will figure out which tab to display
function nextPrev(n, next) {
  var x = document.getElementsByClassName("tab");
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
  //   document.getElementById("regForm").submit();
    window.location.href = "result.html";
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab, next);
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

// buttons
$('#myNext').click(function(){
    nextPrev(1, true);
});

$('#myPrev').click(function(){
    nextPrev(-1, false);
});

// events triggered by the selections of how to customize list
$('#formCheck-1').click(function(){
    document.getElementById("myNext").disabled = true;
    document.getElementById("openModal2").disabled = false;
});

$('#formCheck-2').click(function(){
    document.getElementById("myNext").disabled = true;
    document.getElementById("openModal2").disabled = false;
});

$('#formCheck-3').click(function(){
    document.getElementById("myNext").disabled = false;
    document.getElementById("openModal2").disabled = true;
});


/*
SELECT WORK modal & table
*/

// delete row from table
function deleteRow(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("bridge-result-table1");
  table.deleteRow(i);
  if (table.rows.length <= 3){
      document.getElementById('myNext').disabled = true;
  }
}

// yes triggers hidden fields
$("#bridge-modal-form1-select2").change(function() {
  if ($(this).val() == "yes") {
    $('#bridge-modal-form1-select2-hidden-div').show();
  } else {
    $('#bridge-modal-form1-select2-hidden-div').hide();
  }
});
$("#bridge-modal-form1-select2").trigger("change");

// modal save
$('#bridge-modal-form1-save').click(function(){
    // if showing select value is good enough
    // var book = $('#select-text #select1').val().trim();

    // if showing select label is better than value
    var el = document.getElementById('bridge-modal-form1-select1');
    var book = el.options[el.selectedIndex].innerHTML;

    var sectionFrom = $('#bridge-select-text #bridge-modal-form1-select2-hidden-field1').val();
    var sectionTo =$('#bridge-select-text #bridge-modal-form1-select2-hidden-field2').val();
    if (sectionFrom || sectionTo){ // if user specifies a section
        var sections = `${sectionFrom}-${sectionTo}`;
    } else {
        var sections = '';
    }
    // show the selection in a table
    var table = document.getElementById('bridge-result-table1');
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = '<span style="color:white">' + book + '</span>';
    cell2.innerHTML = '<span style="color:white">' + sections + '</span>';
    cell3.innerHTML = '<button class="btn" onclick="deleteRow(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
    // hide modal when save
    $('#bridge-select-text').modal('hide');
    // reset form values
  //  $('#bridge-select-text').find('#bridge-modal-form1')[0].reset();
    $('#bridge-modal-form1-select2-hidden-div').hide();
    // enable 'next' button
    document.getElementById("myNext").disabled = false;
});

/*
DEFINE VOCAB modal & table
*/

// delete row from table
function deleteRow2(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("bridge-result-table2");
  table.deleteRow(i);
  if (table.rows.length <= 3){
      document.getElementById('myNext').disabled = true;
  }
}

// yes triggers hidden fields
$("#bridge-modal-form2-select2").change(function() {
  if ($(this).val() == "yes") {
    $('#bridge-modal-form2-select2-hidden-div').show();
  } else {
    $('#bridge-modal-form2-select2-hidden-div').hide();
  }
});
$("#bridge-modal-form2-select2").trigger("change");

// modal save
$('#bridge-modal-form2-save').click(function(){
    // if showing select value is good enough
    // var book = $('#select-text #select1').val().trim();

    // if showing select label is better than value
    var el = document.getElementById('bridge-modal-form2-select1');
    var book = el.options[el.selectedIndex].innerHTML;

    var sectionFrom = $('#bridge-change-list #bridge-modal-form2-select2-hidden-field1').val();
    var sectionTo =$('#bridge-change-list #bridge-modal-form2-select2-hidden-field2').val();
    if (sectionFrom || sectionTo){ // if user specifies a section
        var sections = `${sectionFrom}-${sectionTo}`;
    } else {
        var sections = '';
    }
    // show the selection in a table
    var table = document.getElementById('bridge-result-table2');
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = '<span style="color:white">' + book + '</span>';
    cell2.innerHTML = '<span style="color:white">' + sections + '</span>';
    cell3.innerHTML = '<button class="btn" onclick="deleteRow2(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
    // hide modal when save
    $('#bridge-change-list').modal('hide');
    // reset form values
    $('#bridge-change-list').find('#bridge-modal-form2')[0].reset();
    $('#bridge-modal-form2-select2-hidden-div').hide();
    // enable 'next' button
    document.getElementById("myNext").disabled = false;
});
