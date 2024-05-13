from functools import cached_property

import pygame

from mdma.card import Card
from mdma.config import config


class BinSurfaces():

    def __init__(self, card: Card, nb_bins: int):
        self.card = card
        self.nb_bins = nb_bins

    @cached_property
    def margin(self):
        return (self.card.position[0] + self.card.size[1] *
                config.bin.margin_ratio)

    @cached_property
    def ratio_space(self):
        return config.bin.ratio.space

    @cached_property
    def ratio_height(self):
        return config.bin.ratio.height

    @cached_property
    def size(self):
        width = (self.card.size[0] - 2 * self.margin)/(
         self.nb_bins + (self.nb_bins - 1) * self.ratio_space)
        height = self.card.size[1] * self.ratio_height
        return (width, height)

    @cached_property
    def space_width(self):
        return self.size[0] * self.ratio_space

    @cached_property
    def reward_size(self):
        return self.size

    @cached_property
    def reward_color(self):
        return config.bin.color.reward

    @cached_property
    def reward_surface(self):
        surface = pygame.Surface(self.reward_size)
        surface.fill(self.reward_color)
        return surface

    @cached_property
    def ratio_user_height(self):
        return config.bin.ratio.user_height

    @cached_property
    def left_size(self):
        return (self.size[0], self.size[1] * self.ratio_user_height)

    @cached_property
    def left_color(self):
        return config.bin.color.left

    @cached_property
    def left_surface(self):
        surface = pygame.Surface(self.left_size)
        surface.fill(self.left_color)
        return surface

    @cached_property
    def left_center_size(self):
        return (self.left_size[0], self.left_size[1] * 0.5)

    @cached_property
    def left_center_surface(self):
        surface = pygame.Surface(self.left_center_size)
        surface.fill(self.left_color)
        return surface

    @cached_property
    def right_center_size(self):
        return (self.right_size[0], self.right_size[1] * 0.5)

    @cached_property
    def right_center_surface(self):
        surface = pygame.Surface(self.right_center_size)
        surface.fill(self.right_color)
        return surface

    @cached_property
    def right_size(self):
        return (self.size[0], self.size[1] * self.ratio_user_height)

    @cached_property
    def right_color(self):
        return config.bin.color.right

    @cached_property
    def right_surface(self):
        surface = pygame.Surface(self.right_size)
        surface.fill(self.right_color)
        return surface
