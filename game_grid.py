import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid
import numpy as np  # fundamental Python module for scientific computing
import copy as cp


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # set the color used for the empty grid cells
        # self.empty_cell_color = Color(203, 194, 179)
        self.empty_cell_color = Color(213, 204, 199)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(187, 173, 160)
        self.boundary_color = Color(187, 173, 160)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.006
        self.box_thickness = 2 * self.line_thickness
        self.ghost_tetromino = None

    # Method used for displaying the game grid
    def display(self, SCORE):
        # clear the background canvas to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # Draw the ghost guide
        if self.ghost_tetromino is not None:
            self.ghost_tetromino.draw(True)
        # draw the current (active) tetromino
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms

        self.score(SCORE)

        stddraw.show(16.7)

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # draw each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw()
                    # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # return False if the cell is out of the grid
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method for updating the game grid by placing the given tiles of a stopped
    # tetromino and checking if the game is over due to having tiles above the
    # topmost game grid row. The method returns True when the game is over and
    # False otherwise.
    def update_grid(self, tiles_to_place):
        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each occupied tile onto the game grid
                if tiles_to_place[row][col] is not None:
                    pos = tiles_to_place[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
                    # the game is over if any placed tile is out of the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

    # Looks at the grid and clears full lines, then updates the places of upper tiles.
    def clear(self, row, col):
        number_of_pushes = 0
        has_clearing_started = False  # If there is a full line this frame, then the clearing process is started.
        tile_matrix_before_clear = cp.deepcopy(self.tile_matrix)
        rows_to_clear = []
        # Going through the rows from bottom to top.
        for y in range(col):
            is_full = False
            tile_counter = 0
            # Count the number of tiles in the line
            for x in range(row):  # Going through each tile from left to right
                if self.tile_matrix[y][x] is not None:
                    tile_counter += 1
            # If it is equal to row count then the line is full
            if tile_counter == row:
                is_full = True
                has_clearing_started = True
            if has_clearing_started:
                if is_full:
                    number_of_pushes += 1
                    rows_to_clear.append(y)
                    for x in range(row):  # Going through each tile from left to right
                        self.tile_matrix[y][x] = None
                else:
                    for x in range(row):  # Going through each tile from left to right
                        # Updating both the positions and the tile arrays
                        if self.tile_matrix[y][x] is not None:
                            self.tile_matrix[y][x].position.y -= number_of_pushes
                            self.tile_matrix[y - number_of_pushes][x] = self.tile_matrix[y][x]
                            self.tile_matrix[y][x] = None
        if number_of_pushes > 0:
            self.clear_effect(tile_matrix_before_clear, rows_to_clear)
        # Return the number of pushes, which is equal to the number of lines cleared at the end of the process
        return number_of_pushes

    def clear_2048(self, row, col):
        for y in range(col):
            for x in range(row):
                if self.tile_matrix[y][x] != None and self.tile_matrix[y + 1][x] != None:
                    if self.tile_matrix[y][x].get_number() == self.tile_matrix[y + 1][x].get_number():
                        self.tile_matrix[y + 1][x] = None
                        self.tile_matrix[y][x].set_number(self.tile_matrix[y][x].get_number() * 2)
                        for i in range(y + 2, col - 1):
                            if self.tile_matrix[i][x] != None:
                                self.tile_matrix[i][x].move(0, -1)
                                self.tile_matrix[i - 1][x] = self.tile_matrix[i][x]
                                self.tile_matrix[i][x] = None
                        self.clear_2048(row, col)
                        return

    # If there is a tile that doesn't have any 4-connected neighbours, delete the tile
    def delete_alone(self, row, col):
        for y in range(col):
            for x in range(row):
                if self.tile_matrix[y][x] != None:
                    if y > 0:  # if the tile doesn't touch the bottommost place
                        if x == 11:  # if the tile is at the righmost place, don't look for the right neighbour
                            if self.tile_matrix[y + 1][x] == None and self.tile_matrix[y - 1][x] == None and \
                                    self.tile_matrix[y][x - 1] == None:
                                self.tile_matrix[y][x] = None
                        elif x == 0:  # if the tile is at the leftmost place, don't look dot the left neighnour
                            if self.tile_matrix[y + 1][x] == None and self.tile_matrix[y - 1][x] == None and \
                                    self.tile_matrix[y][x + 1] == None:
                                self.tile_matrix[y][x] = None
                        # bence bu commentli kısım lazım değil ama bir bug çıkarsa uncomment yapıp deneriz
                        # elif y == 19:
                        #     if self.tile_matrix[y-1][x] == None and self.tile_matrix[y][x+1] == None and self.tile_matrix[y][x-1] == None:
                        #         self.tile_matrix[y][x] = None
                        # elif y == 0:
                        #     if self.tile_matrix[y + 1][x] == None and self.tile_matrix[y][x + 1] == None and self.tile_matrix[y][x - 1] == None:
                        #         self.tile_matrix[y][x] = None
                        else:  # if the tile is not at the rightmost or leftmost place, look for, up, down, lef and right neighbours
                            if self.tile_matrix[y + 1][x] == None and self.tile_matrix[y - 1][x] == None and \
                                    self.tile_matrix[y][x + 1] == None and self.tile_matrix[y][x - 1] == None:
                                self.tile_matrix[y][x] = None

    def clear_everything(self, row, col):
        for y in range(col):
            for x in range(row):
                self.tile_matrix[y][x] = None

    def score(self, SCORE):
        text_color = Color(0, 0, 0)
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.setPenColor(text_color)
        text_to_display = "Score: " + str(SCORE)
        stddraw.text(1.2, self.grid_height + 0.5, text_to_display)

    def clear_effect(self, tile_matrix_before_clear, rows_to_clear):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if tile_matrix_before_clear[y][x] is not None:
                    tile_matrix_before_clear[y][x].draw()
                    if y in rows_to_clear:
                        tile_matrix_before_clear[y][x].draw(is_cleared=True)
        stddraw.show(250)
