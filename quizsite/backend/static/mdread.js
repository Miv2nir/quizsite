window.onload = function () {
    var id = 'mdtext';
    var el = document.getElementById(id);
    var text = el.textContent;
    console.log(text);
    showdown.setOption('strikethrough', 'true');
    showdown.setOption('tables', 'true');
    showdown.setOption('underline', 'true');
    var converter = new showdown.Converter(),
        html = converter.makeHtml(text);
    console.log(html);
    el.innerHTML = html;
    //TODO: XSS filtering;
}