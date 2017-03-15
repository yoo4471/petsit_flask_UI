
function onClicked(elem) {
  if(elem.id == "create_using_email_button") {
    var signup_select = document.getElementById("signup-select");
    var signup_email = document.getElementById("signup-email");
    signup_select.classList.add('hide');
    signup_email.classList.remove('hide');
  }

}


function onClicked_Plus(elem) {
  var value = parseInt(document.getElementById('input_number_of_room').value, 10);
  value = isNaN(value) ? 0 : value;
  value++;
  document.getElementById('input_number_of_room').value = value;
  document.getElementById("span_number_of_room").innerHTML="방 " + value + '개';

}

function onClicked_Minus(elem) {
  alert("Hello! I am an alert box!!");
  var value = parseInt(document.getElementById('input_number_of_room').value, 10);
  value = isNaN(value) ? 0 : value;
  if(value > 0) {
    value--;
    document.getElementById('input_number_of_room').value = value;
    document.getElementById("span_number_of_room").innerHTML="방 " + value + '개';
  }
}

function onClicked_profile(elem) {
  console.log(elem);
  elem.setAttribute("aria-selected",true)

}
// object.setAttribute("aria-selected",value);var value = object.getAttribute("aria-selected");
