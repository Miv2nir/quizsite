var time_target = document.getElementById('timestamp');
console.log(time_target.innerHTML);
var deadline = new Date(time_target.innerHTML * 1000);
function deadline_count() {
    var now = new Date();
    var utc = new Date(now.getTime() + (now.getTimezoneOffset() * 60000));
    //console.log(deadline);
    //console.log(utc.getTime());
    var seconds = (now.getTime() - deadline.getTime()) / 1000;
    time_target.innerHTML = new Date(seconds * 1000).toISOString().substring(11, 19);
}
setInterval(deadline_count, 1000);
window.onload = deadline_count;