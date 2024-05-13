import os
from functools import cached_property

import pygame

from mdma.config import config
from mdma.screen import Screen


class Button():

    def __init__(self, screen: Screen, center: tuple, text: str):
        self.screen = screen
        self.center = center
        self.text = text
        self.is_pressed = False

    @cached_property
    def fonts_path(self):
        return os.path.join(config.program_dir, 'fonts')

    @cached_property
    def expand_ratio(self):
        return config.button.expand_ratio

    @cached_property
    def size(self):
        rectangle = self.text_surface.get_rect()
        size_x = rectangle.width * self.expand_ratio
        size_y = rectangle.height * self.expand_ratio
        return (size_x, size_y)

    @cached_property
    def border_radius(self):
        return config.button.border_radius

    @cached_property
    def color(self):
        return config.button.color

    @cached_property
    def surface(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
        return surface

    @cached_property
    def rectangle(self):
        return self.surface.get_rect(center=self.center)

    @cached_property
    def color_focus(self):
        return config.button.color_focus

    @cached_property
    def surface_focus(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
        return surface

    @cached_property
    def rectangle_focus(self):
        return self.surface_focus.get_rect(center=self.center)

    @cached_property
    def font_path(self):
        return os.path.join(self.fonts_path,
                            f'{config.button.font.name}.ttf')

    @cached_property
    def font_size(self):
        return config.button.font.size

    @cached_property
    def font(self):
        return pygame.font.Font(self.font_path, self.font_size)

    @cached_property
    def font_color(self):
        return config.button.font.color

    @property
    def text_surface(self):
        return self.font.render(self.text, True, self.font_color)

    @property
    def text_rectangle(self):
        center = self.rectangle.center
        center_x = center[0]
        center_y = center[1] - 2
        return self.text_surface.get_rect(center = (center_x, center_y))

    @property
    def is_focused(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        mouse_pos = pygame.mouse.get_pos()
        return self.rectangle.collidepoint(mouse_pos)

    @property
    def is_clicked(self):
        keys = pygame.key.get_pressed()
        if self.is_pressed:
            if not keys[pygame.K_RETURN]:
                self.is_pressed = False
                return True
        self.is_pressed = keys[pygame.K_RETURN]
        return self.is_focused and pygame.mouse.get_pressed()[0]

    def display(self):
        if self.is_focused:
            pygame.draw.rect(self.screen.screen,
                             self.color_focus,
                             self.rectangle_focus,
                             border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.screen.screen,
                             self.color,
                             self.rectangle,
                             border_radius=self.border_radius)
        self.screen.display(self.text_surface, self.text_rectangle)
