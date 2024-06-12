//console.log(time_targets[0]);
var time_targets = document.getElementsByClassName('deadline');
var deadlines = [];
for (var i = 0; i < time_targets.length; i++) {
    deadlines[i] = new Date(time_targets[i].innerHTML * 1000);
}
function deadline_count() {
    var now = new Date();
    for (var i = 0; i < time_targets.length; i++) {
        var time_target = time_targets[i];
        //var utc = new Date(now.getTime() + (now.getTimezoneOffset() * 60000));
        //console.log(deadline);
        //console.log(utc.getTime());
        //var deadlines[i] = new Date(time_target.innerHTML * 1000);

        var seconds = (now.getTime() - deadlines[i].getTime()) / 1000;
        if (isNaN(seconds)) {
            time_target.innerHTML = '';
            continue;
        }
        // get total seconds between the times
        var difference = Math.abs(deadlines[i] - now) / 1000;

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
}
setInterval(deadline_count, 1000);
window.onload = deadline_count;