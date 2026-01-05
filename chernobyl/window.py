from typing import Optional

import pygame

from .surface import Menu
from .surface.board import Board
from .surface.reactor import Reactor
from .utils import Fixer


class Window:
    def __init__(self, width: int, height: int, title: str = "Chernobyl", full_screen: bool = True,
                 fps: Optional[int] = None):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title
        self.full_screen = full_screen
        self.flags = pygame.FULLSCREEN if full_screen else pygame.RESIZABLE
        self.fps = Fixer.fps(fps)

        self.level = 1

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps) / 1000.0

        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        pygame.display.set_caption(self.title)

        self.hovered_item = None

        self.menu_surface = Menu(self.screen, 0, 0, self.dt)
        self.reactor_surface = None
        self.board_surface = None

        self.running = True

    def stop(self):
        self.running = False

    def draw(self):
        for surface in [self.menu_surface, self.reactor_surface, self.board_surface]:
            if surface is not None:
                self.screen.blit(surface.surface, (surface.x, surface.y))

        if not None in [self.board_surface, self.reactor_surface]:
            self.board_surface.power = self.reactor_surface.generated_power
            self.board_surface.time_left = self.reactor_surface.time_left
            self.board_surface.power_capacity = self.reactor_surface.power_capacity

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for surface in [self.menu_surface, self.reactor_surface, self.board_surface]:
                if surface is not None:
                    action = surface.event_handler(event)

                    if action == "New Game":
                        self.menu_surface = None
                        self.reactor_surface = Reactor(self.screen, 0, 100, self.dt)
                        self.board_surface = Board(self.screen, 0, 0, self.dt)

                    elif action == "Options":
                        print("Options")
                    elif action == "Exit":
                        self.running = False

    def run(self):
        while self.running:
            self.event_handler()

            for surface in [self.menu_surface, self.reactor_surface, self.board_surface]:
                if surface is not None:
                    surface.hover_handler()
                    surface.draw()

            self.screen.fill((0, 0, 0))
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
