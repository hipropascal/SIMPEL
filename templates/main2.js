var map = L.map('map').setView([-6.041546, 106.851985], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var activemenu = "observasi";
var areas = [];
var instruments = [];

$(".datepicker").datepicker();

$(".menu-item[id=" + activemenu + "]").animate({
    "background-color": "#20a95e",
    "margin": "-3px 0px 0px 0px",
    "padding-top": "7px"
});

$(".menu-item").click(function () {
    $(this).animate({
        "background-color": "#20a95e",
        "margin": "-3px 0px 0px 0px",
        "padding-top": "7px",
        "border-top-right-radius": "5px",
        "border-top-left-radius": "5px"
    });
    $(".menu-item").not(this).animate({
        "background-color": "#024466",
        "margin": "0px 0px 0px 0px",
        "padding-top": "7px",
        "border-radius": "0"
    });
});

setTimeout(function () {
    $.get("/page_ajax/pred", function (data) {
        $("#list-menu").append(data);
    })
});

setTimeout(function () {
    $.get("/page_ajax/raster", function (data) {
        $("#list-menu").append(data);
    })
});

setTimeout(function () {
    $.get("/page_ajax/linegraph", function (data) {
        $("#list-menu").append(data);
    })
});

setTimeout(function () {
    $.get("/page_ajax/multilinegraph", function (data) {
        $("#list-menu").append(data);
    })
});

$.get("/api/all_area", function (data) {
    areas = data.data;
    for (var i = 0; i < area.length; i++) {
        $('#__polygon').append('<option value="' + area[i].foldername + '">' + area[i].name + '</option>')
    }
});

$('#__polygon').change(function () {
    var val = $(this).val();
    $('#instrument').html('');
    $.get('/api/observasi/' + val, function (data) {
        console.log(data);
        instruments = data.data;
        for (var i = 0; i < instrument.length; i++) {
            $('#instrument').append('<option value="' + instrument[i].foldername + '">' + instrument[i].name + '</option>');
        }
    });
    if (val !== "") {
        var lat = parseFloat(val.split('__')[1]);
        var lng = parseFloat(val.split('__')[2]);
        var zoom = parseInt(val.split('__')[3]);
        map.setView([lat, lng], zoom);
    }
});

function loadmarker() {

}

function setmapto(lat, lng, zoom) {

}