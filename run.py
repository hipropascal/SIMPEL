import os
import csv
import json
from flask import Flask, render_template, jsonify, send_file

app = Flask(__name__)


@app.route('/')
def page_main():
    return render_template('main.html')


@app.route('/display')
def page_display():
    return render_template('display.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/page_ajax/<page>')
def page_ajax(page):
    return render_template('ajax_' + page + '.html')


@app.route('/api/all_area')
def api_all_area():
    list_area = list_dir('data/data_trees')
    area_items = []
    for area in list_area:
        parse_info = area.split('__')
        coordinate = parse_info[1:]
        id = parse_info[0].split('_')[0]
        name = ' '.join(parse_info[0].split('_')[1:]).title()
        area_item = {'id': id, 'coor': [coordinate], 'name': name, 'foldername': area}
        area_items.append(area_item)
    bundle = {'data': area_items}
    print bundle
    return jsonify(bundle)


@app.route('/api/observasi/<area>/')
def api_list_obs(area):
    list_instrument = list_dir('data/data_trees/' + area + '/observasi')
    inst_items = []
    for instrument in list_instrument:
        parse_info = instrument.split('__')
        category = parse_info[1]
        parse_id_name = parse_info[0].split('_')
        id = parse_id_name[0]
        name = ' '.join(parse_id_name[1:])
        inst_item = {'id': id, 'name': name, 'cat': category, 'foldername': instrument}
        inst_items.append(inst_item)
    bundle = {'data': inst_items}
    return jsonify(bundle)


@app.route('/api/observasi/<area>/<instrument>')
def api_list_obs_spot(area, instrument):
    inst_path = 'data/data_trees/' + area + '/observasi/' + instrument
    inst_cat = instrument.split('__')
    if inst_cat[1] == 'point':
        coor_items = []
        list_coor = list_dir(inst_path)
        for coor in list_coor:
            coor_lat_lng = coor.split('_')
            coor_items.append(coor_lat_lng)
        return jsonify({'coor': coor_items})
    elif inst_cat[1] == 'grid':
        bound_items = []
        list_bound = list_dir(inst_path)
        for bound in list_bound:
            bounding_box = bound.split('_')
            bound_items.append(bounding_box)
        return jsonify({'bound': bound_items})


@app.route('/api/observasi/all_param/<area>/<instrument>/')
def api_list_obs_spot_all(area, instrument):
    inst_path = 'data/data_trees/' + area + '/observasi/' + instrument
    inst_cat = instrument.split('__')
    list_all_inst = []
    if inst_cat[1] == 'point':
        coor_items = []
        list_coor = list_dir(inst_path)
        for coor in list_coor:
            coor_path = 'data/data_trees/' + area + '/observasi/' + instrument + '/' + coor
            params = list_file(coor_path)
            for param in params:
                parse1 = param.split('_')
                name = parse1[1].split('.')[0]
                id = parse1[0]
                list_all_inst.append({'id': id, 'name': name, 'filename': param})
        list_all_inst = remove_duplicates(list_all_inst)
        return jsonify({'params': list_all_inst})
    if inst_cat[1] == 'grid':
        list_all_param = []
        list_param = list_dir(inst_path)
        for param in list_param:
            parsed = param.split('_')
            obj_param = {'id':parsed[0], 'name':parsed[1], 'filename': param }
            list_all_param.append(obj_param)
        return jsonify({'params': list_all_param})


@app.route('/api/observasi/<area>/<instrument>/<coor>')
def api_list_obs_parameter(area, instrument, coor):
    list_param = list_file('data/data_trees/{}/observasi/{}/{}'.format(area, instrument, coor))
    param_items = []
    for param in list_param:
        parsed = param.split('_')
        id = parsed[0]
        name = parsed[1].split('.')[0]
        param_item = {'id': id, 'name': name, 'filename': param}
        param_items.append(param_item)
    bundle = {'data': param_items}
    return jsonify(bundle)


@app.route("/api/observasi/all_point/<area>/<instrument>/<filename>")
def api_get_obs_data(area, instrument, filename):
    inst_path = 'data/data_trees/' + area + '/observasi/' + instrument
    inst_cat = instrument.split('__')
    if inst_cat[1] == 'point':
        coor_id = []
        coor_data = []
        list_coor = list_dir(inst_path)
        for coor in list_coor:
            csv_file = 'data/data_trees/' + area + '/observasi/' + instrument + '/' + coor + '/' + filename
            arr = csv_to_arr(csv_file)
            coor_id.append(coor)
            coor_data.append(arr)
        return jsonify({'location':coor_id,'data':coor_data})


@app.route("/api/observasi/grid/get_date/<area>/<instrument>/<param>")
def api_get_obs_grid(area,instrument,param):
    image_list = list_file('data/data_trees/{}/observasi/{}/{}'.format(area,instrument,param))
    date_only_s = []
    for image in image_list:
        date_only = image.split(' ')[0]
        date_only_s.append(date_only)
    date_only_s = remove_duplicates(date_only_s)
    date_arr = []
    for date in date_only_s:
        hour_in_date = []
        for image in image_list:
            if date in image:
                hour_in_date.append(image.split(' ')[1].split('.')[0].replace('_',':'))
        date_obj = {'date':date,'hours':hour_in_date}
        date_arr.append(date_obj)
    return jsonify({'data':date_arr})


@app.route("/api/observasi/grid/get_raster/<area>/<instrument>/<param>/<filename>")
def api_get_obs_raster(area,instrument,param,filename):
    return send_file('data/data_trees/{}/observasi/{}/{}/{}'.format(area, instrument, param,filename))


@app.route('/api/get_geojson/')
def get_geo_json():
    path_data = 'data/data_trees'
    areas = list_dir(path_data)
    geos = []
    for area in areas:
        path = 'data/data_trees/{}/__polygon/'.format(area)
        geofile = path+list_file(path)[0]
        with open(geofile) as json_data:
            d = json.load(json_data)
            geos.append(d)
    return jsonify({'data':geos})


@app.route('/api/prakiraan/all_param/<area>/')
def api_list_pred_param(area):
    path = 'data/data_trees/' + area + '/prakiraan/'
    list_pred = list_dir(path)
    par_items = []
    for pred in list_pred:
        parse_info = pred.split('__')
        coor = list_dir(path + pred)[0]
        params = list_file(path + pred+'/'+coor)
        par_items = par_items+params
    bundle = {'param': remove_duplicates(par_items)}
    return jsonify(bundle)


@app.route('/api/prakiraan/<area>/')
def api_list_pred(area):
    path = 'data/data_trees/' + area + '/prakiraan/'
    list_pred = list_dir(path)
    loc_items = []
    for pred in list_pred:
        parse_info = pred.split('__')
        category = parse_info[1]
        parse_id_name = parse_info[0].split('_')
        id = parse_id_name[0]
        name = ' '.join(parse_id_name[1:])
        coor = list_dir(path + pred)[0]
        loc_item = {'id': id, 'name': name, 'cat': category, 'foldername': pred, 'coor':coor}
        loc_items.append(loc_item)
    bundle = {'data': loc_items}
    return jsonify(bundle)


@app.route('/api/prakiraan/data/<area>/<coor>/<loc>/<file>')
def api_list_pred_data(area,coor,loc,file):
    path = 'data/data_trees/' + area + '/prakiraan/' +loc+'/'+ coor+ '/' + file
    arr = csv_to_arr(path)
    return jsonify({'data':arr})


@app.route('/api/peta-prakiraan/all_param/<area>')
def api_list_predmap_param(area):
    path = 'data/data_trees/{}/peta_prakiraan/'.format(area)
    params = list_dir(path)
    param_list = []
    for param in params:
        id = param.split('_')[0]
        param_list.append({'id':id,'foldername':param})
    return jsonify({'data': param_list})


@app.route('/api/peta-prakiraan/date/<area>/<param>')
def api_get_date_predmap(area,param):
    image_list = list_file('data/data_trees/{}/peta_prakiraan/{}'.format(area,param))
    date_only_s = []
    for image in image_list:
        date_only = image.split(' ')[0]
        date_only_s.append(date_only)
    date_only_s = remove_duplicates(date_only_s)
    date_arr = []
    for date in date_only_s:
        hour_in_date = []
        for image in image_list:
            if date in image:
                hour_in_date.append(image.split(' ')[1].split('.')[0].replace('_',':'))
        date_obj = {'date':date,'hours':hour_in_date}
        date_arr.append(date_obj)
    return jsonify({'data':date_arr})


@app.route('/api/peta-prakiraan/get_data/<area>/<param>/<file>')
def api_get_data_predmap(area,param,file):
    path = 'data/data_trees/{}/peta_prakiraan/{}/{}'.format(area,param,file)
    return send_file(path)


def list_dir(path):
    return sorted([name for name in os.listdir(path)
                   if os.path.isdir(os.path.join(path, name))])


def list_file(path):
    return sorted([name for name in os.listdir(path)])


def csv_to_arr(path):
    results = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            results.append(row)
    return results


def remove_duplicates(listofElements):
    uniqueList = []
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)
    return uniqueList


if __name__ == '__main__':
    # api_all_area()
    app.run(debug=True, host='0.0.0.0' ,port=8180)
