# Based on code from https://arcade.academy/examples/asteroid_smasher.html#asteroid-smasher

import arcade
import math

import constants


class PlayerShipSprite(arcade.Sprite):
    def __init__(self, filename, scale=1.0):
        super().__init__(filename, scale)

        self.center_x = constants.SCREEN_WIDTH / 2
        self.center_y = constants.SCREEN_HEIGHT / 2
        self.angle = 90

        self.thrust = 0
        self.drag = 0
        self.speed = 0
        self.max_speed = 7

    def update(self):
        super().update()
        # Update the ship speed each frame
        self.speed += self.thrust
        if self.speed >= self.max_speed:
            self.speed = self.max_speed
        if self.speed <= -self.max_speed:
            self.speed = -self.max_speed

        # Reduce the speed by the drag factor each frame
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0
        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        # Calculate the x and y speeds based on the ship speed and angle
        self.change_y = math.sin(math.radians(self.angle)) * self.speed
        self.change_x = math.cos(math.radians(self.angle)) * self.speed

        # If the ship goes off screen, move it to the opposite side
        if self.right < 0:
            self.left = constants.SCREEN_WIDTH
        if self.left > constants.SCREEN_WIDTH:
            self.right = 0
        if self.top < 0:
            self.bottom = constants.SCREEN_HEIGHT
        if self.bottom > constants.SCREEN_HEIGHT:
            self.top = 0
