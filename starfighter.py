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
        self.player_ship_sprite_list = arcade.SpriteList()
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
        self.create_ship('player')

        # Create an enemy ship.
        self.create_ship('enemy')

    def on_draw(self):
        # Draws everything to the screen.
        arcade.start_render()

        self.background.draw()
        self.laser_sprite_list.draw()
        self.enemy_ships_sprite_list.draw()
        self.player_ship_sprite_list.draw()
        self.explosion_sprite_list.draw()

    def on_update(self, delta_time):
        # If a laser hits an enemy ship trigger a small explosion and spawn a
        # new enemy.
        position = self.check_for_list_collisions(
            self.laser_sprite_list, self.enemy_ships_sprite_list)
        if (position != None):
            self.make_explosion(position, scaling=constants.SPRITE_SCALING)
            self.create_ship('enemy')

        # If the player ship collides with an enemy ship trigger a big explosion
        # and spawn a new player and enemy.
        position = self.check_for_list_collisions(
            self.player_ship_sprite_list, self.enemy_ships_sprite_list)
        if (position != None):
            self.make_explosion(position)
            self.create_ship('player')
            self.create_ship('enemy')

        # Update the enemy ships with the player ship's current position.
        for enemy_ship in self.enemy_ships_sprite_list:
            enemy_ship.target_x = self.player_ship.center_x
            enemy_ship.target_y = self.player_ship.center_y

        # Update everything on each frame.
        self.laser_sprite_list.update()
        self.enemy_ships_sprite_list.update()
        self.player_ship_sprite_list.update()
        self.explosion_sprite_list.update()

    def on_key_press(self, key, modifiers):
        # Ignore keyboard input if the player ship is spawning.
        if(self.player_ship.spawning == False):
            if (key == arcade.key.W):
                self.player_ship.thrust = constants.PLAYER_SHIP_THRUST
            elif (key == arcade.key.S):
                self.player_ship.thrust = -constants.PLAYER_SHIP_THRUST
            elif (key == arcade.key.A):
                # Persist the state of the left turning key
                self.is_left_pressed = True
                self.player_ship.change_angle = 3
            elif (key == arcade.key.D):
                # Persist the state of the right turning key
                self.is_right_pressed = True
                self.player_ship.change_angle = -3
            elif (key == arcade.key.ENTER):
                self.fire_weapon(self.player_ship)

    def on_key_release(self, key, modifiers):
        # Handles the key release event.
        # If the left or right turn keys have been released, check if the other
        # turning key is still pressed. If so, turn the ship in the other
        # direction. Otherwise stop turning.
        if (key == arcade.key.A):
            self.is_left_pressed = False
            if (self.is_right_pressed):
                self.player_ship.change_angle = -3
            else:
                self.player_ship.change_angle = 0
        elif (key == arcade.key.D):
            self.is_right_pressed = False
            if (self.is_left_pressed):
                self.player_ship.change_angle = 3
            else:
                self.player_ship.change_angle = 0
        # Kill the ship's thrust if the forward or backward keys are released.
        elif (key == arcade.key.W or key == arcade.key.S):
            self.player_ship.thrust = 0
            self.player_ship.drag = constants.PLAYER_SHIP_DRAG

    def fire_weapon(self, ship):
        # Break the laws of physics by adding the speed of the ship to the
        # speed of the laser. (Looks better than having a constant laser speed)
        laser_speed = ship.speed + constants.LASER_SPEED

        # Adjust the laser position a little toward the front of the ship.
        x = ship.center_x + math.cos(math.radians(ship.angle)) * 20
        y = ship.center_y + math.sin(math.radians(ship.angle)) * 20

        # Create the laser object.
        laser = Laser(constants.ENEMY_LASER_FILENAME,
                      (x, y),
                      laser_speed,
                      ship.angle)

        self.laser_sprite_list.append(laser)

    def check_for_list_collisions(self, list_1, list_2):
        # If a sprite in the first list collides with a sprite in the second
        # list, remove both sprites from their respective lists. Return the
        # position of the sprite in the second list or None if there was no
        # collision.
        position = None

        for sprite in list_1:
            hit_list = sprite.collides_with_list(list_2)
            if (len(hit_list) > 0):
                position = hit_list[0].position
                sprite.remove_from_sprite_lists()
                for hit in hit_list:
                    hit.remove_from_sprite_lists()

        return position

    def make_explosion(self, position, scaling=1):
        # Create an explosion at the specified x y position.
        explosion = Explosion(position, scaling)
        self.explosion_sprite_list.append(explosion)

    def create_ship(self, ship_type=''):
        if (ship_type == ''):
            return

        if (ship_type == 'player'):
            self.player_ship = PlayerShipSprite(
                constants.PLAYER_SHIP_FILENAME, constants.PLAYER_SHIP_SCALING)
            self.player_ship_sprite_list.append(self.player_ship)
        elif (ship_type == 'enemy'):
            self.enemy_ship = EnemyShipSprite(
                scale=constants.ENEMY_SHIP_SCALING)
            self.enemy_ships_sprite_list.append(self.enemy_ship)


if __name__ == "__main__":
    window = App(constants.SCREEN_WIDTH,
                 constants.SCREEN_HEIGHT, 'StarFighter')
    window.setup()
    arcade.run()
