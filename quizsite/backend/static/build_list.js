//grab the input field of interest
var thing = document.getElementById('json_input');
console.log(thing);
//get dict
var choices = JSON.parse(thing.textContent);
console.log(choices);
for (var i in choices) {
    console.log(choices[i]);
}