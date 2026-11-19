"""A snake game, directly in the terminal"""
import random
import math
import curses

#arrows
# up 259
# down 258
# left 261
# right 260

#pad
#up 258
#down 259

# o 11
# esc 27
# z 122
#         q 113
#         s 115     
# d 100    
# c 99

def place_snake_head(map_height):
    """Initial position of the snake head"""
    snake_head_y = int(map_height/2)
    snake_head_x = 2
    return (snake_head_x, snake_head_y)

    

def detect_keys(stdscr, map, snake_head_x, snake_head_y): 
    """Detects the user input"""
    direction = "none"
    while True:
        key = stdscr.getch()
        if key == 259 and direction != "down":
            direction = "up"
            snake_head_y -= 1
        elif key == 258 and direction != "up":
            direction = "down"
            snake_head_y += 1
        elif key == 261 and direction != "right":
            direction = "left"
            snake_head_x += 1
        elif key == 260 and direction != "left":
            direction = "right"
            snake_head_x -= 1

        stdscr.clear()
        map = map_creation(12, 12)
        (random_x, random_y) = place_fruit(12, 12)
        map[snake_head_y][snake_head_x] = "1"
        map[random_y][random_x] = "🍎"
        render(stdscr, map)
        stdscr.addstr(direction)

def initialize_colors():
    """Creates the colors and color pairs used in the game"""
    curses.start_color()
    curses.init_color(1, 236, 28, 40)
    curses.init_color(2, 352, 112, 540)
    curses.init_color(3, 672, 340, 988)
    curses.init_color(4, 296, 888, 512)
    curses.init_pair(10, 1, 2)
    curses.init_pair(11, 2, 1)
    curses.init_pair(12, 2, 3)
    curses.init_pair(13, 4, 4)


def print_pixel(x, y, stdscr, string):
    """Prints a singular square made up of 4 pixels."""
    if string == "0":
        stdscr.addstr(y, x, "▄", curses.color_pair(10))
        stdscr.addstr(y, x+1, "▄", curses.color_pair(11))
    elif string == "1":
        stdscr.addstr(y, x, "▄", curses.color_pair(13))
        stdscr.addstr(y, x+1, "▄", curses.color_pair(13))
    else:
        stdscr.addstr(y, x, string, curses.color_pair(10))

def map_creation (width, height=None):
    """Crée un tableau de longueur de côté MAP_SIZE""" 
    if height == None:
        height = width
    map_line = []
    map = []
    for i in range(width):
        map_line.append("0")
    for i in range(height):
        map.append(map_line.copy())
    print(map)
    return map

def return_center(stdscr, map_len, amount):
    """Return the abciss an element should have to be centered"""
    (height,width) = stdscr.getmaxyx()
    window_center = int(width / 2)
    map_center = math.ceil(map_len / 2) * amount
    return window_center - map_center

def print_text(stdscr, text):
    """Handle title display"""
    max_width = 0 
    for i in range(len(text)):
        if len(text[i]) > 0:
            max_width = len(text[i])
    base_x = return_center(stdscr, max_width, 1)
    x = base_x
    y = 0
    for i in range(len(text)):
        for j in range(len(text[i])):
            stdscr.addstr(y, x, text[i][j])
            x += 1
        y += 1
        x = base_x


def render(stdscr, map):
    """The function rendering the map on the screen"""
    text = [
        [' ', '_', '_', '_', '_', '_', '_', '_', '_', ' ', ' ', '_', '_', '_', '_', '_', '_', '_', '_', ' ', ' ', ' ', '_', '_', '_', '_', '_', '_', '_', '_', ' ', ' ', '_', '_', '_', ' ', ' ', '_', '_', ' ', ' ', ' ', ' ', '_', '_', '_', '_', '_', '_', '_', ' ', ' ', ' ', ' ', ' ', ' '],
        ['|', '\\', ' ', ' ', ' ', '_', '_', '_', '_', '\\', '|', '\\', ' ', ' ', ' ', '_', '_', '_', ' ', ' ', '\\', '|', '\\', ' ', ' ', ' ', '_', '_', ' ', ' ', '\\', '|', '\\', ' ', ' ', '\\', '|', '\\', ' ', ' ', '\\', ' ', '|', '\\', ' ', ' ', '_', '_', '_', ' ', '\\', ' ', ' ', ' ', ' ', ' '],
        ['\\', ' ', '\\', ' ', ' ', '\\', '_', '_', '_', '|', '\\', ' ', '\\', ' ', ' ', '\\', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '|', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '/', ' ', ' ', '/', '|', '\\', ' ', '\\', ' ', ' ', ' ', '_', '_', '/', '|', ' ', ' ', ' ', ' '],
        [' ', '\\', ' ', '\\', '_', '_', '_', '_', '_', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', ' ', '_', '_', ' ', ' ', '\\', ' ', '\\', ' ', ' ', ' ', '_', '_', '_', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '_', '|', '/', '_', '_', ' ', ' '],
        [' ', ' ', '\\', '|', '_', '_', '_', '_', '|', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '\\', ' ', '\\', ' ', ' ', '\\', ' ', '\\', ' ', ' ', '\\', '_', '|', '\\', ' ', '\\', ' '],
        [' ', ' ', ' ', ' ', '_', '_', '_', '_', '\\', '_', '\\', ' ', ' ', '\\', ' ', '\\', '_', '_', '\\', '\\', ' ', '\\', '_', '_', '\\', ' ', '\\', '_', '_', '\\', ' ', '\\', '_', '_', '\\', ' ', '\\', '_', '_', '\\', '\\', ' ', '\\', '_', '_', '\\', ' ', '\\', '_', '_', '_', '_', '_', '_', '_', '\\'],
        [' ', ' ', ' ', '|', '\\', '_', '_', '_', '_', '_', '_', '_', '_', '_', '\\', '|', '_', '_', '|', ' ', '\\', '|', '_', '_', '|', '\\', '|', '_', '_', '|', '\\', '|', '_', '_', '|', '\\', '|', '_', '_', '|', ' ', '\\', '|', '_', '_', '|', '\\', '|', '_', '_', '_', '_', '_', '_', '_', '|'],
        [' ', ' ', ' ', '\\', '|', '_', '_', '_', '_', '_', '_', '_', '_', '_', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]
    text2 = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'd', '8', 'b', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '?', '8', '8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '8', '8', 'b', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', '.', 'd', '8', '8', '8', 'b', ',', ' ', ' ', '8', '8', 'b', 'd', '8', '8', 'b', ' ', ' ', 'd', '8', '8', '8', 'b', '8', 'b', ' ', ' ', ' ', ' ', '8', '8', '8', ' ', ' ', 'd', '8', '8', "'", ' ', 'd', '8', '8', '8', '8', 'b'], [' ', '?', '8', 'b', ',', ' ', ' ', ' ', ' ', ' ', '8', '8', 'P', "'", ' ', '?', '8', 'b', 'd', '8', 'P', "'", ' ', '?', '8', '8', ' ', ' ', ' ', ' ', '8', '8', '8', 'b', 'd', '8', 'P', "'", ' ', 'd', '8', 'b', '_', ',', 'd', 'P'], [' ', ' ', ' ', '`', '?', '8', 'b', ' ', ' ', 'd', '8', '8', ' ', ' ', ' ', '8', '8', 'P', '8', '8', 'b', ' ', ' ', ',', '8', '8', 'b', ' ', ' ', 'd', '8', '8', '8', '8', '8', 'b', ' ', ' ', ' ', '8', '8', 'b', ' ', ' ', ' ', ' '], ['`', '?', '8', '8', '8', 'P', "'", ' ', 'd', '8', '8', "'", ' ', ' ', ' ', '8', '8', 'b', '`', '?', '8', '8', 'P', "'", '`', '8', '8', 'b', 'd', '8', '8', "'", ' ', '`', '?', '8', '8', 'b', ',', '`', '?', '8', '8', '8', 'P', "'"]]
    
    print_text(stdscr, text)
    base_x = return_center(stdscr, len(map[0]), 2)
    x = base_x
    y = len(text) + 1
    for i in range(len(map)):
        for j in range(len(map[i])):
            #print(map[i][j], end="")
            print_pixel(x, y, stdscr, map[i][j])
            x += 2
        x = base_x
        y += 1

def place_fruit(max_x, max_y=None):
    """Place a fruit on a random case"""
    if max_y == None:
        max_y = max_x

    random_x = random.randint(0, max_x - 1)
    random_y = random.randint(0, max_y - 1)

    return (random_x, random_y)

def main(stdscr):
    """Entry point"""
    x = 12
    y = 12
    initialize_colors()
    blank_map = map_creation(x, y)
    map = blank_map
    (random_x, random_y) = place_fruit(x, y)
    map[random_y][random_x] = "🍎"
    (snake_head_x, snake_head_y) = place_snake_head(y)
    map[snake_head_y][snake_head_x] = "1"
    render(stdscr, map)
    #print(random_x, random_y)
    detect_keys(stdscr, map, snake_head_x, snake_head_y)


curses.wrapper(main)
