import arcade
from random import random, randrange

SMALL_STARS_MIN = 300
SMALL_STARS_MAX = 500
SMALL_STAR_RADIUS_MIN = 1
SMALL_STAR_RADIUS_MAX = 3

LARGE_STARS_MIN = 5
LARGE_STARS_MAX = 10
LARGE_STAR_RADIUS_MIN = 4
LARGE_STAR_RADIUS_MAX = 10


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

        self.width = width
        self.height = height

        # Create the background color and append to the shape list.
        bg_points = [(0, height), (width, height), (width, 0), (0, 0)]
        bg_color_top = arcade.color.BLACK
        bg_color_bottom = arcade.color.MIDNIGHT_BLUE
        bg_colors = [bg_color_top, bg_color_top,
                     bg_color_bottom, bg_color_bottom]
        bg_rect = arcade.create_rectangle_filled_with_colors(bg_points,
                                                             bg_colors)
        self.append(bg_rect)

        # Generate a large number of small stars and a few big ones.
        self.generate_stars(SMALL_STARS_MIN, SMALL_STARS_MAX,
                            SMALL_STAR_RADIUS_MIN, SMALL_STAR_RADIUS_MAX)
        self.generate_stars(LARGE_STARS_MIN, LARGE_STARS_MAX,
                            LARGE_STAR_RADIUS_MIN, LARGE_STAR_RADIUS_MAX)

    def generate_stars(self, min, max, r_min, r_max):
        # Create each star and append to the list.
        number_of_stars = randrange(min, max, step=1)

        for _ in range(number_of_stars):
            x = random() * self.width
            y = random() * self.height
            radius = randrange(r_min, r_max, step=1)
            star = arcade.create_ellipse_filled_with_colors(
                x, y, radius, radius, (0, 0, 0, 0), arcade.color.WHITE)
            self.append(star)
