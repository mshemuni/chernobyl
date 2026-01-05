from random import random

import pygame

from .. import V2D
from ..particle import Atom
from ..surface.surface import Surface
from ..utils import FPS


class Reactor(Surface):
    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        super().__init__(screen, x, y)
        self.background_color = 28, 28, 28
        self.foreground_color = 255, 255, 255
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.surface.fill(self.background_color)

        self.current_score = 0

        self.available_clicks = 3
        self.power_capacity = 50
        self.atom_capacity = 50
        self.total_power = 0

        self.atom_spawn_probability = 0.2
        self.atom_decay_probability = 0.1
        self.atom_attraction_strength = 0.0
        self.atom_absorption_ratio = 0.5
        self.atom_maximum_health = 1

        self.generated_power = []
        self.atoms = []
        self.neutrons = []

    def atom_spawn_rate_dict(self, r: float = 1.5) -> dict[float, int]:
        weights = [r ** (h - 1) for h in range(1, self.atom_maximum_health + 1)]
        total = sum(weights)

        return {
            w / total: h
            for h, w in zip(range(1, self.atom_maximum_health + 1), weights)
        }

    def spawn_atom(self) -> None:
        if random() > self.atom_spawn_probability:
            return

        if len(self.atoms) >= self.atom_capacity:
            return

        x = 10 + random() * (self.surface.get_width() - 10)
        y = 10 + random() * (self.surface.get_height() - 10)

        atom = Atom(self.surface, V2D(x, y))
        roll = random()
        cumulative = 0.0

        for prob, hp in self.atom_spawn_rate_dict().items():
            cumulative += prob
            if roll <= cumulative:
                atom.health_point = hp

        atom.health_point = next(reversed(self.atom_spawn_rate_dict().values()))

        atom.decay_probability = self.atom_decay_probability
        atom.attraction_strength = self.atom_attraction_strength
        atom.absorption_ratio = self.atom_absorption_ratio

        self.atoms.append(atom)

    def draw(self):
        self.surface.fill(self.background_color)
        for atom_index in range(len(self.atoms) -1, -1, -1):
            atom = self.atoms[atom_index]

            if atom.escaped():
                del self.atoms[atom_index]
                continue

            atom.move(FPS)

            self.circle(atom.position, atom.radius, atom.color)

        self.spawn_atom()
