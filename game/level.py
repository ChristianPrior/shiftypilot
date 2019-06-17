from random import randint, choice, randrange, uniform

import pyxel

from game.config import HIGHSCORE_GAME_MODE

from game.config import SIZE, LITTLE_METEOR_COUNT, BIG_METEOR_COUNT
from game.projectile import Meteor
from game.vector import Vec2


class Difficulty:
    multiplier: float
    # level: int

    def __init__(self, app, multiplier):
        self.app = app
        self.multiplier = multiplier
        self.speed_range = (0.5, 1.5)

        self.reset_meteor_count()

    def reset_meteor_count(self):
        if self.app.level:
            self.app.level.small_meteors = [
                    Meteor(
                        Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                        Vec2(8, 8),
                        SIZE,
                        move_speed=Vec2(0, uniform(*self.speed_range))
                    ) for _ in range(LITTLE_METEOR_COUNT)
                ]

            self.app.level.big_meteors = [
                Meteor(
                    Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                    Vec2(16, 16),
                    SIZE,
                    move_speed=Vec2(0, uniform(*self.speed_range))
                ) for _ in range(BIG_METEOR_COUNT)
            ]

    def increase_meteors(self):
        self.app.level.small_meteors = self.app.level.small_meteors + [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(8, 8),
                SIZE,
                move_speed=Vec2(0, uniform(*self.speed_range))
            ) for _ in range(int(self.multiplier * LITTLE_METEOR_COUNT - LITTLE_METEOR_COUNT))
        ]

        self.app.level.big_meteors = self.app.level.big_meteors + [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(16, 16),
                SIZE,
                move_speed=Vec2(0, uniform(*self.speed_range))
            ) for _ in range(int(self.multiplier * BIG_METEOR_COUNT - BIG_METEOR_COUNT))
        ]

    def change_meteor_speeds(self, speed_range: tuple):
        self.speed_range = speed_range
        self.app.level.small_meteors = self.app.level.small_meteors + [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(8, 8),
                SIZE,
                move_speed=Vec2(0, uniform(*self.speed_range))
            ) for _ in range(int(LITTLE_METEOR_COUNT))
        ]

        self.app.level.big_meteors = self.app.level.big_meteors + [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(16, 16),
                SIZE,
                move_speed=Vec2(0, uniform(*self.speed_range))
            ) for _ in range(int(BIG_METEOR_COUNT))
        ]


class Level:
    timer: int = 0
    LEVEL_COUNT: int = 0

    def __init__(self, app, difficulty: Difficulty = None):
        self.app = app
        self.difficulty = difficulty or Difficulty(app=self.app, multiplier=1.2)
        self.is_active = True
        self.small_meteors: list
        self.big_meteors: list
        self.level_phases: dict
        self.current_phase = 0
        self.phase_timer = 0

    def update(self):
        raise NotImplementedError(f'update function for Level {self.LEVEL_COUNT} not implemented')

    def draw(self):
        raise NotImplementedError(f'draw function for Level {self.LEVEL_COUNT} not implemented')


class HighscoreLevel(Level):
    LEVEL_COUNT = 0
    LEVEL_END_TIME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level_phases = self.init_phases()
        self.small_meteors = self.init_small_meteors()
        self.big_meteors = self.init_big_meteors()

    def init_phases(self):
        phase_mapping = {
            0: {"update_func": self.phase_zero_update, "length": 100},
            1: {"update_func": self.phase_one_update, "length": 1000},
            2: {"update_func": self.phase_two_update, "length": 3000},
            3: {"update_func": self.phase_three_update, "length": 1000},

        }
        return phase_mapping

    @staticmethod
    def init_small_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(4, SIZE.y)),
                Vec2(8, 8),
                SIZE,
                move_speed=Vec2(0, uniform(0.5, 1.5))
            ) for _ in range(LITTLE_METEOR_COUNT)
        ]

    @staticmethod
    def init_big_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(8, SIZE.y)),
                Vec2(16, 16),
                SIZE,
                move_speed=Vec2(0, uniform(0.5, 1.5))
            ) for _ in range(BIG_METEOR_COUNT)
        ]

    def phase_has_ended(self, phase, phase_timer=None):
        phase_timer = phase_timer or self.phase_timer

        elapsed_phase_length_sum = 0
        for phase_count in range(phase + 1):
            elapsed_phase_length_sum += self.level_phases[phase_count]['length']

        has_ended = phase_timer >= self.level_phases[phase]['length']
        end_frame = phase_timer == self.level_phases[phase]['length']

        return has_ended, end_frame

    # def level_end(self):
    #     if self.LEVEL_END_TIME and self.timer > self.LEVEL_END_TIME:
    #         self.is_active = False
    #         return True
    #     return False

    def increment_phase(self):
        self.current_phase += 1
        print('incrementing phase')

    def phase_zero_update(self):
        _, end_frame = self.phase_has_ended(0, self.phase_timer)
        self.phase_timer += 1
        if end_frame:
            print(self.timer)
            print('ending phase 0')
            self.phase_timer = 0
            self.increment_phase()

    def phase_one_update(self):
        phase_ended, end_frame = self.phase_has_ended(1, self.phase_timer)

        if end_frame:
            print(self.timer)
            print('ending phase 1')

        if phase_ended:
            for meteor in self.small_meteors:
                meteor.update(end_sequence=True)
            for meteor in self.big_meteors:
                meteor.update(end_sequence=True)

            if (not any(meteor.is_active for meteor in self.small_meteors)
                    and not any(meteor.is_active for meteor in self.big_meteors)):
                self.increment_phase()
                self.difficulty.reset_meteor_count()
                self.difficulty.change_meteor_speeds((1, 2))
                self.phase_timer = 0
        else:
            for meteor in self.small_meteors:
                meteor.update()
            for meteor in self.big_meteors:
                meteor.update()

            if self.app.score % 250 == 0:
                self.difficulty.increase_meteors()

        self.phase_timer += 1

    def phase_two_update(self):
        phase_ended, end_frame = self.phase_has_ended(2, self.phase_timer)

        if end_frame:
            print(self.timer)
            print('ending phase 2')

        if phase_ended:
            for meteor in self.small_meteors:
                meteor.update(end_sequence=True, speed_range=self.difficulty.speed_range)
            for meteor in self.big_meteors:
                meteor.update(end_sequence=True, speed_range=self.difficulty.speed_range)

            if (not any(meteor.is_active for meteor in self.small_meteors)
                    and not any(meteor.is_active for meteor in self.big_meteors)):
                self.increment_phase()
                self.difficulty.reset_meteor_count()
        else:
            for meteor in self.small_meteors:
                meteor.update(speed_range=self.difficulty.speed_range)
            for meteor in self.big_meteors:
                meteor.update(speed_range=self.difficulty.speed_range)

        self.phase_timer += 1

    def phase_three_update(self):
        if self.current_phase == 3:
            for meteor in self.small_meteors:
                meteor.update(speed_range=self.difficulty.speed_range)
            for meteor in self.big_meteors:
                meteor.update(speed_range=self.difficulty.speed_range)

            if self.app.score % 250 == 0:
                self.difficulty.increase_meteors()

    def update(self):
        self.level_phases[self.current_phase]['update_func']()

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


class LevelOne(Level):
    LEVEL_COUNT = 1
    LEVEL_END_TIME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level_phases = self.init_phases()
        self.small_meteors = self.init_small_meteors()
        self.big_meteors = self.init_big_meteors()

    def init_phases(self):
        phase_mapping = {
            0: {"update_func": self.phase_zero_update, "length": 100},
            1: {"update_func": self.phase_one_update, "length": 500}

        }
        return phase_mapping

    @staticmethod
    def init_small_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(4, SIZE.y)),
                Vec2(8, 8),
                SIZE,
                move_speed=Vec2(0, uniform(0.5, 1.5))
            ) for _ in range(LITTLE_METEOR_COUNT)
        ]

    @staticmethod
    def init_big_meteors():
        return [
            Meteor(
                Vec2(randint(0, SIZE.x), -randint(8, SIZE.y)),
                Vec2(16, 16),
                SIZE,
                move_speed=Vec2(0, uniform(0.5, 1.5))
            ) for _ in range(BIG_METEOR_COUNT)
        ]

    def phase_has_ended(self, phase):
        if phase == 1 and HIGHSCORE_GAME_MODE:
            return False, False

        elapsed_phase_length_sum = 0
        for phase_count in range(phase + 1):
            elapsed_phase_length_sum += self.level_phases[phase_count]['length']

        has_ended = elapsed_phase_length_sum - self.timer <= 0
        end_frame = elapsed_phase_length_sum - self.timer == 0

        return has_ended, end_frame

    # def level_end(self):
    #     if self.LEVEL_END_TIME and self.timer > self.LEVEL_END_TIME:
    #         self.is_active = False
    #         return True
    #     return False

    def increment_phase(self):
        self.current_phase += 1
        print(f'incrementing phase to phase {self.current_phase}')

    def phase_zero_update(self):
        _, end_frame = self.phase_has_ended(0)

        if end_frame:
            print(self.timer)
            print('ending phase 0')
            self.increment_phase()

    def phase_one_update(self):
        if self.current_phase == 1:
            phase_ended, end_frame = self.phase_has_ended(1)

            if end_frame and not HIGHSCORE_GAME_MODE:
                print(self.timer)
                print('ending phase 1')

            if phase_ended:
                for meteor in self.small_meteors:
                    meteor.update(end_sequence=True)
                for meteor in self.big_meteors:
                    meteor.update(end_sequence=True)

                if (not any(meteor.is_active for meteor in self.small_meteors)
                        and not any(meteor.is_active for meteor in self.big_meteors)):
                    self.increment_phase()
            else:
                for meteor in self.small_meteors:
                    meteor.update()
                for meteor in self.big_meteors:
                    meteor.update()

                if self.app.score % 250 == 0:
                    self.difficulty.increase_meteors()

    def update(self):
        for phase in self.level_phases.keys():
            self.level_phases[phase]['update_func']()

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
    scroll_speed = 0.2

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
