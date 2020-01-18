var body = document.body,

var addRow = function(tabl){
    var tr = tabl.insertRow();
    for(var j = 0; j < 3; j++){
        var td = tr.insertCell();

        var x = document.createElement('input')
        x.setAttribute("type", "text")
        td.appendChild(x);
        td.style.border = '1px solid black';    
    }
}

tbl1  = document.createElement('table');
tbl1.style.width  = '100px';
tbl1.style.border = '1px solid black';

var tr = tbl1.insertRow();

var td = tr.insertCell();
var x = document.createTextNode('Origin')
td.appendChild(x);
td.style.border = '1px solid black'; 

var td = tr.insertCell();
var x = document.createTextNode(('Destination'))
td.appendChild(x);
td.style.border = '1px solid black'; 

var td = tr.insertCell();
var x = document.createTextNode('Volume')
td.appendChild(x);
td.style.border = '1px solid black'; 

body.appendChild(tbl1);

var btn = document.createElement('Button')
btn.innerHTML = "new row";                   // Insert text
document.body.appendChild(btn);               // Append <button> to <body>

btn.onclick = function(){
    addRow(tbl1);
}

