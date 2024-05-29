var checkbox_items = document.getElementsByName('user_response');
console.log(checkbox_items);
for (var i = 0; i < checkbox_items.length; i++) {
    checkbox_items[i].parentElement.classList.add("content");
    checkbox_items[i].parentElement.classList.add("row");
    checkbox_items[i].parentElement.classList.add("center");
}