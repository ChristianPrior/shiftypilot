from pyxel import constants

constants.APP_SCREEN_MAX_SIZE = 320

import json
import os
from random import randint
import string

import pyxel

from game.player import Player, PlayerBody
from game.projectile import Projectile
from game.vector import Vec2


ALPHABET = string.ascii_uppercase
SIZE = Vec2(320, 320)
ASSETS_PATH = f"{os.getcwd()}/assets/sprites.pyxel"
HIGHSCORE_FILENAME = "highscores.json"
START_LIVES = 3
TOTAL_DEATH_CIRCLES = 100


def btni(key):
    return 1 if pyxel.btn(key) else 0


class App:
    def __init__(self):
        pyxel.init(SIZE.x, SIZE.y, caption="shitty pilot", fps=60)
        pyxel.load(ASSETS_PATH)

        self.intro = True
        self.game_over = False
        self.highscores = self.init_highscores()
        self.highscores_need_update = None
        self.death_circles = self.init_death_circles()
        self.score = 0
        self.highscore_name = 'AAA'
        self.lives = 0

        self.init_player()
        pyxel.run(self.update, self.draw)

    def init_highscores(self):
        with open(HIGHSCORE_FILENAME, 'r') as highscore_file:
            return json.load(highscore_file)

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 0), Vec2(8, 8))
        self.player_body = PlayerBody(SIZE // 2 + Vec2(0, 20), Vec2(8, 8), player=self.player)

    def init_death_circles(self):
        return [
            Projectile(Vec2(randint(0, SIZE.x), (i * -60)), Vec2(5, 5), SIZE) for i in range(TOTAL_DEATH_CIRCLES)
        ]

    def update_highscores(self):
        with open(HIGHSCORE_FILENAME, 'r') as highscore_file:
            self.highscores = json.load()
        self.highscores = json.load(highscore_file)

    def death(self):
        if self.lives < 1:
            self.game_over = True
        else:
            self.lives -= 1
            self.death_circles = self.init_death_circles()
            self.init_player()

    def end_game(self):
        if len(self.highscore_name) > 3:
            new_highscore = {
                'name': self.highscore_name,
                'score': self.score
            }
            self.score = 0
            self.highscores.append(new_highscore)
            self.highscores = sorted(self.highscores, key=lambda k: k['score'], reverse=True)[:10]
            with open(HIGHSCORE_FILENAME, 'w') as highscore_file:
                json.dump(self.highscores, highscore_file)
            self.highscores_need_update = True
            self.intro = True

        else:
            pass
        #     if pyxel.btnp(pyxel.KEY_W):
        #
        #     elif pyxel.btnp(pyxel.KEY_S):
        #
        #     elif pyxel.btnp(pyxel.KEY_ENTER):
        #         self.highscore_name +=
        #     else:
        #         pass

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.intro:
            if self.highscores_need_update:
                self.update_highscores()

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

            self.player_body.teleport(pyxel.btnp(pyxel.KEY_J))    # Christian said use J

            self.player.update()
            self.player_body.update(projectiles)
            if self.player_body.is_dead:
                self.death()
            for death_circle in self.death_circles:
                death_circle.update(self.player_body)

    def draw(self):
        if self.game_over:
            pyxel.cls(1)
            pyxel.text(2, 15, "Enter name: {AAA}", 7)

        elif self.intro:
            pyxel.cls(12)
            pyxel.text(2, 15, "ShiftPilot", 7)
            pyxel.text(2, 7, "Press space to start", 7)
            pyxel.text(SIZE.x - 60, 7, "HIGHSCORES:", 7)
            for i, x in enumerate(self.highscores):
                pyxel.text(
                    SIZE.x - 60,
                    (7 + (i + 1) * 8),
                    f"{x['name']}: {x['score']}",
                    7
                )

        else:
            pyxel.cls(0)
            score_text = f"Score: {self.score}"
            life_text = f"Lives: {self.lives}"
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
