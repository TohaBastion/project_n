"""
Основний файл застосунку, що ініціалізує  сам застосунок та ододає вікна через
менеджера вікон.
"""
from kivy.core.window import Window

Window.fullscreen = 'auto'


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.main_screen import MainScreen
from screens.activation_screen import ActivationScreen


class ASD(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(ActivationScreen(name='activation_screen'))
        return sm


if __name__ == '__main__':
    ASD().run()
