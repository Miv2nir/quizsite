function render_list_item(i, data) {
    var html_list_items = document.createElement('div');
    html_list_items.classList.add('content');
    html_list_items.classList.add('center');
    html_list_items.classList.add('row');
    html_list_items.innerHTML = html_text_template;
    html_list_items.id = "option-" + i.toString();
    var html_list_field = html_list_items.getElementsByClassName('form-field')[0];
    html_list_field.value = data;
    var html_list_container = document.getElementById('choices-container');
    html_list_container.appendChild(html_list_items);
}
//grab the input field of interest
var thing = document.getElementById('json_input');
//console.log(thing);
//get dict
console.log(option_type);
var choices = JSON.parse(thing.textContent);
//console.log(choices);
if (option_type === "M") {
    var html_text_template = '<input type="checkbox" disabled="disabled" class="checkbox-editor">\
<input value="" placeholder="Answer Choice" class="form-field" onchange="upd_list_item(this);" required>\
<button type="button" class="list-delete-button" onclick="del_list_item(this);">-</button>';
}
for (var i in choices) {
    render_list_item(i, choices[i]);
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

    write_result(choices);
}
function upd_list_item(item) {
    var pos = parseInt(item.parentElement.id.split("-")[1]);
    choices[pos] = item.value;
    console.log(choices);

    write_result(choices);
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
