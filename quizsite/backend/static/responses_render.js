const n_pages = parseInt(document.getElementById('n_pages').innerHTML);

function render_list_item(i, correct, html_text_template, target) { //reused from build_list
    if (correct == null) { correct = false };
    //console.log(correct);
    var html_list_items = document.createElement('div');
    html_list_items.classList.add('content');
    html_list_items.classList.add('center');
    html_list_items.classList.add('row');
    html_list_items.innerHTML = html_text_template;
    html_list_items.name = "option-" + i.toString();
    var html_list_checkbox = html_list_items.getElementsByClassName('checkbox-editor')[0];
    //console.log(html_list_items.getElementsByClassName('checkbox-editor')[0].innerHTML);
    html_list_checkbox.checked = correct;
    var html_list_container = target
    //console.log(responses);
    html_list_container.appendChild(html_list_items);
}

for (var i = 1; i <= n_pages; i++) {
    var responses = document.getElementById('response_' + i.toString());
    var spans = responses.getElementsByTagName('span');
    var answer_text = spans[0];
    var answer_type = spans[1];
    if (answer_type.innerHTML == 'T') {
        console.log(responses.getElementsByClassName('hide-if-t').length);
        for (var a = 0; a < responses.getElementsByClassName('hide-if-t').length; a++) {
            responses.getElementsByClassName('hide-if-t')[a].style.display = 'None';
        }
        continue;
    }
    var student_answer = spans[2];
    var correct_answer = spans[3];
    for (var a = 0; a < responses.getElementsByTagName('p').length; a++) {
        responses.getElementsByTagName('p')[a].style.display = 'None';
    }
    //console.log(answer_text);
    var choices = JSON.parse(student_answer.innerHTML);
    var correct_choices = JSON.parse(correct_answer.innerHTML);
    if (answer_type.innerHTML === "M") {
        var html_text_template = '<input type="checkbox" class="checkbox-editor" disabled>';
    }
    if (answer_type.innerHTML === "S") {
        var html_text_template = '<input type="radio" class="checkbox-editor" disabled>';
    }
    var k = Object.keys(JSON.parse(answer_text.innerHTML));
    //console.log(k);
    for (var j = 0; j < k.length; j++) {
        //correctness val sets the checked variable
        //console.log(k[j], JSON.parse(correct_answer.innerHTML)[j]);
        var found = false;
        //console.log(JSON.parse(student_answer.innerHTML));
        if (is_in(k[j], JSON.parse(student_answer.innerHTML))) {
            found = true;
        }

        target_text = responses.getElementsByClassName('choices-container')[0]; //student
        target_student = responses.getElementsByClassName('choices-container')[1]; //student
        target_correct = responses.getElementsByClassName('choices-container')[2]; //correct choices
        //manually append answer text where it needs to go
        var answer_html = document.createElement('div');
        answer_html.innerHTML = JSON.parse(answer_text.innerHTML)[k[j]];
        answer_html.style.height = '1.5rem';
        target_text.appendChild(answer_html);
        render_list_item(k[j], found, html_text_template, target_student);
        render_list_item(k[j], JSON.parse(correct_answer.innerHTML)[k[j]], html_text_template, target_correct);
    }
}

function is_in(item, values) {
    for (var i = 0; i < values.length; i++) {
        if (item === values[i]) {
            return true;
        }
    }
    return false;
}