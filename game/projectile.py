from random import randint

from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor


class Projectile(Actor):
    MOVEMENT_SPD_X = 0
    MOVEMENT_SPD_Y = 1

    def __init__(self, position: Vec2, size: Vec2, screen_size: Vec2):
        super().__init__(position, size)
        self.velocity = Vec2(0, 0)
        self.is_active = True
        self.screen_size = screen_size

    def velocity_x(self, direction: int):
        direction = sign(direction)

        self.velocity.x = direction * self.MOVEMENT_SPD_X

    def velocity_y(self, direction: int):
        direction = sign(direction)

        self.velocity.y = direction * self.MOVEMENT_SPD_Y

    def update(self, end_sequence=False):
        self.velocity_y(1)

        if end_sequence:
            if self.position.y - self.size.y // 2 > self.screen_size.y:
                self.is_active = False
            self.move_y(self.velocity.y)
            return

        if self.position.y - self.size.y // 2 > self.screen_size.y:
            self.position.x = randint(0, self.screen_size.x)
            self.position.y = -randint(self.size.y // 2, self.screen_size.y)
            self.is_active = True

        self.move_y(self.velocity.y)


class Meteor(Projectile):

    def __init__(self, position: Vec2, size: Vec2, screen_size: Vec2):
        super().__init__(position, size, screen_size)
        self.kind = randint(0, 1)
