from random import randint, choice, randrange

import pyxel

from game.projectile import Meteor
from game.vector import Vec2
from run import SIZE, LITTLE_METEOR_COUNT, BIG_METEOR_COUNT


class Difficulty:
    multiplier: float
    # level: int

    def __init__(self, app, multiplier):
        self.app = app
        self.multiplier = multiplier

    def increase_difficulty(self):
        if self.app.score >= 1000 and self.app.score % 250 == 0:
            self.app.small_meteors = self.app.small_meteors + [
                Meteor(
                    Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                    Vec2(8, 8),
                    SIZE
                ) for _ in range(int(self.multiplier * LITTLE_METEOR_COUNT - LITTLE_METEOR_COUNT))
            ]

            self.app.big_meteors = self.app.big_meteors + [
                Meteor(
                    Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                    Vec2(16, 16),
                    SIZE
                ) for _ in range(int(self.multiplier * BIG_METEOR_COUNT - BIG_METEOR_COUNT))
            ]


class Background:
    star_colours = [5, 6]
    star_sep_distance = 13
    scroll_speed = 0.1

    def __init__(self, tilemap=0):
        self.tilemap = tilemap
        self.stars = []

        self.init_stars()

    def init_stars(self):
        for y in range(SIZE.y // self.star_sep_distance):
            for x in range(SIZE.x // self.star_sep_distance):
                star = [
                    (x * self.star_sep_distance + randint(0, 32)) % SIZE.x,
                    (y * self.star_sep_distance + randint(0, 32)) % SIZE.y,
                    choice(self.star_colours)
                ]

                self.stars.append(star)

    def draw(self):
        for star in self.stars:
            pyxel.pix(star[0], star[1], star[2])
            star[1] += self.scroll_speed
            if star[1] > SIZE.y:
                star[1] = 0
                star[0] = randrange(0, SIZE.x, 1)
