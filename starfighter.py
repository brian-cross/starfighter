import arcade
import random
import math

import constants
from starfield import Starfield
from player_ship_sprite import PlayerShipSprite
from enemy_ship_sprite import EnemyShipSprite
from laser import Laser
from explosion import Explosion


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
        self.laser_sprite_list = arcade.SpriteList()
        self.explosion_sprite_list = arcade.SpriteList()

        # Load the explosion spritesheet here to prevent a delay in the
        # explosion animation.
        Explosion.load_spritesheet()

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
        # Draws everything to the screen.
        arcade.start_render()

        self.background.draw()
        self.all_sprites_list.draw()
        self.explosion_sprite_list.draw()

    def on_update(self, delta_time):
        # Update the enemy ships with the player ship's current location.
        for enemy_ship in self.enemy_ships_sprite_list:
            enemy_ship.target_x = self.player_ship.center_x
            enemy_ship.target_y = self.player_ship.center_y

        # Check if any sprites have collided
        self.check_for_list_collisions(
            self.enemy_ships_sprite_list, self.laser_sprite_list)
        self.check_for_sprite_collision_with_list(
            self.player_ship, self.enemy_ships_sprite_list)

        # Update everything on each frame.
        self.all_sprites_list.update()
        self.explosion_sprite_list.update()

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
        elif (key == arcade.key.ENTER):
            self.fire_weapon()

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

    def fire_weapon(self):
        # Break the laws of physics by adding the speed of the ship to the
        # speed of the laser. (Looks better than having a constant laser speed)
        laser_speed = self.player_ship.speed + constants.PLAYER_LASER_SPEED
        laser = Laser(constants.ENEMY_LASER_FILENAME,
                      self.player_ship.center_x,
                      self.player_ship.center_y,
                      laser_speed,
                      self.player_ship.angle)

        # Insert the sprite at the start of the list so it's drawn under the
        # ships.
        self.all_sprites_list.insert(0, laser)
        self.laser_sprite_list.append(laser)

    def check_for_list_collisions(self, list_1, list_2):
        # If a sprite in the first list collides with a sprite in the second
        # list, trigger an explosion and remove both sprites from their
        # respective lists.
        for sprite in list_1:
            hit_list = sprite.collides_with_list(list_2)
            if (len(hit_list) > 0):
                self.make_explosion(hit_list[0], constants.SPRITE_SCALING)
                sprite.remove_from_sprite_lists()
                for hit in hit_list:
                    hit.remove_from_sprite_lists()

    def check_for_sprite_collision_with_list(self, sprite, list):
        hit_list = sprite.collides_with_list(list)
        if (len(hit_list) > 0):
            self.make_explosion(hit_list[0])
            sprite.remove_from_sprite_lists()
            for hit in hit_list:
                hit.remove_from_sprite_lists()

    def make_explosion(self, sprite, scaling=1.0):
        # Create an explosion at the location of the specified sprite.
        explosion = Explosion(
            sprite.center_x, sprite.center_y, scaling)
        self.explosion_sprite_list.append(explosion)


if __name__ == "__main__":
    window = App(constants.SCREEN_WIDTH,
                 constants.SCREEN_HEIGHT, 'StarFighter')
    window.setup()
    arcade.run()
