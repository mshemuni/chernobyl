from typing import Dict

import pygame

from .surface import Surface
from ..sound import Sound


class Menu(Surface):
    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        super().__init__(screen, x, y)
        self.background_color = 227, 227, 227
        self.foreground_color = 0, 0, 0
        self.surface.fill(self.background_color)
        self.hovered_item = None

        self.sounds = {
            "click": Sound("statics/sound/click.mp3"),
            "hover": Sound("statics/sound/hover.mp3"),
        }

    def hover_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        current_hover = None

        for name, rect in self.items().items():
            if rect.collidepoint(mouse_pos):
                current_hover = name

                if self.hovered_item != name:
                    self.sounds["hover"].play()

                break

        self.hovered_item = current_hover

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            for name, rect in self.items().items():
                if rect.collidepoint(mouse_pos):
                    self.sounds["click"].play()
                    return name


    def items(self) -> Dict[str, pygame.Rect]:
        items = {}

        font_title = pygame.font.SysFont(None, 128)
        title_text = font_title.render("Chernobyl", True, self.foreground_color)
        title_rect = title_text.get_rect(
            center=(self.surface.get_width() // 2, self.surface.get_height() // 10)
        )
        self.surface.blit(title_text, title_rect)

        font_each_menu = pygame.font.SysFont(None, 64)

        def add_item(name, y_ratio):
            text = font_each_menu.render(name, True, self.foreground_color)
            rect = text.get_rect(
                center=(self.surface.get_width() // 2, int(self.surface.get_height() / y_ratio))
            )
            self.surface.blit(text, rect)
            items[name] = rect

        add_item("New Game", 1.80)
        add_item("Options", 1.625)
        add_item("Exit", 1.475)

        return items