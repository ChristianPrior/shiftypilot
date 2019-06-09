from pyxel import constants

from game.animation import Particle
from game.config import SIZE, ASSETS_PATH, GAME_NAME, BUTTON_CONFIG_FILEPATH, HIGHSCORE_FILEPATH, START_LIVES
from game.level import Background, Level, LevelOne, LevelTwo

constants.APP_SCREEN_MAX_SIZE = 320

from random import random

import pyxel

from game.button_config import ControllerConfig
from game.highscores import Highscores
from game.player import Player, PlayerBody
from game.vector import Vec2


def btni(key):
    return 1 if pyxel.btn(key) else 0


def btnpi(key):
    return 1 if pyxel.btnp(key) else 0


class App:
    def __init__(self):
        pyxel.init(SIZE.x, SIZE.y, caption=GAME_NAME, fps=60)
        pyxel.load(ASSETS_PATH)

        self.level = None
        self.particles = []
        self.control_config_in_progress = False
        self.controls = ControllerConfig(BUTTON_CONFIG_FILEPATH)
        self.intro = True
        self.game_over = False
        self.highscores = Highscores(HIGHSCORE_FILEPATH)
        self.highscore_reached = False
        self.score = 0
        self.lives = 0

        self.cam_x = 0
        self.cam_y = 0
        self.cam_punch = 0

        self.init_player()
        self.bg = Background()

        pyxel.run(self.update, self.draw)

    def restart(self):
        pyxel.stop()
        self.intro = True
        self.control_config_in_progress = False
        self.game_over = False
        self.highscores = Highscores(HIGHSCORE_FILEPATH)
        self.highscore_reached = False

        self.level = None
        self.score = 0
        self.lives = 0

        self.init_player()

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 80), Vec2(8, 8))
        self.player_body = PlayerBody(SIZE // 2 + Vec2(0, 100), Vec2(8, 8), player=self.player, app=self)

    def death(self):
        pyxel.play(0, 3)
        if self.lives < 1:
            pyxel.stop()
            self.game_over = True
            if self.highscores.check_highscores(self.score):
                pyxel.play(0, 6)
                self.highscore_reached = True
            else:
                pyxel.play(0, 5)
        else:
            self.lives -= 1
            self.player.position = SIZE // 2 + Vec2(0, 80)
            self.player_body.teleport(activated=True)
            self.player_body.invincible_frames = 300
            self.player_body.invincibilty_animation.start()
            self.player_body.is_dead = False

    def end_game(self):
        if not self.highscore_reached:
            if btnpi(pyxel.KEY_SPACE) or btnpi(self.controls.mapping[self.controls.START]):
                self.highscores.move_to_next = True
                self.restart()
            return

        if self.highscores.ready_to_save:
            self.highscores.save_new(self.highscores.highscore_name, self.score)
            self.restart()
            return

        if btnpi(pyxel.KEY_W) or btnpi(self.controls.mapping[self.controls.UP]):
            pyxel.play(0, 4)
            self.highscores.alphabet_direction = 1

        elif btnpi(pyxel.KEY_S) or btnpi(self.controls.mapping[self.controls.DOWN]):
            pyxel.play(0, 4)
            self.highscores.alphabet_direction = -1

        if btnpi(pyxel.KEY_SPACE) or btnpi(self.controls.mapping[self.controls.START]):
            pyxel.play(0, 4)
            self.highscores.move_to_next = True

        self.highscores.update()

    def border_checker(self):
        position = self.player.position
        velocity = self.player.velocity

        if position.x < (0 + self.player.size.x) and velocity.x < 0:
            velocity.x = 0
        if position.x > (SIZE.x - self.player.size.x) and velocity.x > 0:
            velocity.x = 0
        if position.y < (0 + self.player.size.y) and velocity.y < 0:
            velocity.y = 0
        if position.y > (SIZE.y - self.player.size.y) and velocity.y > 0:
            velocity.y = 0

    def add_particle(self, x, y):
        particle = Particle(x, y)
        for i, p in enumerate(self.particles):
            if p.active is False:
                self.particles[i] = particle
                break
        else:
            self.particles.append(particle)

    def update(self):
        if self.control_config_in_progress:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

            key = self.controls.check_for_key()
            if key:
                self.controls.update_key(key)

                if self.controls.config_index > self.controls.max_index:
                    self.controls.save_config()
                    self.control_config_in_progress = False

            return

        if self.intro:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(self.controls.mapping[self.controls.START]):
                pyxel.playm(0, loop=True)
                self.intro = False
                self.lives = START_LIVES - 1
                self.level = LevelOne(app=self)

            if pyxel.btnp(pyxel.KEY_R) or self.controls.btn_hold(self.controls.check_for_held_key()):
                self.control_config_in_progress = True

            if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(self.controls.mapping[self.controls.SELECT]):
                pyxel.quit()
        elif self.game_over:
            self.end_game()
        else:
            self.score += 1
            self.player.velocity_x(
                (btni(pyxel.KEY_D) or btni(self.controls.mapping[self.controls.RIGHT])) - (btni(pyxel.KEY_A) or btni(self.controls.mapping[self.controls.LEFT]))
            )
            self.player.velocity_y(
                (btni(pyxel.KEY_S) or btni(self.controls.mapping[self.controls.DOWN])) - (btni(pyxel.KEY_W) or btni(self.controls.mapping[self.controls.UP]))
            )
            self.border_checker()

            self.player_body.teleport(
                (pyxel.btnp(pyxel.KEY_J) or pyxel.btnp(self.controls.mapping[self.controls.WARP]))    # Christian said use J
            )

            if not self.player_body.in_animation:
                self.player.update()

            projectiles = self.level.small_meteors + self.level.big_meteors
            self.player_body.update(projectiles)
            if self.player_body.is_dead:
                self.death()

            if self.cam_punch > 0:
                self.cam_x = -self.cam_punch + random() * self.cam_punch * 2
                self.cam_y = -self.cam_punch + random() * self.cam_punch * 2
                self.cam_punch -= 1
            else:
                self.cam_punch = 0
                self.cam_x = 0
                self.cam_y = 0

            for particle in self.particles:
                if particle.active:
                    if particle.age >= particle.life:
                        particle.active = False
                    particle.update()

            if self.level.LEVEL_COUNT == 1 and self.level.is_active is False:
                self.level = LevelTwo(app=self)

            self.level.update()

    def draw(self):
        if self.control_config_in_progress:
            pyxel.cls(0)
            key_to_change = self.controls.key_to_change()
            pyxel.text(115, 50, f"Push controller key for: {key_to_change}", 9)
            return

        elif self.intro:
            pyxel.cls(0)
            pyxel.text(85, 40, GAME_NAME, pyxel.frame_count % 16)
            pyxel.text(115, 50, "Press SPACE to start", 9)
            pyxel.text(20, 60, "Press R (Keyboard) OR Any controller button to assign controller keys", 9)
            pyxel.text(135, 80, "HIGHSCORES:", 7)
            for i, x in enumerate(self.highscores.ordered_score_list()):
                pyxel.text(
                    135,
                    (80 + (i + 1) * 10),
                    f"{x['name']}: {x['score']}",
                    7
                )

        elif self.game_over:
            pyxel.cls(0)
            pyxel.text(135, 60, "GAME OVER", 9)
            if self.highscore_reached:
                pyxel.text(100, 80, f"Enter name: {self.highscores.highscore_name}", 9)
                pyxel.text(100, 90, "USE 'W' 'S' and 'SPACE' keys", 9)
            else:
                pyxel.text(110, 80, "Push space to restart", 9)

        else:
            pyxel.cls(0)
            self.bg.draw()
            self.level.draw()

            for particle in self.particles:
                if particle.active:
                    particle.draw()

            if not self.player_body.teleport_in_animation.is_active:
                pyxel.blt(
                    self.player.position.x - self.player.size.x // 2 - self.cam_x,
                    self.player.position.y - self.player.size.y // 2 - self.cam_y,
                    0,
                    16,
                    0,
                    self.player.size.x,
                    self.player.size.y,
                    0
                )

            self.player_body.animate_teleport()
            self.player_body.animate_invincibility()

            if not self.player_body.in_animation and not self.player_body.invincibilty_animation.is_active:
                pyxel.blt(
                    self.player_body.position.x - self.player_body.size.x // 2 - self.cam_x,
                    self.player_body.position.y - self.player_body.size.y // 2 - self.cam_y,
                    0,
                    8,
                    0,
                    self.player_body.size.x,
                    self.player_body.size.y,
                    0
                )

            score_text = f"Score: {self.score}"
            life_text = f"Lives: {self.lives + 1}"
            pyxel.text(5, 5, score_text, 9)
            pyxel.text(60, 5, life_text, 9)


App()
