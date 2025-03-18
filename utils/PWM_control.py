import RPi.GPIO as GPIO
import time

# Налаштування GPIO
GPIO.setmode(GPIO.BCM)
PWM_PIN = 17  # Вибери потрібний пін
GPIO.setup(PWM_PIN, GPIO.OUT)

# Запускаємо ШІМ із частотою 1000 Гц
pwm = GPIO.PWM(PWM_PIN, 1000)
pwm.start(50)  # Початкова скважність 50%

def calculate_duty_cycle(angle):
    """Обчислює скважність на основі кута."""
    if 0 <= angle <= 60:
        return 50 + (angle / 60) * 50  # Лінійний ріст 50% → 100%
    elif 300 <= angle <= 360:
        return ((angle - 300) / 60) * 50  # Лінійне зменшення 50% → 0%
    else:
        return 50  # В інших випадках 50%


def pwm_calculate(angle):
    try:
        duty = calculate_duty_cycle(angle)
        pwm.ChangeDutyCycle(duty)
        #print(f"Кут: {angle}° -> Скважність: {duty:.1f}%")

    except KeyboardInterrupt:
        print("\nЗавершення роботи.")
        pwm.stop()
        GPIO.cleanup()
