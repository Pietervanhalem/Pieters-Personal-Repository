mapboxgl.accessToken = 'pk.eyJ1IjoiZ2xvYmFsLWRhdGEtdmlld2VyIiwiYSI6ImNqdG9lYWQ3NTFsNWk0M3Fqb2Q5dXBpeWUifQ.3DvxuGByM33VNa59rDogWw';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [0, 0],
zoom: 0.5
}); 

var x1 = document.getElementById("x1");
var x2 = document.getElementById("x2");
var y1 = document.getElementById("y1");
var y2 = document.getElementById("y2");
var t0 = document.getElementById("t0");
var v = document.getElementById("v");
var calc = document.getElementById("calc");

x1.oninput = function(){
    console.log(x1.value)
}

calc.onclick = function(){

    console.log('hallo')
}
var url = 'http://localhost:6543/fastest_route.csv?lat1=4.557103&lat2=6.591765&lon1=52.935479&lon2=53.891146&t0=22/03/2019%2003:00:00'
// var url = 'https://randomuser.me/api/?results=1'

fetch(url) //, {mode: 'no-cors'})
  .then(function(data) {
    console.log(data)
  })
  .catch(function(error) {
    console.log('error occured')
  }); 
