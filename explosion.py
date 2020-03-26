# Based on https://arcade.academy/examples/sprite_explosion.html#sprite-explosion

import arcade

import constants


class Explosion(arcade.Sprite):
    # A list to hold the animation frames.
    texture_list = []

    def __init__(self, position, scale=1):
        super().__init__(scale=scale)

        # Set the explosion location.
        self.position = position

        # Initialize the current texture to the first animation frame.
        self.current_texture = 0
        self.textures = Explosion.texture_list

    def update(self):
        # Run through each frame and then remove the sprite when done.
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
            self.current_texture += 1
        else:
            self.remove_from_sprite_lists()

    @classmethod
    def load_spritesheet(cls):
        cls.texture_list = arcade.load_spritesheet(constants.EXPLOSION_FILENAME,
                                                   constants.EXPLOSION_SPRITESHEET_WIDTH, constants.EXPLOSION_SPRITESHEET_HEIGHT,
                                                   constants.EXPLOSION_SPRITESHEET_COLUMNS, constants.EXPLOSION_SPRITESHEET_COUNT)
