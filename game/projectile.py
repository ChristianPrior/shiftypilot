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

    def update(self):
        self.move_y(1)

        if self.position.y > self.screen_size.y:
            self.position.x = randint(0, self.screen_size.x)
            self.move_y(-self.screen_size.y)
            self.is_active = True
