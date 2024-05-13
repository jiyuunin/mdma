import os
from functools import cached_property

import pygame

from mdma.background import Background
from mdma.card import Card
from mdma.config import config
from mdma.pool import Pool
from mdma.screen import Screen


class Score():

    def __init__(self,
                 screen: Screen,
                 background: Background,
                 card: Card,
                 pool: Pool):
        self.screen = screen
        self.background = background
        self.card = card
        self.pool = pool
        self.reset()

    def reset(self):
        self.number = 0

    @cached_property
    def fonts_path(self):
        return os.path.join(config.program_dir, 'fonts')

    @cached_property
    def graphics_path(self):
        return os.path.join(config.program_dir, 'graphics')

    @cached_property
    def margin_ratio(self):
        return config.score.margin_ratio

    @cached_property
    def position_y(self):
        return self.background.size[1] * self.margin_ratio

    @cached_property
    def position(self):
        position_x = (self.background.size[0] - self.size[0])/2
        return (position_x, self.position_y)

    @cached_property
    def logo_size_x(self):
        return self.logo_surface.get_rect().width

    @cached_property
    def token_size_x(self):
        return self.token_surface.get_rect().width

    @cached_property
    def expand_ratio(self):
        return config.score.expand_ratio

    @cached_property
    def size(self):
        number_surface = self.number_font.render('1000000', True, self.color)
        size_x = (self.logo_size_x + number_surface.get_rect().width +
                  self.token_size_x) * self.expand_ratio
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def color(self):
        return config.score.color

    @cached_property
    def surface(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
        return surface

    @cached_property
    def rectangle(self):
        return self.surface.get_rect(topleft=self.position)

    @cached_property
    def border_radius(self):
        return config.score.border_radius

    @cached_property
    def logo_path(self):
        return os.path.join(self.graphics_path, f'{config.score.logo}.png')

    @cached_property
    def logo_surface(self):
        return pygame.image.load(self.logo_path).convert_alpha()

    @property
    def logo_rectangle(self):
        rectangle = self.logo_surface.get_rect(
          midleft = self.rectangle.midleft)
        rectangle.x += self.rectangle.width * self.margin_ratio
        return rectangle

    @cached_property
    def number_font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.score.font.number.name}.ttf')

    @cached_property
    def number_font_size(self):
        return config.score.font.number.size

    @cached_property
    def number_font(self):
        return pygame.font.Font(self.number_font_path, self.number_font_size)

    @cached_property
    def number_color(self):
        return config.score.font.number.color

    @property
    def number_surface(self):
        return self.number_font.render(f'{self.number}',
                                       True,
                                       self.number_color)

    @property
    def number_rectangle(self):
        center = self.rectangle.center
        rectangle = self.number_surface.get_rect(center = center)
        rectangle.x = rectangle.x + self.logo_size_x/2 - self.token_size_x/2
        rectangle.y -= 2
        return rectangle

    @cached_property
    def token_font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.score.font.token.name}.ttf')

    @cached_property
    def token_font_size(self):
        return config.score.font.token.size

    @cached_property
    def token_font(self):
        return pygame.font.Font(self.token_font_path, self.token_font_size)

    @cached_property
    def token_color(self):
        return config.score.font.number.color

    @cached_property
    def token_surface(self):
        return self.token_font.render('MOE', True, self.token_color)

    @cached_property
    def text_space(self):
        return config.score.text_space

    @property
    def token_rectangle(self):
        rectangle = self.token_surface.get_rect(
          midleft = self.number_rectangle.midright)
        rectangle.x += self.text_space
        return rectangle

    def update(self):
        reward_bin_range = self.pool.reward_bin_range
        for bin_id in self.pool.user_bin_range:
            if bin_id in reward_bin_range:
                self.number += 1

    def display(self):
        pygame.draw.rect(self.screen.screen,
                         self.color,
                         self.rectangle,
                         border_radius=self.border_radius)
        self.screen.display(self.logo_surface, self.logo_rectangle)
        self.screen.display(self.number_surface, self.number_rectangle)
        self.screen.display(self.token_surface, self.token_rectangle)
