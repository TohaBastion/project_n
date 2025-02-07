from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Triangle
from kivy.properties import NumericProperty
from kivy.clock import Clock


class LineWidget(Widget):
    angle = NumericProperty(0)  # Кут, що оновлюється

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_y = self.center_y
        self.line_x = self.center_x
        self.pixels_per_degree = 0
        self.square_size = 0
        self.circle_size = 0
        self.update_visuals()
        Clock.schedule_interval(self.simulate_angle_change, 0.05)

    def on_size(self, *args):
        """Оновлюємо розміри при зміні розміру вікна."""
        self.line_y = self.center_y
        self.line_x = self.center_x
        self.pixels_per_degree = self.right / 90
        self.square_size = self.pixels_per_degree * 2.5
        self.circle_size = self.square_size // 4
        self.update_visuals()

    def on_angle(self, instance, value):
        """Оновлюємо позицію кола, коли змінюється кут."""
        self.update_visuals()

    def update_visuals(self, *args, **kwargs):
        """Оновлення графічних елементів."""
        self.canvas.clear()
        with self.canvas:
            # Масштабування

            # Лінія
            Color(0, 1., 0, 0.5)
            Line(points=[self.x, self.line_y, self.right, self.line_y], width=1)
            Line(points=[self.line_x, self.line_y - self.square_size, self.line_x, self.line_y + self.square_size], width=1)

            # Квадрат
            square_offset = self.pixels_per_degree * 0
            square_x = self.center_x + square_offset - self.square_size / 2
            square_y = self.line_y - self.square_size / 2

            Line(rectangle=(square_x, square_y, self.square_size, self.square_size), width=1)

            # Коло
            if 315 <= self.angle <= 360 or 0 <= self.angle <= 45:
                relative_angle = 0
                if self.angle >= 315:
                    relative_angle = self.angle - 360
                elif self.angle < 0:
                    relative_angle = self.angle

                displacement = self.pixels_per_degree * relative_angle
                circle_x = self.line_x + displacement
                circle_y = self.line_y

                Line(circle=(circle_x, circle_y, self.circle_size), width=1)


            # Стрілки
            if 180 <= self.angle < 315:
                Color(1, 0, 0, 1)
                Triangle(points=[10, self.line_y, 20, self.line_y + 10, 20, self.line_y - 10])
            if 180 >= self.angle > 45:
                Color(1, 0, 0, 1)
                Triangle(points=[self.width - 10, self.line_y, self.width - 20, self.line_y + 10, self.width - 20, self.line_y - 10])


    def simulate_angle_change(self, dt):
        """Симуляція зміни кута від 360 (ліворуч) через 0 до 180 (праворуч)."""
        import math
        raw_angle = self.angle
        if raw_angle >= 0:
            self.angle = raw_angle
        else:
            self.angle = 360 + raw_angle

class LineApp(App):
    def build(self):
        self.widget = LineWidget()
        Clock.schedule_interval(self.simulate_angle_change, 0.05)  # Для тесту: зміна кута
        return self.widget

    def simulate_angle_change(self, dt):
        """Симуляція зміни кута від 360 (ліворуч) через 0 до 180 (праворуч)."""
        import math
        raw_angle = 10

        if raw_angle >= 0:
            self.widget.angle = raw_angle
        else:
            self.widget.angle = 360 + raw_angle


if __name__ == "__main__":
    LineApp().run()