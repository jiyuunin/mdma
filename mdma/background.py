from functools import cached_property

import pygame

from mdma.config import config
from mdma.screen import Screen


class Background():

    def __init__(self, screen: Screen):
        self.screen = screen

    @cached_property
    def position(self):
        return (0, 0)

    @cached_property
    def size(self):
        return self.screen.size

    @cached_property
    def color(self):
        return config.background.color

    @cached_property
    def surface(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
        return surface

    def display(self):
        self.screen.display(self.surface, self.position)
