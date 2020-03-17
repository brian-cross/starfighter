# Generates an enemy ship at a random location off the screen. The enemy ship
# flies toward and shoots at the player ship. Randomly chooses an enemy ship
# sprite from the assets directory.
import arcade
from random import randint
import math
import os

import constants


class EnemyShipSprite(arcade.Sprite):
    def __init__(self, scale=1.0):
        # Grab the list of sprites from the directory.
        enemy_ship_list = os.listdir(constants.ENEMY_SPRITES_DIR)
        # Randomly pick a ship sprite from the list
        enemy_ship_filename = enemy_ship_list[randint(
            0, len(enemy_ship_list) - 1)]

        # Call the super constructor to create the sprite.
        super().__init__(
            f'{constants.ENEMY_SPRITES_DIR}/{enemy_ship_filename}', scale)

        # Target coordinate and speed.
        self.target_x = None
        self.target_y = None
        self.speed = 1

        # Define rectangular areas off the screen to spawn enemies.
        off_screen_areas = [
            {
                'x_min': -500,
                'x_max': -200,
                'y_min': 0,
                'y_max': constants.SCREEN_HEIGHT
            },
            {
                'x_min': constants.SCREEN_WIDTH + 200,
                'x_max': constants.SCREEN_WIDTH + 500,
                'y_min': 0,
                'y_max': constants.SCREEN_HEIGHT
            },
            {
                'x_min': 0,
                'x_max': constants.SCREEN_WIDTH,
                'y_min': -500,
                'y_max': -200
            },
            {
                'x_min': 0,
                'x_max': constants.SCREEN_WIDTH,
                'y_min': constants.SCREEN_HEIGHT + 200,
                'y_max': constants.SCREEN_HEIGHT + 500
            }
        ]

        # Pick an area.
        off_screen_area = off_screen_areas[randint(0, 3)]

        # Generate a random coordinate in the area picked.
        self.center_x = randint(
            off_screen_area['x_min'], off_screen_area['x_max'])
        self.center_y = randint(
            off_screen_area['y_min'], off_screen_area['y_max'])

    def update(self):
        super().update()

        # Aim the enemy ship at the target.
        dx = self.center_x - self.target_x
        dy = self.center_y - self.target_y

        self.angle = math.degrees(math.atan2(dy, dx)) - 90

        # Calculate the x and y speeds based on the ship speed and angle.
        self.change_y = math.sin(math.radians(self.angle - 90)) * self.speed
        self.change_x = math.cos(math.radians(self.angle - 90)) * self.speed
