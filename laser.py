import arcade
import math

import constants
from vector_sprite import VectorSprite


class Laser(VectorSprite):
    def __init__(self, filename, position, speed, angle, scale=1.0):
        super().__init__(filename, scale)

        self.position = position
        self.speed = speed
        self.angle = angle

    def update(self):
        super().update()

        # If the laser goes off screen then remove it.
        if (self.bottom > constants.SCREEN_HEIGHT or self.top < 0 or
                self.left > constants.SCREEN_WIDTH or self.left < 0):
            self.remove_from_sprite_lists()
