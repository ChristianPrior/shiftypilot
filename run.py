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
        self.highscore_reached = False
        self.death_circles = self.init_death_circles()
        self.score = 0
        self.lives = 0

        self.init_player()
        pyxel.run(self.update, self.draw)

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 0), Vec2(8, 8))
        self.player_body = PlayerBody(SIZE // 2 + Vec2(0, 20), Vec2(8, 8), player=self.player)

    def init_death_circles(self):
        # return [
        #     Projectile(
        #         Vec2(randint(0, SIZE.x), -randint(0, SIZE.y)),
        #         Vec2(5, 5),
        #         SIZE
        #     ) for _ in range(TOTAL_DEATH_CIRCLES)
        # ]
        return [
            Projectile(
                Vec2(120, -randint(0, SIZE.y)),
                Vec2(5, 5),
                SIZE
            ) for _ in range(TOTAL_DEATH_CIRCLES)
        ]

    def death(self):
        if self.lives < 1:
            self.game_over = True
            if self.highscores.check_highscores(self.score):
                self.highscore_reached = True

        else:
            self.lives -= 1
            self.death_circles = self.init_death_circles()
            self.init_player()

    def end_game(self):
        if not self.highscore_reached:
            if btnpi(pyxel.KEY_SPACE):
                self.__init__()
            return

        if self.highscores.ready_to_save:
            self.highscores.save_new(self.highscores.highscore_name, self.score)
            self.__init__()
            return

        if btnpi(pyxel.KEY_W):
            self.highscores.alphabet_direction = 1

        elif btnpi(pyxel.KEY_S):
            self.highscores.alphabet_direction = -1

        if btnpi(pyxel.KEY_SPACE):
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
                death_circle.update()

    def draw(self):
        if self.intro:
            pyxel.cls(0)
            pyxel.text(85, 40, GAME_NAME, pyxel.frame_count % 16)
            pyxel.text(115, 50, "Press SPACE to start", 9)
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
            score_text = f"Score: {self.score}"
            life_text = f"Lives: {self.lives + 1}"
            pyxel.text(5, 5, score_text, 9)
            pyxel.text(50, 5, life_text, 9)
            pyxel.blt(
                self.player.position.x,
                self.player.position.y,
                0,
                16,
                0,
                self.player.size.x,
                self.player.size.y,
            )
            pyxel.blt(
                self.player_body.position.x,
                self.player_body.position.y,
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
