function countdown() {
    var now = new Date().getTime() / 1000;
    var passed_time = Math.floor(now - initial);
    console.log(passed_time);
    if (passed_time >= wait) {
        console.log(true);
        window.location.replace('/courses/quiz_test/browse/' + page_next.toString() + '/')
    }
};

var page_next = document.getElementById('page_next_number').innerHTML;
console.log(page_next);

var initial = new Date().getTime() / 1000;
var wait = 10;
setInterval(countdown, 1000);



