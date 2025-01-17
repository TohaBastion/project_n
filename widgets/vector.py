from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, Rotate, PopMatrix, Line, Translate
from kivy.clock import Clock
from utils.calculate_bearing import calculate_bearing


class ArrowWidget(Widget):
    def __init__(self, lat1, lon1, lat2, lon2, device_orientation=0, **kwargs):
        """
        ArrowWidget обчислює напрямок між двома точками і візуалізує стрілку.

        :param lat1: Широта поточної позиції
        :param lon1: Довгота поточної позиції
        :param lat2: Широта точки призначення
        :param lon2: Довгота точки призначення
        :param device_orientation: Поточний азимут пристрою
        """
        super().__init__(**kwargs)
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.device_orientation = device_orientation

        # Обчислюємо напрямок
        self.bearing = calculate_bearing(lat1, lon1, lat2, lon2)
        self.relative_bearing = (self.bearing - self.device_orientation + 360) % 360

        # Малюємо стрілку
        with self.canvas:
            PushMatrix()
            self.translate = Translate(self.center_x, self.center_y)  # Центруємо стрілку
            self.rotation = Rotate(origin=(0, 0), angle=self.relative_bearing)  # Поворот стрілки
            self.arrow = Line(points=[-30, 0, 30, 0, 0, 90, -30, 0], width=2)  # Стрілка
            PopMatrix()

        # Оновлюємо орієнтацію стрілки при зміні розміру
        self.bind(size=self.on_size, pos=self.on_size)

        # Додаємо приклад періодичного оновлення
        Clock.schedule_once(self.demo_update, 3)

    def set_position(self, lat1, lon1, lat2, lon2):
        """Оновлення координат і перерахунок напрямку."""
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.bearing = calculate_bearing(lat1, lon1, lat2, lon2)
        self.update_arrow()

    def set_device_orientation(self, device_orientation):
        """Оновлення орієнтації пристрою."""
        self.device_orientation = device_orientation
        self.update_arrow()

    def update_arrow(self):
        """Оновлення напряму стрілки на основі нових даних."""
        self.relative_bearing = (self.bearing - self.device_orientation + 360) % 360
        self.rotation.angle = self.relative_bearing

    def on_size(self, *args):
        """Оновлення позиції стрілки при зміні розміру екрану."""
        self.translate.xy = (self.center_x, self.center_y)

    # @staticmethod
    # def calculate_bearing(lat1, lon1, lat2, lon2):
    #     """Розрахунок азимуту між двома GPS координатами."""
    #     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    #     dlon = lon2 - lon1
    #     x = math.sin(dlon) * math.cos(lat2)
    #     y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    #     initial_bearing = math.atan2(x, y)
    #     bearing = (math.degrees(initial_bearing) + 360) % 360
    #     return bearing

    def demo_update(self, *args):
        """Демонстраційне оновлення даних через 3 секунди."""
        self.set_position(50.4501, 30.5234, 49.8397, 24.0297)  # Київ -> Париж
        self.set_device_orientation(2)  # Пристрій повернувся на 90 градусів
