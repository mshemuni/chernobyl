from typing import Dict

import numpy as np
import pygame

from .surface import Surface
from .. import V2D
from ..sound import Sound


class Board(Surface):
    def __init__(self, screen: pygame.Surface, x: int, y: int, dt: float) -> None:
        super().__init__(screen, x, y, dt)
        self.background_color = 64, 64, 64
        self.foreground_color = 255, 255, 255

        self.surface = pygame.Surface((self.screen.get_width(), 100))
        self.surface.fill(self.background_color)

        self.time_left = 0
        self.power = []
        self.power_capacity = 0

    import numpy as np

    def downsample(self, values: list[float], target: int = 100) -> np.ndarray:
        if len(values) <= target:
            return np.asarray(values, dtype=float)

        arr = np.asarray(values, dtype=float)

        # Compute bin edges
        indices = np.linspace(0, len(arr), target + 1, dtype=int)

        return np.array([
            arr[indices[i]:indices[i + 1]].mean()
            if indices[i] < indices[i + 1]
            else arr[indices[i]]
            for i in range(target)
        ])

    def draw_power_graph(self):
        values = self.downsample(self.power, 100)

        if len(values) < 2:
            return

        graph_width = 200
        graph_height = 60
        graph_x = self.screen.get_width() - graph_width - 10
        graph_y = 10

        max_value = max(values) or 1

        points = []
        count = len(values) - 1

        for i, value in enumerate(values):
            x = graph_x + int(i / count * graph_width)
            y = graph_y + graph_height - int((value / max_value) * graph_height)
            points.append((x, y))

        pygame.draw.lines(self.surface, (0, 255, 0), False, points, 2)

        pygame.draw.rect(
            self.surface,
            (200, 200, 200),
            (graph_x, graph_y, graph_width, graph_height),
            1
        )

    def generated_power(self):
        self.text(f"Generated power: {sum(self.power)} TW", V2D())

    def max_power(self):
        if len(self.power) > 0:
            maximum_power = str(max(self.power))
        else:
            maximum_power = "NaN"
        self.text(f"Peak power: {maximum_power}/{self.power_capacity} TW", V2D(0, 32))


    def show_time_left(self):
        font_each_menu = pygame.font.SysFont(None, 64)
        text = font_each_menu.render(str(self.time_left), True, self.foreground_color)
        rect = text.get_rect(
            center=(self.surface.get_width() // 2, 32)
        )
        self.surface.blit(text, rect)

    def draw(self):
        self.surface.fill(self.background_color)
        self.generated_power()
        self.show_time_left()
        self.max_power()
        self.draw_power_graph()