from netCDF4 import Dataset, num2date
import numpy as np
import numpy.ma as ma
import math
import matplotlib.pyplot as plt
from src.stegano import coder
from scipy.ndimage.interpolation import map_coordinates


# (-6.012381, 106.678298, -6.012381, 106.681004)

def plot2d(H):
    plt.imshow(H)
    plt.colorbar(orientation='vertical')
    plt.show()


def resize(arr, target_size):
    new_dims = []
    for original_length, new_length in zip(arr.shape, target_size):
        new_dims.append(np.linspace(0, original_length - 1, new_length))

    coords = np.meshgrid(*new_dims, indexing='ij')
    return map_coordinates(arr, coords)


def regrid():
    # Defined Variables
    lat1 = -8.114958
    lng1 = 114.375859
    lat2 = -8.260393
    lng2 = 114.475508
    interval = 0.0017  # ~300m
    nc_file = '/Users/maritim/Project/BMKG/SIMPEL/data/raw/model_delf3d/0_ketapang gilimanuk/bundle.nc'
    wave_height_tkl = '/Users/maritim/Project/BMKG/SIMPEL/data/raw/model_delf3d/0_ketapang gilimanuk/wave_height.tkl'
    wave_dir_tkl = '/Users/maritim/Project/BMKG/SIMPEL/data/raw/model_delf3d/0_ketapang gilimanuk/wave_dir.tkl'
    target_folder_wave = '/Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/0_Gelombang(meter)__grid/'
    target_folder_current = '/Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/3_Arus(m s^-1)__grid/'
    target_folder_level = '/Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/1_Tinggi Muka Air(meter)__grid/'
    target_folder_wind = '/Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/2_Angin(m s^-1)__grid/'
    tkl_height = 190
    tkl_width = 146

    # Create Grid
    xrange = abs(lat1 - lat2)
    yrange = abs(lng1 - lng2)
    lat2_mod = lat1 - (xrange // interval) * interval
    lng2_mod = lng1 + (yrange // interval) * interval
    array_lat = np.arange(lat2, lat1, interval)
    array_lng = np.arange(lng1, lng2, interval)

    # Load nc file
    nc_file = Dataset(nc_file, 'r', format="NETCDF4")
    xcor = nc_file['XCOR'][:]
    ycor = nc_file['YCOR'][:]
    time_f = num2date(nc_file['time'][:], 'seconds since 2018-01-01 00:00:00', 'proleptic_gregorian')
    s1 = nc_file['S1'][:]
    u1 = nc_file['U1'][:]
    v1 = nc_file['V1'][:]

    # Load tkl file
    array_swh = np.zeros((505, s1.shape[1], s1.shape[2]))
    array_dir = np.zeros((505, s1.shape[1], s1.shape[2]))
    f_swh = open(wave_height_tkl)
    f_dir = open(wave_dir_tkl)
    lines_swh = f_swh.readlines()
    lines_dir = f_dir.readlines()

    mat = 0
    arr_tmp = np.zeros((tkl_width, tkl_height))
    for idx, line in enumerate(lines_swh[4:]):
        data = line.split("  ")
        row_data = np.array(data, dtype=float)
        row_idx = idx % tkl_width
        arr_tmp[row_idx] = row_data[:]
        if idx % tkl_width == 0 and idx != 0:
            arr_resize = resize(arr_tmp[:], (array_swh[0].shape[0], array_swh[0].shape[1]))
            array_swh[mat] = arr_resize[:]
            mat = mat + 1
            if mat == 504:
                break

    mat = 0
    for idx, line in enumerate(lines_dir[4:]):
        data = line.split("  ")
        row_data = np.array(data, dtype=float)
        row_idx = idx % tkl_width
        arr_tmp[row_idx] = row_data[:]
        if idx % tkl_width == 0 and idx != 0:
            arr_resize = resize(arr_tmp[:], (array_dir[0].shape[0], array_swh[0].shape[1]))
            array_dir[mat] = arr_resize[:]
            mat = mat + 1
            if mat == 504:
                break

    u_wave = abs(array_swh) * np.sin((math.pi / 180) * array_dir)
    v_wave = abs(array_swh) * np.cos((math.pi / 180) * array_dir)

    # Create grid
    arr_s1 = np.zeros((505, array_lat.shape[0], array_lng.shape[0]), dtype=np.float)
    arr_u1 = np.zeros((505, array_lat.shape[0], array_lng.shape[0]), dtype=np.float)
    arr_v1 = np.zeros((505, array_lat.shape[0], array_lng.shape[0]), dtype=np.float)
    arr_waveu = np.zeros((505, array_lat.shape[0], array_lng.shape[0]), dtype=np.float)
    arr_wavev = np.zeros((505, array_lat.shape[0], array_lng.shape[0]), dtype=np.float)
    for idt, time in enumerate(s1):
        for idx, x in enumerate(time):
            for idy, y in enumerate(x):
                xcor_cur = xcor[idx, idy]
                ycor_cur = ycor[idx, idy]
                lat_near = find_nearest(array_lat, ycor_cur)
                lng_near = find_nearest(array_lng, xcor_cur)
                arr_s1[idt, lat_near, lng_near] = s1[idt, idx, idy]
                arr_u1[idt, lat_near, lng_near] = u1[idt, 0, idx, idy]
                arr_v1[idt, lat_near, lng_near] = v1[idt, 0, idx, idy]
                if idt < 505:
                    arr_waveu[idt, lat_near, lng_near] = u_wave[idt, idx, idy]
                    arr_wavev[idt, lat_near, lng_near] = v_wave[idt, idx, idy]

        bound = {"bottom": lat2_mod, "top": lat1, "left": lng1, "right": lng2_mod}


        # Create landmask based on current data
        # water_mask = np.copy(arr_s1[0, :])
        # water_mask[water_mask > 0] = 1
        # water_mask[water_mask == 0] = 0
        # masked_s1 = ma.array(arr_s1[idt, :], mask=water_mask).filled(0)
        # masked_waveu = ma.array(arr_waveu[idt, :], mask=water_mask, fill_value=0).filled(0)
        # masked_wavev = ma.array(arr_wavev[idt, :], mask=water_mask, fill_value=0).filled(0)

        img_uv1 = coder.encode_uv_image(np.nan_to_num(arr_u1[idt, :]), np.nan_to_num(arr_v1[idt, :]), bound)
        img_s1 = coder.encode_image(np.nan_to_num(arr_s1[idt, :]), bound)
        # img_winduv = coder.encode_uv_image(np.nan_to_num(arr_windu[idt, :]), np.nan_to_num(arr_windv[idt, :]), bound)
        img_waveuv = coder.encode_uv_image(np.nan_to_num(arr_waveu[idt, :]), np.nan_to_num(arr_wavev[idt, :]), bound)
        # img_uv1 = coder.encode_uv_image(np.nan_to_num(arr_u1[idt, :]), np.nan_to_num(arr_v1[idt, :]), bound)
        # img_s1 = coder.encode_image(np.nan_to_num(masked_s1), bound)
        # img_waveuv = coder.encode_uv_image(np.nan_to_num(masked_waveu), np.nan_to_num(masked_wavev), bound)

        fname = time_f[idt].strftime("%d-%m-%Y %H_%M.png")

        if img_uv1:
            img_uv1.save(target_folder_current + fname)
        if img_s1:
            img_s1.save(target_folder_level + fname)
        if img_waveuv:
            img_waveuv.save(target_folder_wave + fname)
        print('Time = ', idt)


def find_nearest(array, value):
    array = np.asarray(array)
    armin = np.abs(array - value)
    idx = armin.argmin()
    return idx


if __name__ == '__main__':
    regrid()
