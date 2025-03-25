#import random


#def check_machine_status(machine_id):
    #"""
    #Емуляція перевірки підключення кавомашини.
    #Для реального проєкту замінити цей код на читання сигналу датчика.
    #"""
    # Емуляція: кавомашина активна в 80% випадків
    #return random.choice(["active", "select", "active", "active", "inactive"])
    
import RPi.GPIO as GPIO
import time

# Налаштовуємо режим нумерації пінів
GPIO.setmode(GPIO.BCM)

# Визначаємо відповідність ID кавомашини до пінів її датчиків
machines = {
    "Machine 1": [17, 27, 22],  # GPIO-піни для першої кавомашини
    "Machine 2": [16, 20, 21]     # GPIO-піни для другої кавомашини
}

# Налаштовуємо GPIO як вхідні з pull-up резисторами
for pins in machines.values():
    for pin in pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def check_machine_status(machine_id):
    """Отримує ID кавомашини та повертає її стан залежно від датчиків."""
    if machine_id not in machines:
        return "Невідомий ID кавомашини"

    sensor_pins = machines[machine_id]

    # Зчитуємо стан датчиків
    sensor_states = [GPIO.input(pin) for pin in sensor_pins]

    # Логіка визначення стану кавомашини
    if sensor_states[0] == GPIO.LOW:
        return "inactive"
    elif sensor_states[1] == GPIO.LOW:
        return "active"
    elif sensor_states[2] == GPIO.LOW:
        return "select"
    else:
        return "fixed"



