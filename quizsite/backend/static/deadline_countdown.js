var time_target = document.getElementById('timestamp');
console.log(time_target.innerHTML);
var deadline = new Date(time_target.innerHTML * 1000);
function deadline_count() {
    var now = new Date();
    var utc = new Date(now.getTime() + (now.getTimezoneOffset() * 60000));
    //console.log(deadline);
    //console.log(utc.getTime());
    var seconds = (now.getTime() - deadline.getTime()) / 1000;
    // get total seconds between the times
    var difference = Math.abs(deadline - now) / 1000;

    // calculate (and subtract) whole days
    var d = Math.floor(difference / 86400);
    difference -= d * 86400;

    // calculate (and subtract) whole hours
    var h = Math.floor(difference / 3600) % 24;
    difference -= h * 3600;

    // calculate (and subtract) whole minutes
    var m = Math.floor(difference / 60) % 60;
    difference -= m * 60;

    // what's left is seconds
    var s = Math.floor(difference % 60);

    output = '';
    if (d) {
        output += d.toString() + ' days ';
    }
    if (h) {
        output += h.toString() + ' hours ';
    }
    if (m) {
        output += m.toString() + ' minutes ';
    }
    if (s) {
        output += s.toString() + ' seconds';
    }
    console.log(seconds, Math.abs(seconds));
    if (seconds > 0) {
        time_target.style.color = 'red';
        output = 'Overdue by ' + output;
    }
    else {
        output += ' left';
    }
    //time_target.innerHTML = new Date(Math.abs(seconds) * 1000).toISOString().substring(11, 19);
    time_target.innerHTML = output;
}
setInterval(deadline_count, 1000);
window.onload = deadline_count;