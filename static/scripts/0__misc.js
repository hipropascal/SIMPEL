function loadhourgrid() {
    var index = grid_date.indexOf($("#date-grid").val());
    var hours = grid_date_obj[index].hours;
    $("#hour-grid").html("");
    var stroption = "";
    for (var i = 0; i < hours.length; i++) {
        var option = "<option value='" + hours[i] + "'>" + hours[i] + " UTC</option>";
        $("#hour-grid").append(option).val(hours[hours.length - 1]);
    }
    console.log(hours);
}

$.loadScript = function (url, callback) {
    $.ajax({
        url: url,
        dataType: 'script',
        success: callback,
        async: true
    });
};

