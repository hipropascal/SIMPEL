function current_option() {
    // Value
    var menu = activemenu;
    var area = $('#area');
    var instrument = $('#instrument');
    var param_obs = $('#param-obs');
    var param_pred = $('#param-pred');
    var param_pred_map = $('#param-predmap');
    var param_pred_obs_o = $('#param-pvso-o');
    var param_pred_obs_p = $('#param-pvso-p');
    // Description
    var area_desc = area.split('__')[0].split('_')[1];
    var instrument_desc = instrument.split('__')[0].split('_')[1];
    var param_obs_desc = param_obs.split('.')[0].split('_')[1];
    var param_pred_desc = param_pred.split('.')[0].split('_')[1];
    var param_pred_map_desc = param_pred_map.split('.')[0].split('_')[1];
    var param_pred_obs_o_desc = param_pred_obs_o.split('.')[0].split('_')[1];
    var param_pred_obs_p_desc = param_pred_obs_p.split('.')[0].split('_')[1];
    return {
        menu: menu,
        point: {
            date:[],
            value:[]
        },
        grid: {
            date:[]
        },
        value: {
            area: area.val(),
            instrument: instrument.val(),
            param_obs: param_obs.val(),
            param_pred: param_pred.val(),
            param_pred_map: param_pred_map.val(),
            param_pred_obs_o: param_pred_obs_o.val(),
            param_pred_obs_p: param_pred_obs_p.val()
        },
        desc: {
            area: area_desc,
            instrument: instrument_desc,
            param_obs: param_obs_desc,
            param_pred: param_pred_desc,
            param_pred_map: param_pred_map_desc,
            param_pred_obs_o: param_pred_obs_o_desc,
            param_pred_obs_p: param_pred_obs_p_desc
        }
    }
}

function set_view() {
    var info = current_option();
    switch (info.menu) {
        case 'observasi':
            observasi(info);
            break;
        case 'prakiraan_vs_observasi':
            prakiraan_vs_observasi(info);
            break;
        case 'prakiraan':
            prakiraan(info);
            break;
        case 'peta_prakiraan':
            peta_prakiraan(info);
            break;
    }
}

// ------------------------------------ Observasi ---------------------------------

function observasi(info) {
    var data_type = info.value.instrument.split('__')[1];
    switch (data_type) {
        case 'point':
            observasi_point(info);
            break;
        case 'grid':
            observasi_grid(info);
            break;
    }
}

function observasi_point(info) {

}

function observasi_grid(info) {
    $.get('/api/observasi/grid/get_date/' + info.area + '/' + info.instrument + '/' + info.param_obs, function (res) {
        var gdo = res.data;
        var gd = [];
        for (var i = 0; i < gdo.length; i++) {
            gd.push(gdo[i].date);
        }
        info.grid.date = gd;
    });
}

// ------------------------------------ Prakiraaan VS Observasi  ----------------------
function prakiraan_vs_observasi(info) {

}


// ------------------------------------ Prakiraaan  -----------------------------------
function prakiraan(info) {

}


// ------------------------------------ Peta Prakiraaan  ------------------------------
function peta_prakiraan(info) {

}

// ------------------------------------ Left Menu ------------------------------------
// Show this if data Grid

function load_grid(info) {
    $.get('/page_ajax/grid', function (res) {
        var title = info.param_obs.split('|')[0].split('_')[1];
        var rasgrad = gradient[info.desc.instrument.dec + '|' + info.desc.param_obs_desc];
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
}

// Show this if data Point

function load_point() {

}

//------------------------------------ Map ------------------------------------