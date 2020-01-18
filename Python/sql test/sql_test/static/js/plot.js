$(document)
    .ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

$('#graph').height($('#graph').width() * 0.6)

var d3 = Plotly.d3;

var gd3 = d3.select('#graph');
var gd = gd3.node();
var data_url = document
    .getElementById("data_url")
    .innerHTML;
$.getJSON(data_url, function (data) {
    Plotly.newPlot(gd, data.data, data.layout);
});

window.onresize = function () {
    $('#graph').height($('#graph').width() * 0.6)
    Plotly
        .Plots
        .resize(gd);
};

$('.hideshow button').click(function () {
    plot = document.getElementById("graph");

    //- find data id
    var data_index = _.findIndex(plot.data, {'name': this.innerHTML})

    //- get visibility
    visible = plot.data[data_index].visible
    if (visible === undefined) 
        visible = true;
    
    //- toggle visibility
    visible = !visible

    Plotly.restyle("graph", 'visible', visible, data_index);
});