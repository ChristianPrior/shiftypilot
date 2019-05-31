import json
import os
import string

ALPHABET = string.ascii_uppercase
BASE_HIGHSCORE_FILEPATH = f"{os.getcwd()}/assets/base_highscores.json"
DEFAULT_NAME = '___'


class Highscores():

    def __init__(self, highscore_filepath):
        self.highscore_filepath = highscore_filepath
        self.score_list = []
        self.load_highscores()
        self.needs_updating = False
        self.highscore_name = DEFAULT_NAME
        self.active_letter = 0
        self.ready_to_save = False
        self.move_to_next = False
        self.alphabet_direction = 0
        self.alphabet_index = -1

    def load_highscores(self):
        try:
            with open(self.highscore_filepath, 'r') as highscores:
                self.score_list = json.load(highscores)
        except FileNotFoundError:
            with open(BASE_HIGHSCORE_FILEPATH, 'r') as base_highscores:
                base_highscores = json.load(base_highscores)

            with open(self.highscore_filepath, 'w') as highscores:
                json.dump(base_highscores, highscores, indent=4)

        self.needs_updating = False

    def save_new(self, name, score):
        new_highscore = {
            'name': name,
            'score': score
        }
        self.score_list.append(new_highscore)
        self.score_list = self.ordered_score_list()
        with open(self.highscore_filepath, 'w') as highscore_file:
            json.dump(self.score_list, highscore_file, indent=4)

    def check_highscores(self, score):
        current_highscores = [x['score'] for x in self.score_list]
        if all([score < highscore for highscore in current_highscores]):
            return False

        return True

    def ordered_score_list(self):
        return sorted(self.score_list, key=lambda k: k['score'], reverse=True)[:10]

    def update(self):
        if self.active_letter > 2:
            self.ready_to_save = True
            return

        if self.move_to_next:
            if not self.highscore_name[self.active_letter] == '_':
                self.alphabet_index = -1
                self.active_letter += 1

            self.move_to_next = False
            return

        if self.alphabet_direction == 0:
            return

        if self.alphabet_direction > 0:
            self.alphabet_index += 1
            if self.alphabet_index > 25:
                self.alphabet_index = 0

        if self.alphabet_direction < 0:
            self.alphabet_index -= 1
            if self.alphabet_index < 0:
                self.alphabet_index = 25

        self.alphabet_direction = 0
        selected_letter = ALPHABET[self.alphabet_index]
        name = self.highscore_name
        new_name = name[:self.active_letter] + selected_letter + name[self.active_letter + 1:]

        self.highscore_name = new_name
