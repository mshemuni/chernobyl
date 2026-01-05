from typing import Optional, Tuple, Self

from .particle import Particle
from .. import V2D
from ..surface.surface import Surface


class Neutron(Particle):
    def __init__(self,
                 surface: Surface,
                 position: V2D,
                 velocity: Optional[V2D] = None,
                 acceleration: Optional[V2D] = None) -> None:
        super().__init__(surface, position, velocity=velocity, acceleration=acceleration)
        self.health_point: int = 1
        self.radius = 5
        self.attraction_strength = 0.0

    @property
    def color(self) -> Tuple[int, int, int]:
        return 0, 255, 0

    def decrease_health(self) -> None:
        self.health_point -= 1

    def is_dead(self) -> bool:
        return self.health_point == 0

    def attract_to(self, other: Self) -> None:
        if self.attraction_strength == 0:
            return

        delta = other.position - self.position
        distance = delta.mag()

        if distance < 0.1:
            return

        direction = delta / distance

        force_magnitude = self.attraction_strength / (distance ** 2)

        self.acceleration += direction * force_magnitude
