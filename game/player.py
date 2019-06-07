import pyxel

from game.gmath import sign
from game.vector import Vec2
from game.physics.actor import Actor
from game.animation import TeleportOut, TeleportIn, Invincibility


class Player(Actor):
    INITIAL_MOVEMENT_SPD = 3
    MOVEMENT_SPD_X = INITIAL_MOVEMENT_SPD
    MOVEMENT_SPD_Y = INITIAL_MOVEMENT_SPD

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
    MAX_DISTANCE = Vec2(60, 60)

    def __init__(self, position: Vec2, size: Vec2, player: Player, app):
        super().__init__(position, size)
        self.app = app
        self.is_dead = False
        self.velocity = Vec2(0, 0)
        self.player = player
        self.initial_distance = self.player.position - self.position
        self.teleport_out_animation = TeleportOut(app=self.app)
        self.teleport_in_animation = TeleportIn(app=self.app)
        self.invincibilty_animation = Invincibility(app=self.app, entity=self)
        self.invincible_frames = 0

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
            pyxel.play(0, 2)
            self.app.cam_punch = 10
            self.teleport_out_animation = TeleportOut(app=self.app, start_pos_x=x, start_pos_y=y, entity=self)
            self.teleport_out_animation.start()

    def animate_teleport(self):
        if self.teleport_out_animation and self.teleport_out_animation.is_active:
            self.teleport_out_animation.animate()

            if self.teleport_out_animation.current_phase == self.teleport_out_animation.end_phase:
                start_x = self.position.x
                start_y = self.position.y
                dx = self.player.position.x - self.position.x
                dy = self.player.position.y - self.position.y

                x = self.player.position.x
                y = self.player.position.y
                self.position.x = x
                self.position.y = y

                for t in range(0, 10):
                    t /= 10
                    self.app.add_particle(start_x + dx * t, start_y + dy * t)

                self.teleport_in_animation = TeleportIn(app=self.app, start_pos_x=x, start_pos_y=y, entity=self)
                self.teleport_in_animation.start()

        if self.teleport_in_animation and self.teleport_in_animation.is_active:
            self.teleport_in_animation.animate()

    def animate_invincibility(self):
        if self.invincibilty_animation and self.invincibilty_animation.is_active:
            self.invincibilty_animation.animate()

    def collision(self, projectiles):
        if self.invincible_frames:
            self.invincible_frames -= 1
            return False

        for projectile in projectiles:
            gap = self.position - projectile.position
            if (abs(gap.x) < self.size.x // 2 + projectile.size.x // 2
                    and abs(gap.y) < self.size.y // 2 + projectile.size.y // 2):
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
