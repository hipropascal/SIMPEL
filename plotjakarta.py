import netCDF4
import math


def measure(lat1, lon1, lat2, lon2):
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000


if __name__ == '__main__':
    # result = measure(-6.012381, 106.678298,-6.135967, 107.059106)
    result = measure(-6.012381, 106.678298, -6.012381, 106.681004)
    print(result)
# -6.012381, 106.678298
# -6.135967, 107.059106

# 0.0027