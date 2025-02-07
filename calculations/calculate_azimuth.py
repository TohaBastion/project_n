from utils.gps_utils import get_current_gps_data
import math


def calculate_azimuth(lat_2, lon_2):
    """
            Розрахунок азимуту між двома GPS координатами.
            """
    gps_data = get_current_gps_data()
    lat_1, lon_1 = gps_data["lat_1"], gps_data["lon_1"]
    current_azimuth = gps_data["current_azimuth"]
    lat1, lon1, lat2, lon2 = map(math.radians, [lat_1, lon_1, lat_2, lon_2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_bearing = math.atan2(x, y)
    bearing = (math.degrees(initial_bearing) + 360) % 360
    relative_bearing = (bearing - current_azimuth + 360) % 360
    print(relative_bearing)
    return relative_bearing
