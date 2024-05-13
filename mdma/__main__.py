from functools import cached_property

import pygame

from mdma.background import Background
from mdma.card import Card
from mdma.claim import Claim
from mdma.config import config
from mdma.pool import Pool
from mdma.pool_name import PoolName
from mdma.score import Score
from mdma.screen import Screen
from mdma.start import Start
from mdma.timer import Timer


class Mdma():

    @cached_property
    def fps(self):
        return config.fps

    @cached_property
    def screen(self):
        return Screen()

    @cached_property
    def clock(self):
        return pygame.time.Clock()

    @cached_property
    def caption(self):
        return 'MDMA The Game'

    @cached_property
    def background(self):
        return Background(self.screen)

    @cached_property
    def start(self):
        return Start(self.screen, self.background)

    @cached_property
    def card(self):
        return Card(self.screen, self.background)

    @cached_property
    def pool_name(self):
        return PoolName(self.screen, self.background, self.card)

    @cached_property
    def pool(self):
        return Pool(self.screen, self.card, self.fps)

    @cached_property
    def score(self):
        return Score(self.screen, self.background, self.card, self.pool)

    @cached_property
    def timer(self):
        return Timer(self.screen, self.background, self.card)

    @cached_property
    def claim(self):
        return Claim(self.screen, self.card)

    @cached_property
    def nb_frames_pressed_trigger(self):
        return 5

    def run(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen.set_icon()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.start.is_started:
                self.timer.start()

            if self.timer.started:
                if not self.timer.ended:
                    self.pool.move()

                    self.pool.update()
                    self.score.update()
                    self.timer.update()

                self.background.display()
                self.pool_name.display()
                self.card.display()
                self.score.display()
                if not self.timer.ended:
                    self.pool.display()
                    self.timer.display()
                else:
                    self.claim.display()
                    if self.claim.claimed:
                        self.pool.reset()
                        self.score.reset()
                        self.timer.reset()
            else:
                self.background.display()
                self.start.display()

            pygame.display.update()
            self.clock.tick(self.fps)


def main():
    mdma = Mdma()
    mdma.run()


if __name__ == '__main__':
    main()
