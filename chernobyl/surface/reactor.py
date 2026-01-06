from random import random

import numpy as np
import pygame

from .. import V2D, Sound
from ..particle import Atom, Neutron, Rod
from ..particle.particle import Particle
from ..surface.surface import Surface


class Reactor(Surface):
    def __init__(self, screen: pygame.Surface, x: int, y: int, dt: float) -> None:
        super().__init__(screen, x, y, dt)
        self.background_color = 28, 28, 28
        self.foreground_color = 255, 255, 255
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height() - 100))
        self.surface.fill(self.background_color)

        self.background_sound = Sound("statics/sounds/silent-room.mp3")
        self.background_sound.play(loop=True)

        self.background_sound_elect = Sound("statics/sounds/electricity.mp3", 0.2)
        self.background_sound_elect.play(loop=True)

        self.current_score = 0

        self.available_clicks = 3
        self.power_capacity = 4
        self.total_power = 0

        self.time_left = 20

        self.neutron_velocity_mag = 250

        self.atom_capacity = 200
        self.atom_velocity_mag = 100
        self.atom_spawn_probability = 0.5
        self.atom_decay_probability = 0.05
        self.atom_attraction_strength = 0.0
        self.atom_absorption_ratio = 0.25
        self.atom_maximum_health = 4

        self.generated_power = []
        self.atoms = []
        self.neutrons = []
        self.rods = [
            Rod(self.surface, int(x), self.dt)
            for x in np.linspace(100, self.surface.get_width() - 100, 10)
        ]

    def __del__(self):
        try:
            self.background_sound.stop()
            self.background_sound_elect.stop()
        except:
            pass

    def add_atom(self, atom: Atom) -> None:
        self.atoms.append(atom)

    def add_neutron(self, neutron: Neutron) -> None:
        self.neutrons.append(neutron)

    def add(self, particle: Particle) -> None:
        if isinstance(particle, Neutron):
            self.neutrons.append(particle)
        elif isinstance(particle, Atom):
            self.atoms.append(particle)

    def calculate_atom_health(self, r: float = 1.5):
        weights = [r ** (h - 1) for h in range(1, self.atom_maximum_health + 1)]
        total = sum(weights)

        roll = random()
        cumulative = 0.0

        for h, w in enumerate(weights, start=1):
            cumulative += w / total
            if roll <= cumulative:
                return h

        return self.atom_maximum_health

    def spawn_atom(self) -> None:
        if random() > self.atom_spawn_probability:
            return

        if len(self.atoms) >= self.atom_capacity:
            return

        x = 10 + random() * (self.surface.get_width() - 10)
        y = 10 + random() * (self.surface.get_height() - 10)

        atom = Atom(self.surface, V2D(x, y), self.atom_maximum_health)

        atom.decay_probability = self.atom_decay_probability
        atom.attraction_strength = self.atom_attraction_strength
        atom.absorption_ratio = self.atom_absorption_ratio
        atom.velocity = V2D.random(magnitude=self.atom_velocity_mag)
        self.add(atom)

    def draw(self):
        power = 0
        self.surface.fill(self.background_color)
        for rod in self.rods:
            self.line(rod.start(), rod.end(), width=10)
            for neutron_index in range(len(self.neutrons) - 1, -1, -1):
                neutron = self.neutrons[neutron_index]
                if rod.collided(neutron):
                    if random() > rod.absorption_ratio:
                        del self.neutrons[neutron_index]

        for atom_index in range(len(self.atoms) - 1, -1, -1):
            atom = self.atoms[atom_index]

            if atom.escaped():
                del self.atoms[atom_index]
                continue

            atom.move(self.dt)
            if atom.decay(self.dt):
                power += atom.health_point / 2
                for _ in range(atom.initial_health_point):
                    neutron = Neutron(self.surface, atom.position)
                    neutron.velocity = V2D.random(magnitude=self.neutron_velocity_mag)
                    self.add(neutron)
                del self.atoms[atom_index]
            self.circle(atom.position, atom.radius, atom.color)

        for neutron_index in range(len(self.neutrons) - 1, -1, -1):
            neutron = self.neutrons[neutron_index]

            if neutron.escaped() or neutron.end_of_life():
                del self.neutrons[neutron_index]
                continue

            neutron.move(self.dt)
            for atom_index in range(len(self.atoms) - 1, -1, -1):
                atom = self.atoms[atom_index]
                if atom.collided(neutron) and random() < atom.absorption_ratio:

                    atom.health_point -= int(neutron.health_point + np.log(neutron.velocity.mag()) // 1)
                    if atom.is_dead():
                        for _ in range(atom.initial_health_point):
                            neutron = Neutron(self.surface, atom.position)
                            neutron.velocity = V2D.random(magnitude=self.neutron_velocity_mag)
                            self.add(neutron)

                        power += atom.initial_health_point
                        del self.atoms[atom_index]
                    else:
                        atom.bounce(neutron)
                    del self.neutrons[neutron_index]

            self.circle(neutron.position, neutron.radius, neutron.color)

        if power > self.power_capacity:
            print("Boom")

        self.total_power += power
        if power > 0:

            self.generated_power.append(int(power))

        self.spawn_atom()

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = V2D(*event.pos)

            for atom_index in range(len(self.atoms) - 1, -1, -1):
                atom = self.atoms[atom_index]
                x, y = mouse
                if atom.position.dist(V2D(x, y - 100)) < atom.radius:
                    for _ in range(atom.initial_health_point):
                        neutron = Neutron(self.surface, atom.position)
                        neutron.velocity = V2D.random(magnitude=self.neutron_velocity_mag)
                        self.add(neutron)
                    del self.atoms[atom_index]
                    break
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                for rod in self.rods:
                    rod.lift()

            elif event.y < 0:
                for rod in self.rods:
                    rod.lower()


