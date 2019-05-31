from game.gmath import sign
from game.vector import Vec2


class Actor:
    def __init__(self, position: Vec2, size: Vec2):
        self.position = position
        self.size = size
        self.remain = Vec2(0, 0)
        self.in_animation = False

    def move_x(self, amount):
        self.remain.x += amount

        move = round(self.remain.x)
        if move == 0:
            return

        self.remain.x -= move

        sgn = sign(move)

        while move != 0:
            self.position.x += sgn

            move -= sgn

    def move_y(self, amount):
        self.remain.y += amount

        move = round(self.remain.y)
        if move == 0:
            return

        self.remain.y -= move

        sgn = sign(move)

        while move != 0:
            self.position.y += sgn

            move -= sgn
