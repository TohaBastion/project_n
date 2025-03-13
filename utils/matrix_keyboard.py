import time
import board
from digitalio import DigitalInOut
from adafruit_matrixkeypad import Matrix_Keypad

# GPIO для рядків та стовпців
cols = [DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]
rows = [DigitalInOut(x) for x in (board.D26, board.D21, board.D20, board.D16)]

# Визначення клавіш для 4×4
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

# Ініціалізація клавіатури
keypad = Matrix_Keypad(rows, cols, keys)

def get_key():
    keys = keypad.pressed_keys
    if keys:
        return keys[0]
    return None

