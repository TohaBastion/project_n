from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from matrix_keyboard import get_key

class KeypadApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.input1 = TextInput(font_size=32, readonly=True)
        self.input2 = TextInput(font_size=32, readonly=True)
        self.layout.add_widget(self.input1)
        self.layout.add_widget(self.input2)

        self.current_input = self.input1
        Clock.schedule_interval(self.read_keypad, 0.05)
        return self.layout

    def read_keypad(self, dt):
        key = get_key()
        if key:
            if key == "A":   # Переключення між полями
                self.current_input = self.input1
            elif key == "B":   # Переключення між полями
                self.current_input = self.input2
            elif key == "*":  # Очищення введення
                self.current_input.text = ""
            elif key == "C":
                self.current_input.text += "."
            elif key in ["D", "#"]:  # Можливе використання для додаткових функцій
                print(f"Натиснуто спец. клавішу: {key}")
            else:
                self.current_input.text += key  # Введення цифр

if __name__ == '__main__':
    KeypadApp().run()
