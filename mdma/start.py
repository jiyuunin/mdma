import os
from functools import cached_property

import pygame

from mdma.background import Background
from mdma.button import Button
from mdma.config import config
from mdma.screen import Screen


class Start():

    def __init__(self, screen: Screen, background: Background):
        self.screen = screen
        self.background = background

    @cached_property
    def graphics_path(self):
        return os.path.join(config.program_dir, 'graphics')

    @cached_property
    def logo_path(self):
        return os.path.join(self.graphics_path, f'{config.start.logo}.png')

    @cached_property
    def logo_surface(self):
        surface = pygame.image.load(self.logo_path).convert_alpha()
        rectangle = surface.get_rect()
        ratio = rectangle.height / rectangle.width
        size_x = self.background.size[0] * 0.8
        size_y = size_x * ratio
        return pygame.transform.smoothscale(surface, (size_x, size_y))

    @cached_property
    def center(self):
        return self.background.surface.get_rect().center

    @cached_property
    def logo_rectangle(self):
        return self.logo_surface.get_rect(center=self.center)

    @cached_property
    def button(self):
        center_x = self.center[0]
        center_y = self.logo_rectangle.y + self.logo_rectangle.height
        return Button(self.screen, (center_x, center_y), 'START')

    @property
    def is_started(self):
        return self.button.is_clicked

    def display(self):
        self.screen.display(self.logo_surface, self.logo_rectangle)
        self.button.display()
