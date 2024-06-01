var timer_target = document.getElementById('timer');
timer_target.style.display = 'block';

var now = new Date().getTime() / 1000;
var passed_time = Math.floor(now - initial);
function countdown() {
    now = new Date().getTime() / 1000;
    localStorage.setItem('initial', initial);
    localStorage.setItem('now', now);
    passed_time = Math.floor(now - initial);
    timer_target.innerHTML = 'Time left: ' + (wait - passed_time).toString();
    console.log(passed_time);
    if (passed_time >= wait) {
        console.log(true);
        window.location.replace(redir_target);
    }
};


var wait = 15;

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
window.onload = countdown;


