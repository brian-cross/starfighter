# Generates an enemy ship at a random location off the screen. The enemy ship
# flies toward and shoots at the player ship. Randomly chooses an enemy ship
# sprite from the assets directory.
import arcade
from random import randint
import os

import constants


class EnemyShipSprite(arcade.Sprite):
    def __init__(self, scale=1.0):
        # Grab the list of sprites from the directory.
        enemy_ship_list = os.listdir(constants.ENEMY_SPRITES_DIR)
        # Randomly pick a ship sprite from the list
        enemy_ship_filename = enemy_ship_list[randint(
            0, len(enemy_ship_list) - 1)]

        super().__init__(
            f'{constants.ENEMY_SPRITES_DIR}/{enemy_ship_filename}', scale)

        self.center_x = 100
        self.center_y = 100
