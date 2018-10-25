function loadLayerObs(category, data, order) {
    var instrument_name = $('#instrument').find(":selected").text();
    var param_name = $('#param').find(":selected").text();
    var param = $('#param').val();
    if (category === 'point') {
        $.get("/page_ajax/point", function (page) {
            var title = param.split('.')[0].split('_')[1];
            var html = page.replaceAll('{param}', title)
                .replaceAll('{label}', alfabet[order])
                .replaceAll('#ffffff', color[order]);
            $("#list-menu").append(html);
            var formated = [];
            for (var line of data) {
                formated.push({'date': new Date(line[0]), 'value': parseFloat(line[1])})
            }
            MG.data_graphic({
                data: formated,
                width: 450,
                height: 180,
                right: 40,
                left: 30,
                top: 20,
                bottom: 30,
                target: '#graph' + alfabet[order],
                x_accessor: 'date',
                y_accessor: 'value',
                color: '#8C001A'
            })
        })
    }
}

function plotMapList() {
    var area = $('#area').val();
    var instrument = $('#instrument').val();
    var param = $('#param').val();
    var instrument_name = $('#instrument').find(":selected").text();
    var param_name = $('#param').find(":selected").text();
    if (instrument.includes("grid")) {
        reset();
        $.get('/api/observasi/grid/get_date/' + area + '/' + instrument + '/' + param, function (res) {
            grid_date_obj = res.data;
            grid_date = [];
            for (var i = 0; i < grid_date_obj.length; i++) {
                grid_date.push(grid_date_obj[i].date);
            }
            $.get('/page_ajax/grid', function (res) {
                reset();
                var title = param.split('|')[0].split('_')[1];
                var rasgrad = gradient[instrument_name + '|' + param_name];
                var list = '';
                for (var i = 0; i < rasgrad.length; i++) {
                    list = list + '<div>' + rasgrad[i] + '</div>';
                }
                var html = res.replace('{title}', title).replace('{list}', list);
                $("#list-menu").append(html);
                $("#date-grid").datepicker({
                    dateFormat: 'dd-mm-yy',
                    beforeShowDay: enableAllTheseDays,
                    defaultDate: grid_date[grid_date.length - 1]
                });
                loadhourgrid();
                $("#date-grid").change(function () {
                    loadhourgrid();
                });
                $("#hour-grid").change(function () {
                    loadImageObs();
                });
                loadImageObs();
            });
        });
    } else if (instrument.includes("point") > -1) {
        $.get('/api/observasi/all_point/' + area + '/' + instrument + '/' + param, function (res) {
            reset();
            console.log(res);
            coorListObs = res.location;
            layer_point.clearLayers();
            layer_point.removeFrom(map);
            for (var i = 0; i < coorListObs.length; i++) {
                var divlabel = divmarker.replaceAll('label', alfabet[i]).replaceAll('#ffffff', color[i]);
                var icon = L.divIcon({html: divlabel});
                var marker_obs = L.marker([parseFloat(coorListObs[i].split('_')[0]), parseFloat(coorListObs[i].split('_')[1])], {icon: icon});
                layer_point.addLayer(marker_obs);
                loadLayerObs("point", res.data[i], i)
            }
            layer_point.addTo(map);
        })
    }
}

function load_param_obs() {
    var area = $('#area').val();
    var instrument = $('#instrument').val();
    var instrument_name = $('#instrument').find(":selected").text();
    $.get('/api/observasi/all_param/' + area + '/' + instrument, function (data) {
        $('#param').html('');
        for (var par of data.params) {
            if (instrument.includes("point"))
                $('#param').append('<option value="' + par.filename + '">' + par.name.split(' (')[0] + '</option>');
            else if (instrument.includes("grid")) {
                $('#param').append('<option value="' + par.filename + '">' + par.name.split(' (')[0] + '</option>');
            }
        }
        plotMapList();
    })

}