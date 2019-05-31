import pyxel


class Animation:
    start_phase = 0
    end_phase = 0
    current_phase = 0
    frame_count = 0
    sprite_mapping = {}
    is_active = False

    def __init__(self, start_phase=start_phase, end_phase=end_phase, frame_count=frame_count, start_pos_x=None,
                 start_pos_y=None, entity=None):
        self.start_phase = start_phase
        self.end_phase = end_phase
        self.frame_count = frame_count
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.entity = entity


class TeleportOut(Animation):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.end_phase = 7

    def start(self):
        self.is_active = True
        self.entity.in_animation = True

    def animate(self):
        sprite, total_frames = self.get_sprite()

        if self.current_phase == self.end_phase and self.frame_count == total_frames:
            self.is_active = False
            self.entity.in_animation = False

        self.frame_count += 1

        if self.frame_count == total_frames:
            if self.current_phase != self.end_phase:
                self.current_phase += 1
                self.frame_count = 0

        pyxel.blt(*sprite)

    def get_sprite(self):
        x, y = (
            self.entity.position.x,
            self.entity.position.y
        )
        sprite_mapping = {
            7: ((x + 3, y + 3, 0, 120, 0, 2, 2, 0), 1),
            6: ((x + 2, y + 2, 0, 112, 0, 4, 4, 0), 1),
            5: ((x + 1, y + 1, 0, 104, 0, 6, 6, 0), 2),
            4: ((x - 1, y - 1, 0, 88, 0, 10, 10, 0), 2),
            3: ((x - 3, y - 3, 0, 72, 0, 14, 14, 0), 2),
            2: ((x - 3, y - 3, 0, 56, 0, 14, 14, 0), 3),
            1: ((x - 3, y - 3, 0, 40, 0, 14, 14, 0), 2),
            0: ((x - 1, y - 1, 0, 24, 0, 10, 10, 0), 1),
        }

        return sprite_mapping[self.current_phase]


class TeleportIn(TeleportOut):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.end_phase = 7

    def animate(self):
        sprite, total_frames = self.get_sprite()

        if self.current_phase == self.end_phase and self.frame_count == total_frames:
            self.is_active = False
            self.entity.in_animation = False

        self.frame_count += 1

        if self.frame_count == total_frames:
            if self.current_phase != self.end_phase:
                self.current_phase += 1
                self.frame_count = 0

        pyxel.blt(*sprite)

    def get_sprite(self):
        x, y = (
            self.entity.position.x,
            self.entity.position.y
        )
        sprite_mapping = {
            0: ((x + 3, y + 3, 0, 120, 0, 2, 2, 0), 1),
            1: ((x + 2, y + 2, 0, 112, 0, 4, 4, 0), 1),
            2: ((x + 1, y + 1, 0, 104, 0, 6, 6, 0), 2),
            3: ((x - 1, y - 1, 0, 88, 0, 10, 10, 0), 2),
            4: ((x - 3, y - 3, 0, 72, 0, 14, 14, 0), 2),
            5: ((x - 3, y - 3, 0, 56, 0, 14, 14, 0), 3),
            6: ((x - 3, y - 3, 0, 40, 0, 14, 14, 0), 2),
            7: ((x - 1, y - 1, 0, 24, 0, 10, 10, 0), 1),
        }

        return sprite_mapping[self.current_phase]
