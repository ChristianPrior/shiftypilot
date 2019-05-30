from game.vector import Vec2
from game.physics.actor import Actor


class Player(Actor):
    WALK_SPEED = 1

    def __init__(self, position: Vec2, size: Vec2):
        super().__init__(position, size)
        self.velocity = Vec2(0, 0)

    def walk(self, direction: int):
        self.velocity.x = direction * self.WALK_SPEED


    def update(self):
        self.move_x(self.velocity.x)
        self.move_y(self.velocity.y)
