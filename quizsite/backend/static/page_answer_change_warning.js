//1. Save the state of the page form
//2. On change, if it no longer matches with the saved value, warn about the data loss
//3. If we change back to it, hide the warning

const answer_type_el = document.getElementById('answer_type');
var answer_type_val = answer_type_el.options[answer_type_el.selectedIndex].text;
console.log(answer_type_val);

function displayWarning() {
    var el = document.getElementById('warning');
    var answer_type_el_2 = document.getElementById('answer_type');
    var answer_type_val_2 = answer_type_el_2.options[answer_type_el_2.selectedIndex].text;
    check = answer_type_val_2 === answer_type_val;
    if (check) {
        el.style.display = 'none';
    }
    else {
        el.style.display = 'block';
    }
};

//answer_type.addEventListener("input", displayWarning());



