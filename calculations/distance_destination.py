"""
Функція розрахунку відстані між двома геоточками
"""
from geographiclib.geodesic import Geodesic
from utils.gps_utils import get_current_gps_data

# data_pos = get_current_gps_data()
# lat1, lon1 = data_pos["lat_1"], data_pos["lon_1"]
# current_azimuth = data_pos["current_azimuth"]


# lat2, lon2 = 50.43807462527633, 30.47538814538834


# Обчислення відстані


def distance(lat_2, lon_2):
    data_pos = get_current_gps_data()
    lat_1, lon_1 = data_pos["lat_1"], data_pos["lon_1"]
    # print(lat_1, lon_1)
    geod = Geodesic.WGS84  # Модель Землі
    result = geod.Inverse(lat_1, lon_1, lat_2, lon_2)
    # print(result)

    return f"{result['s12'] / 1000:.3f} км"  # Відстань у км


