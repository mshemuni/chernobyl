import pygame


from chernobyl.surface import Menu
from chernobyl.surface.reactor import Reactor
from .utils import FPS


class Window:
    def __init__(self, width: int, height: int, title: str = "Chernobyl", full_screen: bool = True):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title
        self.full_screen = full_screen
        self.flags = pygame.FULLSCREEN if full_screen else pygame.RESIZABLE
        self.fps = FPS

        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        self.hovered_item = None

        self.surfaces = [Menu(self.screen, 0, 0)]
        self.running = True

    def stop(self):
        self.running = False

    def draw(self):
        for surface in self.surfaces:
            self.screen.blit(surface.surface, (surface.x, surface.y))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for surface in self.surfaces:
                action = surface.event_handler(event)

                if action == "New Game":
                    self.surfaces = [Reactor(self.screen, 0, 0)]
                elif action == "Options":
                    print("Options")
                elif action == "Exit":
                    self.running = False

    def run(self):
        while self.running:
            self.event_handler()

            for surface in self.surfaces:
                surface.hover_handler()
                surface.draw()

            self.screen.fill((0, 0, 0))
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
