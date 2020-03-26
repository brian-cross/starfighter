import arcade
import math

import constants


class VectorSprite(arcade.Sprite):
    """
    Base class for flying sprites such as ships and lasers.

    Calculates the x and y position rates of change based on the sprite's
    velocity vector - self.speed and self.angle.

    Parent class: arcade.Sprite

    Parameters:
    filename: Path to the image to use for the sprite.
    scale: Scaling factor. Defaults to 1.
    """

    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.speed = 0

    def update(self):
        super().update()

        # Calculate the x and y speeds based on the sprite's speed and angle.
        self.change_y = math.sin(math.radians(self.angle)) * self.speed
        self.change_x = math.cos(math.radians(self.angle)) * self.speed
