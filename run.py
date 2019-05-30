from pyxel import constants

constants.APP_SCREEN_MAX_SIZE = 320

import os

import pyxel

from game.vector import Vec2
from game.player import Player


SIZE = Vec2(320, 320)
ASSETS_PATH = f"{os.getcwd()}/assets/sprites.pyxel"


class App:
    def __init__(self):
        self.player = None
        pyxel.init(SIZE.x - 1, SIZE.y - 1, caption="name TBC", fps=60)
        pyxel.load(ASSETS_PATH)

        self.init_player()
        self.x = 0
        pyxel.run(self.update, self.draw)

    def init_player(self):
        self.player = Player(SIZE // 2 + Vec2(0, 0), Vec2(0, 0))

    def update(self):
        self.x = (self.x + 1) % pyxel.width

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
