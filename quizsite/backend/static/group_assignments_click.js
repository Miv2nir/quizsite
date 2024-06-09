var field = document.getElementById('id_course');
console.log(field);

function fill_course_name(item) {
    var t = item.getElementsByClassName('course-text')[0];
    console.log(t.innerHTML);
    field.value = t.innerHTML;
}