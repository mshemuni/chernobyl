from random import random

from .particle import Particle
from .. import V2D
from ..surface.surface import Surface


class Rod:
    def __init__(self, surface: Surface, x: int):
        self.surface = surface
        self.x = x
        self.insertion = 0.0
        self.insertion_rate = 0.1
        self.color = 255, 255, 255
        self.width = 4
        self.absorption_ratio = 0.0

    @property
    def current_lowness(self) -> float:
        return self.insertion * self.surface.surface.get_height()

    def start(self):
        return V2D(self.x, 0)

    def end(self):
        return V2D(self.x, self.current_lowness)

    def lower(self):
        if self.insertion >= 1.0:
            self.insertion = 1.0
            return
        self.insertion += self.insertion_rate

    def lift(self):
        if self.insertion <= 0:
            self.insertion = 0
            return
        self.insertion -= self.insertion_rate

    def collided(self, particle: Particle) -> bool:
        start_y = self.start().y
        end_y = self.end().y
        px, py = particle.position.x, particle.position.y

        if abs(px - self.x) > particle.radius:
            return False

        if py < min(start_y, end_y) or py > max(start_y, end_y):
            return False

        return True

    def absorbed(self) -> bool:
        return self.absorption_ratio > random()

    # def show(self):
    #     start_position = self.start()
    #     end_position = self.end()
    #     pygame.draw.line(
    #         self.surface,
    #         self.color,
    #         start_position.as_tuple(),
    #         end_position.as_tuple(),
    #         self.width
    #     )
