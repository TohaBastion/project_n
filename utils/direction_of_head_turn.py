import RPi.GPIO as GPIO
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# Налаштування GPIO
GPIO.setmode(GPIO.BCM)
PWM_PIN = 12  # Замініть на потрібний пін
GPIO.setup(PWM_PIN, GPIO.OUT)

# Запускаємо ШІМ на 1000 Гц
pwm = GPIO.PWM(PWM_PIN, 1000)  # Частота 1 кГц
pwm.start(50)  # Початково 50% скважності (1.65V)

class PWMControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Яскравість: 0%")
        self.slider = Slider(min=0, max=100, value=0)
        self.slider.bind(value=self.update_pwm)

        layout.add_widget(self.label)
        layout.add_widget(self.slider)

        return layout

    def update_pwm(self, value):
        pwm.ChangeDutyCycle(value)  # Змінюємо скважність
        self.label.text = f"Яскравість: {int(value)}%"

    def on_stop(self):
        pwm.stop()
        GPIO.cleanup()  # Очищуємо GPIO при виході

if __name__ == "__main__":
    PWMControlApp().run()