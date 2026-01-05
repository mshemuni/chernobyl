from typing import Optional, Tuple

import pygame

from ..v2d import V2D


class Surface:
    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        self.screen = screen
        self.x = x
        self.y = y

        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background_color = 62, 62, 62
        self.foreground_color = 0, 0, 0
        self.surface.fill(self.background_color)

    def text(self, text: str, position: V2D, color: Optional[Tuple[int, int, int]] = None, font_size: int = 48) -> None:
        if color is None:
            the_color = self.foreground_color
        else:
            the_color = color

        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, the_color)
        self.surface.blit(text_surface, position.as_tuple())

    def circle(self, position: V2D, radius: float, color: Optional[Tuple[int, int, int]] = None) -> None:
        if color is None:
            the_color = self.foreground_color
        else:
            the_color = color

        pygame.draw.circle(
            self.surface,
            the_color,
            position.as_tuple(),
            radius
        )

    def line(self, start: V2D, end: V2D, color: Optional[Tuple[int, int, int]] = None, width: int = 1) -> None:
        if color is None:
            the_color = self.foreground_color
        else:
            the_color = color

        pygame.draw.line(
            self.surface,
            the_color,
            start.as_tuple(),
            end.as_tuple(),
            width
        )



    def hover_handler(self):
        pass

    def event_handler(self, event):
        pass

    def draw(self):
        pass