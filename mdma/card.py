from functools import cached_property

import pygame

from mdma.background import Background
from mdma.config import config
from mdma.screen import Screen


class Card():

    def __init__(self, screen: Screen, background: Background):
        self.screen = screen
        self.background = background

    @cached_property
    def margin_ratio_top(self):
        return config.card.margin_ratio.top

    @cached_property
    def margin_ratio_default(self):
        return config.card.margin_ratio.default

    @cached_property
    def margin_top(self):
        return self.background.size[1] * self.margin_ratio_top

    @cached_property
    def margin_default(self):
        return self.background.size[1] * self.margin_ratio_default

    @cached_property
    def position(self):
        return (self.margin_default, self.margin_top)

    @cached_property
    def size(self):
        return (self.background.size[0] - 2 * self.margin_default,
                self.background.size[1] - self.margin_top -
                self.margin_default)

    @cached_property
    def color(self):
        return config.card.color

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
        return config.card.border_radius

    def display(self):
        pygame.draw.rect(self.screen.screen,
                         self.color,
                         self.rectangle,
                         border_radius=self.border_radius)
