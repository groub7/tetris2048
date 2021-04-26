import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the tile and the number on it
from point import Point  # used for representing the position of the tile
import copy as cp  # the copy module is used for copying tile positions
import math  # math module that provides mathematical functions


# Class used for representing numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # value used for the thickness of the boxes (boundaries) around the tiles
    boundary_thickness = 0.004  # 0.004 to default
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    colors = [
        Color(238, 230, 219),   # 2
        Color(236, 224, 200),   # 4
        Color(239, 178, 124),   # 8
        Color(243, 151, 104),   # 16
        Color(243, 125, 99),    # 32
        Color(244, 96, 66),     # 64
        Color(235, 206, 115),   # 128
        Color(237, 203, 103),   # 256
        Color(236, 200, 90),    # 512
        Color(231, 194, 87),    # 1024
        Color(232, 190, 78),    # 2048
        Color(0, 0, 0),         # 4096
        Color(0, 0, 0),         # 8192
        Color(0, 0, 0),
        Color(0, 0, 0),
        Color(0, 0, 0),
        Color(0, 0, 0),
        Color(0, 0, 0)
    ]

    # Constructor that creates a tile at a given position with 2 as its number
    def __init__(self, position=Point(0, 0)):  # (0, 0) is the default position
        # assign the number on the tile
        self.number = 2
        # set the colors of the tile
        self.background_color = Color(151, 178, 199)  # background (tile) color
        self.foreground_color = Color(0, 100, 200)  # foreground (number) color
        self.boundary_color = Color(187, 173, 160)  # boundary (box) color
        # set the position of the tile as the given position
        self.position = Point(position.x, position.y)

    # Setter method for the position of the tile
    def set_position(self, position):
        # set the position of the tile as the given position
        self.position = cp.deepcopy(position)

        # Getter method for the position of the tile

    def get_position(self):
        # return the position of the tile
        return cp.deepcopy(self.position)

        # Method for moving the tile by dx along the x axis and by dy along the y axis

    def move(self, dx, dy):
        self.position.translate(dx, dy)

    def set_number(self, num):
        self.number = num

    def get_number(self):
        return self.number

    # Method for drawing the tile
    def draw(self, is_transparent=False, is_cleared=False):
        if is_transparent:
            self.boundary_color = Color(0, 0, 0)  # boundary (box) color
            stddraw.setPenColor(self.boundary_color)
            stddraw.setPenRadius(Tile.boundary_thickness)
            stddraw.square(self.position.x, self.position.y, 0.5)  # 0.5 to default
            stddraw.setPenRadius()  # reset the pen radius to its default value
            return
        if is_cleared:
            self.boundary_color = Color(255, 255, 255)  # clear color
            stddraw.setPenColor(self.boundary_color)
            stddraw.setPenRadius(Tile.boundary_thickness)
            stddraw.filledSquare(self.position.x, self.position.y, 0.525)  # 0.5 to default
            stddraw.setPenRadius()  # reset the pen radius to its default value
            return
        # draw the tile as a filled square
        stddraw.setPenColor(self.colors[int(math.log2(self.get_number() - 1))])
        stddraw.filledSquare(self.position.x, self.position.y, 0.5)  # 0.5 to default
        # draw the bounding box of the tile as a square
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(self.position.x, self.position.y, 0.5)  # 0.5 to default
        stddraw.setPenRadius()
        # draw the number on the tile
        stddraw.setPenColor(Color(255, 255, 255))
        if self.get_number() <= 4:
            stddraw.setPenColor(Color(119, 112, 101))
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.boldText(self.position.x, self.position.y, str(self.get_number()))
