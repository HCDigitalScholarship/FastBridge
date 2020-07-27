function myFunction(dropdown_id) {
  document.getElementById(dropdown_id).classList.toggle("show");
}

function add_text(text_name, dropdown_id, depth){
  text_to_add = text_name;
  if (text_to_add == ""){
    alert("please enter a valid text");
    return false;
  }
  myFunction(dropdown_id);
  id =  document.getElementById(dropdown_id).previousElementSibling.id
  display = document.getElementById(id);
  display.innerText = text_name
  document.getElementById("myInput").value = text_name
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
