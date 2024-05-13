import os
from functools import cached_property

import pygame

from mdma.config import config


class Screen():

    def __init__(self):
        self.screen = pygame.display.set_mode(self.size)

    @cached_property
    def graphics_path(self):
        return os.path.join(config.program_dir, 'graphics')

    @cached_property
    def icon_path(self):
        return os.path.join(self.graphics_path, f'{config.icon_name}.png')

    @cached_property
    def icon_surface(self):
        return pygame.image.load(self.icon_path).convert_alpha()

    @cached_property
    def size(self):
        return (config.screen.width, config.screen.height)

    @cached_property
    def screen(self):
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_icon(self.icon_surface)
        return screen

    def set_icon(self):
        pygame.display.set_icon(self.icon_surface)

    def display(self, surface, position):
        self.screen.blit(surface, position)
