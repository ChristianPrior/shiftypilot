import json
import os

import pyxel

BASE_CONFIG_FILEPATH = f"{os.getcwd()}/assets/default_key_config.json"
TOTAL_BUTTONS = 7


class ControllerConfig:
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    WARP = 'WARP'
    START = 'START'
    SELECT = 'SELECT'

    def __init__(self, config_filepath):
        self.config_filepath = config_filepath
        self.mapping = {}
        self.button_list = []
        self.load_button_config()
        self.config_index = 0
        self.max_index = TOTAL_BUTTONS - 1
        self.timer = 0

    def btn_hold(self, key):
        press = pyxel.btn(key)
        if press:
            self.timer += press
        if self.timer > 60:
            self.timer = 0
            return True
        return False

    @staticmethod
    def check_for_key():
        for key in range(3000, 3050):
            if pyxel.btnp(key):
                return key

    @staticmethod
    def check_for_held_key():
        for key in range(3000, 3050):
            if pyxel.btn(key):
                return key

    def save_config(self):
        self.config_index = 0
        with open(self.config_filepath, 'w') as button_config:
            json.dump(self.mapping, button_config, indent=4)

    def load_button_config(self):
        try:
            with open(self.config_filepath, 'r') as button_config:
                self.mapping = json.load(button_config)
        except FileNotFoundError:
            with open(BASE_CONFIG_FILEPATH, 'r') as base_button_config:
                self.mapping = json.load(base_button_config)

            self.save_config()

        self.button_list = [key for key in self.mapping]

    def update_key(self, key):
        key_to_change = self.key_to_change()
        self.mapping[key_to_change] = key
        self.config_index += 1

    def key_to_change(self):
        return self.button_list[self.config_index]
