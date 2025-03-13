"""
Функція розрахунку відстані між двома геоточками
"""
from geographiclib.geodesic import Geodesic



def distance(lat_1, lon_1, lat_2, lon_2):
    geod = Geodesic.WGS84  # Модель Землі
    result = geod.Inverse(lat_1, lon_1, lat_2, lon_2)
    # print(result)

    return f"{result['s12'] / 1000:.3f} км"  # Відстань у км


