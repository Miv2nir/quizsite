var timer_target = document.getElementById('timer');
timer_target.style.display = 'block';

//var answer_form = document.getElementById('answer_form');
var answer_form = document.forms[0];

var now = new Date().getTime() / 1000;
var passed_time = Math.floor(now - initial);
function countdown() {
    now = new Date().getTime() / 1000;
    localStorage.setItem('initial', initial);
    localStorage.setItem('now', now);
    passed_time = Math.floor(now - initial);
    timer_target.innerHTML = 'Time left: ' + (wait - passed_time).toString();
    console.log(passed_time);
    console.log(localStorage.getItem('form_submitted'));
    if (passed_time >= wait) {
        console.log(true);
        //console.log(submitted_test);
        //if (localStorage.getItem('form_submitted') == 'true') {
        //    localStorage.setItem('form_submitted', false);
        //    window.location.replace(redir_target);
        //}
        answer_form.submit();
    }

};


/*function form_submit_flag() {
    localStorage.setItem('form_submitted', true);
}
*/
var wait = parseInt(document.getElementById('quiz_time').innerHTML);


//localStorage.setItem('form_submitted', false);

var page_number = document.getElementById('current_page_number').innerHTML;


var page_next = document.getElementById('page_next_number').innerHTML;
var course_name = document.getElementById('current_course_name').innerHTML;
console.log(localStorage.getItem('page_number_old'), page_number);
if (localStorage.getItem('page_number_old') == page_number) {
    var initial = localStorage.getItem('initial');
}
else {
    localStorage.removeItem('initial');
    var initial = new Date().getTime() / 1000;
}
localStorage.setItem('page_number_old', page_number);
if (page_number == page_next) {
    var redir_target = '/courses/' + course_name + '/';
}
else {

    var redir_target = '/courses/' + course_name + '/browse/' + page_next.toString() + '/';
}

setInterval(countdown, 1000);
//addEventListener("submit", form_submit_flag);
window.onload = countdown;
