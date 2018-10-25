from netCDF4 import Dataset
import numpy as np
import glob,os
from src.stegano import coder


out = "/Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/observasi/3_HF Radar__grid/0_Arus (knot)|0|8/"
src = "/Users/maritim/Project/BMKG/SIMPEL/data/raw/HF_RADAR/"
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(src)
for file in glob.glob("*.nc"):
    print(file)
    hfradar = Dataset(src+file,'r', format="NETCDF4")
    v = hfradar['v'][0][:].filled(0)*0.0194384
    u = hfradar['u'][0][:].filled(0)*0.0194384
    v = np.fliplr(v)
    u = np.fliplr(u)
    v = np.rot90(v)
    u = np.rot90(u)
    parsed = file.split("_")
    mm = parsed[3]
    dd = parsed[4]
    yyyy = parsed[2]
    h = parsed[5][:2]
    m = parsed[5][2:4]
    new_filename = '{}-{}-{} {}_{}.png'.format(dd,mm,yyyy,h,m)
    img = coder.encode_uv_image(u, v, {"bottom": -8.276620, "top": -8.095783, "left": 114.356689-0.002681, "right": 114.497383-0.002681})
    img.save(out+new_filename)

#114.433235 - 114.435916

# /Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/observasi/3_HF Radar__grid/0_Arus (knot)|0|8/11-10-2018 21_30.png
# /Users/maritim/Project/BMKG/SIMPEL/data/data_trees/0_ketapang gilimanuk__-8.148774__114.420108__13/peta_prakiraan/1_Level Permukaan(meter)__grid/11-10-2018 21_30.png