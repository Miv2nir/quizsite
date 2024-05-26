//grab the input field of interest
var thing = document.getElementById('json_input');
console.log(thing);
//get dict
var choices = JSON.parse(thing.textContent);
console.log(choices);
var html_text_template = '<div class="content center row">\
<input type="checkbox" disabled="disabled" class="checkbox-editor">\
<input value="" placeholder="Answer Choice" class="form-field" required id>\
</div>';
for (var i in choices) {
    var html_list_items = document.createElement('div');
    html_list_items.innerHTML = html_text_template;
    html_list_items.id = "option-" + i.toString();
    var html_list_field = html_list_items.getElementsByClassName('form-field')[0]
    html_list_field.value = choices[i];
    var html_list_container = document.getElementById('choices-container');
    html_list_container.appendChild(html_list_items);
    //console.log(html_list_items);
    //for each, create an html list element with the prompt to enter text
    //on change, update json
    //also need to serialize and package with the form somehow

    //multiple selection: checkbox
    //singlular selection: radio & group (group defined through name="")
}
