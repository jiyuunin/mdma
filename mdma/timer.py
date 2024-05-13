import os
from functools import cached_property

import pygame

from mdma.background import Background
from mdma.card import Card
from mdma.config import config
from mdma.screen import Screen
from mdma.time_data import TimeData


class Timer():

    def __init__(self, screen: Screen, background: Background, card: Card):
        self.screen = screen
        self.background = background
        self.card = card
        self.reset()

    def reset(self):
        self.time_data = TimeData(0)
        self.started = False
        self.ended = False

    @cached_property
    def fonts_path(self):
        return os.path.join(config.program_dir, 'fonts')

    @cached_property
    def margin_ratio(self):
        return config.timer.margin_ratio

    @cached_property
    def margin(self):
        return self.background.size[1] * self.margin_ratio

    @cached_property
    def position_y(self):
        return self.background.size[1] * self.margin_ratio

    @cached_property
    def position(self):
        position_x = self.background.size[0] - self.margin
        return (position_x, self.position_y)

    @cached_property
    def color(self):
        return config.timer.color

    @cached_property
    def expand_ratio(self):
        return config.timer.expand_ratio

    @cached_property
    def minutes_size(self):
        surface = self.font.render('00', True, self.color)
        size_x = surface.get_rect().width * self.expand_ratio
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def minutes_surface(self):
        return pygame.Surface(self.minutes_size)

    @cached_property
    def minutes_rectangle(self):
        return self.minutes_surface.get_rect(topright=self.position)

    @cached_property
    def colon_size(self):
        surface = self.font.render(':', True, self.color)
        size_x = surface.get_rect().width
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def colon_surface(self):
        return pygame.Surface(self.colon_size)

    @cached_property
    def colon_rectangle(self):
        topright = self.minutes_rectangle.topleft
        return self.colon_surface.get_rect(topright=topright)

    @cached_property
    def hours_size(self):
        surface = self.font.render('00', True, self.color)
        size_x = surface.get_rect().width * self.expand_ratio
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def hours_surface(self):
        return pygame.Surface(self.hours_size)

    @cached_property
    def hours_rectangle(self):
        topright = self.colon_rectangle.topleft
        return self.hours_surface.get_rect(topright=topright)

    @cached_property
    def day_of_week_size(self):
        surface = self.font.render('Wednesday', True, self.color)
        size_x = surface.get_rect().width * self.expand_ratio
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def day_of_week_surface(self):
        return pygame.Surface(self.day_of_week_size)

    @cached_property
    def day_of_week_rectangle(self):
        topright = self.hours_rectangle.topleft
        return self.day_of_week_surface.get_rect(topright=topright)

    @cached_property
    def week_size(self):
        surface = self.font.render('Week 4', True, self.color)
        size_x = surface.get_rect().width * 1.1
        size_y = self.card.margin_top - 2 * self.position_y
        return (size_x, size_y)

    @cached_property
    def week_surface(self):
        return pygame.Surface(self.week_size)

    @cached_property
    def week_rectangle(self):
        topright = self.day_of_week_rectangle.topleft
        return self.week_surface.get_rect(topright=topright)

    @cached_property
    def font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.timer.font.name}.ttf')

    @cached_property
    def font_size(self):
        return config.timer.font.size

    @cached_property
    def font(self):
        return pygame.font.Font(self.font_path, self.font_size)

    @cached_property
    def font_color(self):
        return config.timer.font.color

    @property
    def minutes_text_surface(self):
        return self.font.render(self.time_data.minutes_text,
                                True,
                                self.font_color)

    @property
    def minutes_text_rectangle(self):
        center = self.minutes_rectangle.center
        return self.minutes_text_surface.get_rect(center = center)

    @cached_property
    def colon_text_surface(self):
        return self.font.render(':', True, self.font_color)

    @cached_property
    def colon_text_rectangle(self):
        center = self.colon_rectangle.center
        return self.colon_text_surface.get_rect(center = center)

    @property
    def hours_text_surface(self):
        return self.font.render(self.time_data.hours_text,
                                True,
                                self.font_color)

    @property
    def hours_text_rectangle(self):
        center = self.hours_rectangle.center
        return self.hours_text_surface.get_rect(center = center)

    @property
    def day_of_week_text_surface(self):
        return self.font.render(self.time_data.day_of_week_text,
                                True,
                                self.font_color)

    @property
    def day_of_week_text_rectangle(self):
        center = self.day_of_week_rectangle.center
        return self.day_of_week_text_surface.get_rect(center = center)

    @property
    def week_text_surface(self):
        return self.font.render(self.time_data.week_text,
                                True,
                                self.font_color)

    @property
    def week_text_rectangle(self):
        center = self.week_rectangle.center
        return self.week_text_surface.get_rect(center = center)

    @cached_property
    def limit(self):
        return config.timer.limit

    @cached_property
    def rate(self):
        return config.timer.rate

    def start(self):
        self.started = True

    def update(self):
        self.time_data += self.rate
        if self.time_data.timestamp >= self.limit:
            self.time_data.timestamp = self.limit
            self.ended = True

    def display(self):
        self.screen.display(self.minutes_text_surface,
                            self.minutes_text_rectangle)
        self.screen.display(self.colon_text_surface,
                            self.colon_text_rectangle)
        self.screen.display(self.hours_text_surface,
                            self.hours_text_rectangle)
        self.screen.display(self.day_of_week_text_surface,
                            self.day_of_week_text_rectangle)
        self.screen.display(self.week_text_surface, self.week_text_rectangle)
