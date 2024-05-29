function del_page_item(item) {
    //1. hide the main main (lol)
    //2. show the warn main
    //3. pass the page number down to where it belongs
    console.log(item.value);
    var main1 = document.getElementById('main');
    main1.style.display = "none";
    var main2 = document.getElementById('warn');
    main2 = document.style.display = "inline";
}