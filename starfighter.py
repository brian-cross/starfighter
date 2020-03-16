import arcade
import random
import math

import constants
from starfield import Starfield
from player_ship_sprite import PlayerShipSprite
from enemy_ship_sprite import EnemyShipSprite


class App(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Screen dimensions.
        self.width = width
        self.height = height

        # Must keep track of the left or right keys being pressed in case the
        # user overlaps the two key presses. Otherwise the left / right turning
        # behaviour isn't intutive.
        self.is_left_pressed = False
        self.is_right_pressed = False

        # Setup sprite lists.
        self.all_sprites_list = arcade.SpriteList()
        self.enemy_ships_sprite_list = arcade.SpriteList()

    def setup(self):
        # Create the background and star field.
        self.background = Starfield(self.width, self.height)

        # Create the player ship.
        self.player_ship = PlayerShipSprite(
            constants.PLAYER_SHIP_FILENAME, constants.PLAYER_SHIP_SCALING)

        # Create an enemy ship.
        self.enemy_ship = EnemyShipSprite(scale=constants.ENEMY_SHIP_SCALING)
        self.enemy_ships_sprite_list.append(self.enemy_ship)

        # Add the sprites to the list to be drawn in a bottom to top order.
        self.all_sprites_list.append(self.enemy_ship)
        self.all_sprites_list.append(self.player_ship)

    def on_draw(self):
        arcade.start_render()

        # Draw everything.
        self.background.draw()
        self.all_sprites_list.draw()

    def on_update(self, delta_time):
        # Update everything on each frame.
        self.all_sprites_list.update()

    def on_key_press(self, key, modifiers):
        # Handle keyboard presses.
        if (key == arcade.key.W or key == arcade.key.UP):
            self.player_ship.thrust = constants.PLAYER_SHIP_THRUST
        elif (key == arcade.key.S or key == arcade.key.DOWN):
            self.player_ship.thrust = -constants.PLAYER_SHIP_THRUST
        elif (key == arcade.key.A or key == arcade.key.LEFT):
            # Persist the state of the left turning key
            self.is_left_pressed = True
            self.player_ship.change_angle = 3
        elif (key == arcade.key.D or key == arcade.key.RIGHT):
            # Persist the state of the right turning key
            self.is_right_pressed = True
            self.player_ship.change_angle = -3

    def on_key_release(self, key, modifiers):
        # Handles the key release event.
        # If the left or right turn keys have been released, check if the other
        # turning key is still pressed. If so, turn the ship in the other
        # direction. Otherwise stop turning.
        if (key == arcade.key.A or key == arcade.key.LEFT):
            self.is_left_pressed = False
            if (self.is_right_pressed):
                self.player_ship.change_angle = -3
            else:
                self.player_ship.change_angle = 0
        elif (key == arcade.key.D or key == arcade.key.RIGHT):
            self.is_right_pressed = False
            if (self.is_left_pressed):
                self.player_ship.change_angle = 3
            else:
                self.player_ship.change_angle = 0
        # Kill the ship's thrust if the forward or backward keys are released.
        elif (key == arcade.key.W or key == arcade.key.UP or key == arcade.key.S or key == arcade.key.DOWN):
            self.player_ship.thrust = 0
            self.player_ship.drag = constants.PLAYER_SHIP_DRAG


if __name__ == "__main__":
    window = App(constants.SCREEN_WIDTH,
                 constants.SCREEN_HEIGHT, 'StarFighter')
    window.setup()
    arcade.run()
