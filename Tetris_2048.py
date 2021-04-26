import stddraw  # the stddraw module is used as a basic graphics library
import random  # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid  # class for modeling the game grid
from tetromino import Tetromino  # class for modeling the tetrominoes
from picture import Picture  # used representing images to display
import os  # used for file and directory operations
from color import Color  # used for coloring the game menu
from time import perf_counter
import keyboard
import time
import copy as cp

# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
SCORE = 0
CLEARED = 0
COMBINED = 0
PAUSE_COUNTER = 0
GAME_OVER = False  # added in order to restart the game properly
DEBUG = False


def start():
    global SCORE
    global CLEARED
    global COMBINED
    global PAUSE_COUNTER
    global GAME_OVER
    global DEBUG
    # Timer for block downfall
    timer_start = -999
    game_speed = 0.5  # In seconds
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w, grid, DEBUG)
    next_tetromino = create_tetromino(grid_h, grid_w, grid, DEBUG)
    grid.current_tetromino = current_tetromino
    grid.next_tetromino = next_tetromino

    # display a simple menu before opening the game
    display_game_menu(grid_h, grid_w)
    stddraw.setXscale(-0.5, grid_w + 2.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    while True:
        while not GAME_OVER:  # main game
            # check user interactions via the keyboard
            if stddraw.hasNextKeyTyped():
                key_typed = stddraw.nextKeyTyped()
                # if the left arrow key has been pressed
                if key_typed == "left":
                    # move the tetromino left by one
                    current_tetromino.move(key_typed, grid)
                    # if the right arrow key has been pressed
                elif key_typed == "right":
                    # move the tetromino right by one
                    current_tetromino.move(key_typed, grid)
                # if the down arrow key has been pressed
                elif key_typed == "down":
                    # move the tetromino down by one
                    # (causes the tetromino to fall down faster)
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "space":
                    for _ in range(24):
                        current_tetromino.move('down', grid)
                        success = False  # Don't allow for any movement after pressing space
                    grid.display(SCORE)
                elif key_typed == "up":
                    current_tetromino.rotate(grid)

                # pause
                elif key_typed == "p":
                    PAUSE_COUNTER = PAUSE_COUNTER + 1
                    if PAUSE_COUNTER % 2 == 1:
                        grid.display(SCORE, game_over=False, paused=True)
                        keyboard.wait("p")

                # restart
                elif key_typed == "r":
                    current_tetromino.clear_tetro(grid)
                    grid.clear_everything(grid_w, grid_h)
                    SCORE = 0
                    CLEARED = 0
                    COMBINED = 0
                    DEBUG = False
                    success = False

                # hold
                elif key_typed == "c":
                    # swap
                    # current_tetromino, next_tetromino = next_tetromino, current_tetromino
                    # temp = current_tetromino
                    # current_tetromino = next_tetromino
                    # next_tetromino = temp
                    #
                    #
                    pass

                # debug mode
                elif key_typed == "i":
                    DEBUG = True

                # debug mode #2
                elif key_typed == "b":
                    if str(input()) == "buayb":
                        DEBUG = True

                # normal mode
                elif key_typed == "n":
                    DEBUG = False

                # clear the queue that stores all the keys pressed/typed
                stddraw.clearKeysTyped()

            # Ghost Guide
            grid.ghost_tetromino = cp.deepcopy(current_tetromino)
            for i in range(24):
                grid.ghost_tetromino.move("down", grid)

            # move (drop) the tetromino down by 1 after set amount of time
            end_time = perf_counter()
            if end_time - timer_start >= clamp(0.001, 0.11, 5):
                success = current_tetromino.move("down", grid)
                timer_start = perf_counter()

            # place the tetromino on the game grid when it cannot go down anymore
            if not success:
                # get the tile matrix of the tetromino
                tiles_to_place = current_tetromino.tile_matrix
                # update the game grid by adding the tiles of the tetromino
                game_over = grid.update_grid(tiles_to_place)
                #  score for combining tiles
                # COMBINED += grid.clear_2048(grid_w, grid_h)
                # to_add = grid.delete_floating()
                # SCORE += to_add
                while True:
                    cleared = grid.clear(grid_w, grid_h)
                    CLEARED += cleared
                    cleared_2048 = 0
                    cleared_2048 += grid.clear_2048(grid_w, grid_h)
                    COMBINED += cleared_2048
                    COMBINED += grid.delete_floating()
                    if cleared + cleared_2048 == 0:
                        break
                if game_over:
                    # breaking game's while loop
                    GAME_OVER = True
                    break
                # create the next tetromino to enter the game grid
                # by using the create_tetromino function defined below
                current_tetromino = create_tetromino(grid_h, grid_w, grid, DEBUG)
                grid.current_tetromino = current_tetromino

                # next tetromino
                #
                # current_tetromino = next_tetromino
                # next_tetromino = create_tetromino(grid_h, grid_w, grid)
                # grid.current_tetromino = current_tetromino

                # After spawning move the block once and update success or instant game over
                success = current_tetromino.move("down", grid)

            SCORE = CLEARED * 100 + COMBINED
            # display the game grid and as well the current tetromino
            # grid.clear(grid_w, grid_h)
            # default display with score
            grid.display(SCORE)
        # game over screen
        grid.display(SCORE, GAME_OVER)

        # main game loop (keyboard interaction for moving the tetromino)
        if keyboard.is_pressed("y"):
            current_tetromino.clear_tetro(grid)
            grid.clear_everything(grid_w, grid_h)
            SCORE = 0
            CLEARED = 0
            COMBINED = 0
            GAME_OVER = False
            DEBUG = False
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino(grid_h, grid_w, grid)
            grid.current_tetromino = current_tetromino
            success = current_tetromino.move("down", grid)

        elif keyboard.is_pressed("n"):
            break

    print(SCORE)
    print("Game over")


# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width, grid, debug=False):
    # DEBUG VALUES
    if debug:
        tetromino_types = ['I']
    else:
        # type (shape) of the tetromino is determined randomly
        tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type, grid_height, grid_width)
    tetromino.set_random_tile_numbers(grid)
    return tetromino


# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 1.5, 2
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w:
                if button_blc_y <= mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
