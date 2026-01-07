from random import random
from typing import Optional, Tuple

import numpy as np

from .particle import Particle
from .. import V2D
from ..surface.surface import Surface
from ..utils import Fixer


class Atom(Particle):
    def __init__(self,
                 surface: Surface,
                 position: V2D,
                 health_point: int,
                 velocity: Optional[V2D] = None,
                 acceleration: Optional[V2D] = None) -> None:
        super().__init__(surface, position, velocity=velocity, acceleration=acceleration)
        self._health_point: int = health_point
        self.initial_health_point = health_point
        self.radius = 20
        self.decay_probability = 0.1
        self.attraction_strength = 0.0
        self.colors = Fixer.colors(n=self.health_point)
        self.absorption_ratio = 0.5

    @property
    def health_point(self) -> int:
        return self._health_point

    @health_point.setter
    def health_point(self, value):
        if value < 0:
            value = 0
        self._health_point = value

    @property
    def color(self) -> Tuple[int, int, int]:
        return self.colors[self.health_point - 1]

    def decay(self, dt: float) -> bool:
        p = 1.0 - (1.0 - self.decay_probability) ** dt
        return random() < p

    def decrease_health(self) -> None:
        self.health_point -= 1

    def is_dead(self) -> bool:
        return self.health_point == 0

    def absorbed(self, dt: float) -> bool:
        p = 1.0 - (1.0 - self.absorption_ratio) ** dt
        return random() < p
