import random

from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor


class Projectile(Actor):
    def __init__(self, position: Vec2, size: Vec2, screen_size: Vec2, move_speed: Vec2):
        super().__init__(position, size)
        self.move_speed = move_speed
        self.velocity = Vec2(0, 0)
        self.is_active = True
        self.screen_size = screen_size

    def velocity_x(self, direction: int):
        direction = sign(direction)

        self.velocity.x = direction * self.move_speed.x

    def velocity_y(self, direction: int):
        direction = sign(direction)

        self.velocity.y = direction * self.move_speed.y

    def update(self):
        self.move_x(self.velocity.x)
        self.move_y(self.velocity.y)


class Meteor(Projectile):

    def __init__(self, position: Vec2, size: Vec2, screen_size: Vec2, move_speed: Vec2):
        super().__init__(position, size, screen_size, move_speed)
        self.kind = random.randint(0, 1)
        self.move_speed = move_speed

    def update(self, end_sequence=False):
        self.velocity_y(1)

        if end_sequence:
            if self.position.y - self.size.y // 2 > self.screen_size.y:
                self.is_active = False
            self.move_y(self.velocity.y)
            return

        if self.position.y - self.size.y // 2 > self.screen_size.y:
            self.position.x = random.randint(0, self.screen_size.x)
            self.position.y = -random.randint(self.size.y // 2, self.screen_size.y // 2)
            self.move_speed.y = random.uniform(0.5, 1)
            self.is_active = True

        self.move_y(self.velocity.y)
