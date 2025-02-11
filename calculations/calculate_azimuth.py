import multiprocessing
import math

data_queue = multiprocessing.Queue()


def calculate_azimuth(lat_1, lon_1, lat_2, lon_2, current_azimuth):
    """
            Розрахунок азимуту між двома GPS координатами.
            """

    try:

        lat1, lon1, lat2, lon2 = map(math.radians, [lat_1, lon_1, lat_2, lon_2])
        dlon = lon2 - lon1
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        initial_bearing = math.atan2(x, y)
        bearing = (math.degrees(initial_bearing) + 360) % 360
        relative_bearing = (bearing - current_azimuth + 360) % 360
        print(relative_bearing)
        return relative_bearing
    except Exception as e:
        print("Щось пішло не так")
