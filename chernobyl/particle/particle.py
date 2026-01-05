from typing import Optional, Self, Tuple
from datetime import timedelta, datetime

from ..surface.surface import Surface
from ..utils import Fixer
from ..v2d import V2D


class Particle:
    def __init__(self,
                 surface: Surface,
                 position: V2D,
                 velocity: Optional[V2D] = None,
                 acceleration: Optional[V2D] = None) -> None:
        self.surface = surface
        self.position: V2D = position
        self.velocity: V2D = Fixer.vector(velocity) / 20
        self.acceleration: V2D = Fixer.vector(acceleration, randomize=False)
        self.radius = 1
        self.time_to_live = 1.0
        self.life = 0
        self.created_at = datetime.now()

    @classmethod
    def random(cls, surface: Surface) -> Self:
        return Particle(surface, V2D.random(), velocity=V2D.random())

    @property
    def color(self) -> Tuple[int, int, int]:
        return 0, 0, 0

    def collided(self, other: Self) -> bool:
        return self.position.dist(other.position) < self.radius + other.radius

    def end_of_life(self) -> bool:
        return self.life >= self.time_to_live

    def escaped(self) -> bool:
        return not (
                    -self.radius <= self.position.x < self.surface.get_width() + self.radius and
                    -self.radius <= self.position.y < self.surface.get_height() + self.radius)

    def bounce(self, other: Self) -> None:
        if not self.collided(other):
            return

        delta = self.position - other.position
        distance = delta.mag()

        if distance < 0.1:
            return

        normal = delta / distance

        rel_vel = self.velocity - other.velocity
        vel_along_normal = rel_vel.dot(normal)

        if vel_along_normal > 0:
            return

        m1 = self.radius
        m2 = other.radius

        impulse = (2 * vel_along_normal) / (m1 + m2)

        self.velocity -= impulse * m2 * normal
        other.velocity += impulse * m1 * normal

    def move(self, delta: float = 1.0) -> None:
        self.life += delta
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
