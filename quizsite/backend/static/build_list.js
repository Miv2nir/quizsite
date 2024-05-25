//grab the input field of interest
var thing = document.getElementById('json_input');
console.log(thing);
//get dict
var choices = JSON.parse(thing.textContent);
console.log(choices);
for (var i in choices) {
    console.log(choices[i]);
    //for each, create an html list element with the prompt to enter text
    //on change, update json
    //also need to serialize and package with the form somehow
}