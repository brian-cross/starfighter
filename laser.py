import arcade
import math

import constants


class Laser(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, speed, angle, scale=1.0):
        super().__init__(filename, scale)

        self.center_x = center_x
        self.center_y = center_y
        self.speed = speed
        self.angle = angle

    def update(self):
        super().update()
        self.change_y = math.sin(math.radians(self.angle + 90)) * self.speed
        self.change_x = math.cos(math.radians(self.angle + 90)) * self.speed
