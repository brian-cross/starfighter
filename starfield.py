import arcade
from random import random, randrange

STARS_MIN = 100
STARS_MAX = 125
STAR_RADIUS_MIN = 2
STAR_RADIUS_MAX = 6


class Starfield(arcade.ShapeElementList):
    """
    Creates a star field of randomly placed and sized stars.

    Parent class: arcade.ShapeElementList

    Parameters:
    width: The width of the star field in pixels, should be the window width
    height: The height of the star field in pixels, should be the window height
    """

    def __init__(self, width, height):
        super().__init__()

        # Create the background color and append to the shape list.
        bg_points = [(0, height), (width, height), (width, 0), (0, 0)]
        bg_color_top = arcade.color.BLACK
        bg_color_bottom = arcade.color.MIDNIGHT_BLUE
        bg_colors = [bg_color_top, bg_color_top,
                     bg_color_bottom, bg_color_bottom]
        bg_rect = arcade.create_rectangle_filled_with_colors(bg_points,
                                                             bg_colors)
        self.append(bg_rect)

        # Create each star and append to the list.
        number_of_stars = randrange(STARS_MIN, STARS_MAX, step=1)

        for _ in range(number_of_stars):
            x = random() * width
            y = random() * height
            radius = randrange(STAR_RADIUS_MIN, STAR_RADIUS_MAX, step=1)
            star = arcade.create_ellipse_filled_with_colors(
                x, y, radius, radius, (0, 0, 0, 0), arcade.color.WHITE)
            self.append(star)
