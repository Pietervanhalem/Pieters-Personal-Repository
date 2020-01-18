var xNew = [250]
var yNew = [250]
var RNew = [0]


var myDemo = function() {
    var slider = document.getElementById("myRange");
    var output = document.getElementById("TXTslider");
    output.innerHTML = 'N:' + slider.value;

    var slider2 = document.getElementById("myRange2");
    var output2 = document.getElementById("TXTslider2");
    output2.innerHTML = 'A:' + slider2.value;

    var slider3 = document.getElementById("myRange3");
    var output3 = document.getElementById("TXTslider3");
    output3.innerHTML = 'A2:' + slider3.value;

    var slider4 = document.getElementById("myRange4");
    var output4 = document.getElementById("TXTslider4");
    output4.innerHTML = 'A4:' + slider4.value;

    var N = slider.value
    var A = slider2.value
    var A2 = slider3.value
    var A3 = slider4.value
    var color = 0

    var canvas = document.getElementById("canvas");
    var c = canvas.getContext("2d");
    c.fillStyle = "#FF0000";
    c.strokeStyle = 'rgb(' + 0 + ', ' + 255 + ', ' + 0 + ')';
    c.translate(250, 0);
    c.moveTo(0, 0);
    c.lineTo(0, 250);
    c.stroke();
    c.translate(-250, 0);
    for (i = 0; i < N; i++) {
        color = 255 - 2 * i
        c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
        draw(c, i, A, A2, A3);
    }

    slider.oninput = function() {
        N = this.value;
        document.getElementById('TXTslider').innerHTML = 'N:' + this.value;
        c.clearRect(0, 0, canvas.width, canvas.height);

        xNew = [250]
        yNew = [250]
        RNew = [0]
        c.strokeStyle = 'rgb(' + 0 + ', ' + 255 + ', ' + 0 + ')';
        c.translate(250, 0);
        c.moveTo(0, 0);
        c.lineTo(0, 250);
        c.stroke();
        c.translate(-250, 0);
        for (i = 0; i < N; i++) {
            color = 255 - 2 * i
            c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
            draw(c, i, A, A2, A3);
        }
    };

    slider2.oninput = function() {
        A = this.value;
        document.getElementById('TXTslider2').innerHTML = 'A:' + this.value;
        c.clearRect(0, 0, canvas.width, canvas.height);

        xNew = [250]
        yNew = [250]
        RNew = [0]
        c.strokeStyle = 'rgb(' + 0 + ', ' + 255 + ', ' + 0 + ')';
        c.translate(250, 0);
        c.moveTo(0, 0);
        c.lineTo(0, 250);
        c.stroke();
        c.translate(-250, 0);
        for (i = 0; i < N; i++) {
            color = 255 - 2 * i
            c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
            draw(c, i, A, A2, A3);
        }
    };

    slider3.oninput = function() {
        A2 = this.value;
        document.getElementById('TXTslider3').innerHTML = 'A:' + this.value;
        c.clearRect(0, 0, canvas.width, canvas.height);

        xNew = [250]
        yNew = [250]
        RNew = [0]
        c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
        c.translate(250, 0);
        c.moveTo(0, 0);
        c.lineTo(0, 250);
        c.stroke();
        c.translate(-250, 0);
        for (i = 0; i < N; i++) {
            color = 255 - 2 * i
            c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
            draw(c, i, A, A2, A3);
        }
    };

    slider4.oninput = function() {
        A3 = this.value;
        document.getElementById('TXTslider4').innerHTML = 'A3:' + this.value;
        c.clearRect(0, 0, canvas.width, canvas.height);

        xNew = [250]
        yNew = [250]
        RNew = [0]
        c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
        c.translate(250, 0);
        c.moveTo(0, 0);
        c.lineTo(0, 250);
        c.stroke();
        c.translate(-250, 0);
        for (i = 0; i < N; i++) {
            color = 255 - 2 * i
            c.strokeStyle = 'rgb(' + 2 * i + ', ' + color + ', ' + 200 + ')';
            draw(c, i, A, A2, A3);
        }
    };
}


var drawBranch = function(c, x, y, Q, R, A, A2, A3) {
    L = Math.exp(-Q / 80) * 30

    c.translate(x, y);
    c.rotate(R)
    c.beginPath();
    c.moveTo(0, 0);
    c.lineTo(L * Math.sin(A), L * Math.cos(A));
    c.moveTo(0, 0);
    c.lineTo(-L * Math.sin(A), L * Math.cos(A));
    c.stroke();
    c.rotate(-R)
    c.translate(-x, -y);
    c.closePath();

    // console.log(A2)

    var TT = [
        (R - parseFloat(A2) + parseFloat(A3)),
        (R + parseFloat(A2) + parseFloat(A3)),

        x + L * Math.sin(A - R),
        x + L * Math.sin(-A - R),

        y + L * Math.cos(A - R),
        y + L * Math.cos(-A - R),
    ]

    return TT;
};

var draw = function(c, Q, A, A2, A3) {
    var xNew2 = []
    var yNew2 = []
    var RNew2 = []

    for (i = 0; i < xNew.length; i++) {
        var xNew22 = drawBranch(c, xNew[i], yNew[i], Q, RNew[i], A, A2, A3)

        RNew2.push(xNew22[0])
        RNew2.push(xNew22[1])

        xNew2.push(xNew22[2])
        xNew2.push(xNew22[3])

        yNew2.push(xNew22[4])
        yNew2.push(xNew22[5])
    }


    xNew = xNew2
    yNew = yNew2
    RNew = RNew2
}