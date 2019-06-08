from random import randint, choice, randrange

import pyxel

from game.config import SIZE, LITTLE_METEOR_COUNT, BIG_METEOR_COUNT
from game.projectile import Meteor
from game.vector import Vec2


class Difficulty:
    multiplier: float
    # level: int

    def __init__(self, app, multiplier):
        self.app = app
        self.multiplier = multiplier

    #     self.reset_difficulty()
    #
    # def reset_difficulty(self):
    #     if self.app.level:
    #         self.app.level.small_meteors = [
    #                 Meteor(
    #                     Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
    #                     Vec2(8, 8),
    #                     SIZE
    #                 ) for _ in range(LITTLE_METEOR_COUNT)
    #             ]
    #
    #         self.app.level.big_meteors = [
    #             Meteor(
    #                 Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
    #                 Vec2(16, 16),
    #                 SIZE
    #             ) for _ in range(BIG_METEOR_COUNT)
    #         ]

    def increase_difficulty(self):
        if self.app.score >= 1000 and self.app.score % 250 == 0:
            self.app.level.small_meteors = self.app.level.small_meteors + [
                Meteor(
                    Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                    Vec2(8, 8),
                    SIZE
                ) for _ in range(int(self.multiplier * LITTLE_METEOR_COUNT - LITTLE_METEOR_COUNT))
            ]

            self.app.level.big_meteors = self.app.level.big_meteors + [
                Meteor(
                    Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                    Vec2(16, 16),
                    SIZE
                ) for _ in range(int(self.multiplier * BIG_METEOR_COUNT - BIG_METEOR_COUNT))
            ]


class Level:
    timer: int = 0
    LEVEL_COUNT: int = 0

    def __init__(self, app, difficulty: Difficulty = None):
        self.app = app
        self.difficulty = difficulty or Difficulty(app=self.app, multiplier=1.2)
        self.is_active = True
        self.small_meteors = []
        self.big_meteors = []

    def update(self):
        raise NotImplementedError(f'update function for Level {self.LEVEL_COUNT} not implemented')

    def draw(self):
        raise NotImplementedError(f'draw function for Level {self.LEVEL_COUNT} not implemented')


class LevelOne(Level):
    LEVEL_COUNT = 1
    LEVEL_END_TIME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.small_meteors = self.init_small_meteors()
        self.big_meteors = self.init_big_meteors()

    @staticmethod
    def init_small_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(8, 8),
                SIZE
            ) for _ in range(LITTLE_METEOR_COUNT)
        ]

    @staticmethod
    def init_big_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(16, 16),
                SIZE
            ) for _ in range(BIG_METEOR_COUNT)
        ]

    def level_end(self):
        if self.LEVEL_END_TIME and self.timer > self.LEVEL_END_TIME:
            return True
        return False

    def update(self):
        if self.level_end():
            for meteor in self.small_meteors:
                meteor.update(end_sequence=True)
            for meteor in self.big_meteors:
                meteor.update(end_sequence=True)

            if (not any(meteor.is_active for meteor in self.small_meteors)
                    and not any(meteor.is_active for meteor in self.big_meteors)):
                self.is_active = False
        else:
            for meteor in self.small_meteors:
                meteor.update()
            for meteor in self.big_meteors:
                meteor.update()

            self.difficulty.increase_difficulty()

        self.timer += 1

    def draw(self):
        for meteor in self.small_meteors:
            if meteor.is_active:
                pyxel.blt(
                    meteor.position.x - meteor.size.x // 2 - self.app.cam_x,
                    meteor.position.y - meteor.size.y // 2 - self.app.cam_y,
                    0,
                    0,
                    16 + (8 * meteor.kind),
                    meteor.size.x,
                    meteor.size.y,
                    0
                )

        for meteor in self.big_meteors:
            if meteor.is_active:
                pyxel.blt(
                    meteor.position.x - meteor.size.x // 2 - self.app.cam_x,
                    meteor.position.y - meteor.size.y // 2 - self.app.cam_y,
                    0,
                    8 + (16 * meteor.kind),
                    16,
                    meteor.size.x,
                    meteor.size.y,
                    0
                )


class LevelTwo(Level):
    LEVEL_COUNT = 2

    def update(self):
        pass

    def draw(self):
        pass


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
