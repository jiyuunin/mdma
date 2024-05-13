from functools import cached_property

from mdma.bin_surfaces import BinSurfaces
from mdma.screen import Screen


class Bin():

    def __init__(self,
                 screen: Screen,
                 bin_surfaces: BinSurfaces,
                 position: tuple):
        self.screen = screen
        self.surfaces = bin_surfaces
        self.position = position
        self.rewarding = False
        self.positioning = None

    @cached_property
    def reward_position(self):
        return self.position

    @cached_property
    def left_position(self):
        position_y = (self.position[1] + self.surfaces.reward_size[1] -
                      self.surfaces.left_size[1])
        return self.position[0], position_y

    @cached_property
    def left_center_position(self):
        position_y = (self.position[1] + self.surfaces.reward_size[1] -
                      self.surfaces.left_center_size[1])
        return self.position[0], position_y

    @cached_property
    def right_center_position(self):
        return self.right_position

    @cached_property
    def right_position(self):
        position_y = (self.position[1] + self.surfaces.reward_size[1] -
                      self.surfaces.right_size[1])
        return self.position[0], position_y

    def display(self):
        if self.rewarding:
            self.screen.display(self.surfaces.reward_surface,
                                self.reward_position)
        if self.positioning == -1:
            self.screen.display(self.surfaces.left_surface, self.left_position)
        elif self.positioning == 0:
            self.screen.display(self.surfaces.left_center_surface,
                                self.left_center_position)
            self.screen.display(self.surfaces.right_center_surface,
                                self.right_center_position)
        elif self.positioning == 1:
            self.screen.display(self.surfaces.right_surface,
                                self.right_position)
