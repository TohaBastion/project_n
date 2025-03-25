import time
import math
from rpi_ws281x import PixelStrip, Color

# 🔹 Параметри стрічки
LED_COUNT = 16      # Кількість світлодіодів
LED_PIN = 18        # Пін Raspberry Pi (GPIO 18)
LED_FREQ_HZ = 800000  # Частота
LED_DMA = 10        # DMA канал
LED_BRIGHTNESS = 255 # Яскравість (0-255)
LED_INVERT = False   # Чи потрібно інвертувати сигнал

# 🔹 Ініціалізація стрічки
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

# 🔹 Налаштування
#STEP_ANGLE = 3      # Крок зміни кута (3°)
#DELAY_TIME = 0.2    # Затримка оновлення (секунди)

# 🔹 Початковий кут
angle = 0.0

def update_leds(theta):
    """ Оновлення кольору діодів відповідно до кута """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)  # Встановлюємо чорний (вимкнено)
    strip.show()  # Гасимо всі діоди перед оновленням

    # 🔹 Середні діоди (8 і 9) світять білим при куті близькому до 0° або 360°
    if (358.5 <= theta <= 360) or (0 <= theta <= 1.5):
        strip.setPixelColor(7, Color(255, 255, 255))  # 8-й діод (індекс 7)
        strip.setPixelColor(8, Color(255, 255, 255))  # 9-й діод (індекс 8)

    # 🔹 Правий сектор (кут 1.5° - 45°)
    if 1.5 < theta < 45:
        num_leds = math.ceil(theta / (45.0 / 8))  # Визначаємо кількість червоних діодів
        for i in range(num_leds):
            strip.setPixelColor(8 + i, Color(255, 0, 0))  # 9-й по 16-й

    # 🔹 Правий сектор повністю (кут 45° - 180°)
    if 45 <= theta <= 180:
        for i in range(8, 16):
            strip.setPixelColor(i, Color(255, 0, 0))  # 9-й по 16-й

    # 🔹 Лівий сектор (кут 358.5° - 315°)
    if 315 < theta < 358.5:
        num_leds = math.ceil((360 - theta) / (45.0 / 8))  # Визначаємо кількість діодів
        for i in range(num_leds):
            strip.setPixelColor(7 - i, Color(255, 0, 0))  # 8-й по 1-й

    # 🔹 Лівий сектор повністю (кут 180° - 315°)
    if 180 <= theta < 315:
        for i in range(8):
            strip.setPixelColor(i, Color(255, 0, 0))  # 8-й по 1-й

    strip.show()  # Оновлення стрічки
    
def stop_leds():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)  # Встановлюємо чорний (вимкнено)
    strip.show()
    


