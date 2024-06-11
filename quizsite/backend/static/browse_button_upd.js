var input_box = document.getElementById('id_user_response');
var submit_button = document.getElementById('form-button');
input_box.onchange = function () { submit_button.innerHTML = 'Submit Answer'; };