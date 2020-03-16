# Code borrowed from https://arcade.academy/examples/asteroid_smasher.html#asteroid-smasher

import arcade
import math


class TurningSprite(arcade.Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """

    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
