

//setInterval(output, 1000, sidebar.clientWidth);

//var target_width = window.innerWidth - sidebar.clientWidth;
//setInterval(output, 1000, window, sidebar);
//var sidebar = document.getElementsByClassName('sidebar')[0];
function width_update() {
    var assignments_list = document.getElementsByClassName('assignments-list')[0];
    var assignments_grid = document.getElementsByClassName('assignments-grid')[0];
    var sidebar = document.getElementsByClassName('sidebar')[0];
    var precalc = Math.min(((window.innerWidth - sidebar.clientWidth - 40) / 20), 63);
    var target_width = precalc.toString() + "rem";
    var target_width_2 = (precalc + 0.9).toString() + "rem";
    assignments_list.style.maxWidth = target_width;
    assignments_grid.style.maxWidth = target_width;
    console.log(target_width, assignments_list.clientWidth);
    requestAnimationFrame(width_update);
}
//window.addEventListener("resize", width_update);
//window.addEventListener("load", width_update);
//sidebar.addEventListener("mouseover", width_update);
//setInterval(width_update, 1)
window.addEventListener('load', width_update);
