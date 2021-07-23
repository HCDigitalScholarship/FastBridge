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
var eunits = [];
var e_section_size = [];
var text_to_add = "";

var languageselected;
var sectionfrom1 = "start";
var sectionto1 = "end";
var sectionfrom2 = "start";
var sectionto2 = "end";
var holdsectiondata;
var unitValue;

//dropdown menu
function myFunction(dropdown_id) {
  document.getElementById(dropdown_id).classList.toggle("show");
}

function add_text(text_name, dropdown_id, depth) {
  text_to_add = text_name;
  var new_placeholder;

  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }

  if (window.location.href.includes("Latin")) {
    languageselected = "Latin";
  } else {
    languageselected = "Greek";
  }

  myFunction(dropdown_id);
  id = document.getElementById(dropdown_id).previousElementSibling.id;
  // console.log(id);
  display = document.getElementById(id);
  $(display).change(createDropdown(text_name, dropdown_id));
  display.innerText = text_name;
  // console.log(document.getElementById('myInput'));

  if (depth == 1) {
    new_placeholder = "1";
  } else if (depth == 2) {
    new_placeholder = "1.1";
  } else if (depth == 3) {
    new_placeholder = "1.1.1";
  }

  document.getElementById(
    "oracle-modal-form1-select2-hidden-field3"
  ).innerHTML = "Select Unit";
  $("#unitdropdown").empty();
  let element = document.getElementById("unitdropdown");
  console.log(element);
  for (var i = 1; i <= depth; i++) {
    let a = document.createElement("a");
    a.innerHTML = i;

    a.id = i + "unit";

    a.classList.add("dropdown-item");
    if (i % 2 == 0) {
      a.classList.add("even");
    } else {
      a.classList.add("odd");
    }

    element.appendChild(a);
    a.addEventListener("click", function () {
      unitValue = this.innerHTML;
      myFunction("unitdropdown");
      display = document.getElementById(
        "oracle-modal-form1-select2-hidden-field3"
      );
      display.innerText = unitValue;
    });
  }

  // document.getElementById('oracle-modal-form1-select2-hidden-field1').placeholder = new_placeholder
  // document.getElementById('oracle-modal-form1-select2-hidden-field2').placeholder = new_placeholder
  // document.getElementById('oracle-modal-form2-select2-hidden-field1').placeholder = new_placeholder
  // document.getElementById('oracle-modal-form2-select2-hidden-field2').placeholder = new_placeholder
  // if (text_to_add == ""){
  //   alert("please enter a valid text");
  //   return false;
  // }
  // myFunction(dropdown_id);
  // id =  document.getElementById(dropdown_id).previousElementSibling.id
  // display = document.getElementById(id);
  // display.innerText = text_name
}

function createDropdown(text, dropdown_id) {
  if (dropdown_id === "myDropdown2") {
    document.getElementById(
      "oracle-modal-form2-select2-hidden-field1"
    ).innerHTML = "Start Range";
    document.getElementById(
      "oracle-modal-form2-select2-hidden-field2"
    ).innerHTML = "End Range";
    $("#dropdownstartoracle2").empty();
    $("#dropdownendoracle2").empty();

    //fetching the url for the given text_name and using the dictionary, containing the sections, create a dropdown.
    $.get(
      "/select/sections/" + text + "/" + languageselected + "/",
      function (data) {
        let elementS = document.getElementById("dropdownstartoracle2");
        let elementE = document.getElementById("dropdownendoracle2");

        elementS.innerHTML =
          '<input type="text" autocomplete="off" placeholder="Search..." id="start2" onkeyup="filterFunction(`start2`,`dropdownstartoracle2`)">';
        elementE.innerHTML =
          '<input type="text" autocomplete="off" placeholder="Search..." id="end2" onkeyup="filterFunction(`end2`,`dropdownendoracle2`)">';

        keyholder = [];
        for (var key in data) {
          if (key == "start" || key == "end") {
          } else {
            keyholder.push(key);
          }
        }
        holdsectiondata = keyholder.sort(sortAlphaNum);
        holdsectiondata.push("end");
        holdsectiondata.unshift("start");
        console.log(holdsectiondata);

        console.log(elementS);
        for (var i = 0; i < holdsectiondata.length; i++) {
          let a = document.createElement("a");
          let b = document.createElement("a");

          key = holdsectiondata[i];

          a.innerHTML = key;
          b.innerHTML = key;

          a.id = key + dropdown_id + "s";
          b.id = key + dropdown_id + "e";

          a.classList.add("dropdown-item");
          b.classList.add("dropdown-item");
          if (key % 2 == 0) {
            a.classList.add("even");
            b.classList.add("even");
          } else {
            a.classList.add("odd");
            b.classList.add("odd");
          }

          elementS.appendChild(a);
          elementE.appendChild(b);
          // console.log(key);

          //end section button onclick function
          b.addEventListener("click", function () {
            sectionto2 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            myFunction("dropdownendoracle2");
            display = document.getElementById(
              "oracle-modal-form2-select2-hidden-field2"
            );
            display.innerText = sectionto2;
          });
          //start section button onclick function
          a.addEventListener("click", function () {
            sectionfrom2 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            myFunction("dropdownstartoracle2");
            display = document.getElementById(
              "oracle-modal-form2-select2-hidden-field1"
            );
            display.innerText = sectionfrom2;
          });
        }
      }
    );
  } else {
    document.getElementById(
      "oracle-modal-form1-select2-hidden-field1"
    ).innerHTML = "Start Range";
    document.getElementById(
      "oracle-modal-form1-select2-hidden-field2"
    ).innerHTML = "End Range";
    $("#dropdownstartoracle").empty();
    $("#dropdownendoracle").empty();
    //fetching the url for the given text_name and using the dictionary, containing the sections, create a dropdown.
    $.get(
      "/select/sections/" + text + "/" + languageselected + "/",
      function (data) {
        let elementS = document.getElementById("dropdownstartoracle");
        let elementE = document.getElementById("dropdownendoracle");

        elementS.innerHTML =
          '<input type="text" autocomplete="off" placeholder="Search..." id="start" onkeyup="filterFunction(`start`,`dropdownstartoracle`)">';
        elementE.innerHTML =
          '<input type="text" autocomplete="off" placeholder="Search..." id="end" onkeyup="filterFunction(`end`,`dropdownendoracle`)">';

        keyholder = [];
        for (var key in data) {
          if (key == "start" || key == "end") {
          } else {
            keyholder.push(key);
          }
        }

        holdsectiondata = keyholder.sort(sortAlphaNum);
        holdsectiondata.push("end");
        holdsectiondata.unshift("start");
        console.log(holdsectiondata);

        console.log(elementS);
        for (var i = 0; i < holdsectiondata.length; i++) {
          let a = document.createElement("a");
          let b = document.createElement("a");

          key = holdsectiondata[i];

          a.innerHTML = key;
          b.innerHTML = key;

          a.id = key + "s";
          b.id = key + "e";

          a.classList.add("dropdown-item");
          b.classList.add("dropdown-item");
          if (key % 2 == 0) {
            a.classList.add("even");
            b.classList.add("even");
          } else {
            a.classList.add("odd");
            b.classList.add("odd");
          }

          elementS.appendChild(a);
          elementE.appendChild(b);
          // console.log(key);

          //end section button onclick function
          b.addEventListener("click", function () {
            sectionto1 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            myFunction("dropdownendoracle");
            display = document.getElementById(
              "oracle-modal-form1-select2-hidden-field2"
            );
            display.innerText = sectionto1;
          });
          //start section button onclick function
          a.addEventListener("click", function () {
            sectionfrom1 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            myFunction("dropdownstartoracle");
            display = document.getElementById(
              "oracle-modal-form1-select2-hidden-field1"
            );
            display.innerText = sectionfrom1;
          });
        }
      }
    );
  }
}

// https://stackoverflow.com/questions/4340227/sort-mixed-alpha-numeric-array  <- source for the belowe used method

var reA = /[^a-zA-Z]/g;
var reN = /[^0-9]/g;
function sortAlphaNum(a, b) {
  var AInt = parseInt(a, 10);
  var BInt = parseInt(b, 10);

  if (isNaN(AInt) && isNaN(BInt)) {
    var aA = a.replace(reA, "");
    var bA = b.replace(reA, "");
    if (aA === bA) {
      var aN = parseInt(a.replace(reN, ""), 10);
      var bN = parseInt(b.replace(reN, ""), 10);
      return aN === bN ? 0 : aN > bN ? 1 : -1;
    } else {
      return aA > bA ? 1 : -1;
    }
  } else if (isNaN(AInt)) {
    //A is not an Int
    return 1; //to make alphanumeric sort first return -1 here
  } else if (isNaN(BInt)) {
    //B is not an Int
    return -1; //to make alphanumeric sort first return 1 here
  } else {
    return AInt > BInt ? 1 : -1;
  }
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
    document.getElementById("page-buttons-oracle").style.marginTop = "-30px";
  } else {
    prev.disabled = false;
    open2.style.display = "";
    open1.style.display = "none";
    if (len2 <= 3) {
      next.disabled = true;
    } else {
      next.disabled = false;
    }
    document.getElementById("page-buttons-oracle").style.marginTop = "-50px";
  }
  // fix next button
  if (n == x.length - 1) {
    next.innerHTML = '<i class="fas fa-check"></i>';
  } else {
    next.innerHTML = '<i class="fas fa-angle-double-right"></i>';
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n + 1);
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
    knowntexts = knowntexts.toString().replace(",", "+");
    known_starts = known_starts.toString().replace(",", "+");
    known_ends = known_ends.toString().replace(",", "+");

    etexts = etexts.toString().replace(",", "+");
    estarts = estarts.toString().replace(",", "+");
    eends = eends.toString().replace(",", "+");
    eunits = eunits.toString().replace(",", "+");
    e_section_size = e_section_size.toString().replace(",", "+");

    window.location.href =
      window.location.href +
      "/result/" +
      etexts +
      "/" +
      estarts +
      "/" +
      eends +
      "/" +
      eunits +
      "/" +
      e_section_size +
      "/" +
      knowntexts +
      "/" +
      known_starts +
      "-" +
      known_ends +
      "/";
    return false;
  }
  // Otherwise, display the correct tab:
  showTabOracle(currentTab, next);
}

// This function is the same as in select-vocab-step-form.js
function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

// buttons
$("#myNext-oracle").click(function () {
  nextPrevOracle(1, true);
});

$("#myPrev-oracle").click(function () {
  nextPrevOracle(-1, false);
});

/*
SELECT WORK modal & table
*/

// delete row from table
function deleteRowOracle(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("oracle-result-table1");
  etexts.splice(i - 3, 1);
  estarts.splice(i - 3, 1);
  eends.splice(i - 3, 1);
  eunits.splice(i - 3, 1);
  e_section_size.splice(i - 3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3) {
    document.getElementById("myNext-oracle").disabled = true;
  }
}

// yes triggers hidden fields
$("#oracle-modal-form1-select2").change(function () {
  if ($(this).val() == "yes") {
    $("#oracle-modal-form1-select2-hidden-div").show();
  } else {
    $("#oracle-modal-form1-select2-hidden-div").hide();
  }
});
$("#oracle-modal-form1-select2").trigger("change");

// modal save
$("#oracle-modal-form2-save").click(function () {
  // if showing select value is good enough
  // var book = $('#select-text #select1').val().trim();

  // if showing select label is better than value

  var book = text_to_add;
  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }
  selectionvalue = $("#oracle-modal-form2-select2").val();
  if (selectionvalue == "yes") {
    console.log("start: " + sectionfrom2);
    console.log("end: " + sectionto2);
    if (sectionfrom2 == "end" || sectionto2 == "start") {
      alert("please select a valid range");
      return false;
    } else if (sectionto2 == "end" || sectionfrom2 == "start") {
      var sections = `${sectionfrom2}-${sectionto2}`;
    } else if (!isNaN(sectionto2) && !isNaN(sectionfrom2)) {
      console.log("both floats");
      if (
        Number(sectionfrom2) > Number(sectionto2) ||
        Number(sectionto2) === Number(sectionfrom2)
      ) {
        alert("please select a valid range");
        return false;
      } else {
        var sections = `${sectionfrom2}-${sectionto2}`;
      }
    } else if (!isNaN(sectionto2) || !isNaN(sectionfrom2)) {
      console.log("one float");
      if (sectionfrom2 > sectionto2 || sectionto2 === sectionfrom2) {
        alert("please select a valid range");
        return false;
      } else {
        var sections = `${sectionfrom2}-${sectionto2}`;
      }
    } else {
      console.log("else clause");
      var sections = `${sectionfrom2}-${sectionto2}`;
    }
  } else {
    var sections = `${sectionfrom2}-${sectionto2}`;
  }

  // show the selection in a table
  var table = document.getElementById("oracle-result-table2");
  knowntexts.push(string_to_slug(book));
  known_starts.push(sectionfrom2);
  known_ends.push(sectionto2);
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = '<span style="color:white">' + book + "</span>";
  cell2.innerHTML = '<span style="color:white">' + sections + "</span>";
  cell3.innerHTML =
    '<button class="btn" onclick="deleteRowOracle2(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
  // hide modal when save
  $("#oracle-define-vocab").modal("hide");
  // reset form values
  document.getElementById(
    "oracle-modal-form2-select2-hidden-field1"
  ).innerText = "Start Range";
  document.getElementById(
    "oracle-modal-form2-select2-hidden-field2"
  ).innerText = "End Range";
  
  document.getElementById("oracle-modal-form2").reset();
  $("#oracle-modal-form2-select2-hidden-div").hide();

  $("#dropdownstartoracle2").empty();
  $("#dropdownendoracle2").empty();
  document.getElementById("chosen_text2").innerText = "Select Text";
  sectionfrom1 = "start";
  sectionto1 = "end";
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
    document.getElementById("computer").style.display = "";
  }
}

function hideComputer(x) {
  if (x.checked) {
    document.getElementById("computer").style.display = "none";
    document.getElementById("bridge").style.display = "";
  }
}

// delete row from table
function deleteRowOracle2(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("oracle-result-table2");
  knowntexts.splice(i - 3, 1);
  known_starts.splice(i - 3, 1);
  known_ends.splice(i - 3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3) {
    document.getElementById("myNext-oracle").disabled = true;
  }
}

// yes triggers hidden fields
$("#oracle-modal-form2-select2").change(function () {
  if ($(this).val() == "yes") {
    $("#oracle-modal-form2-select2-hidden-div").show();
  } else {
    $("#oracle-modal-form2-select2-hidden-div").hide();
  }
});
$("#oracle-modal-form2-select2").trigger("change");

// modal save
$("#oracle-modal-form1-save").click(function () {
  // if showing select value is good enough
  // var book = $('#select-text #select1').val().trim();

  // if showing select label is better than value

  var book = text_to_add;
  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }
  console.log("start: " + sectionfrom1);
  console.log("end: " + sectionto1);
  if (sectionfrom1 == "end" || sectionto1 == "start") {
    alert("please select a valid range");
    return false;
  } else if (sectionto1 == "end" || sectionfrom1 == "start") {
    var sections = `${sectionfrom1}-${sectionto1}`;
  } else if (!isNaN(sectionto1) && !isNaN(sectionfrom1)) {
    console.log("both floats");
    if (
      Number(sectionfrom1) > Number(sectionto1) ||
      Number(sectionto1) === Number(sectionfrom1)
    ) {
      alert("please select a valid range");
      return false;
    } else {
      var sections = `${sectionfrom1}-${sectionto1}`;
    }
  } else if (!isNaN(sectionto1) || !isNaN(sectionfrom1)) {
    console.log("one float");
    if (sectionfrom1 > sectionto1 || sectionto1 === sectionfrom1) {
      alert("please select a valid range");
      return false;
    } else {
      var sections = `${sectionfrom1}-${sectionto1}`;
    }
  } else {
    console.log("else clause");
    var sections = `${sectionfrom1}-${sectionto1}`;
  }

  var size = $("#oracle-modal-form1-select2-hidden-field4").val();

  if (size) {
    // if user specifies a section
    var size = `${size}`;
  } else {
    var size = "9";
  }
  console.log(size);
  etexts.push(string_to_slug(book));
  estarts.push(sectionfrom1);
  eends.push(sectionto1);
  eunits.push(unitValue);
  e_section_size.push(size);

  // show the selection in a table
  sections = sectionfrom1 + " - " + sectionto1 + "; " + size;
  var table = document.getElementById("oracle-result-table1");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = '<span style="color:white">' + book + "</span>";
  cell2.innerHTML = '<span style="color:white">' + sections + "</span>";
  cell3.innerHTML =
    '<button class="btn" onclick="deleteRowOracle(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
  // hide modal when save
  $("#oracle-select-text").modal("hide");
  //document.getElementById("computer").style.display="none";
  //document.getElementById("bridge").style.display="none";
  // reset form values
  document.getElementById(
    "oracle-modal-form1-select2-hidden-field1"
  ).innerText = "Start Range";
  document.getElementById(
    "oracle-modal-form1-select2-hidden-field2"
  ).innerText = "End Range";
  document.getElementById(
    "oracle-modal-form1-select2-hidden-field3"
  ).innerHTML = "Select Unit";
  document.getElementById("oracle-modal-form1").reset();
  $("#oracle-modal-form1-select2-hidden-div").hide();
  $("#dropdownstartoracle").empty();
  $("#dropdownendoracle").empty();
  $("#unitdropdown").empty();
  document.getElementById("chosen_text").innerText = "Select Text";
  sectionfrom1 = "start";
  sectionto1 = "end";
  // enable 'next' button
  document.getElementById("myNext-oracle").disabled = false;
});

// from: https://gist.github.com/codeguy/6684588. modified to make whitespace a _ instead of a -
function string_to_slug(str) {
  str = str.replace(/^\s+|\s+$/g, ""); // trim
  str = str.toLowerCase();

  // remove accents, swap ñ for n, etc
  var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to = "aaaaeeeeiiiioooouuuunc      ";
  for (var i = 0, l = from.length; i < l; i++) {
    str = str.replace(new RegExp(from.charAt(i), "g"), to.charAt(i));
  }

  str = str
    .replace(/[^a-z0-9 -]/g, "") // remove invalid chars
    .replace(/\s+/g, "_"); // collapse whitespace and replace by _

  return str;
}
