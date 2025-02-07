from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from utils.machine_check import check_machine_status
from kivy.uix.boxlayout import BoxLayout
from widgets.line_test import LineWidget
from calculations.calculate_azimuth import calculate_azimuth
from calculations.distance_destination import distance


class MainScreen(Screen):
    initialized = True  # Чи були введені координати?

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10)
        self.add_widget(self.layout)
        self.machines = {}
        self.current_selection = 0  # Індекс обраної кавомашини

        # Верхня частина єкрану (поля для введеня координат)
        self.top_layout = GridLayout(cols=2, padding=2, size_hint_y=0.25)
        self.layout.add_widget(self.top_layout)

        # Ліва частина (широта)
        self.lat_input_layout = BoxLayout(padding=1)
        self.lat_input = TextInput(hint_text="Широта точки призначення", multiline=False)
        self.lat_input_layout.add_widget(self.lat_input)

        # Права частина (довгота)
        self.lon_input_layout = BoxLayout(padding=1)
        self.lon_input = TextInput(hint_text="Довгота точки призначення", multiline=False)
        self.lon_input_layout.add_widget(self.lon_input)

        self.top_layout.add_widget(self.lat_input_layout)
        self.top_layout.add_widget(self.lon_input_layout)

        # Кнопка для підтвердження введення
        self.submit_button = Button(text="Обчислити напрямок", size_hint_y=0.2)
        self.submit_button.bind(on_press=self.submit_on_press)
        self.layout.add_widget(self.submit_button)

        # Дані по відстані
        self.label_layout = BoxLayout(padding=1, size_hint_y=0.1)
        self.layout.add_widget(self.label_layout)
        if self.initialized:
            self.label = Label(text="дані відсутні")
            self.label_layout.add_widget(self.label)

        # Додаємо віджет лінії
        self.line_widget_layout = BoxLayout(orientation="vertical")
        self.layout.add_widget(self.line_widget_layout)
        self.line_widget = LineWidget(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.line_widget_layout.add_widget(self.line_widget)

        # Додаємо 4 кавомашини
        for i in range(1, 3):
            machine_id = f"Machine {i}"
            button = Button(
                text=machine_id,
                font_size=16,
                background_normal="",
                background_color=[1, 1, 1, 1],  # Білий фон за замовчуванням
                color=[0, 0, 0, 1],  # Чорний текст за замовчуванням
                disabled=False,
            )
            self.machines[machine_id] = {
                "status": False,  # Початковий стан — неактивна
                "button": button,
            }
            button.bind(on_release=lambda btn, mid=machine_id: self.activate_machine(mid))
            self.layout.add_widget(button)

        # self.add_widget(self.layout)

        # Оновлення статусу кожні 5 секунд
        self.update_machine_status()

        # Підключення обробки клавіш
        Window.bind(on_key_down=self.on_key_down)

        # Виділяємо першу активну кавомашину
        self.update_selection()

    def submit_on_press(self, *args):
        try:
            azimuth = calculate_azimuth(float(self.lat_input.text), float(self.lon_input.text))
            self.line_widget.angle = azimuth
            current_distance = distance(float(self.lat_input.text), float(self.lon_input.text))
            self.label.text = (f"до цілі:  {current_distance}")

        except:
            self.label.text = ("Невірно введені данні!!!")

    def on_size(self, *args):
        self.line_widget.on_size()

    def update_machine_status(self, *args):
        """
        Оновлює стан кожної кавомашини: активна чи неактивна.
        """
        for machine_id, machine in self.machines.items():
            status = check_machine_status(machine_id)  # Перевірка підключення
            machine["status"] = status
            button = machine["button"]

            if status:
                # Активна кнопка: чорний текст, білий фон
                button.color = [0, 0, 0, 1]
                button.background_color = [1, 1, 1, 1]
                button.disabled = False
            else:
                # Неактивна кнопка: сірий текст, світло-сірий фон
                button.color = [0.5, 0.5, 0.5, 1]
                button.background_color = [0.9, 0.9, 0.9, 1]
                button.disabled = True

        # Перевіряємо, чи обрана кнопка активна
        self.ensure_active_selection()

        # Оновлюємо статус через 5 секунд
        Clock.schedule_once(self.update_machine_status, 5)

    def ensure_active_selection(self):
        """
        Якщо поточно обрана кавомашина неактивна, перемикає вибір на першу активну.
        """
        active_machines = [id for id, m in self.machines.items() if m["status"]]
        if active_machines:
            selected_id = list(self.machines.keys())[self.current_selection]
            if selected_id not in active_machines:
                self.current_selection = list(self.machines.keys()).index(active_machines[0])
        self.update_selection()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """
        Обробка натискання клавіш:
        - Стрілка вверх/вниз: перемикає вибір між активними кавомашинами.
        - Enter: активує вибрану кавомашину.
        """
        if self.lon_input.focus or self.lat_input.focus:
            return False
        if not self.manager or self.manager.current != "main_screen":
            return  # Дія відхиляється, якщо цей екран не активний
        active_machines = [id for id, m in self.machines.items() if m["status"]]
        if not active_machines:
            return  # Немає активних машин

        if key == 273:  # Стрілка вгору
            self.current_selection = self.get_next_selection(-1, active_machines)
            self.update_selection()
        elif key == 274:  # Стрілка вниз
            self.current_selection = self.get_next_selection(1, active_machines)
            self.update_selection()
        elif key == 13:  # Enter
            selected_id = list(self.machines.keys())[self.current_selection]
            if selected_id in active_machines:
                self.activate_machine(selected_id)
        return True

    def get_next_selection(self, direction, active_machines):
        """
        Отримує індекс наступної активної кавомашини в заданому напрямку.
        """
        current_id = list(self.machines.keys())[self.current_selection]
        current_index = active_machines.index(current_id) if current_id in active_machines else 0

        # Обчислюємо наступний індекс
        next_index = (current_index + direction) % len(active_machines)

        # Отримуємо глобальний індекс
        return list(self.machines.keys()).index(active_machines[next_index])

    def update_selection(self):
        """
        Підсвічує обрану кавомашину.
        """
        for i, (machine_id, machine) in enumerate(self.machines.items()):
            button = machine["button"]
            if machine["status"]:
                if i == self.current_selection:
                    # Підсвічуємо обрану кнопку
                    button.background_color = [0.5, 0.8, 1, 1]  # Блакитний фон
                else:
                    # Звичайна активна кнопка
                    button.background_color = [1, 1, 1, 1]  # Білий фон

    def activate_machine(self, machine_id):
        """
        Логіка активації кавомашини.
        """
        print(f"Кавомашина {machine_id} активована!")
        self.manager.current = "activation_screen"
        self.manager.get_screen("activation_screen").setup(machine_id)
