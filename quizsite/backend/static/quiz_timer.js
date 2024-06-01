
var now = new Date().getTime() / 1000;
var passed_time = Math.floor(now - initial);
function countdown() {
    now = new Date().getTime() / 1000;
    localStorage.setItem('initial', initial);
    localStorage.setItem('now', now);
    passed_time = Math.floor(now - initial);
    console.log(passed_time);
    if (passed_time >= wait) {
        console.log(true);
        window.location.replace('/courses/quiz_test/browse/' + page_next.toString() + '/')
    }
};


var wait = 15;

var page_number = document.getElementById('current_page_number').innerHTML;


var page_next = document.getElementById('page_next_number').innerHTML;
console.log(localStorage.getItem('page_number_old'), page_number);
if (localStorage.getItem('page_number_old') == page_number) {
    var initial = localStorage.getItem('initial');
}
else {
    localStorage.removeItem('initial');
    var initial = new Date().getTime() / 1000;
}
localStorage.setItem('page_number_old', page_number);

setInterval(countdown, 1000);



