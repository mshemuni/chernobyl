from pathlib import Path
from typing import Union
import pygame


class Sound:
    def __init__(self, path: Union[str, Path], volume: float = 1.0):
        self.sound = pygame.mixer.Sound(str(path))
        self.sound.set_volume(volume)
        self.channel = None

    def play(self, loop: bool = False):
        loops = -1 if loop else 0
        self.channel = self.sound.play(loops=loops)

    def stop(self):
        if self.channel:
            self.channel.stop()

    def set_volume(self, volume: float):
        self.sound.set_volume(volume)
