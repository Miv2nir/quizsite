

//setInterval(output, 1000, sidebar.clientWidth);

//var target_width = window.innerWidth - sidebar.clientWidth;
//setInterval(output, 1000, window, sidebar);
//var sidebar = document.getElementsByClassName('sidebar')[0];
function width_update() {
    var assignments_list = document.getElementsByClassName('assignments-list')[0];
    var sidebar = document.getElementsByClassName('sidebar')[0];
    var target_width = (window.innerWidth - sidebar.clientWidth - 40).toString() + "px";
    assignments_list.style.maxWidth = target_width;
    console.log(target_width, assignments_list.clientWidth);
    requestAnimationFrame(width_update);
}
//window.addEventListener("resize", width_update);
//window.addEventListener("load", width_update);
//sidebar.addEventListener("mouseover", width_update);
//setInterval(width_update, 1)
window.addEventListener('load', width_update);
