import os
from functools import cached_property

import pygame

from mdma.background import Background
from mdma.card import Card
from mdma.config import config
from mdma.screen import Screen


class PoolName():

    def __init__(self, screen: Screen, background: Background, card: Card):
        self.screen = screen
        self.background = background
        self.card = card

    @cached_property
    def fonts_path(self):
        return os.path.join(config.program_dir, 'fonts')

    @cached_property
    def graphics_path(self):
        return os.path.join(config.program_dir, 'graphics')

    @cached_property
    def font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.pool_name.font.name}.ttf')

    @cached_property
    def font_size(self):
        return config.pool_name.font.size

    @cached_property
    def font(self):
        return pygame.font.Font(self.font_path, self.font_size)

    @cached_property
    def font_color(self):
        return config.pool_name.font.color

    @cached_property
    def margin_ratio(self):
        return config.pool_name.margin_ratio

    @cached_property
    def margin(self):
        return self.background.size[1] * self.margin_ratio

    @cached_property
    def position_y(self):
        return self.background.size[1] * self.margin_ratio

    @cached_property
    def position(self):
        position_x = self.margin
        return (position_x, self.position_y)

    @cached_property
    def expand_ratio(self):
        return config.pool_name.expand_ratio

    @cached_property
    def size(self):
        width = (self.logo1_surface.get_rect().width +
                 self.token1_surface.get_rect().width +
                 self.logo2_surface.get_rect().width +
                 self.token2_surface.get_rect().width)
        size_x = width * self.expand_ratio
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def surface(self):
        return pygame.Surface(self.size)

    @cached_property
    def rectangle(self):
        return self.surface.get_rect(topleft=self.position)

    @cached_property
    def text_space(self):
        return config.pool_name.text_space

    @cached_property
    def logo_size(self):
        size = config.pool_name.logo_size
        return (size, size)

    @cached_property
    def logo1_path(self):
        return os.path.join(self.graphics_path,
                            f'{config.pool_name.logo1}.png')

    @cached_property
    def logo1_surface(self):
        surface = pygame.image.load(self.logo1_path).convert_alpha()
        surface = pygame.transform.smoothscale(surface, self.logo_size)
        return surface

    @property
    def logo1_rectangle(self):
        midleft = (self.rectangle.x, self.rectangle.center[1])
        return self.logo1_surface.get_rect(midleft=midleft)

    @cached_property
    def token1_text(self):
        return config.pool_name.token1

    @cached_property
    def token1_surface(self):
        return self.font.render(self.token1_text, True, self.font_color)

    @property
    def token1_rectangle(self):
        midleft = self.logo1_rectangle.midright
        rectangle = self.token1_surface.get_rect(midleft=midleft)
        rectangle.x += self.text_space
        return rectangle

    @cached_property
    def slash_surface(self):
        return self.font.render('/', True, self.font_color)

    @property
    def slash_rectangle(self):
        midleft = self.token1_rectangle.midright
        rectangle = self.slash_surface.get_rect(midleft=midleft)
        rectangle.x += self.text_space
        return rectangle

    @cached_property
    def logo2_path(self):
        return os.path.join(self.graphics_path,
                            f'{config.pool_name.logo2}.png')

    @cached_property
    def logo2_surface(self):
        surface = pygame.image.load(self.logo2_path).convert_alpha()
        surface = pygame.transform.smoothscale(surface, self.logo_size)
        return surface

    @property
    def logo2_rectangle(self):
        midleft = self.slash_rectangle.midright
        rectangle = self.logo2_surface.get_rect(midleft=midleft)
        rectangle.x += self.text_space
        return rectangle

    @cached_property
    def token2_text(self):
        return config.pool_name.token2

    @cached_property
    def token2_surface(self):
        return self.font.render(self.token2_text, True, self.font_color)

    @property
    def token2_rectangle(self):
        midleft = self.logo2_rectangle.midright
        rectangle = self.token1_surface.get_rect(midleft=midleft)
        rectangle.x += self.text_space
        return rectangle

    def display(self):
        self.screen.display(self.logo1_surface, self.logo1_rectangle)
        self.screen.display(self.token1_surface, self.token1_rectangle)
        self.screen.display(self.slash_surface, self.slash_rectangle)
        self.screen.display(self.logo2_surface, self.logo2_rectangle)
        self.screen.display(self.token2_surface, self.token2_rectangle)
