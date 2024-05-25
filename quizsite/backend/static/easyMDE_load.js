const texts = document.getElementById('textfield');
console.log(texts.textContent);
var easymde = new EasyMDE({ element: document.getElementById('textfield') });
easymde.value(texts.textContent);

//enable resizing
var easymdefield = document.getElementsByClassName('EasyMDEContainer')[0];
var toolbar = easymdefield.getElementsByClassName('editor-toolbar')[0];
var mdfield = easymdefield.getElementsByClassName('CodeMirror cm-s-easymde CodeMirror-wrap')[0];
mdfield.style.resize = "both";
mdfield.style.minWidth = (toolbar.clientWidth + 3).toString() + 'px';