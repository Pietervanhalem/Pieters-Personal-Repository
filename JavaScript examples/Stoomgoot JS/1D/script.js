var t = 0
var M = 1000
var x = []
for (i = 0; i < M; i++) {
    x.push(500 / M * i)
}
var lastCalledTime = Date.now();

var h = x
var u = x
var dx = x[1] - x[0]

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

var getLine = function(h, u, dx, dt) {
    console.log(y)
    h1 = []
    u1 = []

    return h1, u1
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

    var dt = fps_function()
    h, u = getLine(h, u, dx, dt)

    c.clearRect(0, 0, canvas.width, canvas.height);
    drawLine(x, y)

    t = t + dt
}
7