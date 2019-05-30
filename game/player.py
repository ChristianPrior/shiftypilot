from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor


class Player(Actor):
    INITIAL_MOVEMENT_SPD = 1.5
    MOVEMENT_SPD_X = 1.5
    MOVEMENT_SPD_Y = 1.5

    def __init__(self, position: Vec2, size: Vec2):
        super().__init__(position, size)
        self.velocity = Vec2(0, 0)

    def velocity_x(self, direction: int):
        direction = sign(direction)

        self.velocity.x = direction * self.MOVEMENT_SPD_X

    def velocity_y(self, direction: int):
        direction = sign(direction)

        self.velocity.y = direction * self.MOVEMENT_SPD_Y

    def update(self):
        self.move_x(self.velocity.x)
        self.move_y(self.velocity.y)


class PlayerBody(Actor):
    MOVEMENT_SPD = 0.5
    MAX_DISTANCE = Vec2(40, 40)

    def __init__(self, position: Vec2, size: Vec2, player: Player):
        super().__init__(position, size)
        self.velocity = Vec2(0, 0)
        self.player = player
        self.initial_distance = self.player.position - self.position

    def velocity_x(self, direction: int):
        direction = sign(direction)

        self.velocity.x = direction * self.MOVEMENT_SPD

    def velocity_y(self, direction: int):
        direction = sign(direction)

        self.velocity.y = direction * self.MOVEMENT_SPD

    def calc_distance(self):
        return self.player.position - self.position

    def teleport(self, activated: bool):
        x = self.player.position.x
        y = self.player.position.y

        if activated:
            print(activated)
            self.position.x = x
            self.position.y = y

    def update(self):
        distance = self.calc_distance()
        self.velocity.x = 0
        self.velocity.y = 0
        self.player.MOVEMENT_SPD_X = self.player.MOVEMENT_SPD_Y = self.player.INITIAL_MOVEMENT_SPD

        if distance.x > self.MAX_DISTANCE.x or distance.x < -self.MAX_DISTANCE.x:
            self.player.MOVEMENT_SPD_X = self.MOVEMENT_SPD
            self.velocity_x(distance.x)

        if distance.y > self.MAX_DISTANCE.y or distance.y < -self.MAX_DISTANCE.y:
            self.player.MOVEMENT_SPD_Y = self.MOVEMENT_SPD
            self.velocity_y(distance.y)

        self.move_x(self.velocity.x)
        self.move_y(self.velocity.y)
