var lastCalledTime = Date.now();
var delta = 0
var t = 0

var canvas = document.getElementById('canvas')
var c = canvas.getContext('2d')

var slider1 = document.getElementById("myRange1");
var output1 = document.getElementById("TXTslider1");
output1.innerHTML = 'l1:' + slider1.value;

var slider2 = document.getElementById("myRange2");
var output2 = document.getElementById("TXTslider2");
output2.innerHTML = 'l2:' + slider2.value;

var slider3 = document.getElementById("myRange3");
var output3 = document.getElementById("TXTslider3");
output3.innerHTML = 'm1:' + slider3.value;

var slider4 = document.getElementById("myRange4");
var output4 = document.getElementById("TXTslider4");
output4.innerHTML = 'm2:' + slider4.value;

var slider5 = document.getElementById("myRange5");
var output5 = document.getElementById("TXTslider5");
output5.innerHTML = 'g:' + slider5.value;

var g = slider5.value

var t1 = -3
var l1 = slider1.value
var m1 = slider3.value

var t2 = 2
var l2 = slider2.value
var m2 = slider4.value

var x1 = 0
var y1 = 0
var td1 = 0
var p1 = 0
var c1 = 0

var x2 = 0
var y2 = 0
var td2 = 0
var p2 = 0
var c2 = 0

var Q1 = 0
var Q2 = 0
var Q3 = 0

xline = []
yline = []

var drawLine = function(x, y) {
    c.strokeStyle = 'lightblue'
    c.beginPath();

    for (i = 0; i < x.length - 1; i++) {
        c.moveTo(x[i], y[i]);
        c.lineTo(x[i + 1], y[i + 1]);
    }
    c.stroke();
}

var fps_function = function() {
    delta = (Date.now() - lastCalledTime) / 1000;

    lastCalledTime = Date.now();
    fps = 1 / delta;
    document.getElementById("fps").innerHTML = 'fps:' + Math.round(fps);

    return delta
};

var update = function(dt, t1, t2, td1, td2) {

    Q1 = 0 - g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - t2)
    Q2 = 0 - 2 * Math.sin(t1 - t2) * m2 * ((td2 ^ 2) * l2 + (td1 ^ 2) * l1 * Math.cos(t1 - t2))
    Q3 = l1 * (2 * m1 + m2 - m2 * Math.cos(2 * t1 - 2 * t2))
    td1 = td1 + dt * ((Q1 + Q1) / Q3)

    Q1 = 2 * Math.sin(t1 - t2) * ((td1 ^ 2) * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1) + (td2 ^ 2) * l2 * m2 * Math.cos(t1 - t2))
    Q3 = l2 * (2 * m1 + m2 - m2 * Math.cos(2 * t1 - 2 * t2))
    td2 = td2 + dt * (Q1 / Q3)

    t1 = t1 + dt * td1
    t2 = t2 + dt * td2

    return [t1, t2, td1, td2]
}


var draw = function(t1, t2) {

    x1 = 250 + l1 * Math.sin(t1);
    y1 = 250 + l1 * Math.cos(t1)

    x2 = x1 + l2 * Math.sin(t2)
    y2 = y1 + l2 * Math.cos(t2)

    xline.push(x2)
    yline.push(y2)

    c.beginPath();
    c.strokeStyle = 'blue'

    c.moveTo(250, 250);
    c.lineTo(x1, y1);

    c.moveTo(x1, y1);
    c.lineTo(x2, y2);
    c.stroke();

    drawLine(xline, yline)

    c.fillStyle = 'darkblue'
    c.fillRect(x1 - m1/20, y1 - m1/20, m1/10, m1/10);
    c.fillRect(x2 - m2/20, y2 - m2/20, m2/10, m2/10);


}

var ani
var animatie = function() {

    dt = fps_function();
    Q1 = update(dt, t1, t2, td1, td2);

    t1 = Q1[0];
    t2 = Q1[1];
    td1 = Q1[2];
    td2 = Q1[3];

    c.clearRect(0, 0, canvas.width, canvas.height);
    draw(t1, t2);
    t = t + dt;

    ani = requestAnimationFrame(animatie)
}

slider1.oninput = function() {
    l1 = this.value;
    document.getElementById('TXTslider1').innerHTML = 'l1:' + this.value;
}

slider2.oninput = function() {
    l2 = this.value;
    document.getElementById('TXTslider2').innerHTML = 'l2:' + this.value;
}

slider3.oninput = function() {
    m1 = this.value;
    document.getElementById('TXTslider3').innerHTML = 'm1:' + this.value;
}

slider4.oninput = function() {
    m2 = this.value;
    document.getElementById('TXTslider4').innerHTML = 'm1:' + this.value;
}

slider5.oninput = function() {
    g = this.value;
    document.getElementById('TXTslider5').innerHTML = 'g:' + this.value;
}

var button = document.createElement("button");
button.innerHTML = "Clear Paths";

// 2. Append somewhere
var body = document.getElementsByTagName("body")[0];
body.appendChild(button);

// 3. Add event handler
button.addEventListener("click", function() {
    xline = []
    yline = []
});

var mouseIsDown
var mouseX
var mouseY

canvas.addEventListener('mousedown', function(e){handleMouseDown(e);});
canvas.addEventListener('mousemove', function(e){handleMouseMove(e);});
canvas.addEventListener('mouseup', function(e){handleMouseUp(e)});
function handleMouseDown(e){
    mouseIsDown=true
    cancelAnimationFrame(ani)
};
function handleMouseUp(e){
    mouseIsDown=false
    ani = requestAnimationFrame(animatie)

};

function handleMouseMove(e){
if(!mouseIsDown){ return; }

mouseX=parseInt(e.clientX);
mouseY=parseInt(e.clientY);

Q1 = (mouseX - x1)^2 + (mouseY - y1)^2
Q2 = (mouseX - x2)^2 + (mouseY - y2)^2

if(Q1<Q2){
    t1 = Math.PI/2 - Math.atan2(mouseY - 250,mouseX - 250 )
    td1 = 0
    td2 = 0
    
    c.clearRect(0, 0, canvas.width, canvas.height);
    draw(t1, t2);

}else{
    t2 = Math.PI/2-Math.atan2(mouseY - x1,mouseX - y1 )
    td1 = 0
    td2 = 0

    c.clearRect(0, 0, canvas.width, canvas.height);
    draw(t1, t2);
}


}