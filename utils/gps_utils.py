import time
import serial
from calculations.calculate_azimuth import calculate_azimuth


import serial

def get_current_gps_data(lat_2, lon_2, *args):
    rawcoordinates = serial.Serial('COM7', baudrate=115200)

    lat_1 = None
    lon_1 = None
    current_azimuth = None

    while True:
        try:
            ser_bytes = rawcoordinates.readline()
            decoded_bytes = ser_bytes.decode('utf-8').strip()
            dataset = decoded_bytes.split(",")
            print(dataset)

            if dataset[0] == '$GNHDT' and len(dataset) > 1:
                try:
                    current_azimuth = float(dataset[1])
                except ValueError:
                    continue  # Пропускаємо рядки з помилками

            elif dataset[0] == '$GNRMC' and len(dataset) > 6:
                try:
                    lati_nmea = dataset[3]
                    lati_degrees = int(lati_nmea[:2])
                    lati_mmm = round(float(lati_nmea[2:]) / 60, 8)
                    latitude = lati_degrees + lati_mmm if dataset[4] == 'N' else -(lati_degrees + lati_mmm)

                    longti_nmea = dataset[5]
                    longti_degrees = int(longti_nmea[:3])
                    longti_mmm = round(float(longti_nmea[3:]) / 60, 8)
                    longtitude = longti_degrees + longti_mmm if dataset[6] == 'E' else -(longti_degrees + longti_mmm)

                    lat_1, lon_1 = latitude, longtitude
                except ValueError:
                    continue  # Пропускаємо рядки з помилками

            if lat_1 is not None and lon_1 is not None and current_azimuth is not None:
                relative_bearing = calculate_azimuth(lat_1, lon_1, lat_2, lon_2, current_azimuth)
                print(lat_1, lon_1)
                return relative_bearing

                # print(lat_1, lon_1, current_azimuth)
                # return {"lat_1": lat_1, "lon_1": lon_1, "current_azimuth": current_azimuth}

        except serial.SerialException:
            print("No GPS receiver connected.")


    #
    # print(lat_1, lon_1, current_azimuth)
    # return {"lat_1": lat_1, "lon_1": lon_1, "current_atimuth": current_azimuth}

    # return {"lat_1": latitude, "lon_1": longtitude, "current_azimuth": current_azimuth}


# get_current_gps_data()

# import random
# import math


# def get_current_gps_data():
#     # Початкові координати (наприклад, десь у Києві)
#     lat = 50.376560176166755
#     lon = 30.7289498822662
#     azimuth = 90  # Початковий азимут (північ)
#
#     # Випадкове зміщення координат (імітація руху)
#     delta_lat = random.uniform(-0.0005, 0.0005)  # Приблизно 50 метрів
#     delta_lon = random.uniform(-0.0005, 0.0005)
#
#     lat += delta_lat
#     lon += delta_lon
#
#     # Обчислення нового азимута (напрямку руху)
#     azimuth = (math.degrees(math.atan2(delta_lon, delta_lat)) + 360) % 360
#
#     return {"lat_1": lat, "lon_1": lon, "current_azimuth": azimuth}
#
#
# # Приклад виклику
# print(get_current_gps_data())
