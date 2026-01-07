from typing import Dict

import pygame

from .surface import Surface
from ..sound import Sound


class Upgrader(Surface):
    def __init__(self, screen: pygame.Surface, x: int, y: int, dt: float, paused: bool = False) -> None:
        super().__init__(screen, x, y, dt)
        self.background_color = 227, 227, 227
        self.foreground_color = 0, 0, 0
        self.surface.fill(self.background_color)
        self.paused = paused
        self.hovered_item = None

        self.background_sound = Sound("statics/sounds/spooky.mp3")
        self.background_sound.play(loop=True)

        self.sounds = {
            "click": Sound("statics/sounds/click.mp3"),
            "hover": Sound("statics/sounds/hover.mp3"),
        }

    def __del__(self):
        try:
            self.background_sound.stop()
        except:
            pass

    def draw(self):
        self.items()

    def items(self) -> Dict[str, pygame.Rect]:
        grid: Dict[str, pygame.Rect] = {}

        rows = cols = 10
        padding = 8
        gap = 4

        width, height = self.surface.get_size()

        cell_width = (width - 2 * padding - (cols - 1) * gap) // cols
        cell_height = (height - 2 * padding - (rows - 1) * gap) // rows

        font = pygame.font.SysFont(None, 16)

        index = 0
        for row in range(rows):
            for col in range(cols):
                x = padding + col * (cell_width + gap)
                y = padding + row * (cell_height + gap)

                rect = pygame.Rect(x, y, cell_width, cell_height)

                color = (200, 200, 200) if (row + col) % 2 == 0 else (180, 180, 180)

                pygame.draw.rect(self.surface, color, rect, border_radius=4)
                pygame.draw.rect(self.surface, (120, 120, 120), rect, 1, border_radius=4)

                label = f"Item {index}"
                text = font.render(label, True, self.foreground_color)
                text_rect = text.get_rect(center=rect.center)
                self.surface.blit(text, text_rect)

                grid[label] = rect
                index += 1

        return grid
