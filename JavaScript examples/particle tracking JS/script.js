mapboxgl.accessToken = 'pk.eyJ1IjoiZ2xvYmFsLWRhdGEtdmlld2VyIiwiYSI6ImNqdG9lYWQ3NTFsNWk0M3Fqb2Q5dXBpeWUifQ.3DvxuGByM33VNa59rDogWw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [0, 0],
    zoom: 0.5
});

var lastCalledTime = 0;
var fps;
var slider = document.getElementById("myRange");
var output = document.getElementById("TXTslider");
var slider2 = document.getElementById("myRange2");
var output2 = document.getElementById("TXTslider2");
var slider3 = document.getElementById("myRange3");
var output3 = document.getElementById("TXTslider3");
var slider4 = document.getElementById("myRange4");
var output4 = document.getElementById("TXTslider4");
var N = slider.value;
var xy_points
var survival_time
var regen_factor = 1000
var speed_factor = 0.5
var zoom_prev = 0.5
var flow
var x
var y
var tail = 10


output.innerHTML = 'N:' + slider.value;
output2.innerHTML = 'Regen:' + slider2.value;
output3.innerHTML = 'v:' + slider3.value;
output4.innerHTML = 'tail:' + slider4.value;

function getflow([x, y]) {
    u = Math.sin(2 * Math.PI * y / 180) / 10
    v = Math.cos(2 * Math.PI * x / 180) / 10

    return [u, v]
};

function fps_function() {
    delta = (Date.now() - lastCalledTime) / 1000;

    lastCalledTime = Date.now();
    fps = 1 / delta;
    document.getElementById("pause").innerHTML = 'fps:' + Math.round(fps);
};

function addPoint() {
    var features = []
    for (i = 0; i < N; i++) {
        x = map.getCenter().lng + (1 - 2 * Math.random()) * 180 / (1 + map.getZoom() ** 2)
        y = map.getCenter().lat + (1 - 2 * Math.random()) * 180 / (1 + map.getZoom() ** 2)
        features.push({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "survival_time": Math.random() * regen_factor,
                "coordinates": [
                    [x, y]
                ]
            },
        }, )

    }
    return features
}
var features = addPoint();
var geojson = {
    "type": "FeatureCollection",
    "features": features
};
map.on('load', function() {


    map.addLayer({
            'id': 'line-animation',
            'type': 'line',
            'source': {
                'type': 'geojson',
                'data': geojson
            },
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#ed6498',
                'line-width': 1.5,
                'line-opacity': .8
            }
        }),

        animatiemaker();


    function animatiemaker() {
        for (i = 1; i < N; i++) {
            survival_time = map.getSource('line-animation')._data.features[i].geometry.survival_time
            xy_points = map.getSource('line-animation')._data.features[i].geometry.coordinates
            xy_points = xy_points[xy_points.length - 1]

            if (survival_time < regen_factor &&
                Math.abs(xy_points[0]) < 180 &&
                Math.abs(xy_points[1]) < 90) {

                flow = getflow(xy_points)
                x = xy_points[0] - speed_factor * flow[0]
                y = xy_points[1] - speed_factor * flow[1]

                geojson.features[i].geometry.coordinates.push([x, y])
                geojson.features[i].geometry.survival_time = survival_time + 1
                if (geojson.features[i].geometry.coordinates.length > tail) {
                    geojson.features[i].geometry.coordinates.shift()
                }

            } else {
                x = map.getCenter().lng + (1 - 2 * Math.random()) * 180 / (1 + map.getZoom() ** 2)
                y = map.getCenter().lat + (1 - 2 * Math.random()) * 180 / (1 + map.getZoom() ** 2)

                geojson.features[i] = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "survival_time": 0,
                        "coordinates": [
                            [x, y]
                        ]
                    },
                }
            }
        }

        map.getSource('line-animation').setData(geojson)

        animation = requestAnimationFrame(animatiemaker);

        slider.oninput = function() {
            N = this.value;
            document.getElementById('TXTslider').innerHTML = 'N:' + this.value;

            var features = addPoint();
            geojson.features = features

        }

        slider2.oninput = function() {
            regen_factor = this.value;
            document.getElementById('TXTslider2').innerHTML = 'Regen:' + this.value;

            var features = addPoint();
            geojson.features = features
        }

        slider3.oninput = function() {
            speed_factor = this.value;
            document.getElementById('TXTslider3').innerHTML = 'v:' + this.value;
        }

        slider4.oninput = function() {
            tail = this.value;
            document.getElementById('TXTslider4').innerHTML = 'tail:' + this.value;
        }
        fps_function()
    };
});