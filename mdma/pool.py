import os
import random
from functools import cached_property

import pygame

from mdma.bin import Bin
from mdma.bin_surfaces import BinSurfaces
from mdma.card import Card
from mdma.config import config
from mdma.screen import Screen


class Pool():

    def __init__(self, screen: Screen, card: Card, fps: int):
        self.screen = screen
        self.card = card
        self.fps = fps
        self.reset()

    def reset(self):
        self.active_bin_id = self.nb_bins//2 + 1
        self.next_active_bin_id = self.active_bin_id
        self.user_bin_id = self.active_bin_id
        self.nb_frames_left_pressed = 0
        self.nb_frames_right_pressed = 0

    @cached_property
    def fonts_path(self):
        return os.path.join(config.program_dir, 'fonts')

    @cached_property
    def font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.pool.font.name}.ttf')

    @cached_property
    def font_size(self):
        return config.pool.font.size

    @cached_property
    def font(self):
        return pygame.font.Font(self.font_path, self.font_size)

    @cached_property
    def font_color(self):
        return config.pool.font.color

    @cached_property
    def text_surface(self):
        return self.font.render('Out of position', True, self.font_color)

    @cached_property
    def margin_left(self):
        return config.pool.margin_left

    @cached_property
    def margin_top(self):
        return config.pool.margin_top

    @cached_property
    def text_rectangle(self):
        topleft_x = self.card.position[0] + self.margin_left
        topleft_y = self.card.position[1] + self.margin_top
        topleft = (topleft_x, topleft_y)
        return self.text_surface.get_rect(topleft = topleft)

    @cached_property
    def dot_color(self):
        return config.pool.dot.color

    @cached_property
    def dot_center(self):
        center_x = self.text_rectangle.midright[0] + 12
        center_y = self.text_rectangle.midright[1] + 2
        return (center_x, center_y)

    @cached_property
    def dot_radius(self):
        return config.pool.dot.radius

    @cached_property
    def nb_bins(self):
        return config.nb_bins

    @cached_property
    def reward_bin_radius(self):
        return config.reward_bin_radius

    @cached_property
    def bin_surfaces(self):
        return BinSurfaces(self.card, self.nb_bins)

    @cached_property
    def bins(self):
        bins = []
        position_x = self.card.position[0] + self.bin_surfaces.margin
        position_y = (self.card.position[1] +
                      self.card.size[1] -
                      self.bin_surfaces.size[1] -
                      self.bin_surfaces.margin)
        for _ in range(self.nb_bins):
            position = (position_x, position_y)
            bin_instance = Bin(self.screen, self.bin_surfaces, position)
            bins.append(bin_instance)
            position_x += (self.bin_surfaces.size[0] +
                           self.bin_surfaces.space_width)
        return bins

    @cached_property
    def random_active_bin_range(self):
        return range(self.reward_bin_radius,
                     self.nb_bins - self.reward_bin_radius)

    @property
    def should_randomize_next_active_bin_id(self):
        return self.active_bin_id == self.next_active_bin_id

    @cached_property
    def occurrence_per_second(self):
        return 30

    def randomize_next_active_bin_id(self):
        if (
            self.should_randomize_next_active_bin_id and
            (random.randint(self.occurrence_per_second, self.fps) <=
             self.occurrence_per_second)
        ):
            self.next_active_bin_id = random.choice(
              self.random_active_bin_range)

    @cached_property
    def min_bin_range(self):
        return min(self.random_active_bin_range)

    @cached_property
    def max_bin_range(self):
        return max(self.random_active_bin_range)

    @cached_property
    def nb_frames_pressed_trigger(self):
        return config.nb_frames_pressed_trigger

    def move_left(self):
        if self.user_bin_id > self.min_bin_range:
            self.user_bin_id -= 1

    def move_right(self):
        if self.user_bin_id < self.max_bin_range:
            self.user_bin_id += 1

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if (
                self.nb_frames_left_pressed == 0 or
                self.nb_frames_left_pressed >= self.nb_frames_pressed_trigger
            ):
                self.move_left()
            self.nb_frames_left_pressed += 1
        else:
            self.nb_frames_left_pressed = 0
        if keys[pygame.K_RIGHT]:
            if (
                self.nb_frames_right_pressed == 0 or
                self.nb_frames_right_pressed >= self.nb_frames_pressed_trigger
            ):
                self.move_right()
            self.nb_frames_right_pressed += 1
        else:
            self.nb_frames_right_pressed = 0

    @property
    def reward_bin_range(self):
        return range(self.active_bin_id - self.reward_bin_radius,
                     self.active_bin_id + self.reward_bin_radius + 1)

    @property
    def user_bin_range(self):
        return range(self.user_bin_id - self.reward_bin_radius,
                     self.user_bin_id + self.reward_bin_radius + 1)

    def update(self):
        if self.active_bin_id < self.next_active_bin_id:
            self.active_bin_id += 1
        elif self.active_bin_id > self.next_active_bin_id:
            self.active_bin_id -= 1
        for bin_id, bin_instance in enumerate(self.bins):
            bin_instance.rewarding = bin_id in self.reward_bin_range
            if bin_id in self.user_bin_range:
                if bin_id < self.active_bin_id:
                    bin_instance.positioning = -1
                elif bin_id == self.active_bin_id:
                    bin_instance.positioning = 0
                else:
                    bin_instance.positioning = 1
            else:
                bin_instance.positioning = None
        self.randomize_next_active_bin_id()

    @property
    def is_out_of_position(self):
        for bin_id in self.user_bin_range:
            if bin_id in self.reward_bin_range:
                return False
        return True

    def display(self):
        if self.is_out_of_position:
            self.screen.display(self.text_surface, self.text_rectangle)
            pygame.draw.circle(self.screen.screen,
                               self.dot_color,
                               self.dot_center,
                               self.dot_radius)
        for bin_instance in self.bins:
            bin_instance.display()
