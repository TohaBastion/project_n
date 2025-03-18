import time
import board
from digitalio import DigitalInOut
from adafruit_matrixkeypad import Matrix_Keypad

# GPIO налаштування
cols = [DigitalInOut(x) for x in (board.D25, board.D8, board.D7, board.D1)]
rows = [DigitalInOut(x) for x in (board.D6, board.D13, board.D19, board.D26)]

keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

# Ініціалізація клавіатури
keypad = Matrix_Keypad(rows, cols, keys)

# Буфер для debounce
last_key = None
last_press_time = 0
DEBOUNCE_TIME = 0.2  # 200 мс

def get_key():
    global last_key, last_press_time
    keys = keypad.pressed_keys
    if keys:
        key = keys[0]  # Беремо перший натиснутий символ
        current_time = time.monotonic()
        if key != last_key or (current_time - last_press_time > DEBOUNCE_TIME):
            last_key = key
            last_press_time = current_time
            return key
    else:
        last_key = None  # Скидання при відпусканні клавіші
    return None

