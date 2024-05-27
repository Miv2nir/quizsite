function render_list_item(i, data, correct) {
    console.log(correct);
    var html_list_items = document.createElement('div');
    html_list_items.classList.add('content');
    html_list_items.classList.add('center');
    html_list_items.classList.add('row');
    html_list_items.innerHTML = html_text_template;
    html_list_items.id = "option-" + i.toString();
    var html_list_field = html_list_items.getElementsByClassName('form-field')[0];
    html_list_field.value = data;
    var html_list_checkbox = html_list_items.getElementsByClassName('checkbox-editor')[0];
    html_list_checkbox.checked = correct;
    var html_list_container = document.getElementById('choices-container');
    html_list_container.appendChild(html_list_items);
}
//grab the input field of interest
var thing = document.getElementById('json_input');
var verify = document.getElementById('json_check');
//console.log(thing);
//get dict
//console.log(verify);
var choices = JSON.parse(thing.textContent);
console.log(thing.textContent);
console.log(verify.textContent);
var correct_choices = JSON.parse(verify.textContent);
console.log(correct_choices);
if (option_type === "M") {
    var html_text_template = '<input type="checkbox" class="checkbox-editor" onclick="upd_list_correctness(this);">\
<input value="" placeholder="Answer Choice" class="form-field" onchange="upd_list_item(this);" required>\
<button type="button" class="list-delete-button" onclick="del_list_item(this);">-</button>';
}

if (option_type === "S") {
    var html_text_template = '<input type="radio" name="choices-radio" class="checkbox-editor" onclick="upd_r_list_correctness(this);">\
    <input value="" placeholder="Answer Choice" class="form-field" onchange="upd_list_item(this);" required>\
    <button type="button" class="list-delete-button" onclick="del_list_item(this);">-</button>';
    var i = Object.keys(correct_choices)[0];
    console.log(JSON.parse('{"' + i.toString() + '":"' + correct_choices[i] + '"}'));
    correct_choices = JSON.parse('{"' + i.toString() + '":"' + correct_choices[i] + '"}');
    write_c_result(correct_choices);
}
for (var i in choices) {
    console.log(i);
    render_list_item(i, choices[i], correct_choices[i]);
    //console.log(html_list_items);
    //for each, create an html list element with the prompt to enter text (done)
    //on change, update json
    //also need to serialize and package with the form somehow

    //multiple selection: checkbox
    //singlular selection: radio & group (group defined through name="")
}
function del_list_item(item) {
    var pos = parseInt(item.parentElement.id.split("-")[1]);
    console.log(choices[pos]);
    item.parentElement.remove(); //delete rendered list item
    delete choices[pos]; //delete respective json item
    delete correct_choices[pos];

    write_result(choices);
    write_c_result(correct_choices);
}
function upd_list_item(item) {
    var pos = parseInt(item.parentElement.id.split("-")[1]);
    choices[pos] = item.value;
    console.log(choices);

    write_result(choices);
}

function upd_list_correctness(item) {
    var pos = parseInt(item.parentElement.id.split("-")[1]);
    console.log(pos);
    if (item.checked == true) {
        correct_choices[pos] = "True";
    }
    else {
        delete correct_choices[pos];
    }
    write_c_result(correct_choices);
}
function upd_r_list_correctness(item) {
    var pos = parseInt(item.parentElement.id.split("-")[1]);
    console.log(pos);
    if (item.checked == true) {
        correct_choices = {};
        correct_choices[pos] = "True";
    }
    else {
        delete correct_choices[pos];
    }
    write_c_result(correct_choices);
}


function add_list_item(item) {
    //pos = document.getElementById('choices-container').childElementCount + 1;

    //var pos = parseInt(item.parentElement.id.split("-")[1]) + 1;
    var l = Object.keys(choices).length - 1;
    if (l === -1) {
        var pos = 0;
    }
    else {
        var pos = parseInt(Object.keys(choices)[l]) + 1;
    }
    choices[pos] = 'Choice ' + (pos + 1).toString();
    console.log(choices);
    render_list_item(pos, choices[pos]);

    write_result(choices);
}
function write_result(choices) {
    thing.textContent = JSON.stringify(choices);
}
function write_c_result(correct_choices) {
    verify.textContent = JSON.stringify(correct_choices);
}
