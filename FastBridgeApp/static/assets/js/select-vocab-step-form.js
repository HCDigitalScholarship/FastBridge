/*
step form structure
source: https://www.w3schools.com/howto/howto_js_form_steps.asp
*/
var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab, true); // Display the current tab
var sourcetexts = [];
var source_starts = [];
var source_ends = [];
var in_exclude = "exclude";
var othertexts = [];
var other_starts = [];
var other_ends = [];
var text_to_add = "";
var sectionfrom1 = "start";
var sectionto1 = "end";
var sectionfrom2 = "start";
var sectionto2 = "end";
var holdsectiondata;
var languageselected;
//dropdown menu
function myFunction(dropdown_id) {
  if (dropdown_id == "myDropdown2") {
    $("#myDropdown2").show();
    $("#sectionenddropdown2").hide();
    $("#sectionstartdropdown2").hide();
  } else {
    $("#myDropdown").show();
    $("#sectionstartdropdown").hide();
    $("#sectionenddropdown").hide();
  }
}

//dropdown function for first (main) text
function dropdownSectionStart() {
  $("#sectionstartdropdown").show();
  // document.getElementById('sectionstartdropdown').classList.toggle('show');
  $("#myDropdown").hide();
  $("#sectionenddropdown").hide();
}

function dropdownSectionEnd() {
  $("#sectionenddropdown").show();
  // document.getElementById('sectionenddropdown').classList.toggle('show');
  $("#myDropdown").hide();
  $("#sectionstartdropdown").hide();
}

//dropdown function for second text
function dropdownSectionStart2() {
  $("#sectionstartdropdown2").show();
  // document.getElementById('sectionstartdropdown2').classList.toggle('show');
  $("#myDropdown2").hide();
  $("#sectionenddropdown2").hide();
}

function dropdownSectionEnd2() {
  $("#sectionenddropdown2").show();
  //   document.getElementById('sectionenddropdown2').classList.toggle('show');
  $("#myDropdown2").hide();
  $("#sectionstartdropdown2").hide();
}

function add_text(text_name, dropdown_id, depth) {
  text_to_add = text_name;
  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }

  if (window.location.href.includes("Latin")) {
    languageselected = "Latin";
  } else {
    languageselected = "Greek";
  }

  $("#" + dropdown_id).hide();
  id = document.getElementById(dropdown_id).previousElementSibling.id;
  // console.log(id);
  display = document.getElementById(id);
  $(display).change(createDropdown(text_name, dropdown_id, depth));
  display.innerText = text_name;
  console.log(document.getElementById("myInput"));
}

function createDropdown(text, dropdown_id, sections) {
  console.log(text);
  console.log(dropdown_id);
  if (dropdown_id === "myDropdown2") {
    document.getElementById(
      "bridge-modal-form2-select2-hidden-field1"
    ).innerHTML = "Start";
    document.getElementById(
      "bridge-modal-form2-select2-hidden-field2"
    ).innerHTML = "End";
    $("#sectionstartdropdown2").empty();
    $("#sectionenddropdown2").empty();

    //fetching the url for the given text_name and using the dictionary, containing the sections, create a dropdown.
    $.get(
      "/select/sections/" + text + "/" + languageselected + "/",
      function (data) {
        console.log("heds");
        console.log(data);
        let elementS = document.getElementById("sectionstartdropdown2");
        let elementE = document.getElementById("sectionenddropdown2");

        elementS.innerHTML =
          '<input type="text" class="dropdown-search" autocomplete="off" placeholder="Search..." id="start2" onkeyup="filterFunction(`start2`,`sectionstartdropdown2`)">';
        elementE.innerHTML =
          '<input type="text" class="dropdown-search" autocomplete="off" placeholder="Search..." id="end2" onkeyup="filterFunction(`end2`,`sectionenddropdown2`)">';

        let keyholder = [];
        keySectiondict = {};
        // var sorted = [];
        for (var key in data) {
          if (key == "start" || key == "end") {
          } else {
            let splitedSectionKey = key.split(".");
            splitedSectionKey = splitedSectionKey.join("");
            keyholder.push(splitedSectionKey);
            keySectiondict[splitedSectionKey] = key;
          }
        }
        keySectiondict["start"] = "start";
        keySectiondict["end"] = "end";

        keyholder.sort(sortAlphaNum);
        keyholder.push("end");
        keyholder.unshift("start");
        console.log(keyholder);

        for (var i = 0; i < keyholder.length; i++) {
          let a = document.createElement("a");
          let b = document.createElement("a");

          key = keySectiondict[keyholder[i]];

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
            $("#sectionenddropdown2").hide();
            display = document.getElementById(
              "bridge-modal-form2-select2-hidden-field2"
            );
            display.innerText = sectionto2;
          });
          //start section button onclick function
          a.addEventListener("click", function () {
            sectionfrom2 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            $("#sectionstartdropdown2").hide();
            display = document.getElementById(
              "bridge-modal-form2-select2-hidden-field1"
            );
            display.innerText = sectionfrom2;
          });
        }
      }
    );
  } else {
    document.getElementById(
      "bridge-modal-form1-select2-hidden-field1"
    ).innerHTML = "Start";
    document.getElementById(
      "bridge-modal-form1-select2-hidden-field2"
    ).innerHTML = "End";
    $("#sectionstartdropdown").empty();
    $("#sectionenddropdown").empty();
    //fetching the url for the given text_name and using the dictionary, containing the sections, create a dropdown.
    $.get(
      "/select/sections/" + text + "/" + languageselected + "/",
      function (data) {
        let elementS = document.getElementById("sectionstartdropdown");
        let elementE = document.getElementById("sectionenddropdown");

        elementS.innerHTML =
          '<input type="text" class="dropdown-search" autocomplete="off" placeholder="Search..." id="start" onkeyup="filterFunction(`start`,`sectionstartdropdown`)">';
        elementE.innerHTML =
          '<input type="text" class="dropdown-search" autocomplete="off" placeholder="Search..." id="end" onkeyup="filterFunction(`end`,`sectionenddropdown`)">';

        let keyholder = [];
        keySectiondict = {};
        // var sorted = [];
        for (var key in data) {
          if (key == "start" || key == "end") {
          } else {
            let splitedSectionKey = key.split(".");
            splitedSectionKey = splitedSectionKey.join("");
            keyholder.push(splitedSectionKey);
            keySectiondict[splitedSectionKey] = key;
          }
        }

        keyholder.sort(sortAlphaNum);
        keySectiondict["start"] = "start";
        keySectiondict["end"] = "end";

        keyholder.sort(sortAlphaNum);
        keyholder.push("end");
        keyholder.unshift("start");
        console.log(keyholder);

        for (var i = 0; i < keyholder.length; i++) {
          let a = document.createElement("a");
          let b = document.createElement("a");

          key = keySectiondict[keyholder[i]];

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
            $("#sectionenddropdown").hide();
            display = document.getElementById(
              "bridge-modal-form1-select2-hidden-field2"
            );
            display.innerText = sectionto1;
          });
          //start section button onclick function
          a.addEventListener("click", function () {
            sectionfrom1 = this.innerHTML;
            // console.log("id of the dropdown" + this.id);
            $("#sectionstartdropdown").hide();
            display = document.getElementById(
              "bridge-modal-form1-select2-hidden-field1"
            );
            display.innerText = sectionfrom1;
          });
        }
      }
    );
  }
}

//https://coderwall.com/p/5fu9xw/how-to-sort-multidimensional-array-using-javascript

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

// //https://stackoverflow.com/questions/25500316/sort-a-dictionary-by-value-in-javascript belowe function sorts in descending order
// function sort_object(obj) {
//   items = Object.keys(obj).map(function(key) {
//       return [key, obj[key]];
//   });
//   items.sort(function(first, second) {
//       return second[1] - first[1];
//   });
//   sorted_obj={}
//   $.each(items, function(k, v) {
//       use_key = v[0]
//       use_value = v[1]
//       sorted_obj[use_key] = use_value
//   })
//   return(sorted_obj)
// }

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
    document.getElementById("page-buttons").style.marginTop = "-30px";
  } else {
    prev.disabled = false;
    open2.style.display = "";
    open1.style.display = "none";
    if (len2 <= 3) {
      next.disabled = true;
    } else {
      next.disabled = false;
    }
    document.getElementById("page-buttons").style.marginTop = "-50px";
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

//hack to make a post request on submit because the input is a fake form
function post(path, parameters) {
  var form = $("<form></form>");

  form.attr("method", "post");
  form.attr("action", path);

  $.each(parameters, function (key, value) {
    if (typeof value == "object" || typeof value == "array") {
      $.each(value, function (subkey, subvalue) {
        var field = $("<input />");
        field.attr("type", "hidden");
        field.attr("name", key + "[]");
        field.attr("value", subvalue);
        form.append(field);
      });
    } else {
      var field = $("<input />");
      field.attr("type", "hidden");
      field.attr("name", key);
      field.attr("value", value);
      form.append(field);
    }
  });
  $(document.body).append(form);
  form.submit();
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
    str_sourcetexts = sourcetexts.join("+");
    str_source_starts = source_starts.join("+");
    str_source_ends = source_ends.join("+");

    str_othertexts = othertexts.join("+");
    str_other_starts = other_starts.join("+");
    str_other_ends = other_ends.join("+");

    if (in_exclude.length == 0) {
      path =
        window.location.href +
        "result/" +
        str_sourcetexts +
        "/" +
        str_source_starts +
        "-" +
        str_source_ends +
        "/" +
        "non_running" +
        "/";
    } else {
      path =
        window.location.href +
        "result/" +
        str_sourcetexts +
        "/" +
        str_source_starts +
        "-" +
        str_source_ends +
        "/" +
        in_exclude +
        "/" +
        str_othertexts +
        "/" +
        str_other_starts +
        "-" +
        str_other_ends +
        "/" +
        "non_running" +
        "/";
    }
    post(path, []);
    return;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab, next);
}

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
$("#myNext").click(function () {
  nextPrev(1, true);
});

$("#myPrev").click(function () {
  nextPrev(-1, false);
});

// events triggered by the selections of how to customize list
$("#formCheck-1").click(function () {
  document.getElementById("myNext").disabled = true;
  document.getElementById("openModal2").disabled = false;
  in_exclude = "exclude";
  console.log(in_exclude);
});

$("#formCheck-2").click(function () {
  document.getElementById("myNext").disabled = true;
  document.getElementById("openModal2").disabled = false;
  in_exclude = "include";
  console.log(in_exclude);
});

$("#formCheck-3").click(function () {
  document.getElementById("myNext").disabled = false;
  document.getElementById("openModal2").disabled = true;
  in_exclude = "";
  console.log(in_exclude);
});

/*
SELECT WORK modal &&table
*/

// delete row from table
function deleteRow(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("bridge-result-table1");
  sourcetexts.splice(i - 3, 1);
  source_starts.splice(i - 3, 1);
  source_ends.splice(i - 3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3) {
    document.getElementById("myNext").disabled = true;
  }
  document.getElementById(
    "bridge-modal-form1-select2-hidden-field1"
  ).innerText = "Start";
  document.getElementById("modal-bridge-form1").reset();
  document.getElementById(
    "bridge-modal-form1-select2-hidden-field2"
  ).innerText = "End";
  $("#sectionstartdropdown").empty();
  $("#sectionenddropdown").empty();
  document.getElementById("chosen_text").innerText = "Select Text";
  sectionfrom1 = "start";
  sectionto1 = "end";
}
//include/exclude choice

// yes triggers hidden fields
$("#bridge-modal-form1-select2").change(function () {
  if ($(this).val() == "yes") {
    $("#bridge-modal-form1-select2-hidden-div").show();
    $("#bridge-modal-form1-select2-hidden-field1").required = true;
    $("#bridge-modal-form1-select2-hidden-field2").required = true;
  } else {
    $("#bridge-modal-form1-select2-hidden-div").hide();
    $("#bridge-modal-form1-select2-hidden-field1").required = false;
    $("#bridge-modal-form1-select2-hidden-field2").required = false;
  }
});
$("#bridge-modal-form1-select2").trigger("change");

// modal 1 save. could be made a single function with a better understanding of js.
$("#bridge-modal-form1-save").click(function () {
  // if showing select value is good enough
  // var book = $('#select-text #select1').val().trim();

  // if showing select label is better than value
  var book = text_to_add;
  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }

  selectionvalue = $("#bridge-modal-form1-select2").val();
  if (selectionvalue == "yes") {
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
  } else {
    var sections = `${sectionfrom1}-${sectionto1}`;
  }
  // show the selection in a table
  var table = document.getElementById("bridge-result-table1");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = '<span style="color:white">' + book + "</span>";
  sourcetexts.push(string_to_slug(book));
  console.log(sourcetexts);
  cell2.innerHTML = '<span style="color:white">' + sections + "</span>";
  source_starts.push(sectionfrom1);
  source_ends.push(sectionto1);
  cell3.innerHTML =
    '<button class="btn" onclick="deleteRow(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
  // hide modal when save
  $("#bridge-select-text").modal("hide");
  // reset form values
  document.getElementById(
    "bridge-modal-form1-select2-hidden-field1"
  ).innerText = "Start";
  document.getElementById("modal-bridge-form1").reset();
  document.getElementById(
    "bridge-modal-form1-select2-hidden-field2"
  ).innerText = "End";
  $("#sectionstartdropdown").empty();
  $("#sectionenddropdown").empty();
  document.getElementById("chosen_text").innerText = "Select Text";
  $("input[name=textselection]").val("");
  // console.log($('input[name=textselection]').val(''));
  filterFunction("myInput", "myDropdown");
  sectionfrom1 = "start";
  sectionto1 = "end";

  $("#bridge-modal-form1-select2-hidden-div").hide();
  // enable 'next' button
  document.getElementById("myNext").disabled = false;
});

// yes triggers hidden fields
$("#bridge-modal-form2-select2").change(function () {
  if ($(this).val() == "yes") {
    $("#bridge-modal-form2-select2-hidden-div").show();
    $("#bridge-modal-form2-select2-hidden-field1").required = true;
    $("#bridge-modal-form2-select2-hidden-field2").required = true;
  } else {
    $("#bridge-modal-form2-select2-hidden-div").hide();
    $("#bridge-modal-form2-select2-hidden-field1").required = false;
    $("#bridge-modal-form2-select2-hidden-field2").required = false;
  }
});
$("#bridge-modal-form2-select2").trigger("change");

// modal 2 save
$("#bridge-modal-form2-save").click(function () {
  var book = text_to_add;
  if (text_to_add == "") {
    alert("please enter a valid text");
    return false;
  }

  selectionvalue = $("#bridge-modal-form2-select2").val();
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
  // var book = $('#bridge-change-list #bridge-modal-form2-select1').val();
  // var sectionFrom = $('#bridge-change-list #bridge-modal-form2-select2-hidden-field1').val();
  // var sectionTo =$('#bridge-change-list #bridge-modal-form2-select2-hidden-field2').val();
  // if (sectionFrom &&sectionTo){ // if user specifies a section
  //     var sections = `${sectionFrom}-${sectionTo}`;
  // }else if (!sectionFrom &&sectionTo) {
  //   var sections = `start-${sectionTo}`;
  //   sectionFrom = 'start'
  // }
  // else if (!sectionTo &&sectionFrom) {
  //   var sections = `${sectionFrom}-end`;
  //   sectionTo = 'end'
  // }
  //  else {
  //     sectionFrom = 'start'
  //     sectionTo = 'end'
  //     var sections = 'start-end';
  // }

  // show the selection in a table
  var table = document.getElementById("bridge-result-table2");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = '<span style="color:white">' + book + "</span>";
  othertexts.push(string_to_slug(book));
  cell2.innerHTML = '<span style="color:white">' + sections + "</span>";
  other_starts.push(sectionfrom2);
  other_ends.push(sectionto2);
  cell3.innerHTML =
    '<button class="btn" onclick="deleteRow(this)"><i class="fa fa-remove" style="font-size:25px;color:#e8837d;"></i></button>';
  // hide modal when save
  $("#bridge-change-list").modal("hide");
  // reset form values
  $("#bridge-change-list").find("#bridge-modal-form2")[0].reset();
  // $('#myDropdown').html("Click Me");
  document.getElementById(
    "bridge-modal-form2-select2-hidden-field1"
  ).innerText = "Start";
  document.getElementById(
    "bridge-modal-form2-select2-hidden-field2"
  ).innerText = "End";
  // document.getElementById('modal-bridge-form2').reset();
  $("#sectionstartdropdown2").empty();
  $("#sectionenddropdown2").empty();
  document.getElementById("chosen_text2").innerText = "Select Text";
  $("input[name=textselection2]").val("");
  // console.log($('input[name=textselection]').val(''));
  filterFunction("myInput2", "myDropdown2");
  sectionfrom2 = "start";
  sectionto2 = "end";
  $("#bridge-modal-form2-select2-hidden-div").hide();
  // enable 'next' button
  document.getElementById("myNext").disabled = false;
});

/*
DEFINE VOCAB modal &&table
*/

// delete row from table
function deleteRow2(r) {
  var i = r.parentNode.parentNode.rowIndex;
  var table = document.getElementById("bridge-result-table2");
  othertexts.splice(i - 3, 1);
  other_starts.splice(i - 3, 1);
  other_ends.splice(i - 3, 1);
  table.deleteRow(i);
  if (table.rows.length <= 3) {
    document.getElementById("myNext").disabled = true;
  }
  document.getElementById(
    "bridge-modal-form2-select2-hidden-field1"
  ).innerText = "Start";
  document.getElementById("modal-bridge-form2").reset();
  document.getElementById(
    "bridge-modal-form2-select2-hidden-field2"
  ).innerText = "End";
  $("#sectionstartdropdown2").empty();
  $("#sectionenddropdown2").empty();
  document.getElementById("chosen_text2").innerText = "Select Text";
  sectionfrom1 = "start";
  sectionto1 = "end";
}

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
  //.replace(/-+/g, '_'); // collapse dashes

  return str;
}
