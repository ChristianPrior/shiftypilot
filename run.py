from pyxel import constants

constants.APP_SCREEN_MAX_SIZE = 320

import os
from random import randint
import string

import pyxel

from game.highscores import Highscores
from game.player import Player, PlayerBody
from game.projectile import Projectile
from game.vector import Vec2

ALPHABET = string.ascii_uppercase
GAME_NAME = "Shifty Pilot 1: Galactic Apocalypse"
SIZE = Vec2(320, 320)

ASSETS_PATH = f"{os.getcwd()}/assets/sprites.pyxel"
HIGHSCORE_FILEPATH = f"{os.getcwd()}/highscores.json"

START_LIVES = 1
TOTAL_DEATH_CIRCLES = 100


def btni(key):
    return 1 if pyxel.btn(key) else 0


def btnpi(key):
    return 1 if pyxel.btnp(key) else 0


class App:
    def __init__(self):
        pyxel.init(SIZE.x, SIZE.y, caption=GAME_NAME, fps=60)
        pyxel.load(ASSETS_PATH)

        self.intro = True
        self.game_over = False
        self.highscores = Highscores(HIGHSCORE_FILEPATH)
        self.death_circles = self.init_death_circles()
        self.score = 0
        self.lives = 0

        self.init_player()
        pyxel.run(self.update, self.draw)

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 0), Vec2(8, 8))
        self.player_body = PlayerBody(SIZE // 2 + Vec2(0, 20), Vec2(8, 8), player=self.player)

    def init_death_circles(self):
        return [
            Projectile(
                Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
                Vec2(5, 5),
                SIZE
            ) for _ in range(TOTAL_DEATH_CIRCLES)
        ]

    def death(self):
        if self.lives < 1:
            self.game_over = True
        else:
            self.lives -= 1
            self.death_circles = self.init_death_circles()
            self.init_player()

    def end_game(self):
        if not self.highscores.ready_to_save:
            if btnpi(pyxel.KEY_W):
                self.highscores.alphabet_direction = 1

            elif btnpi(pyxel.KEY_S):
                self.highscores.alphabet_direction = -1

            if btnpi(pyxel.KEY_SPACE):
                self.highscores.move_to_next = True

            self.highscores.update()

        else:
            self.highscores.save_new(self.highscores.highscore_name, self.score)
            self.__init__()

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

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.intro:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.intro = False
                self.lives = START_LIVES - 1
        elif self.game_over:
            self.end_game()
        else:
            projectiles = self.death_circles
            self.score += 1
            self.player.velocity_x(btni(pyxel.KEY_D) - btni(pyxel.KEY_A))
            self.player.velocity_y(btni(pyxel.KEY_S) - btni(pyxel.KEY_W))
            self.border_checker()

            self.player_body.teleport(pyxel.btnp(pyxel.KEY_J))    # Christian said use J

            self.player.update()
            self.player_body.update(projectiles)
            if self.player_body.is_dead:
                self.death()
            for death_circle in self.death_circles:
                death_circle.update(self.player_body)

    def draw(self):
        if self.intro:
            pyxel.cls(12)
            pyxel.text(2, 15, GAME_NAME, 7)
            pyxel.text(2, 7, "Press space to start", 7)
            pyxel.text(SIZE.x - 60, 7, "HIGHSCORES:", 7)
            for i, x in enumerate(self.highscores.score_list):
                pyxel.text(
                    SIZE.x - 60,
                    (7 + (i + 1) * 8),
                    f"{x['name']}: {x['score']}",
                    7
                )

        elif self.game_over:
            pyxel.cls(1)
            pyxel.text(2, 15, f"Enter name: {self.highscores.highscore_name}", 7)
            pyxel.text(2, 50, "USE 'W' 'S' and 'SPACE' keys", 7)

        else:
            pyxel.cls(0)
            score_text = f"Score: {self.score}"
            life_text = f"Lives: {self.lives + 1}"
            pyxel.text(0, 0, score_text, 9)
            pyxel.text(60, 0, life_text, 9)
            pyxel.blt(
                self.player.position.x - self.player.size.x // 2,
                self.player.position.y - self.player.size.y // 2,
                0,
                16,
                0,
                self.player.size.x,
                self.player.size.y,
            )
            pyxel.blt(
                self.player_body.position.x - self.player.size.x // 2,
                self.player_body.position.y - self.player.size.y // 2,
                0,
                8,
                0,
                self.player_body.size.x,
                self.player_body.size.y,
            )

            for death_circle in self.death_circles:
                if death_circle.is_active:
                    pyxel.blt(
                        death_circle.position.x,
                        death_circle.position.y,
                        0,
                        8,
                        8,
                        death_circle.size.x,
                        death_circle.size.y,
                    )


App()
