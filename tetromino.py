import random  # each tetromino is created with a random x value above the grid
from tile import Tile  # used for representing each tile on the tetromino
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for representing tetrominoes with 3 out of 7 different types/shapes
# as (I, O and Z)
# sa
class Tetromino:
    # Constructor to create a tetromino with a given type (shape)
    def __init__(self, type, grid_height, grid_width):
        # set grid_height and grid_width from input parameters
        self.grid_height = grid_height
        self.grid_width = grid_width
        # set the shape of the tetromino based on the given type
        occupied_tiles = []
        if type == 'I':
            n = 4  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial orientation
            occupied_tiles.append((1, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((1, 3))
        elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial orientation
            occupied_tiles.append((0, 0))
            occupied_tiles.append((1, 0))
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
        elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 0))
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
        elif type == 'S':
            n = 3
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 0))
            occupied_tiles.append((2, 0))
        elif type == 'L':
            n = 3
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((2, 2))
        elif type == 'J':
            n = 3
            occupied_tiles.append((0, 2))
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
        elif type == 'T':
            n = 3
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
            occupied_tiles.append((1, 2))
        # create a matrix of numbered tiles based on the shape of the tetromino
        self.tile_matrix = np.full((n, n), None)
        # initial position of the bottom-left tile in the tile matrix just before
        # the tetromino enters the game grid
        self.bottom_left_corner = Point()
        # upper side of the game grid
        self.bottom_left_corner.y = grid_height
        # a random horizontal position
        self.bottom_left_corner.x = random.randint(0, grid_width - n)
        # create each tile by computing its position w.r.t. the game grid based on
        # its bottom_left_corner
        for i in range(len(occupied_tiles)):
            col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
            position = Point()
            # horizontal position of the tile
            position.x = self.bottom_left_corner.x + col_index
            # vertical position of the tile
            position.y = self.bottom_left_corner.y + (n - 1) - row_index
            # create the tile on the computed position
            self.tile_matrix[row_index][col_index] = Tile(position)

    # Method for drawing the tetromino on the game grid
    def draw(self):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                # draw each occupied tile (not equal to None) on the game grid
                if self.tile_matrix[row][col] != None:
                    # considering newly entered tetrominoes to the game grid that may
                    # have tiles with position.y >= grid_height
                    position = self.tile_matrix[row][col].get_position()
                    if position.y < self.grid_height:
                        self.tile_matrix[row][col].draw()

                        # Method for moving the tetromino in a given direction by 1 on the game grid

    def move(self, direction, game_grid):
        # check if the tetromino can be moved in the given direction by using the
        # can_be_moved method defined below
        if not (self.can_be_moved(direction, game_grid)):
            return False  # tetromino cannot be moved in the given direction
        # move the tetromino by first updating the position of the bottom left tile
        if direction == "left":
            self.bottom_left_corner.x -= 1
        elif direction == "right":
            self.bottom_left_corner.x += 1
        else:  # direction == "down"
            self.bottom_left_corner.y -= 1
        # then moving each occupied tile in the given direction by 1
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] != None:
                    if direction == "left":
                        self.tile_matrix[row][col].move(-1, 0)
                    elif direction == "right":
                        self.tile_matrix[row][col].move(1, 0)
                    else:  # direction == "down"
                        self.tile_matrix[row][col].move(0, -1)
        return True  # successful move in the given direction

    def rotate(self, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        if (self.can_be_rotated(game_grid) == False):
            print("cannot rotate occupied")
            return False

        # elif (self.can_be_rotated(game_grid) == 'left' or self.can_be_rotated(game_grid) == 'right'):
        #    print("anan")
        #    direction = self.can_be_rotated(game_grid)
        #    for row in range(n):
        #       for col in range(n):
        #          if self.tile_matrix[row][col] != None:
        #             if direction == "left":
        #                print("moving right")
        #                self.tile_matrix[row][col].move(1, 0)
        #             elif direction == "moving left":
        #                self.tile_matrix[row][col].move(-1, 0)

        # Push amount in case of overflow from edges.
        push_right_num = 0
        push_left_num = 0

        rotated_matrix = np.full((n, n), None)
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] != None:
                    rotated_matrix[col][n - 1 - row] = self.tile_matrix[row][col]
                    position = rotated_matrix[col][n - 1 - row].get_position()
                    position.x = self.bottom_left_corner.x + (n - 1 - row)
                    position.y = self.bottom_left_corner.y + (n - 1 - col)
                    # Checking for overflow
                    if position.x < 0:
                        push_right_num += 1
                    elif position.x >= game_grid.grid_width:
                        push_left_num += 1

                    rotated_matrix[col][n - 1 - row].set_position(position)

        self.tile_matrix = rotated_matrix

        if push_left_num + push_right_num > 0:  # If there is overflow
            for i in range(push_right_num):
                self.move("right", game_grid)
            for i in range(push_left_num):
                self.move("left", game_grid)
        return True

    def can_be_rotated(self, game_grid):

        # added these 2 lines for not passing blocks
        # if not (self.can_be_moved("left", game_grid)):
        #    return False
        #
        # if not (self.can_be_moved("right", game_grid)):
        #    return False

        n = len(self.tile_matrix)  # n = number of rows = number of columns
        rotated_matrix = np.full((n, n), None)
        positions = []
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] != None:
                    rotated_matrix[col][n - 1 - row] = self.tile_matrix[row][col]
                    position = rotated_matrix[col][n - 1 - row].get_position()
                    bottom_left = self.bottom_left_corner
                    position.x = bottom_left.x + (n - 1 - row)
                    position.y = bottom_left.y + (n - 1 - col)
                    positions.append(position)
        # for i in range(len(positions)):
        #    print(str(positions[i].x) + ", " +

        for i in range(len(positions)):
            if game_grid.is_occupied(positions[i].x, positions[i].y):
                return False

        return True

    # Method to check if the tetromino can be moved in the given direction or not
    def can_be_moved(self, dir, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        if dir == "left" or dir == "right":
            for row in range(n):
                for col in range(n):
                    # direction = left --> check the leftmost tile of each row
                    if dir == "left" and self.tile_matrix[row][col] != None:
                        leftmost = self.tile_matrix[row][col].get_position()
                        # tetromino cannot go left if any leftmost tile is at x = 0
                        if leftmost.x == 0:
                            return False
                        # skip each row whose leftmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if leftmost.y >= self.grid_height:
                            break
                        # tetromino cannot go left if the grid cell on the left of any
                        # of its leftmost tiles is occupied
                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False
                        break  # end the inner for loop
                    # direction = right --> check the rightmost tile of each row
                    elif dir == "right" and self.tile_matrix[row][n - 1 - col] != None:
                        rightmost = self.tile_matrix[row][n - 1 - col].get_position()
                        # tetromino cannot go right if any of its rightmost tiles is
                        # at x = grid_width - 1
                        if rightmost.x == self.grid_width - 1:
                            return False
                        # skip each row whose rightmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if rightmost.y >= self.grid_height:
                            break
                        # tetromino cannot go right if the grid cell on the right of
                        # any of its rightmost tiles is occupied
                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False
                        break  # end the inner for loop
        # direction = down --> check the bottommost tile of each column
        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    if self.tile_matrix[row][col] != None:
                        bottommost = self.tile_matrix[row][col].get_position()
                        # skip each column whose bottommost tile is out of the grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if bottommost.y > self.grid_height:
                            break
                        # tetromino cannot go down if any bottommost tile is at y = 0
                        if bottommost.y == 0:
                            return False
                            # or the grid cell below any bottommost tile is occupied
                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False
                        break  # end the inner for loop
        return True  # tetromino can be moved in the given direction
