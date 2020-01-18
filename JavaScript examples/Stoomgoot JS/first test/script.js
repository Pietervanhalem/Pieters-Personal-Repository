var t = 0
var M = 1000
var x = []
for (i = 0; i < M; i++) {
    x.push(500 / M * i)
}
var lastCalledTime = Date.now();

var canvas = document.getElementById('canvas')
var c = canvas.getContext('2d')
c.strokeStyle = 'lightblue'

function fps_function() {
    delta = (Date.now() - lastCalledTime) / 1000;

    lastCalledTime = Date.now();
    fps = 1 / delta;
    document.getElementById("fps").innerHTML = 'fps:' + Math.round(fps);

    return delta
};

var getLine = function(x, t) {
    var y = []
    for (i = 0; i < x.length; i++) {
        y.push(300 + 50 * Math.sin(2 * Math.PI * x[i] / 100 - t))
    }
    return y
}

var drawLine = function(x, y) {
    c.beginPath();
    for (i = 0; i < x.length - 1; i++) {
        c.moveTo(x[i], y[i]);
        c.lineTo(x[i + 1], y[i + 1]);
    }
    c.stroke();
}

var animatie = function() {
    if (t < 1000) { requestAnimationFrame(animatie); }

    var delta = fps_function()
    var y = getLine(x, t)

    c.clearRect(0, 0, canvas.width, canvas.height);
    drawLine(x, y)

    t = t + delta
}
7