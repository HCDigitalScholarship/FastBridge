/*
step form structure
source: https://www.w3schools.com/howto/howto_js_form_steps.asp
*/

var currentTab = 0; // Current tab is set to be the first tab (0)
var knowntexts = [];
var known_starts = [];
var known_ends = [];
var etexts = [];
var estarts = [];
var eends = [];
var e_section_size = [];
var text_to_add = "";
//dropdown menu
function myFunction(dropdown_id) {
  document.getElementById(dropdown_id).classList.toggle("show");
}

function add_text(text_name, dropdown_id, depth){
  text_to_add = text_name;
  var new_placeholder;
  if(depth == 1){
    new_placeholder = "1"
  }
  else if (depth == 2) {
    new_placeholder = "1.1"
  }
  else if (depth == 3){
    new_placeholder = "1.1.1"
  }
  document.getElementById('oracle-modal-form1-select2-hidden-field1').placeholder = new_placeholder
  document.getElementById('oracle-modal-form1-select2-hidden-field2').placeholder = new_placeholder
  document.getElementById('oracle-modal-form2-select2-hidden-field1').placeholder = new_placeholder
  document.getElementById('oracle-modal-form2-select2-hidden-field2').placeholder = new_placeholder
  if (text_to_add == ""){
    alert("please enter a valid text");
    return false;
  }
  myFunction(dropdown_id);
  id =  document.getElementById(dropdown_id).previousElementSibling.id
  display = document.getElementById(id);
  display.innerText = text_name
}
function filterFunction(input_id, dropdown_id) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(input_id);
  filter = input.value.toUpperCase();
  div = document.getElementById(dropdown_id);
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

showTabOracle(currentTab, true); // Display the current tab
// This function will display the specified tab of the form ...
function showTabOracle(n, isNext) {
  var x = document.getElementsByClassName("tab-oracle");
  x[n].style.display = "block";
  var prev = document.getElementById("myPrev-oracle");
  var next = document.getElementById("myNext-oracle");
  var open1 = document.getElementById("openModal1-oracle");
  var open2 = document.getElementById("openModal2-oracle");
  var len1 = document.getElementById("oracle-result-table1").rows.length;
  var len2 = document.getElementById("oracle-result-table2").rows.length;
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
    document.getElementById('page-buttons-oracle').style.marginTop="-30px";
  } else {
    prev.disabled = false;
    open2.style.display = "";
    open1.style.display = "none";
    if (len2 <= 3) {
        next.disabled = true;
    } else {
        next.disabled = false;
    }
    document.getElementById('page-buttons-oracle').style.marginTop="-50px";
  }
  // fix next button
  if (n == (x.length - 1)) {
    next.innerHTML = '<i class="fas fa-check"></i>';
  } else {
    next.innerHTML = '<i class="fas fa-angle-double-right"></i>';
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n+1);
}

// This function will figure out which tab to display
function nextPrevOracle(n, next) {
  var x = document.getElementsByClassName("tab-oracle");
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
  //   document.getElementById("regForm").submit();
  knowntexts = knowntexts.toString().replace(",", "+")
  known_starts = known_starts.toString().replace(",", "+")
  known_ends = known_ends.toString().replace(",", "+")

  etexts = etexts.toString().replace(",", "+")
  estarts = estarts.toString().replace(",", "+")
  eends = eends.toString().replace(",", "+")
  e_section_size = e_section_size.toString().replace(",", "+")

    window.location.href = window.location.href + "/result/" + etexts + "/"+ estarts+ "/" + eends+ "/" + e_section_size + "/" +  knowntexts + "/" + known_starts + "-" + known_ends + "/";
    return false;
  }
  // Otherwise, display the correct tab:
  showTabOracle(currentTab, next);
}


// This function is the same as in select-vocab-step-form.js
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
$('#myNext-oracle').click(function(){
    nextPrevOracle(1, true);
});

$('#myPrev-oracle').click(function(){
    nextPrevOracle(-1, false);
});

/*
SELECT WORK modal & table
*/

// delete row from table
function deleteRowOracle(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("oracle-result-table1");
  etexts.splice(i-3, 1);
  estarts.splice(i-3, 1);
  eends.splice(i-3, 1);
  e_section_size.splice(i-3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3){
      document.getElementById('myNext-oracle').disabled = true;
  }
}

// yes triggers hidden fields
$("#oracle-modal-form1-select2").change(function() {
  if ($(this).val() == "yes") {
    $('#oracle-modal-form1-select2-hidden-div').show();
  } else {
    $('#oracle-modal-form1-select2-hidden-div').hide();
  }
});
$("#oracle-modal-form1-select2").trigger("change");

// modal save
$('#oracle-modal-form2-save').click(function(){
    // if showing select value is good enough
    // var book = $('#select-text #select1').val().trim();

    // if showing select label is better than value

    var book = text_to_add
    if (text_to_add == ""){
      alert("please enter a valid text");
      return false;
    }

    var sectionFrom = $('#oracle-modal-form2-select2-hidden-field1').val();
    var sectionTo =$('#oracle-modal-form2-select2-hidden-field2').val();
    console.log(sectionFrom, sectionTo)
    if (sectionFrom && sectionTo){ // if user specifies a section
        var sections = `${sectionFrom}-${sectionTo}`;
    }else if (!sectionFrom && sectionTo) {
      var sections = `start-${sectionTo}`;
      sectionFrom = 'start'
    }
    else if (!sectionTo && sectionFrom) {
      var sections = `${sectionFrom}-end`;
      sectionTo = 'end'
    }
     else {
        sectionFrom = 'start'
        sectionTo = 'end'
        var sections = 'start-end';
    }
    // show the selection in a table
    var table = document.getElementById('oracle-result-table2');
    knowntexts.push(string_to_slug(book))
    known_starts.push(sectionFrom)
    known_ends.push(sectionTo)
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = '<span style="color:white">' + book + '</span>';
    cell2.innerHTML = '<span style="color:white">' + sections + '</span>';
    cell3.innerHTML = '<button class="btn" onclick="deleteRowOracle2(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
    // hide modal when save
    $('#oracle-define-vocab').modal('hide');
    // reset form values

    document.getElementById('oracle-modal-form2').reset();
    $('#oracle-modal-form2-select2-hidden-div').hide();
    // enable 'next' button
    document.getElementById("myNext-oracle").disabled = false;
});

/*
DEFINE VOCAB modal & table
*/
// radio button triggers different forms
function hideBridge(x) {
   if (x.checked) {
     document.getElementById("bridge").style.display = "none";
     document.getElementById("computer").style.display="";
   }
 }

function hideComputer(x) {
   if (x.checked) {
     document.getElementById("computer").style.display="none";
     document.getElementById("bridge").style.display="";
   }
 }

// delete row from table
function deleteRowOracle2(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("oracle-result-table2");
  knowntexts.splice(i-3, 1);
  known_starts.splice(i-3, 1);
  known_ends.splice(i-3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3){
      document.getElementById('myNext-oracle').disabled = true;
  }
}

// yes triggers hidden fields
$("#oracle-modal-form2-select2").change(function() {
  if ($(this).val() == "yes") {
    $('#oracle-modal-form2-select2-hidden-div').show();
  } else {
    $('#oracle-modal-form2-select2-hidden-div').hide();
  }
});
$("#oracle-modal-form2-select2").trigger("change");

// modal save
$('#oracle-modal-form1-save').click(function(){
    // if showing select value is good enough
    // var book = $('#select-text #select1').val().trim();

    // if showing select label is better than value

    var book = text_to_add
    if (text_to_add == ""){
      alert("please enter a valid text");
      return false;
    }

    var size = $('#oracle-modal-form1-select2-hidden-field3').val();
    var sectionFrom = $('#oracle-modal-form1-select2-hidden-field1').val();
    var sectionTo = $('#oracle-modal-form1-select2-hidden-field2').val();

    if(sectionFrom == "")
    {
      alert("Please enter a section from which to start")
      return false
    }
    if(sectionTo == "")
    {
      alert("Please enter a section at which to end")
      return false
    }
    if (size){ // if user specifies a section
        var size = `${size}`;
    } else {
        var size = '9';
    }
    console.log(size)
    etexts.push(string_to_slug(book))
    estarts.push(sectionFrom)
    eends.push(sectionTo)
    e_section_size.push(size)

    // show the selection in a table
    sections=(sectionFrom + " - " + sectionTo + "; " + size)
    var table = document.getElementById('oracle-result-table1');
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = '<span style="color:white">' + book + '</span>';
    cell2.innerHTML = '<span style="color:white">' + sections + '</span>';
    cell3.innerHTML = '<button class="btn" onclick="deleteRowOracle(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
    // hide modal when save
    $('#oracle-select-text').modal('hide');
    //document.getElementById("computer").style.display="none";
    //document.getElementById("bridge").style.display="none";
    // reset form values
    document.getElementById('oracle-modal-form1').reset();
    $('#oracle-modal-form1-select2-hidden-div').hide();
    // enable 'next' button
    document.getElementById("myNext-oracle").disabled = false;
});


// from: https://gist.github.com/codeguy/6684588. modified to make whitespace a _ instead of a -
function string_to_slug (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc      ";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '_') // collapse whitespace and replace by _

    return str;
}
