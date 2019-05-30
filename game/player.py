from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor


class Player(Actor):
    MOVEMENT_SPD = 1

    def __init__(self, position: Vec2, size: Vec2):
        super().__init__(position, size)
        self.velocity = Vec2(0, 0)

    def velocity_x(self, direction: int):
        direction = sign(direction)

        self.velocity.x = direction * self.MOVEMENT_SPD

    def velocity_y(self, direction: int):
        direction = sign(direction)

        self.velocity.y = direction * self.MOVEMENT_SPD

    def update(self):
        self.move_x(self.velocity.x)
        self.move_y(self.velocity.y)
