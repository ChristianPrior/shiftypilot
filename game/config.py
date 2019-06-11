import os
import string

from game.vector import Vec2

ALPHABET = string.ascii_uppercase
GAME_NAME = "Shifty Pilot 1: Galactic Apocalypse"
SIZE = Vec2(320, 320)

ASSETS_PATH = f"{os.getcwd()}/assets/sprites.pyxel"
HIGHSCORE_FILEPATH = f"{os.getcwd()}/highscores.json"
BUTTON_CONFIG_FILEPATH = f"{os.getcwd()}/button_config.json"

START_LIVES = 3
LITTLE_METEOR_COUNT = 10
BIG_METEOR_COUNT = 5

HIGHSCORE_GAME_MODE = True
