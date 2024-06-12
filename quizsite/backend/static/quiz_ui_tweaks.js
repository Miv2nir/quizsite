//colors
let colors = ['#e1223c', '#1268ce', '#ffa602', '#25890c'];

var form = document.getElementById('id_user_response');
//set the class to a grid
form.classList.add('grid');
form.classList.add('smaller');
form.style.gap = '0.3rem';
form.style.columnGap = '1.5rem';
form.parentElement.style.paddingRight = '1.2rem';
//remove the gap in content row center elements
for (var i = 0; i < form.childElementCount; i++) {
    var option = form.children[i].getElementsByTagName('label')[0];
    option.style.gap = '0';
    option.classList.add('quiz-button');
    option.style.backgroundColor = colors[i % 4];
    option.style.borderColor = colors[i % 4];

    console.log(option);
}
//console.log(form);