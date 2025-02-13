from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from utils.check_signal import check_signal_1_status, check_signal_2_status
from kivy.uix.boxlayout import BoxLayout
from widgets.vector import ArrowWidget
from widgets.line_test import LineWidget


class ActivationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Головне компонування екрана
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.add_widget(self.layout)
        self.machine_id = None

        # Верхня частина екрану (статуси + новий віджет)
        self.top_layout = GridLayout(cols=2, spacing=20)
        self.layout.add_widget(self.top_layout)

        # Ліва частина: статуси датчиків
        self.left_status_layout = BoxLayout(orientation="vertical", spacing=10)
        self.indicator1 = Label(text="Signal 1: 0", font_size=20, color=[1, 0, 0, 1])  # Червоний текст
        self.indicator2 = Label(text="Signal 2: 0", font_size=20, color=[1, 0, 0, 1])
        self.left_status_layout.add_widget(self.indicator1)
        self.left_status_layout.add_widget(self.indicator2)

        # Права частина: новий віджет
        self.line_widget_layout = BoxLayout(orientation="vertical")
        self.top_layout.add_widget(self.line_widget_layout)
        self.line_widget = LineWidget(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.line_widget_layout.add_widget(self.line_widget)
        # self.right_widget = ArrowWidget(50.4501, 30.5234, 49.8397, 24.0297, 45,
        #                                 size_hint=(1, 1))  # Ваша логіка налаштування
        self.top_layout.add_widget(self.left_status_layout)
        # self.top_layout.add_widget(self.right_widget)

        # Нижня частина: кнопки
        self.bottom_layout = BoxLayout(orientation="vertical", spacing=10)
        self.layout.add_widget(self.bottom_layout)

        # Кнопки
        self.start_button = Button(
            text="Пуск",
            font_size=20,
            color=[0, 0, 0, 1],
            background_normal="",
            background_color=[0.5, 0.5, 0.5, 1],  # Сірий фон (неактивний стан)
            disabled=True,
        )
        self.back_button = Button(
            text="Назад",
            font_size=20,
            color=[0, 0, 0, 1],
            background_normal="",
            background_color=[1, 1, 1, 1],
        )
        self.bottom_layout.add_widget(self.start_button)
        self.bottom_layout.add_widget(self.back_button)

        # Підключення кнопок до дій
        self.start_button.bind(on_release=self.start_action)
        self.back_button.bind(on_release=self.go_back)

        # Логіка клавіш
        self.current_selection = 0  # Індекс вибраної кнопки
        self.buttons = (self.start_button, self.back_button)
        Window.bind(on_key_down=self.on_key_down)

    def setup(self, machine_id):
        """
        Викликається під час переходу до екрану.
        Скидає стан індикаторів та оновлює логіку для вибраної кавомашини.
        """
        self.machine_id = machine_id
        self.indicator1.text = "Signal 1: 0"
        self.indicator1.color = [1, 0, 0, 1]  # Червоний текст
        self.indicator2.text = "Signal 2: 0"
        self.indicator2.color = [1, 0, 0, 1]
        self.start_button.disabled = True
        self.start_button.background_color = [0.5, 0.5, 0.5, 1]  # Сірий фон

        # Скидаємо вибір
        self.current_selection = None
        self.check_signals()

        # Автоматично вибираємо першу активну кнопку
        self.current_selection = 0
        while self.buttons[self.current_selection].disabled:
            self.current_selection = (self.current_selection + 1) % len(self.buttons)

        self.update_selection()

    def check_signals(self):
        """
        Логіка перевірки сигналів (імітація).
        Якщо обидва сигнали True, активує кнопку "Пуск".
        """
        signal1 = check_signal_1_status(self.machine_id)  # Замінити на реальну логіку
        signal2 = check_signal_2_status(self.machine_id)  # Замінити на реальну логіку

        # Оновлюємо індикатори
        self.indicator1.text = "Датчик 1: доступний" if signal1 else "Датчик 1: відсутній"
        self.indicator1.color = [0, 1, 0, 1] if signal1 else [1, 0, 0, 1]
        self.indicator2.text = "Датчик 2: доступний" if signal2 else "Датчик 2: відсутній"
        self.indicator2.color = [0, 1, 0, 1] if signal2 else [1, 0, 0, 1]

        # Активуємо кнопку "Пуск", якщо обидва сигнали True
        if signal1 and signal2:
            self.start_button.disabled = False
            self.start_button.background_color = [0, 1, 0, 1]  # Зелений фон
        else:
            self.start_button.disabled = True
            self.start_button.background_color = [0.5, 0.5, 0.5, 1]  # Сірий фон

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """
        Обробка натискання клавіш:
        - Стрілка вгору/вниз: перемикає вибір між кнопками, пропускаючи неактивні.
        - Enter: натискає вибрану кнопку, якщо вона активна.
        """
        if not self.manager or self.manager.current != "activation_screen":
            return  # Дія відхиляється, якщо цей екран не активний

        if key == 273:  # Стрілка вгору
            self.current_selection = (self.current_selection - 1) % len(self.buttons)
            while self.buttons[self.current_selection].disabled:
                self.current_selection = (self.current_selection - 1) % len(self.buttons)
            self.update_selection()
        elif key == 274:  # Стрілка вниз
            self.current_selection = (self.current_selection + 1) % len(self.buttons)
            while self.buttons[self.current_selection].disabled:
                self.current_selection = (self.current_selection + 1) % len(self.buttons)
            self.update_selection()
        elif key == 13:  # Enter
            if self.current_selection is not None:
                selected_button = self.buttons[self.current_selection]
                if not selected_button.disabled:
                    selected_button.trigger_action()  # Виконує прив'язану дію кнопки
        return True

    def update_selection(self):
        """
        Підсвічує вибрану кнопку.
        """
        for i, button in enumerate(self.buttons):
            if i == self.current_selection:
                button.background_color = [0.5, 0.8, 1, 1]  # Блакитний фон
            else:
                # Відновлюємо колір залежно від стану
                button.background_color = (
                    [0, 1, 0, 1] if not button.disabled and button == self.start_button else
                    [1, 1, 1, 1] if button == self.back_button else
                    [0.5, 0.5, 0.5, 1]
                )

    def start_action(self, instance):
        """
        Дія для кнопки "Пуск".
        """
        print("Кавомашина запущена!")
        self.update_selection()

    def go_back(self, instance):
        """
        Дія для кнопки "Назад".
        """
        self.manager.current = "main_screen"
