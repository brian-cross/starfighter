# Source: https://arcade.academy/examples/sprite_explosion.html#sprite-explosion

import arcade


class Explosion(arcade.Sprite):
    def __init__(self, texture_list, scale=1.0):
        super().__init__(scale=scale)

    # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()
