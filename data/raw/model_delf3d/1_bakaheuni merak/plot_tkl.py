import numpy as np
import math
from src.stegano import coder
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



def plot2d(H):
    plt.imshow(H)
    plt.colorbar(orientation='vertical')
    plt.show()

def repos(m):
    return np.flipud(np.rot90(m))


if __name__ == '__main__':
    # -8.114958, 114.342588
    # -8.260393, 114.491698
    lat1 = -8.114958
    lng1 = 114.342588
    lat2 = -8.260393
    lng2 = 114.491698
    interval = 0.0027  # ~300m
    xrange = abs(lat1 - lat2)
    yrange = abs(lng1 - lng2)
    lat2_mod = lat1 - (xrange // interval) * interval
    lng2_mod = lng1 + (yrange // interval) * interval
    path = 'data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/0_Gelombang(meter)__grid/'
    array_swh = np.zeros((10, 139, 82))
    array_dir = np.zeros((10, 139, 82))
    f_swh = open('wave_height.tkl')
    f_dir = open('wave_dir.tkl')
    lines_swh = f_swh.readlines()
    lines_dir = f_dir.readlines()
    mat = 0

    for idx,line in enumerate(lines_swh):
        data = line.split("  ")
        row_data = np.array(data, dtype=float)
        row_idx = idx % 139
        array_swh[mat,row_idx] = row_data[:]
        if idx % 139 == 0 and idx != 0:
            # plot2d(array_swh[mat])
            mat = mat + 1
            if mat == 10:
                break
    mat = 0

    for idx,line in enumerate(lines_dir):
        data = line.split("  ")
        row_data = np.array(data, dtype=float)
        row_idx = idx % 139
        array_dir[mat,row_idx] = row_data[:]
        if idx % 139 == 0 and idx != 0:
            # plot2d(array_dir[mat])
            mat = mat + 1
            if mat == 10:
                break


    # change into uv
    u = abs(array_swh) * np.sin((math.pi/180)*array_dir)
    v = abs(array_swh) * np.cos((math.pi/180)*array_dir)

    initial_date = datetime.strptime('01-10-2018 00:00','%d-%m-%Y %H:%M')
    for idt, time in enumerate(array_swh):
        incremental_date = initial_date + timedelta(hours=3*idt)
        fname = incremental_date.strftime("%d-%m-%Y %H_%M.png")
        img = coder.encode_uv_image(repos(u[idt]),repos(v[idt]),{"bottom": lat2_mod, "top":lat1 , "left": lng1, "right": lng2_mod})
        img.save(path+fname)
    print('done')


# ** VARIABLE x from map-series(50) ELEMENT HSIGN(139,82) REAL     *4
# **    NROW       NCOL     NPLANE
# XXXX
#       6950         82         50