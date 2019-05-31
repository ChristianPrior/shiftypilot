from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor
from game.animation import TeleportOut, TeleportIn


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
        self.is_dead = False
        self.velocity = Vec2(0, 0)
        self.player = player
        self.initial_distance = self.player.position - self.position
        self.teleport_out_animation = TeleportOut()
        self.teleport_in_animation = TeleportIn()

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
            self.teleport_out_animation = TeleportOut(start_pos_x=x, start_pos_y=y, entity=self)
            self.teleport_out_animation.start()

    def animate_teleport(self):
        if self.teleport_out_animation and self.teleport_out_animation.is_active:
            self.teleport_out_animation.animate()

            if self.teleport_out_animation.current_phase == self.teleport_out_animation.end_phase:
                x = self.player.position.x
                y = self.player.position.y
                self.position.x = x
                self.position.y = y

                self.teleport_in_animation = TeleportIn(start_pos_x=x, start_pos_y=y, entity=self)
                self.teleport_in_animation.start()

        if self.teleport_in_animation and self.teleport_in_animation.is_active:
            self.teleport_in_animation.animate()

    def collision(self, projectiles):
        for projectile in projectiles:
            if (abs(self.position.x - projectile.position.x) < self.size.x
                    and abs(self.position.y - projectile.position.y) < self.size.y):
                return True

        return False

    def update(self, projectiles):
        if self.collision(projectiles):
            self.is_dead = True

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
