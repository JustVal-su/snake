"""A snake game, directly in the terminal"""
import random
import math
import time
import curses
import json

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

KEYS = {
    "up": 450,
    "down": 456,
    "left": 452,
    "right": 454
}

def place_snake_head(map_height):
    """Initial position of the snake head"""
    snake_head_y = int(map_height/2)
    snake_head_x = 3
    return (snake_head_x, snake_head_y)

def read_json():
    """Read titles.json to get the ascii art titles"""
    with open("titles.json", "r") as file:
        data = json.load(file)
    return data["threeD"]

def append_body(map, snake_body):
    """Append all the snake cells to the map"""
    for i in snake_body:
        map[i[1]][i[0]] = "1"

def body_update(snake_body, snake_head_x, snake_head_y, snake_length):
    """Update snake body display"""
    if len(snake_body) >= snake_length:
        snake_body.pop()
    snake_body.insert(0, [snake_head_x, snake_head_y])

def check_apple(snake_head_coordonates, apple_coordonates, is_apple_eaten, stdscr):
    """Check if snake is eating an apple"""
    return snake_head_coordonates == apple_coordonates

def change_direction(direction: str, snake_head_x, snake_head_y, stdscr):
    key = stdscr.getch()
    """Changes snake direction if a key is pressed"""
    if key == KEYS["up"] and direction != "down":
        direction = "up"
        is_moving = True
        #snake_head_y -= 1
    elif key == KEYS["down"] and direction != "up":
        direction = "down"
        is_moving = True
        #snake_head_y += 1
    elif key == KEYS["right"] and direction != "left":
        direction = "right"
        is_moving = True
        #snake_head_x += 1
    elif key == KEYS["left"] and direction != "right":
        direction = "left"
        #snake_head_x -= 1
        
    return (direction, key)

def move_snake(snake_head_x, snake_head_y, direction):
    """Handle snake movements"""
    if direction == "up":
        snake_head_y -= 1
    elif direction == "down":
        snake_head_y += 1
    elif direction == "right":
        snake_head_x += 1
    elif direction == "left":
        snake_head_x -= 1
    return (snake_head_x, snake_head_y)

def detect_keys(stdscr, snake_body, snake_length, x, y, text): 
    """Detects the user input"""
    stdscr.timeout(300)

    map = map_creation(x, y)
    (snake_head_x, snake_head_y) = place_snake_head(y)

    for i in range(snake_length):
        snake_body.append([snake_head_x - i, snake_head_y])
    append_body(map, snake_body)

    (random_x, random_y) = place_fruit(x, y)
    map[random_y][random_x] = "🍎"
    score = snake_length - 3
    
    render(stdscr, map, score, text)

    
    is_moving = False
    is_apple_eaten = False
    direction = "right"
    player_alive = True
    test = "a"
    key = -1
    while True:
        (direction, key) = change_direction(direction, snake_head_x, snake_head_y, stdscr)
        (snake_head_x, snake_head_y) = move_snake(snake_head_x, snake_head_y, direction)
        body_update(snake_body, snake_head_x, snake_head_y, snake_length)
        is_apple_eaten = check_apple((random_x, random_y), (snake_head_x, snake_head_y), is_apple_eaten, stdscr)
        if is_apple_eaten:
            snake_length += 1
            (random_x, random_y) = place_fruit(x, y)
            is_apple_eaten = False

        #player_alive = body_update(snake_body, snake_head_x, snake_head_y, snake_length)
        map = map_creation(x, y)
        map[random_y][random_x] = "🍎"
        append_body(map, snake_body)
        score = snake_length - 3
        stdscr.clear()
        if player_alive:
            render(stdscr, map, score, text)
        else:
            stdscr.addstr("gameover")
        stdscr.addstr(str(key))

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
        if len(text[i]) > max_width:
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


def render(stdscr, map, score, text):
    """The function rendering the map on the screen"""
    
    print_text(stdscr, text)
    base_x = return_center(stdscr, len(map[0]), 2)
    stdscr.addstr(0, len(text) + 1, f"Score : {score}")
    x = base_x
    y = len(text) + 2
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
    x = 15
    y = 15
    snake_body = []
    snake_length = 3
    initialize_colors()
    text = read_json(stdscr)
    detect_keys(stdscr, snake_body, snake_length, x, y, text)
    
curses.wrapper(main)