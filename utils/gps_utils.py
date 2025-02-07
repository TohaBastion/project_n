import serial


# def get_gps_data():
#
#     try:
#
#         rawcoordinates = serial.Serial('COM17', baudrate=115200)
#
#         ser_bytes = rawcoordinates.readline()
#         decoded_bytes = ser_bytes.decode('utf-8')
#         dataset = decoded_bytes.split(",")
#         if dataset[0] == '$GNRMC':
#             # Convert latitude data to decimal coordinates
#             lati_nmea = dataset[3]
#             lati_nmea = lati_nmea
#             lati_degrees = lati_nmea[:2]
#
#             if dataset[4] == 'S':
#                 latitude_degrees = int(lati_degrees) * -1
#             else:
#                 latitude_degrees = int(lati_degrees)
#             lati_ddd = lati_nmea[2:10]
#             lati_mmm = float(lati_ddd) / 60
#             lati_mmm = round(lati_mmm, 8)
#             latitude = latitude_degrees + lati_mmm
#
#             # Convert longtitude data to decimal coordinates
#             longti_nmea = dataset[5]
#             longti_degrees = longti_nmea[:3]
#             if dataset[6] == 'W':
#                 longtitude_degrees = int(longti_degrees) * -1
#             else:
#                 longtitude_degrees = int(longti_degrees)
#             longti_ddd = longti_nmea[3:10]
#             longti_mmm = float(longti_ddd) / 60
#             longti_mmm = round(longti_mmm, 8)
#             longtitude = longtitude_degrees + longti_mmm
#
#             print(dataset[8])
#             # print("Longtitude",(longtitude), "Latitude",(latitude))
#
#
#
#     except serial.SerialException:
#         print("No GPS receiver connected.")

import random
import math


def get_current_gps_data():
    # Початкові координати (наприклад, десь у Києві)
    lat = 50.376560176166755
    lon = 30.7289498822662
    azimuth = 0  # Початковий азимут (північ)

    # Випадкове зміщення координат (імітація руху)
    delta_lat = random.uniform(-0.0005, 0.0005)  # Приблизно 50 метрів
    delta_lon = random.uniform(-0.0005, 0.0005)

    lat += delta_lat
    lon += delta_lon

    # Обчислення нового азимута (напрямку руху)
    azimuth = (math.degrees(math.atan2(delta_lon, delta_lat)) + 360) % 360

    return {"lat_1": lat, "lon_1": lon, "current_azimuth": azimuth}


# Приклад виклику
print(get_current_gps_data())