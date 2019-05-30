from pyxel import constants

constants.APP_SCREEN_MAX_SIZE = 320

import os

import pyxel

from game.vector import Vec2
from game.player import Player


SIZE = Vec2(320, 320)
ASSETS_PATH = f"{os.getcwd()}/assets/sprites.pyxel"


def btni(key):
    return 1 if pyxel.btn(key) else 0


class App:
    def __init__(self):
        pyxel.init(SIZE.x - 1, SIZE.y - 1, caption="shitty pilot", fps=60)
        pyxel.load(ASSETS_PATH)

        self.init_player()
        pyxel.run(self.update, self.draw)

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 0), Vec2(0, 0))

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.velocity_x(btni(pyxel.KEY_D) - btni(pyxel.KEY_A))
        self.player.velocity_y(btni(pyxel.KEY_S) - btni(pyxel.KEY_W))

        self.player.update()

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 40, 25)
        pyxel.blt(
            self.player.position.x - self.player.size.x // 2,
            self.player.position.y - self.player.size.y // 2,
            0,
            8,
            0,
            8,
            8
        )


App()
