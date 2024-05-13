from functools import cached_property

from mdma.button import Button
from mdma.card import Card
from mdma.screen import Screen


class Claim():

    def __init__(self, screen: Screen, card: Card):
        self.screen = screen
        self.card = card

    @cached_property
    def button(self):
        return Button(self.screen, self.card.rectangle.center, 'Claim rewards')

    @property
    def claimed(self):
        return self.button.is_clicked

    def display(self):
        self.button.display()
